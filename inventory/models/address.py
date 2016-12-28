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
from network import Network

class Address(models.Model):

    """
    Address and prefix. Can be network or network host address
    """

    network = models.ForeignKey(Network)
    address = models.GenericIPAddressField(unique=True)
    prefix = models.IntegerField(default=24)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s: Network: %s.%s Address: %s/%s" % (self.id, self.network.tenant.name, self.network.name, self.address, self.prefix)

    def __unicode__(self):
        return "%s: Network: %s.%s Address: %s/%s" % (self.id, self.network.tenant.name, self.network.name, self.address, self.prefix)

    class Meta:
        app_label="inventory"
        unique_together = ('address', 'prefix')
        permissions = (
            ('view_address', 'Can view address'),
        )

    def to_dict(self):

        attributes = json.loads(serializers.serialize('json',[self,]))[0]['fields']
        attributes['id'] = self.id

        return attributes