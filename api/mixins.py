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


from rest_framework import authentication
from rest_framework import permissions
from rest_framework import filters
from api.permissions import ObjectPermissions
from api.permissions import IsAssociatedWithTenant
from rest_condition import And
import logging
logger = logging.getLogger('api')


class DefaultMixin(object):

    """
    Default settings for authentication, authorization and filering. We support 3 types of authentication
    1. Basic authentication sending username/password in every request
    2. Token authentication, for retriving a token from auth API
    3. Session authentication

    Users are required to be authenticated

    We allow filtering using arguments and ordering using ordering keyword

    Permissions are asigned based on objects and affiliations.

    """
    #max_paginate_by = 500
    paginate_by = 50
    paginate_by_param = 'page_size'

    authentication_classes = (
        authentication.SessionAuthentication,
        authentication.BasicAuthentication,
        authentication.TokenAuthentication
    )

    filter_backends = (
        filters.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
        filters.DjangoObjectPermissionsFilter,
    )
    permission_classes = [
        And(permissions.IsAuthenticated, IsAssociatedWithTenant),
        ObjectPermissions
    ]

class LoggingMixin(object):

    """
    Class for request logging. Logs all requests to API.
    """

    def finalize_response(self, request, response, *args, **kwargs):

        logger.info("[{0}] method: {1} user: {2} data: {3}".format(self.__class__.__name__, request.method, request.user, request.data))
        return super(LoggingMixin, self).finalize_response(request, response, *args, **kwargs)

class MultiSerializerViewSetMixin(object):

    """
    Class that enables us to select serializer based on request action type defined inside viewset using this mixin.
    """

    def get_serializer_class(self):

        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super(MultiSerializerViewSetMixin, self).get_serializer_class()