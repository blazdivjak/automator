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

import ipaddress

def convert_access_class(access_class, platform='ios'):
    if platform == 'ios':
        if access_class == 'admin':
            return '15'
        elif access_class == 'user':
            return '1'
        else:
            return '0'
    elif platform == 'junos':
        if access_class == 'admin':
            return 'super-user'
        elif access_class == 'user':
            return 'read-only'
        else:
            return 'unauthorized'
    else:
        return access_class

def is_ipv4(s):

    try:
        address = ipaddress.ip_interface(unicode(s))

        if address.version == 4:
            return True
        else:
            return False

    except Exception as detail:

        return "#VALUE ERROR# %s" % (detail)

def is_ipv6(s):

    try:

        address = ipaddress.ip_interface(unicode(s))

        if address.version == 6:
            return True
        else:
            return False

    except Exception as detail:

        return "#VALUE ERROR# %s" % (detail)

def address_with_netmask(s):

    try:

        address = ipaddress.ip_interface(unicode(s))

        return "%s %s" % (address.ip, address.netmask)

    except Exception as detail:

        return "#VALUE ERROR# %s" % (detail)

def address_with_wildcard(s):

    try:

        address = ipaddress.ip_interface(unicode(s))

        return "%s %s" % (address.ip, address.hostmask)

    except Exception as detail:

        return "#VALUE ERROR# %s" % (detail)

def dhcp_option_is_v4(s):

    if "dhcp6" in s:
        return False

    else:
        return True

def dhcp_option_is_v6(s):

    if "dhcp6" in s:
        return True

    else:
        return False

def cidr_to_netmask(s):

    try:

        address = ipaddress.ip_interface(unicode(s))

        return "%s" % address.netmask

    except Exception as detail:

        return "#VALUE ERROR# %s" % (detail)

class FilterModule(object):
    
    '''
    Filters for networking
    '''

    def filters(self):
        return {
            'convert_access_class' : convert_access_class,
            'is_ipv4': is_ipv4,
            'is_ipv6': is_ipv6,
            'address_with_netmask': address_with_netmask,
            'address_with_wildcard': address_with_wildcard,
            'dhcp_option_is_v4': dhcp_option_is_v4,
            'dhcp_option_is_v6': dhcp_option_is_v6,
            'cidr_to_netmask': cidr_to_netmask
        }
