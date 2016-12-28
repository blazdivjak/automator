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

import yaml
import json
from datetime import datetime
from django.core import serializers
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from inventory.models.interface import Interface
from inventory.models.network import Network
from tenants.models.tenant import Tenant
from inventory.models.address import Address
from lib.networker.validator import IPValidator
from lib.networker.validator import IPValidatorException
from inventory.models.validation import ip_validator
from inventory.models.validation import validate_special_characters
from django.conf import settings
import ipaddress
import re

def dhcp_unique_client_id_validator(value):

    """
    Validate MAC or DUID for client
    """

    #Process IPs
    try:
        v = IPValidator()
        v.validate_mac(id=value)

    except IPValidatorException:

        try:
            v.validate_duid(id=value)

        except IPValidatorException as detail:
            raise ValidationError("Field is not in correct format: MAC or DUID.")

def validate_characters_mac(value):

    if re.match("[a-fA-F0-9\:]*$", value) is None:
        raise ValidationError("Invalid characters. Allowed characters are: a-f, A-f, 0-9, :")

class Helper(models.Model):

    """
    Helper object. We assign it to interface if we want to enable dhcp relay on it.
    """

    interface = models.OneToOneField(Interface)
    addresses = models.ManyToManyField(Address)
    active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def to_dict(self):
        return json.loads(serializers.serialize('json',[self,]))[0]['fields']

    def __str__(self):
        return "%s: %s %s" % (self.id, self.interface.name, self.interface.description)

    def __unicode__(self):
        return "%s: %s %s" % (self.id, self.interface.name, self.interface.description)

    class Meta:
        app_label="dhcp"
        permissions = (
            ('view_helper', 'Can view helper'),
        )

class Option(models.Model):

    """
    Options for DHCP
    """
    OPTION_NAMES=(
        ('domain-name','domain-name'),
        ('domain-name-servers','domain-name-servers'),
        ('ntp-servers', 'ntp-servers'),
        ('netbios-name-servers', 'netbios-name-servers'),
        ('dhcp6.domain-search', 'dhcp6.domain-search'),
        ('dhcp6.name-servers', 'dhcp6.name-servers'),
        ('vendor-encapsulated-options', 'vendor-encapsulated-options')
    )

    tenant = models.ForeignKey(Tenant)
    option_name = models.CharField(max_length=255, choices=OPTION_NAMES)
    option_value = models.CharField(max_length=255, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def to_dict(self):
        return json.loads(serializers.serialize('json',[self,]))[0]['fields']

    def __str__(self):
        return "%s %s" % (self.option_name, self.option_value)

    def __unicode__(self):
        return "%s %s" % (self.option_name, self.option_value)

    class Meta:
        app_label="dhcp"
        permissions = (
            ('view_option', 'Can view option'),
        )

class SharedNetwork(models.Model):

    """
    Model for DHCPv4 or DHCPv6 shared network
    """

    #Recommended lease times for different subnet types
    DEFAULT_LEASE_TIMES=(
        ('360','Eduroam'),
        ('3600','Pedagoško'),
        ('3600','Administrativno'),
    )
    MAX_LEASE_TIMES=(
        ('360','Eduroam'),
        ('3600','Pedagoško'),
        ('3600','Administrativno'),
    )

    network = models.OneToOneField(Network)
    options = models.ManyToManyField(Option, blank=True)
    max_lease_time = models.CharField(max_length=10, choices=MAX_LEASE_TIMES)
    default_lease_time = models.CharField(max_length=10, choices=DEFAULT_LEASE_TIMES)
    active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def to_dict(self):

        attributes = json.loads(serializers.serialize('json',[self,]))[0]['fields']
        attributes['id'] = self.id

        return attributes

    def __str__(self):
        return "%s %s: %s" % (self.id, self.network.tenant.name, self.network.name)

    def __unicode__(self):
        return "%s %s: %s" % (self.id, self.network.tenant.name, self.network.name)

    class Meta:
        app_label="dhcp"
        permissions = (
            ('view_sharednetwork', 'Can view shared network'),
        )

    def configure(self):

        """
        Configures service based on addresses configured for selected Network object.
        - Triggered post_save, automaticaly configures subnets and pools.
        - It should also be triggered if Address is added to network. Configuration rebuild is executed automaticaly
        :return: None
        """

        for address in Address.objects.filter(network=self.network):

            v = IPValidator(address.address)

            if v.is_ipv6():
                interface = ipaddress.IPv6Interface(unicode("%s/%s" % (address.address, address.prefix)))
            else:
                interface = ipaddress.IPv4Interface(unicode("%s/%s" % (address.address, address.prefix)))

            if len(Subnet.objects.filter(address=str(interface.network.network_address),
                                         prefix=interface.network.prefixlen))==0:

                s = Subnet(shared_network=self,
                           address=interface.network.network_address,
                           prefix=interface.network.prefixlen,
                           router=interface.network.network_address+1)
                s.save()

                network = ipaddress.ip_network(unicode("%s/%s" % (s.address, s.prefix)))

                p = Pool(subnet=s,
                         start=network[1]+1,
                         stop=network[-2])
                p.save()


    def notify(self):

        from dhcp.tasks import provision_dhcp_service

        provision_dhcp_service.apply_async(kwargs={'noop': 0}, countdown=settings.CELERY_TIMER)

    def get_configuration(self):

        """
        Build configuration dict and return it for SharedNetwork
        @return:
        """

        self.configuration = self.to_dict()
        self.configuration['name'] = "%s_%s" % (self.network_id, self.network.name)
        self.configuration['tenant']={'name': self.network.tenant.name, 'tenant_identifier': self.network.tenant.identifier}
        self.configuration['subnets']=[]
        self.configuration['options']=[]
        self.configuration['ipv4']=False
        self.configuration['ipv6']=False

        options = self.options.all()
        for option in options:
            self.configuration['options'].append(option.to_dict())

        subnets = Subnet.objects.filter(shared_network=self, active=True)
        for subnet in subnets:
            subnet_dict = subnet.to_dict()
            subnet_dict['fixed_hosts']=[]
            subnet_dict['pools']=[]

            #Validate which types of protocols network contains (IPv4 and IPv6)
            v = IPValidator(network_ip=subnet.address,
                            network_mask=subnet.prefix)

            if v.is_ipv4():
                self.configuration['ipv4']=True
            if v.is_ipv6():
                self.configuration['ipv6']=True

            pools = Pool.objects.filter(subnet=subnet, active=True)
            fixed_hosts = FixedHost.objects.filter(subnet=subnet, active=True)

            for pool in pools:
                subnet_dict['pools'].append(pool.to_dict())

            for fixed_host in fixed_hosts:
                subnet_dict['fixed_hosts'].append(fixed_host.to_dict())

            self.configuration['subnets'].append(subnet_dict)

        return self.configuration

class Subnet(models.Model):

    """
    Model for DHCPv4 or DHCPv6 Subnet
    """

    shared_network = models.ForeignKey(SharedNetwork)
    address = models.GenericIPAddressField(unique=True,validators=[ip_validator])
    router = models.GenericIPAddressField(unique=True,validators=[ip_validator])
    prefix = models.IntegerField(default=24)
    active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def to_dict(self):
        return json.loads(serializers.serialize('json',[self,]))[0]['fields']

    def __str__(self):
        return "%s %s: %s/%s" % (self.id, self.shared_network.network.name, self.address, self.prefix)

    def __unicode__(self):
        return "%s %s: %s/%s" % (self.id, self.shared_network.network.name, self.address, self.prefix)

    class Meta:
        app_label="dhcp"
        permissions = (
            ('view_subnet', 'Can view subnet'),
        )

    def validate_subnet(self):

        try:

            v = IPValidator(network_ip=self.address,
                            network_mask=self.prefix)

            if v.is_ipv4():
                if self.router == None:
                    msg="Router IPv4 Address is required."
                    raise ValidationError(msg)
                else:
                    v.validate_ip_is_in_subnet(ip=self.router)

            v.validate_ip_in_allowed_class()

        except Exception as detail:
            msg = "%s" % detail
            raise ValidationError(msg)

    def clean(self):

        self.validate_subnet()

    def save(self, *args, **kwargs):

        self.full_clean()
        super(Subnet, self).save(*args, **kwargs)

class Pool(models.Model):

    """
    Model for DHCPv4 or DHCPv6 Pool
    """
    subnet = models.ForeignKey(Subnet)
    start = models.GenericIPAddressField(unique=True, null=True, blank=True,validators=[ip_validator])
    stop = models.GenericIPAddressField(unique=True, null=True, blank=True,validators=[ip_validator])
    active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def to_dict(self):
        return json.loads(serializers.serialize('json',[self,]))[0]['fields']

    def __str__(self):
        return "%s: subnet: %s range: %s - %s" % (self.subnet.shared_network.network.name, self.subnet.address, self.start, self.stop)

    def __unicode__(self):
        return "%s: subnet: %s range: %s - %s" % (self.subnet.shared_network.network.name, self.subnet.address, self.start, self.stop)

    class Meta:
        app_label="dhcp"
        permissions = (
            ('view_pool', 'Can view pool'),
        )

    def validate_pool(self):

        try:
            v = IPValidator(network_ip=self.subnet.address,
                            network_mask=self.subnet.prefix)

            v.validate_range(start=self.start,
                             stop=self.stop,
                             router=self.subnet.router)

            pools = Pool.objects.filter(subnet=self.subnet).values()
            pools = list(pools)
            pools.append({'range_start': self.start, 'range_stop': self.stop})
            v.validate_range_overlap(ranges=pools)

        except Exception as detail:
            msg = "%s" % detail
            raise ValidationError(msg)

    def clean(self):

        self.validate_pool()

    def save(self, *args, **kwargs):

        self.full_clean()
        super(Pool, self).save(*args, **kwargs)

class FixedHost(models.Model):

    """
    Fixed hostname for some hardcoded computers
    """

    name = models.CharField(max_length=255, validators=[MinLengthValidator(4), validate_special_characters])
    address = models.GenericIPAddressField(validators=[ip_validator])
    mac = models.CharField(max_length=255, validators=[validate_characters_mac])
    subnet = models.ForeignKey(Subnet)
    active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def to_dict(self):
        return json.loads(serializers.serialize('json',[self,]))[0]['fields']

    def __str__(self):
        return "%s %s: subnet: %s %s %s %s" % (self.id, self.subnet.shared_network.network.name, self.subnet.address, self.name, self.address, self.mac)

    def __unicode__(self):
        return "%s %s: subnet: %s %s %s %s" % (self.id, self.subnet.shared_network.network.name, self.subnet.address, self.name, self.address, self.mac)

    class Meta:
        app_label="dhcp"
        unique_together = [('mac', 'subnet'), ('name', 'subnet'), ('subnet', 'address')]
        permissions = (
            ('view_fixedhost', 'Can view fixedhost'),
        )

    def validate_fixed_host(self):

        try:
            v = IPValidator(network_ip=self.subnet.address,
                            network_mask=self.subnet.prefix)

            v.validate_ip_is_in_subnet(ip=self.address)

            if v.is_ipv4():
                v.validate_mac(id=self.mac)

            if v.is_ipv6():
                v.validate_duid(id=self.mac)

        except Exception as detail:
            msg = "%s" % detail
            raise ValidationError(msg)

    def clean(self):

        self.validate_fixed_host()

    def save(self, *args, **kwargs):

        self.full_clean()
        super(FixedHost, self).save(*args, **kwargs)


