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

from django.contrib.auth import update_session_auth_hash
from rest_framework import serializers
from django.contrib.auth.models import User
from authentication.models.user import Profile
#from authentication.models.association import Association
from tenants.serializers import TenantSerializer

class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile

class UserSerializer(serializers.ModelSerializer):

    profile = ProfileSerializer(read_only=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    #confirm_password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        #fields = ('id', 'username', 'first_name', 'last_name', 'email', 'password', 'confirm_password', 'profile')
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'password', 'profile')
        read_only_fields = ('created_at', 'updated_at',)
        extra_kwargs = {'password': {'write_only': True}}

        #TODO: Validate if password == confirm_password

        """
        def create(self, validated_data):

            return User.objects.create(**validated_data)

        def update(self, instance, validated_data):

            instance.username = validated_data.get('username', instance.username)
            instance.save()

            password = validated_data.get('password', None)
            confirm_password = validated_data.get('confirm_password', None)

            if password and confirm_password and password == confirm_password:
                instance.set_password(password)
                instance.save()

            update_session_auth_hash(self.context.get('request'), instance)

            return instance
        """

"""
class AssociationWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Association
        read_only_fields = ('created_at', 'updated_at')

class AssociationReadSerializer(serializers.ModelSerializer):

    tenant = TenantSerializer(read_only=True, required=False)
    user = UserSerializer(read_only=True, required=False)

    class Meta:
        model = Association
        fields = ('id', 'tenant', 'user')
        read_only_fields = ('created_at', 'updated_at')
"""
