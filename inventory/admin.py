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

from django.contrib import admin
from inventory.models.device import DeviceModel
from inventory.models.device import Device
from inventory.models.address import Address
from inventory.models.interface import Interface
from inventory.models.link import Link
from inventory.models.network import Network
from inventory.models.vlan import Vlan
from guardian.admin import GuardedModelAdmin

class AddressAdmin(GuardedModelAdmin):
    search_fields = ['id','address', 'prefix', 'network__name']
    list_filter = ['network__name', 'network__tenant__name']

class InterfaceAdmin(GuardedModelAdmin):
    search_fields = ['id','name', 'description', 'device__tenant__name', 'device__name']
    list_filter = ['device__name']
    ordering = ['device__name', 'name']

class InterfaceInline(admin.StackedInline):
    model = Interface
    can_delete = True
    verbose_name_plural = 'Interfaces'

class LinkAdmin(GuardedModelAdmin):
    search_fields = ['id','interface1__name', 'interface1__name', 'interface1__device__tenant__name', 'interface2__device__tenant__name']
    list_filter = ['interface1__device__name','interface2__device__name']

class NetworkAdmin(GuardedModelAdmin):
    search_fields = ['id','name', 'description', 'vlan']
    ordering = ['tenant__name', 'name']
    list_filter = ['tenant__name']

class VlanAdmin(GuardedModelAdmin):
    search_fields = ['id','interface__name', 'untagged_network__name', 'tagged_networks__name']
    list_filter = ['interface__device__name','interface__device__tenant__name']

class DeviceModelAdmin(GuardedModelAdmin):
    search_fields = ['id','vendor', 'name']

#class DeviceAdmin(admin.ModelAdmin):
class DeviceAdmin(GuardedModelAdmin):
    search_fields = ['id', 'name','tenant__name', 'tenant__identifier']
    list_filter = ['tenant__name']
    #inlines = (InterfaceInline,)

admin.site.register(Address, AddressAdmin)
admin.site.register(Interface, InterfaceAdmin)
admin.site.register(Link, LinkAdmin)
admin.site.register(Network, NetworkAdmin)
admin.site.register(Vlan, VlanAdmin)
admin.site.register(DeviceModel, DeviceModelAdmin)
admin.site.register(Device, DeviceAdmin)

