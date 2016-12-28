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
from tenants.models.tenant import Tenant
from django.conf import settings

@receiver(post_save, sender=Tenant)
@receiver(pre_delete, sender=Tenant)
def tenant_change_handler(sender, **kwargs):

    """
    Rebuild DHCP Service configuration if changes happen
    """

    from inventory.models.device import Device
    from dhcp.models.shared_network import SharedNetwork

    instance = kwargs['instance']

    devices = Device.objects.filter(tenant=instance)
    for device in devices:
        device.notify()

    shared_networks = SharedNetwork.objects.filter(network__tenant=instance)
    for network in shared_networks:
        network.notify()






