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
from views.swagger import schema_view

from tenants.views.tenant import TenantViewSet

"""
API Endpoints for Tenants
"""

#Router
router = routers.DefaultRouter()

#Tenants
router.register(r'tenant', TenantViewSet)

#Devices
#device_router = routers.NestedSimpleRouter(router, r'tenants', lookup='tenant')
#device_router.register(r'devices', DeviceViewSet, base_name='devices')

urlpatterns = [
    url(r'^api/v1/tenants/', include(router.urls)),
    #url(r'^api/v1/', include(device_router.urls)),
    url(r'^api/v1/tenants/schema', schema_view),
]