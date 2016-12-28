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
from django.db import models
from tenants.models.tenant import Tenant
from django.core.validators import MinLengthValidator
from django.core import serializers
from validation import validate_special_characters
from validation import validate_mac
from address import Address
from network import Network
from device import Device

class Interface(models.Model):

    """
    Interface
    """

    TYPE = (
        ('ethernetCsmacd', 'ethernetCsmacd'), #ethernet physical ints
        ('l3ipvlan', 'l3ipvlan'), #vlan interface
        ('propVirtual', 'propVirtual'), #vlan interface
        ('l2vlan', 'l2vlan'), #subinterface
        ('softwareLoopback', 'softwareLoopback'), #loopback
        ('tunnel', 'tunnel'), #tunnel
        ('ppp', 'ppp'), #ppp
        ('ieee8023adLag', 'ieee8023adLag'), #etherchannel
        ('other', 'other'), #other :D wtf
    )

    name = models.CharField(max_length=255, validators=[MinLengthValidator(2)])
    description = models.CharField(max_length=255)
    device = models.ForeignKey(Device)
    type = models.CharField(max_length=255, choices=TYPE)
    addresses = models.ManyToManyField(Address, blank=True) #Address asigned to routed-vlan or smtin
    state = models.BooleanField(default=True)
    uplink = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s: %s - %s" % (self.id, self.device.name, self.name)

    def __unicode__(self):
        return "%s: %s - %s" % (self.id, self.device.name, self.name)

    class Meta:
        app_label="inventory"
        unique_together=["name", "device"]
        permissions = (
            ('view_interface', 'Can view interface'),
        )

    def to_dict(self):

        attributes = json.loads(serializers.serialize('json',[self,]))[0]['fields']
        attributes['id'] = self.id

        return attributes

    def get_tenant(self):

        return self.device.tenant.id