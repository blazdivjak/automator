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

from rest_framework import serializers
from models.device import Device
from models.device import DeviceModel
from models.address import Address
from models.interface import Interface
from models.link import Link
from models.network import Network
from models.vlan import Vlan

class DeviceWriteSerializer(serializers.ModelSerializer):


    class Meta:
        model = Device
        read_only_fields = ('created_at', 'updated_at')

    def get_tenant(self, obj):

        return self.context['tenant']

    def validate(self, data):

        """
        Validate device we are adding
        """

        return data

class DeviceReadSerializer(serializers.ModelSerializer):

    class Meta:
        model = Device
        read_only_fields = ('created_at', 'updated_at', 'test')

class DeviceModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = DeviceModel
        #read_only_fields = ('created_at', 'updated_at', 'test')

class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address

class InterfaceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Interface

class LinkSerializer(serializers.ModelSerializer):

    class Meta:
        model = Link

class NetworkSerializer(serializers.ModelSerializer):

    class Meta:
        model = Network

class VlanSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vlan