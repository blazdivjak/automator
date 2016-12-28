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
import yaml
from lib.openconfig.oc.interfaces.interface import interface
from oc.interfaces import interfaces
import pyangbind.lib.pybindJSON as pybindJSON
from lib.openconfig.oc.vlans import vlans
from lib.openconfig.oc.relay_agent import relay_agent
import pyangbind.lib.pybindJSON as pybindJSON

def interface_to_openconfig(interfaces_list):

    """
    Serialize interfaces from database to OpenConfig representation
    :param interfaces_list: List of interface model objects
    :return: OpenConfig serialized to dict
    """

    from inventory.models.vlan import Vlan
    from inventory.models.network import Network
    from inventory.models.address import Address
    from lib.networker.validator import IPValidator


    interfaces_openconfig = interfaces()

    for interface in interfaces_list:

        interface_openconfig = interfaces_openconfig.interface.add(interface.name)
        interface_openconfig.config.description = interface.description
        interface_openconfig.config.type = interface.type
        interface_openconfig.config.enabled = interface.state

        # Check if its trunk or access configured
        if interface.type == 'ethernetCsmacd':
            try:

                if interface.vlan.tagged_networks.count()>0:

                    interface_openconfig.ethernet.switched_vlan.config.interface_mode = 'TRUNK'
                    interface_openconfig.ethernet.switched_vlan.config.trunk_vlans.extend([v.vlan for v in  interface.vlan.tagged_networks.all()])

                    if interface.vlan.untagged_network:
                        interface_openconfig.ethernet.switched_vlan.config.native_vlan = interface.vlan.untagged_network.vlan

                elif interface.vlan.untagged_network:

                    interface_openconfig.ethernet.switched_vlan.config.interface_mode = 'ACCESS'
                    interface_openconfig.ethernet.switched_vlan.config.access_vlan = interface.vlan.untagged_network.vlan
                #Get all tagged and untagged objects

            except Vlan.DoesNotExist:
                pass

        if interface.type == 'l2vlan':
            pass
            #TODO: How to detect subinterfaces (based on name?!?) - subinterfaces.subinterface

        if interface.type == 'propVirtual':

            for address in interface.addresses.all():

                v = IPValidator(address.address)
                if v.is_ipv4():
                    interface_openconfig.routed_vlan.config.vlan = address.network.vlan
                    addr = interface_openconfig.routed_vlan.ipv4.addresses.address.add(address.address)
                    addr.config.ip = address.address
                    addr.config.prefix_length = address.prefix
                    #interface_openconfig.routed_vlan.config.prefix = address.prefix

                else:
                    interface_openconfig.routed_vlan.config.vlan = address.network.vlan
                    addr = interface_openconfig.routed_vlan.ipv6.addresses.address.add(address.address)
                    addr.config.ip = address.address
                    addr.config.prefix_length = address.prefix

        if interface.type == 'softwareLoopback':

            subint = interface_openconfig.subinterfaces.subinterface.add(0)

            for address in interface.addresses.all():

                v = IPValidator(address.address)

                if v.is_ipv4():
                    addr = subint.ipv4.addresses.address.add(address.address)
                    addr.config.ip = address.address
                    addr.config.prefix_length = address.prefix
                else:
                    addr = subint.ipv6.addresses.address.add(address.address)
                    addr.config.ip = address.address
                    addr.config.prefix_length = address.prefix

    #print(yaml.safe_dump(json.loads(pybindJSON.dumps(interfaces_openconfig)), default_flow_style=False))
    #print pybindJSON.dumps(interfaces_openconfig, mode='default')
    return interfaces_openconfig.get(filter=True)

def vlan_to_openconfig(vlans_list):

    """
    Serialize vlans from databse to OpenConfig representation
    :param vlans_list: List of vlan model objects
    :return: OpenConfig serialized to dict
    """

    vlans_openconfig = vlans()

    for v in vlans_list:
        vlan_openconfig = vlans_openconfig.vlan.add(v.vlan)
        vlan_openconfig.config.name = v.name

    #print(yaml.safe_dump(json.loads(pybindJSON.dumps(vlans_openconfig)), default_flow_style=False))
    #return pybindJSON.dumps(vlans_openconfig, mode='default')
    return vlans_openconfig.get(filter=True)

def relay_agent_to_openconfig(relay_agents):

    """
    Serialize relay-agent from databse to OpenConfig representation
    :param relay_agents: List of Relay-agent model objects
    :return: OpenConfig serialized to dict
    """

    from inventory.models.interface import Interface

    relay_agents_openconfig = relay_agent()

    for agent in relay_agents:
        relay_agent_openconfig = relay_agents_openconfig.dhcp.interfaces.interface.add(agent.interface.name)
        relay_agent_openconfig.config.enable = True
        for addr in agent.addresses.all():
            relay_agent_openconfig.config.helper_address.append(addr.address)

    return relay_agents_openconfig.get(filter=True)