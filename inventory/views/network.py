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

from inventory.forms import NetworkFilter
from inventory.serializers import NetworkSerializer
from inventory.models.network import Network
from api.mixins import LoggingMixin
from api.mixins import DefaultMixin
from api.permissions import ObjectPermissions
from rest_framework import permissions
from rest_framework import viewsets


class NetworkViewSet(DefaultMixin,
                     LoggingMixin,
                     viewsets.ModelViewSet):

    """
    Network viewset
    """

    queryset = Network.objects.all()
    serializer_class = NetworkSerializer
    filter_class = NetworkFilter
    ordering_fields = ('id',)
    permission_classes = [permissions.IsAuthenticated, ObjectPermissions]