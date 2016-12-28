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
from django.contrib import admin
from rest_framework.authtoken.views import obtain_auth_token
from views.swagger import schema_view

urlpatterns = [
    url(r'^', include('authentication.urls', namespace='authentication')),
    url(r'^', include('tenants.urls', namespace='tenants')),
    url(r'^', include('inventory.urls', namespace='inventory')),
    url(r'^', include('dhcp.urls', namespace='dhcp')),
    url(r'^api/v1/schema/', schema_view),
    url(r'^api/v1/token/', obtain_auth_token, name='api-token'),
    #url('^.*$', IndexView.as_view(), name='index'),
]


