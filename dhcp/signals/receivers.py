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
from dhcp.models.shared_network import Helper
from dhcp.models.shared_network import SharedNetwork
from dhcp.models.shared_network import Subnet
from dhcp.models.shared_network import FixedHost
from dhcp.models.shared_network import Pool
from dhcp.models.shared_network import Option
from inventory.tasks import install_config
from django.conf import settings

@receiver(post_save, sender=SharedNetwork)
def dhcp_shared_network_configure_handler(sender, **kwargs):

    """
    Reconfigure DHCP service for Network when added
    """

    instance = kwargs['instance']
    instance.configure()

#TODO: Support this triggers
#@receiver(post_save, sender=Option)
#@receiver(pre_delete, sender=Option)
#@receiver(post_save, sender=Pool)
#@receiver(pre_delete, sender=Pool)
#@receiver(post_save, sender=FixedHost)
#@receiver(pre_delete, sender=FixedHost)

@receiver(post_save, sender=SharedNetwork)
@receiver(pre_delete, sender=SharedNetwork)
def dhcp_shared_network_change_handler(sender, **kwargs):

    """
    Rebuild DHCP Service configuration if changes happen
    """

    instance = kwargs['instance']
    instance.notify()

@receiver(post_save, sender=SharedNetwork)
def dhcp_subnet_change_handler(sender, **kwargs):

    """
    Rebuild DHCP Service configuration if changes happen
    """

    instance = kwargs['instance']
    instance.shared_network.notify()

@receiver(post_save, sender=Subnet)
@receiver(pre_delete, sender=Subnet)
def dhcp_subnet_change_handler(sender, **kwargs):

    """
    Rebuild DHCP Service configuration if changes happen
    """

    instance = kwargs['instance']
    instance.shared_network.notify()

@receiver(post_save, sender=Helper)
@receiver(pre_delete, sender=Helper)
def helper_change_handler(sender, **kwargs):

    """
    Trigger device change if Helper changes
    """

    instance = kwargs['instance']
    instance.interface.device.notify()






