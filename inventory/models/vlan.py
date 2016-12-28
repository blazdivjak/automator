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
from django.core import serializers
from tenants.models.tenant import Tenant
from django.core.exceptions import ValidationError
from network import Network
from interface import Interface
from validation import validate_interface_type

class Vlan(models.Model):

    """
    Vlan core service model. Enables assignment of virtual networks to physical interfaces.

    """

    interface = models.OneToOneField(Interface, validators=[validate_interface_type], unique=True) #TODO: Validate that interface is ethernet type

    tagged_networks = models.ManyToManyField(Network, related_name='tagged_networks', blank=True) #tagged networks
    untagged_network = models.ForeignKey(Network, related_name='untagged_network', blank=True, null=True) #native a.k.a untagged network

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s: %s.%s" % (self.id, self.interface.device.name, self.interface.name)

    def __unicode__(self):
        return "%s: %s.%s" % (self.id, self.interface.device.name, self.interface.name)

    class Meta:
        app_label="inventory"
        permissions = (
            ('view_vlan', 'Can view vlan'),
        )

    def to_dict(self):

        attributes = json.loads(serializers.serialize('json',[self,]))[0]['fields']
        attributes['id'] = self.id

        return attributes




