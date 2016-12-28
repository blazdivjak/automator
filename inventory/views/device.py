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
import logging

from rest_framework import viewsets
from rest_framework.response import Response
from api.mixins import LoggingMixin
from api.mixins import MultiSerializerViewSetMixin
from inventory.serializers import DeviceReadSerializer
from inventory.serializers import DeviceWriteSerializer
from inventory.serializers import DeviceModelSerializer
from inventory.models.device import Device
from inventory.models.device import DeviceModel
from tenants.models.tenant import Tenant
from inventory.forms import DeviceFilter
from inventory.forms import DeviceModelFilter
from django.shortcuts import get_object_or_404
from guardian.shortcuts import get_objects_for_user
from api.mixins import DefaultMixin
from api.permissions import ObjectPermissions
from api.permissions import IsAssociatedWithTenant
from rest_condition import ConditionalPermission, C, And, Or, Not
from rest_framework import permissions

logger = logging.getLogger('api')


class DeviceViewSet(DefaultMixin,
                    LoggingMixin,
                    MultiSerializerViewSetMixin,
                    viewsets.ModelViewSet):

    """
    Viewset for editing devices. It automaticaly sets tenant based on kwargs
    """

    serializer_action_classes = {
       'list': DeviceReadSerializer,
       'retrieve': DeviceReadSerializer,
       'create': DeviceWriteSerializer,
       'update':  DeviceReadSerializer,
       'partial_update': DeviceReadSerializer,
       'destroy': DeviceReadSerializer
    }

    queryset = Device.objects.all()
    serializer_class = DeviceReadSerializer
    filter_class = DeviceFilter
    permission_classes = [permissions.IsAuthenticated, ObjectPermissions]

    """
    def list(self, request,tenant_pk=None):
        devices_queryset = get_objects_for_user(request.user, 'inventory.view_device')
        devices = devices_queryset.filter(tenant=tenant_pk)
        serializer = DeviceReadSerializer(devices, many=True)
        return Response(serializer.data)

    def retrieve(self, request, tenant_pk=None, pk=None):
        queryset = Device.objects.filter(tenant=tenant_pk, id=pk)
        device = get_object_or_404(queryset, pk=pk)
        serializer = DeviceReadSerializer(device)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(tenant=Tenant.objects.get(id=self.kwargs.get('tenant_pk', None)))

    def perform_update(self, serializer):
        serializer.save(tenant=Tenant.objects.get(id=self.kwargs.get('tenant_pk', None)))
    """
class DeviceModelViewSet(DefaultMixin,
                    LoggingMixin,
                    MultiSerializerViewSetMixin,
                    viewsets.ModelViewSet):

    """

    """

    serializer_action_classes = {
       'list': DeviceModelSerializer,
       'retrieve': DeviceModelSerializer,
       'create': DeviceModelSerializer,
       'update':  DeviceModelSerializer,
       'partial_update': DeviceModelSerializer,
       'destroy': DeviceModelSerializer
    }

    queryset = DeviceModel.objects.all()
    serializer_class = DeviceModelSerializer
    filter_class = DeviceModelFilter
    permission_classes = [permissions.IsAuthenticated, ObjectPermissions]
