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

from django.conf import settings
from django.db.models.signals import pre_save
from django.db.models.signals import post_save
from django.db.models.signals import pre_delete
from django.db.models.signals import post_delete
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from inventory.models.device import Device
from inventory.models.interface import Interface
from inventory.models.network import Network
from inventory.models.link import Link
from inventory.models.vlan import Vlan
from inventory.models.address import Address
from inventory.models.device import DeviceModel
from django.db.models import Q
from django.conf import settings

@receiver(post_save, sender=Device)
def device_change_handler(sender, **kwargs):

    """
    Get facts from device and install new config onto device if something related changes in automator database
    Triggers should be registered as @receiver signals.
    """

    instance = kwargs['instance']

    instance.notify()

@receiver(post_save, sender=Interface)
@receiver(pre_delete, sender=Interface)
def interface_change_handler(sender, **kwargs):

    """
    Trigger device change if interface changes
    """

    instance = kwargs['instance']

    instance.device.notify()

@receiver(post_save, sender=Network)
@receiver(pre_delete, sender=Network)
def network_change_handler(sender, **kwargs):

    """
    Trigger device change if Network changes
    """

    instance = kwargs['instance']

    vlans = Vlan.objects.filter(Q(untagged_network=instance) | Q(tagged_networks=instance))

    for vlan in vlans:
        vlan.interface.device.notify()

@receiver(post_save, sender=Link)
@receiver(pre_delete, sender=Link)
def link_change_handler(sender, **kwargs):

    """
    Trigger device change if Link changes
    """

    instance = kwargs['instance']

    instance.interface1.device.notify()
    instance.interface2.device.notify()

@receiver(post_save, sender=Vlan)
@receiver(pre_delete, sender=Vlan)
def vlan_change_handler(sender, **kwargs):

    """
    Trigger device change if Vlan changes
    """

    instance = kwargs['instance']
    instance.interface.device.notify()

@receiver(post_save, sender=Address)
@receiver(pre_delete, sender=Address)
def address_change_handler(sender, **kwargs):

    """
    Trigger device change if Address changes
    """

    instance = kwargs['instance']

    interfaces = Interface.objects.filter(addresses=instance)

    for iface in interfaces:

        if iface.device.manage == True:
            iface.device.notify()

@receiver(post_save, sender=DeviceModel)
def device_model_change_handler(sender, **kwargs):

    """
    Trigger device change if DeviceModel changes
    """

    instance = kwargs['instance']

    devices = Device.objects.filter(device_model=instance)

    for device in devices:
        device.notify()

@receiver(post_save, sender=Address)
def dhcp_shared_network_configure_handler(sender, **kwargs):

    """
    Reconfigure DHCP service for Network when added
    """

    from dhcp.models.shared_network import SharedNetwork

    instance = kwargs['instance']

    shared_networks = SharedNetwork.objects.filter(network=instance.network)

    for network in shared_networks:
        network.configure()