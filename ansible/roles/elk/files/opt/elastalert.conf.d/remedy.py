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

import argparse

from lib.apinator.api_client import APIClient

#------------------------------------------------------------------------------------
# Static configuration
#------------------------------------------------------------------------------------

AUTOMATOR_API_URL = "http://localhost:1337/api/v1/"
AUTOMATOR_USER = 'admin'
AUTOMATOR_PASSWORD = 'tMRAGkMDfMk3UJ2zJKgb'

ADDRESS_SPACE = ['193.2.194.248/29']
ROUTER_ADDRESS = ['193.2.194.249/29']

def get_address_space_from_ipam():

    """
    Get address space from IPAM. This is a simple example from static settings.
    :return: dict with router and network ip address space
    """

    print "Allocating extra address space from IPAM: %s" % (ADDRESS_SPACE[0])
    return {'network': ADDRESS_SPACE[0],
            'router': ROUTER_ADDRESS[0]}

def register_new_address_space(address_space=None, network_name=None):

    """
    Register new address space via Automator API and reconfigure interface with gateway for selected network
    :param address_space: address space including network and gateway (router) information in dict format
    :param network_name: network name in format <network_id>_<network_name>
    :return: None
    """

    network_id = network_name.split("_")[0]

    #Register address space for network and router
    api = APIClient(username=AUTOMATOR_USER, password=AUTOMATOR_PASSWORD, api_url=AUTOMATOR_API_URL)
    api.authenticate()
    network = api.getter('inventory/networks/%s/' % (network_id))

    #Register new address space
    print "Registering address space %s into network %s via Automator API" % (ADDRESS_SPACE[0], network_name)
    api.setter('inventory/addresses/',
               parameters={"prefix": address_space['network'].split("/")[1],
                           "network": network_id,
                           "address": address_space['network'].split("/")[0]
                })

    print "Registering router address 193.2.194.249/29 into network %s via Automator API" % (network_name)
    router_address = api.setter('inventory/addresses/',
                                parameters={"prefix": address_space['router'].split("/")[1],
                                            "network": network_id,
                                            "address": address_space['router'].split("/")[0]
                                            })


    #Get interface which is gateway for this network
    interfaces = api.getter('inventory/interfaces/?network=%s' % (network_id))
    if(len(interfaces)>0):
        interface = interfaces[0]
        print "Reconfiguring network element's interface ID: %s Name: %s -> router for network: %s" % (interface['id'],
                                                                                                       interface['name'],
                                                                                                       network_name)
        interface['addresses'].append(router_address['id'])
        api.setter('inventory/interfaces/',
                   parameters=interface,
                   id=interface['id'])

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='IPv4 Address space depletion remediator.')
    parser.add_argument('--network', dest="network_name", help='Network name from Automator. Format <network_id>_<network_name>', required=True)
    args = vars(parser.parse_args())
    network_name = str(args['network_name'])
    print "Remediation starting"
    print "IPv4 Address space depleted for network %s" % (network_name)
    extra_subnet = get_address_space_from_ipam()
    register_new_address_space(extra_subnet, network_name=network_name)
    print "Remediation completed"
