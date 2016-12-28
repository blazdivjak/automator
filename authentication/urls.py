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
from authentication.views.swagger import schema_view
from authentication.views.user import UserViewSet
from authentication.views.user import LoginView
from authentication.views.user import LogoutView

"""
API Endopoints for Authentication and User Management.
"""

#Router
router = routers.DefaultRouter()

#Authentication and authorization
router.register(r'user', UserViewSet)

urlpatterns = [
    url(r'^api/v1/auth/', include(router.urls)),
    url(r'^api/v1/auth/login/$', LoginView.as_view(), name='login'),
    url(r'^api/v1/auth/logout/$', LogoutView.as_view(), name='logout'),
    url(r'^api/v1/auth/schema', schema_view),
]