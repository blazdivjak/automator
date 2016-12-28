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
from dhcp.models.shared_network import Helper
from dhcp.models.shared_network import SharedNetwork
from dhcp.models.shared_network import Subnet
from dhcp.models.shared_network import Pool
from dhcp.models.shared_network import FixedHost
from dhcp.models.shared_network import Option

class HelperAdmin(admin.ModelAdmin):
    search_fields = ['id', 'interface__name', 'interface__device__name', 'interface__device__tenant__name']
    list_filter = ['interface__device__name']

class OptionAdmin(admin.ModelAdmin):
    search_fields = ['id', 'name', 'tenant__name','option_name','option_value']
    list_filter = ['tenant__name']

class SharedNetworkAdmin(admin.ModelAdmin):
    search_fields = ['id','network__name','network__tenant__name']
    list_filter = ['network__tenant__name']

class PoolAdmin(admin.ModelAdmin):
    search_fields = ['id','start','stop','subnet__shared_network__name']
    list_filter = ['subnet__shared_network__network__name']

class SubnetAdmin(admin.ModelAdmin):
    search_fields = ['id', 'address','router','shared_network__name', 'shared_network__network__tenant__name']
    list_filter = ['shared_network__network__name']

class FixedHostAdmin(admin.ModelAdmin):
    search_fields = ['id','name', 'address','subnet__shared_network__name','subnet__subnet_address','subnet__shared_network__network__tenant__name']
    list_filter = ['subnet__shared_network__network__name']

admin.site.register(Helper, HelperAdmin)
admin.site.register(SharedNetwork, SharedNetworkAdmin)
admin.site.register(Subnet, SubnetAdmin)
admin.site.register(Pool, PoolAdmin)
admin.site.register(FixedHost, FixedHostAdmin)
admin.site.register(Option, OptionAdmin)

