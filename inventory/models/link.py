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
from interface import Interface

class Link(models.Model):

    """
    Links between two interfaces
    """

    interface1 = models.ForeignKey(Interface, related_name='interface1')
    interface2 = models.ForeignKey(Interface, related_name='interface2')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s: %s.%s -> %s.%s" % (self.id, self.interface1.device.name, self.interface1.name, self.interface2.device.name, self.interface2.name)

    def __unicode__(self):
        return "%s: %s.%s -> %s.%s" % (self.id, self.interface1.device.name, self.interface1.name, self.interface2.device.name, self.interface2.name)

    class Meta:
        app_label="inventory"
        unique_together=["interface1", "interface2"]
        permissions = (
            ('view_link', 'Can view link'),
        )

    def to_dict(self):

        attributes = json.loads(serializers.serialize('json',[self,]))[0]['fields']
        attributes['id'] = self.id

        return attributes