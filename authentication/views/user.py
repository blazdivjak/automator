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

from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework import status
from rest_framework import views
from rest_framework import viewsets
from rest_framework.response import Response
from api.permissions import ObjectPermissions
from api.mixins import LoggingMixin
from api.mixins import MultiSerializerViewSetMixin
from api.mixins import DefaultMixin
from api.permissions import IsUserOwner
#from authentication.forms import AssociationFilter
from authentication.forms import UserFilter
#from authentication.models.association import Association
#from authentication.serializers import AssociationReadSerializer
#from authentication.serializers import AssociationWriteSerializer
from authentication.serializers import UserSerializer
from rest_framework.decorators import permission_classes
from rest_framework import filters
logger = logging.getLogger('api')

"""
class AssociationViewSet(DefaultMixin,
                         LoggingMixin,
                         MultiSerializerViewSetMixin,
                         viewsets.ModelViewSet):

    serializer_action_classes = {
       'list': AssociationReadSerializer,
       'create': AssociationWriteSerializer,
    }

    queryset = Association.objects.all()
    serializer_class = AssociationWriteSerializer
    filter_class = AssociationFilter
    ordering_fields = ('tenant',)

    def get_permissions(self):

        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.IsAuthenticated(),)
        else:
            return (ObjectPermissions(),)
"""
class UserViewSet(LoggingMixin,
                  viewsets.ModelViewSet):

    """API endpoint for listing Users"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_class = UserFilter
    ordering_fields = ('username',)
    filter_backends = (
        filters.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    )

    def get_permissions(self):

        if self.request.method in permissions.SAFE_METHODS:
            return (IsUserOwner(),)


        if self.request.method == 'POST':
            return (permissions.AllowAny(),)

        return (IsUserOwner(),)

    def create(self, request):

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            User.objects.create_user(**serializer.validated_data)

            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)
        else:

            return Response({
                'status': 'Bad request',
                'message': 'Account could not be created with received data.',
                'errors' : serializer.errors

            }, status=status.HTTP_400_BAD_REQUEST)

class LoginView(LoggingMixin,
                views.APIView):

    def post(self, request, format=None):
        data = json.loads(request.body)

        username = data.get('username', None)
        password = data.get('password', None)

        user = authenticate(username=username,password=password)

        if user is not None:

            if user.is_active:

                login(request, user)

                serialized = UserSerializer(user)

                return Response(serialized.data)
            else:
                return Response({
                    'status': 'Unauthorized',
                    'message': 'This account has been disabled',
                }, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({
                'status': 'Unauthorized',
                'message': 'Username/password combination invalid'
            }, status=status.HTTP_401_UNAUTHORIZED)

@permission_classes((permissions.IsAuthenticated, ))
class LogoutView(LoggingMixin,
                 views.APIView):

    def post(self, request, format=None):

        logout(request)

        return Response({}, status=status.HTTP_204_NO_CONTENT)