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

from rest_framework import permissions
from tenants.models.tenant import Tenant

class ObjectPermissions(permissions.DjangoObjectPermissions):

    perms_map = {
        'GET': ['%(app_label)s.view_%(model_name)s'],
        'OPTIONS': ['%(app_label)s.view_%(model_name)s'],
        'HEAD': ['%(app_label)s.view_%(model_name)s'],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }

class IsAssociatedWithTenant(permissions.BasePermission):

    """
    Check if user is associated with tenant
    """

    message = "You are not associated with this tenant. You do not have permission to perform this action."

    def has_permission(self, request, view, *args, **kwargs):

        tenant_pk = view.kwargs.get('tenant_pk', None)

        try:
            tenant = Tenant.objects.get(id=tenant_pk)

        except Tenant.DoesNotExist:

            return False

        #We allow user to list only his tenant and admin to list everything
        if (tenant is not None) and len(request.user.groups.filter(name=tenant.name))>0 or (request.user.is_staff and request.user.is_superuser):
            return True
        else:
            return False

class IsAdmin(permissions.BasePermission):

    """
    Check if user is in admin group and allow him trough
    """

    def has_permission(self, request, view):

        if request.user.is_staff:
            return True

        return False

class IsUserOwner(permissions.BasePermission):

    """
    Check if user equals user in the request or user is admin
    User can add/update itself
    Admin can do all CRUD operations on user
    """

    def has_permission(self, request, view):

        if view.action == 'list' or view.action == 'destroy':
            return request.user.is_staff
        elif view.action == 'retrieve' or view.action == 'update' or view.action == 'partial_update':
            return True
        else:
            return False

    def has_object_permission(self, request, view, user):

        if request.user:
            return user == request.user or request.user.is_staff

        return False

class IsOwnerOrReadOnly(permissions.BasePermission):

    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `owner`.
        return obj.owner == request.user