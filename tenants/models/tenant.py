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

from django.db import models
from django.core import serializers
import json
import yaml

class Tenant(models.Model):

    """
    Organizations in WLAN2020 project. Each organization is presented as tenant, with multiple locations for each subsidary.
    Identifier presents ArnesID for matching with legacy Arnes databases.
    """

    name = models.CharField(unique=True, max_length=255)
    description = models.CharField(max_length=255)
    identifier = models.IntegerField(unique=True)

    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "%s: %s - %s" % (self.id, self.name, self.description)

    def __str__(self):
        return "%s: %s - %s" % (self.id, self.name, self.description)

    class Meta:
        app_label="tenants"

        permissions = (
            ('view_tenant', 'Can view tenant'),
        )


    def to_dict(self):

        attributes = json.loads(serializers.serialize('json',[self,]))[0]['fields']
        attributes['id'] = self.id

        return attributes

    def get_configuration(self):

        return self.to_dict()