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

class Network(models.Model):

    """
    Network
    """

    USAGE = (
        ('management', 'management'),
        ('infrastructure', 'infrastructure'),
        ('lan', 'lan'),
    )

    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    vlan = models.IntegerField(null=True, blank=True)
    usage = models.CharField(max_length=255, choices=USAGE)

    tenant = models.ForeignKey(Tenant)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s: %s Name: %s VLAN ID: %s Description: %s" % (self.id, self.tenant.name, self.name, self.vlan, self.description)

    def __unicode__(self):
        return "%s: %s Name: %s VLAN ID: %s Description: %s" % (self.id, self.tenant, self.name, self.vlan, self.description)

    class Meta:
        app_label="inventory"
        permissions = (
            ('view_network', 'Can view network'),
        )

    def to_dict(self):

        attributes = json.loads(serializers.serialize('json',[self,]))[0]['fields']
        attributes['id'] = self.id

        return attributes