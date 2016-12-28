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
from models.device import Device
from models.device import DeviceModel
from models.address import Address
from models.interface import Interface
from models.link import Link
from models.network import Network
from models.vlan import Vlan

class DeviceFilter(django_filters.FilterSet):

    class Meta:
        model = Device
        #fields = ('id', 'name')

class DeviceModelFilter(django_filters.FilterSet):

    class Meta:
        model = DeviceModel
        #fields = ('id', 'name')

class AddressFilter(django_filters.FilterSet):

    class Meta:
        model = Address

class InterfaceFilter(django_filters.FilterSet):

    network = django_filters.Filter(name="addresses__network", distinct=True)

    class Meta:
        model = Interface
        fields = ('id', 'name', 'description', 'type', 'state', 'uplink', 'device', 'addresses', 'network')

class LinkFilter(django_filters.FilterSet):

    class Meta:
        model = Link

class NetworkFilter(django_filters.FilterSet):

    class Meta:
        model = Network

class VlanFilter(django_filters.FilterSet):

    class Meta:
        model = Vlan