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
import json
import yaml
from celery.utils.log import get_task_logger
from dhcp.models.shared_network import SharedNetwork
from lib.automation_engine.ansible import Ansible
from lib.automation_engine.ansible import AnsibleLayerException
from lib.automation_engine.ansible import AnsibleHostException
from lib.toolson.utils import read
import json
from django.conf import settings

logger = get_task_logger(__name__)

@shared_task_with_locking
def provision_dhcp_service(self, noop=0):

    """
    Build DHCP service configuration and provision service host using Ansible
    :param self: /
    :param noop: Device to process
    :return: Success message
    """

    try:

        #Get configuration and rebuild...
        configuration = {}
        configuration['dhcp']=[]
        shared_networks = SharedNetwork.objects.filter(active=True)
        for network in shared_networks:
            configuration['dhcp'].append(network.get_configuration())

        configuration = yaml.safe_dump(yaml.load(json.dumps(configuration)), default_flow_style=False)

        #Execute Ansible layer
        a = Ansible(ansible_path=settings.ANSIBLE['PATH'], inventory=settings.DHCP_SERVICE['INVENTORY_NAME'])

        #Write configuration
        for host in settings.DHCP_SERVICE['HOSTS']:
            a.write_configuration(target_file="host_vars/%s.yml" % (host),
                                  configuration_content=configuration)

        #Provision host with new configuration
        a.playbook(playbook_name="provision_dhcp.yml", limit="dhcp")

        return "Task completed."

    except Exception as detail:
        msg = "Unknown exception provisioning DHCP service.\nException details: %s\nTrace: %s" % (detail,traceback.format_exc())
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