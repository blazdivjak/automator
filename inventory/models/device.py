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

import json
import yaml
from django.db import models
from django.conf import settings
from tenants.models.tenant import Tenant
from django.core.validators import MinLengthValidator
from django.core import serializers
from validation import validate_special_characters
from validation import validate_mac
from lib.openconfig.oc.interfaces import interfaces
from lib.openconfig.serializers import interface_to_openconfig
from lib.openconfig.serializers import vlan_to_openconfig
from lib.openconfig.serializers import relay_agent_to_openconfig

class DeviceModel(models.Model):

    """
    Device models included in projects can be from different vendors.
    Different types of devices are supported, such as passive or active equipment.
    Every device also have information where it is placed on the map
    """

    VENDOR=(
        ('cisco','cisco'),
        ('juniper','juniper'),
        ('lancom', 'lancom'),
    )
    OS = (
        ('ios', 'ios'),
        ('junos', 'junos'),
    )
    TYPE = (
        ('router', 'router'),
        ('switch', 'switch'),
        ('access point', 'access point')
    )

    name = models.CharField(max_length=255, unique=True)
    vendor = models.CharField(max_length=255, choices=VENDOR)
    model = models.CharField(max_length=255)
    os = models.CharField(max_length=255, choices=OS)
    version = models.CharField(max_length=255)
    type = models.CharField(max_length=255, choices=TYPE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s - %s" % (self.vendor, self.name)

    def __unicode__(self):
        return "%s - %s" % (self.vendor, self.name)

    class Meta:
        app_label="inventory"
        permissions = (
            ('view_devicemodel', 'Can view device model'),
        )

    def to_dict(self):

        attributes = json.loads(serializers.serialize('json',[self,]))[0]['fields']
        attributes['id'] = self.id

        return attributes

class Device(models.Model):

    """
    Device list for each tenant Contains metadata about devices and their type information.
    Also includes information about which project device was aquired in.
    """

    USAGE=(
        ('BACKBONE','BACKBONE'),
        ('ACCESS', 'ACCESS'),
        ('TSP','TSP'),
    )
    FUNCTION=(
        ('ROUTER','ROUTER'),
        ('L3_SWITCH', 'L3_SWITCH'),
        ('L2_SWITCH','L2_SWITCH'),
    )

    tenant = models.ForeignKey(Tenant)
    name = models.CharField(max_length=255, validators=[MinLengthValidator(3) ,validate_special_characters])
    description = models.CharField(max_length=255)
    device_model = models.ForeignKey(DeviceModel)
    usage = models.CharField(max_length=255, choices=USAGE)
    function = models.CharField(max_length=255, choices=FUNCTION)
    serial_number = models.CharField(max_length=255,
                                     unique=True,
                                     validators=[MinLengthValidator(4), validate_special_characters])
    inventory_number = models.BigIntegerField(unique=True)
    mac = models.CharField(max_length=255,
                           validators=[MinLengthValidator(4), validate_mac],
                           null=True,
                           blank=True)

    manage = models.BooleanField(default=True)
    active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s: %s - %s %s" % (self.id, self.name, self.device_model.vendor, self.device_model.name)

    def __unicode__(self):
        return "%s: %s - %s %s" % (self.id, self.name, self.device_model.vendor, self.device_model.name)

    class Meta:

        app_label="inventory"
        permissions = (
            ('view_device', 'Can view device'),
        )

    def to_dict(self):

        attributes = json.loads(serializers.serialize('json',[self,]))[0]['fields']
        attributes['id'] = self.id

        return attributes


    def _get_system_information(self):

        """
        Get all system information from device
        :return: dict object
        """

        system = {
            'hostname': self.name,
            'description': self.description,
            'vendor': self.device_model.vendor,
            'os': self.device_model.os,
            'serial_number': self.serial_number,
            'version': self.device_model.version,
            'model': self.device_model.model,
            'usage': self.usage,
            'inventory_number': self.id,
            'active': self.active,
            'managed': self.manage,
            'tenant_name': self.tenant.name,
            'tenant_id': self.tenant_id,
        }

        #print json.dumps(system, indent=4)

        return system

    def _get_networks(self):

        """
        Get list of networks configured on this device
        :return: list of network objects
        """

        from vlan import Vlan

        vlan_list = Vlan.objects.filter(interface__device=self.id)
        networks = []

        for vlan in vlan_list:
            networks.extend(vlan.tagged_networks.all())
            if vlan.untagged_network != None: networks.append(vlan.untagged_network)

        return set(networks)

    def _get_relay_agents(self):

        """
        Get relay agents configured for this network device
        :return:
        """

        from dhcp.models.shared_network import Helper

        return Helper.objects.filter(interface__device=self)

    def notify(self):

        """
        Notify device to update its configuration. Adds task into AMQ
        :return: None
        """
        from inventory.tasks import get_facts
        from inventory.tasks import install_config
        from inventory.tasks import update_inventory

        # Update inventory anyway
        update_inventory.apply_async(kwargs={'noop': 0}, countdown=settings.CELERY_TIMER)

        # Execute tasks only if device is managed
        if self.manage == True:
            get_facts.apply_async(kwargs={'device_id': self.id}, countdown=settings.CELERY_TIMER)
            install_config.apply_async(kwargs={'device_id': self.id}, countdown=settings.CELERY_TIMER)

    def get_configuration(self):

        """
        Get all configuration needed for device. Device should include all modules it needs.
        OpenConfig models used for data serialization where possible
        :return: dict object with configuration objects
        """

        self.configuration = {
            'system': self._get_system_information(),
            'interfaces': interface_to_openconfig(self.interface_set.all()),
            'vlans' : vlan_to_openconfig(self._get_networks()),
            'relay_agent': relay_agent_to_openconfig(self._get_relay_agents()),
        }

        #DEBUG PRINTOUTS
        #print json.dumps(self.configuration, indent=4)
        #return json.dumps(self.configuration, indent=4)
        #print yaml.safe_dump(yaml.load(json.dumps(self.configuration)),default_flow_style=False)
        return yaml.safe_dump(yaml.load(json.dumps(self.configuration)),default_flow_style=False)


