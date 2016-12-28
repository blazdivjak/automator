# -*- coding: utf-8 -*-

########################################################################
#
# (C) 2016, Blaz Divjak, ARNES <blaz@arnes.si> <blaz@divjak.si>
#
# This file is part of Automator
#
# Automator is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Automator is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Automator.  If not, see <http://www.gnu.org/licenses/>.
#
########################################################################

from __future__ import absolute_import
from lib.celerator.decorators.anso_celery import shared_task_with_locking
import traceback
from celery.utils.log import get_task_logger
from lib.automation_engine.ansible import Ansible
from inventory.models.device import Device
from inventory.models.link import Link
from lib.automation_engine.ansible import AnsibleLayerException
from lib.automation_engine.ansible import AnsibleHostException
from inventory.models.interface import Interface
from lib.toolson.utils import read
from lib.automation_engine.serializers import generate_inventory
from django.db.models import Q
import json
from django.conf import settings

logger = get_task_logger(__name__)

@shared_task_with_locking
def update_inventory(self, noop=0):

    """
    Update inventory
    :param self: /
    :param noop: /
    :return: Success message
    """

    try:

        devices = Device.objects.filter(active=True)

        a = Ansible(ansible_path=settings.ANSIBLE['PATH'], inventory=settings.ANSIBLE['INVENTORY_NAME'])

        #Write configuration
        a.write_configuration(target_file = settings.ANSIBLE['ENVIRONMENT'],
                              configuration_content = generate_inventory(devices, settings.ANSIBLE['INVENTORY_NAME']))

        return "Task completed."

    except Exception as detail:
        msg = "Unknown exception while updating inventory.\nException details: %s\nTrace: %s" % (
        detail, traceback.format_exc())
        logger.error(msg)
        raise

    except AnsibleLayerException as detail:
        msg = "Ansible layer problem.\nException details: %s\nTrace: %s" % (detail, traceback.format_exc())
        logger.error(msg)
        raise

    except AnsibleHostException as detail:
        msg = "Ansible host issue.\nTry: %s/%s.\nRetry timer: %ss\nException details: %s\nTrace: %s" % (
        self.request.retries + 1,
        self.max_retries + 1,
        self.default_retry_delay,
        detail,
        traceback.format_exc())

        logger.error(msg)
        raise self.retry(exc=detail)

@shared_task_with_locking
def install_config(self, device_id=None):

    """
    Write device configuration to inventory and execute playbook to configure network device.
    :param self: /
    :param device_id: Device to process
    :return: Success message
    """

    try:

        device = Device.objects.get(id=device_id)
        configuration = device.get_configuration()

        a = Ansible(ansible_path=settings.ANSIBLE['PATH'], inventory=settings.ANSIBLE['INVENTORY_NAME'])

        #Write configuration
        a.write_configuration(target_file="host_vars/%s.yml" % (device.name),
                              configuration_content= configuration)

        #Build configuration
        a.playbook(playbook_name="config_generate.yml", limit=device.name)

        #Install configuration
        a.playbook(playbook_name="config_install.yml", limit=device.name)

        return "Task completed."

    except Exception as detail:
        msg = "Unknown exception while installing config.\nException details: %s\nTrace: %s" % (
        detail, traceback.format_exc())
        logger.error(msg)
        raise

    except AnsibleLayerException as detail:
        msg = "Ansible layer problem.\nException details: %s\nTrace: %s" % (detail, traceback.format_exc())
        logger.error(msg)
        raise

    except AnsibleHostException as detail:
        msg = "Ansible host issue.\nTry: %s/%s.\nRetry timer: %ss\nException details: %s\nTrace: %s" % (
        self.request.retries + 1,
        self.max_retries + 1,
        self.default_retry_delay,
        detail,
        traceback.format_exc())

        logger.error(msg)
        raise self.retry(exc=detail)

@shared_task_with_locking
def get_facts(self, device_id=None):

    """
    Get device facts and import/update it into the system.
    Features:
    1. If interfaces for device do not exist in the system add them to database.
    :param self: /
    :param device_id: Device to process
    :return: Success message
    """

    try:

        #Get all interface from device using Ansible layer
        device = Device.objects.get(id=device_id)
        configuration = device.get_configuration()

        a = Ansible(ansible_path=settings.ANSIBLE['PATH'], inventory=settings.ANSIBLE['INVENTORY_NAME'])

        #Write configuration
        a.write_configuration(target_file="host_vars/%s.yml" % (device.name),
                              configuration_content=configuration)

        #Get facts
        a.playbook(playbook_name="get_facts.yml", limit=device.name)

        #Load gathered facts
        gathered_facts_json = read(file="%s%s%s.json" % (settings.ANSIBLE['PATH'], settings.ANSIBLE['FACTS_PATH'], device.name))
        gathered_facts = json.loads(gathered_facts_json)

        #TODO: Find neighbors and create connections if possible
        #for interface, neighbor in gathered_facts['ansible_facts']['facts']['lldp_neighbors'].items():

            #TODO: Get all existing links for host and update
            #links = Link.objects.filter(Q(interface1__name=) | Q(tagged_networks=instance))

        #TODO: Draw schema with vis.js

        #Process interfaces
        if(len(Interface.objects.filter(device=device))==0):
            # print gathered_facts['ansible_facts']['facts']['interface_list']
            for interface in gathered_facts['ansible_facts']['facts']['interface_list']:
                i = Interface()
                i.name = interface
                i.description = interface
                i.device=device

                #Get interface type from its name. Match is made using mapping defined in settings
                for key, values in settings.ANSIBLE['INTERFACE_MAP'].items():
                    for value in values:
                        if str(value).lower() in str(i.name).lower():
                            i.type = str(key)
                            break

                if i.type == "":
                    #i.type = "other"
                    break

                i.save()

        return "Task completed."

    except Exception as detail:
        msg = "Unknown exception while getting device facts.\nException details: %s\nTrace: %s" % (detail,traceback.format_exc())
        logger.error(msg)
        raise

    except AnsibleLayerException as detail:
        msg = "Ansible layer problem.\nException details: %s\nTrace: %s" % (detail, traceback.format_exc())
        logger.error(msg)
        raise

    except AnsibleHostException as detail:
        msg="Ansible host issue.\nTry: %s/%s.\nRetry timer: %ss\nException details: %s\nTrace: %s" % (self.request.retries+1,
                                                                                                                self.max_retries+1,
                                                                                                                self.default_retry_delay,
                                                                                                                detail,
                                                                                                                traceback.format_exc())

        logger.error(msg)
        raise self.retry(exc=detail)