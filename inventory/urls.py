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

from django.conf.urls import include
from django.conf.urls import url
from rest_framework_nested import routers
from inventory.views.device import DeviceViewSet
from inventory.views.device import DeviceModelViewSet
from inventory.views.address import AddressViewSet
from inventory.views.interface import InterfaceViewSet
from inventory.views.link import LinkViewSet
from inventory.views.network import NetworkViewSet
from inventory.views.vlan import VlanViewSet
from views.swagger import schema_view

"""
API Endopoints for Inventory.
"""

router = routers.DefaultRouter()
router.register(r'addresses', AddressViewSet)
router.register(r'interfaces', InterfaceViewSet)
router.register(r'links', LinkViewSet)
router.register(r'networks', NetworkViewSet)
router.register(r'vlans', VlanViewSet)
router.register(r'devices', DeviceViewSet)
router.register(r'device_models', DeviceModelViewSet)

urlpatterns = [
    url(r'^api/v1/inventory/', include(router.urls)),
    url(r'^api/v1/inventory/schema/', schema_view),
]