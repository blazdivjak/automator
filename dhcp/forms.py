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

import django_filters
from dhcp.models.shared_network import Helper
from dhcp.models.shared_network import SharedNetwork
from dhcp.models.shared_network import Subnet
from dhcp.models.shared_network import Option
from dhcp.models.shared_network import Pool
from dhcp.models.shared_network import FixedHost

class HelperFilter(django_filters.FilterSet):

    class Meta:
        model = Helper
        fields = ('id', 'addresses', 'interface__name', 'interface')

class SharedNetworkFilter(django_filters.FilterSet):

    updated_after = django_filters.DateFilter(name='date_updated', lookup_type='gte')

    class Meta:
        model = SharedNetwork
        fields = ('id','updated_after', 'network__tenant', 'network__tenant__identifier', 'options', 'max_lease_time', 'default_lease_time', 'active')

class SubnetFilter(django_filters.FilterSet):

    class Meta:
        model = Subnet
        fields = ('id', 'shared_network', 'address', 'router', 'prefix')

class PoolFilter(django_filters.FilterSet):

    class Meta:
        model = Pool
        fields = ('id', 'start', 'stop', 'subnet')

class FixedHostFilter(django_filters.FilterSet):

    class Meta:
        model = FixedHost
        fields = ('id', 'name', 'address', 'mac', 'subnet','active')

class OptionFilter(django_filters.FilterSet):

    class Meta:
        model = Option
        fields = ('id', 'tenant', 'option_name', 'option_value')