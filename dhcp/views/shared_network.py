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

from api.mixins import LoggingMixin
from api.mixins import DefaultMixin
from api.permissions import ObjectPermissions
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from django.forms.forms import NON_FIELD_ERRORS

from dhcp.models.shared_network import Helper
from dhcp.models.shared_network import SharedNetwork
from dhcp.models.shared_network import Subnet
from dhcp.models.shared_network import Option
from dhcp.models.shared_network import Pool
from dhcp.models.shared_network import FixedHost

from dhcp.serializers import HelperSerializer
from dhcp.serializers import SharedNetworkSerializer
from dhcp.serializers import SubnetSerializer
from dhcp.serializers import OptionSerializer
from dhcp.serializers import PoolSerializer
from dhcp.serializers import FixedHostSerializer

from dhcp.forms import HelperFilter
from dhcp.forms import SharedNetworkFilter
from dhcp.forms import SubnetFilter
from dhcp.forms import OptionFilter
from dhcp.forms import PoolFilter
from dhcp.forms import FixedHostFilter

class HelperViewSet(DefaultMixin,
                    LoggingMixin,
                    viewsets.ModelViewSet):

    """API endpoint for listing relay-agent helpers"""

    queryset = Helper.objects.all()
    serializer_class = HelperSerializer
    filter_class = HelperFilter
    permission_classes = [permissions.IsAuthenticated, ObjectPermissions]

class SharedNetworkViewSet(DefaultMixin,
                           LoggingMixin,
                           viewsets.ModelViewSet):

    """API endpoint for listing DHCP shared networks"""

    queryset = SharedNetwork.objects.all()
    serializer_class = SharedNetworkSerializer
    filter_class = SharedNetworkFilter
    permission_classes = [permissions.IsAuthenticated, ObjectPermissions]

class SubnetViewSet(DefaultMixin,
                    LoggingMixin,
                    viewsets.ModelViewSet):

    """API endpoint for listing DHCP subnets inside shared network"""

    queryset = Subnet.objects.all()
    serializer_class = SubnetSerializer
    filter_class = SubnetFilter
    search_fields = ('subnet_ip', 'subnet_mask')
    permission_classes = [permissions.IsAuthenticated, ObjectPermissions]

    def perform_update(self, serializer):

        try:
            instance = serializer.save()

        except Exception as e:
            non_field_errors = e.message_dict[NON_FIELD_ERRORS]
            msg = {'non_field_errors':  non_field_errors}
            raise ValidationError(msg)

    def perform_create(self, serializer):

        try:
            instance = serializer.save()

        except Exception as e:
            non_field_errors = e.message_dict[NON_FIELD_ERRORS]
            msg = {'non_field_errors':  non_field_errors}
            raise ValidationError(msg)

    def perform_destroy(self, instance):

        instance.delete()

class PoolViewSet(DefaultMixin,
                  LoggingMixin,
                  viewsets.ModelViewSet):

    """API endpoint for listing DHCP subnet pools"""

    queryset = Pool.objects.all()
    serializer_class = PoolSerializer
    filter_class = PoolFilter
    ordering_fields = ( 'id', 'subnet')
    permission_classes = [permissions.IsAuthenticated, ObjectPermissions]

    def perform_update(self, serializer):

        try:
            instance = serializer.save()

        except Exception as e:
            non_field_errors = e.message_dict[NON_FIELD_ERRORS]
            msg = {'non_field_errors':  non_field_errors}
            raise ValidationError(msg)

    def perform_create(self, serializer):

        try:
            instance = serializer.save()

        except Exception as e:
            non_field_errors = e.message_dict[NON_FIELD_ERRORS]
            msg = {'non_field_errors':  non_field_errors}
            raise ValidationError(msg)

    def perform_destroy(self, instance):

        instance.delete()

class FixedHostViewSet(DefaultMixin,
                        LoggingMixin,
                        viewsets.ModelViewSet):

    """API endpoint for listing DHCP fixed hosts"""

    queryset = FixedHost.objects.all()
    serializer_class = FixedHostSerializer
    filter_class = FixedHostFilter
    ordering_fields = ( 'id', 'name', 'ip')
    permission_classes = [permissions.IsAuthenticated, ObjectPermissions]

    def perform_update(self, serializer):

        try:
            instance = serializer.save()

        except Exception as e:
            non_field_errors = e.message_dict[NON_FIELD_ERRORS]
            msg = {'non_field_errors':  non_field_errors}
            raise ValidationError(msg)

    def perform_create(self, serializer):

        try:
            instance = serializer.save()

        except Exception as e:
            non_field_errors = e.message_dict[NON_FIELD_ERRORS]
            msg = {'non_field_errors':  non_field_errors}
            raise ValidationError(msg)

    def perform_destroy(self, instance):

        instance.delete()

class OptionViewSet(DefaultMixin,
                    LoggingMixin,
                    viewsets.ModelViewSet):

    """API endpoint for listing DHCP options"""

    queryset = Option.objects.all()
    serializer_class = OptionSerializer
    filter_class = OptionFilter
    ordering_fields = ( 'id', 'option_name', 'option_value')
    permission_classes = [permissions.IsAuthenticated, ObjectPermissions]

    def perform_update(self, serializer):

        try:
            instance = serializer.save()

        except Exception as e:
            non_field_errors = e.message_dict[NON_FIELD_ERRORS]
            msg = {'non_field_errors':  non_field_errors}
            raise ValidationError(msg)

    def perform_create(self, serializer):

        try:
            instance = serializer.save()

        except Exception as e:
            non_field_errors = e.message_dict[NON_FIELD_ERRORS]
            msg = {'non_field_errors':  non_field_errors}
            raise ValidationError(msg)

    def perform_destroy(self, instance):

        instance.delete()