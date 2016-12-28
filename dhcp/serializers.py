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

from dhcp.models.shared_network import Helper
from dhcp.models.shared_network import SharedNetwork
from dhcp.models.shared_network import Subnet
from dhcp.models.shared_network import Option
from dhcp.models.shared_network import Pool
from dhcp.models.shared_network import FixedHost

class HelperSerializer(serializers.ModelSerializer):

    class Meta:
        model = Helper

class SharedNetworkSerializer(serializers.ModelSerializer):

    class Meta:
        model = SharedNetwork

class SubnetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subnet

class PoolSerializer(serializers.ModelSerializer):

    class Meta:
        model = Pool

class FixedHostSerializer(serializers.ModelSerializer):

    class Meta:
        model = FixedHost

class OptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Option