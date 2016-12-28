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

import itertools
import ipaddress
import re

class IPValidatorException(Exception):
    pass

class IPValidator():

    def __init__(self, network_ip=None, network_mask=None):

        """
        Init something here
        :return:
        """

        if network_ip!=None:
            self.network_ip = ipaddress.ip_address(unicode(network_ip))
            self.network_mask = unicode(network_mask)

            if network_mask!=None:
                self.network=ipaddress.ip_network(unicode("%s/%s" % (network_ip, network_mask)))
            else:
                self.network=ipaddress.ip_network(unicode(network_ip))

    def get_netmask(self):

        """
        Get IPv4 or IPv6 Netmask
        :return netmask: netmask in long format e.g. 255.255.255.0
        """

        return self.network.netmask

    def is_ipv4(self):

        if self.network_ip.version == 4:
            return True
        else:
            return False

    def is_ipv6(self):

        if self.network_ip.version == 6:
            return True
        else:
            return False

    def validate_ip_is_in_subnet(self, ip):

        """
        Validate if IP is a member of a subnet
        :return:
        """

        ip = ipaddress.ip_address(unicode(ip))

        if ip in self.network: #list(ipaddress.ip_network(self.network).hosts()):
            return True
        else:
            raise IPValidatorException("IP: %s is not a member of subnet %s" % (ip, self.network.with_prefixlen))

    def validate_range(self, start, stop, router=None):

        start = ipaddress.ip_address(unicode(start))
        stop = ipaddress.ip_address(unicode(stop))

        if router not in [None, 'None', 'null', '']:
            router = ipaddress.ip_address(unicode(router))
            if start==router or stop==router:
                raise IPValidatorException("Router IP: %s is included in range: %s-%s" % (router, start,stop))

        if (start not in self.network) or (stop not in self.network) or stop<start:
            raise IPValidatorException("Range start: %s or stop: %s is not a member of subnet %s or start>stop." % (start, stop, self.network.with_prefixlen))
        else:
            return True

    def validate_range_overlap(self, ranges):

        """
        Validate if two start/stop ranges are overlaping
        :param ranges = array of dicts with two parameters 'range_start' and 'range_stop'
        :return:
        """

        #Build network from range 1 and check if range two IP addresses are in it
        for x,y in itertools.combinations(ranges,2):

            x1 = ipaddress.ip_address(unicode(x['range_start']))
            y1 = ipaddress.ip_address(unicode(x['range_stop']))


            x2 = ipaddress.ip_address(unicode(y['range_start']))
            y2 = ipaddress.ip_address(unicode(y['range_stop']))

            for network in ipaddress.summarize_address_range(x1,y1):

                #if network.overlaps(x2) or network.overlaps(y2):
                if x2 in network or y2 in network:
                    raise IPValidatorException("Ranges for subnet overlap. Range1: %s - %s Range2: %s - %s" % (x['range_start'], x['range_stop'], y['range_start'],y['range_stop']))

    def validate_ip_in_allowed_class(self):

        """
        Validate if ip belongs to one of the unsupported groups or raise error
        :return:
        """

        if self.network_ip.is_link_local:
            raise IPValidatorException("Address: %s is LinkLocal." % self.network.with_prefixlen)
        elif self.network_ip.is_loopback:
            raise IPValidatorException("Address: %s is Loopback." % self.network.with_prefixlen)
        elif self.network_ip.is_multicast:
            raise IPValidatorException("Address: %s is Multicast." % self.network.with_prefixlen)
        elif self.network_ip.is_private:
            raise IPValidatorException("Address: %s is Private." % self.network.with_prefixlen)
        elif self.network_ip.is_reserved:
            raise IPValidatorException("Address: %s is Reserved." % self.network.with_prefixlen)

    def validate_mac(self, id):

        """
        Validate mac address
        :param mac: mac address
        :return: Boolean value or raise exception if false
        """

        mac_pattern = r'^(?i)([0-9A-F]{2}[:-]){5}([0-9A-F]{2})$'

        if re.match(mac_pattern, id):
            return True
        else:
            raise IPValidatorException("MAC address is in invalid format. MAC: %s" % id)

    def validate_duid(self, id):

        """
        Validate IPv6 DHCP Unique ID
        :param duid:
        :return:
        """

        duid_pattern = r'(?i)([0-9a-fA-F]*)$'

        #Validate length
        if (len(id.replace(":",""))*4)<96 or (len(id.replace(":",""))*4)>160:
            raise IPValidatorException("IPv6 DHCP Unique identified (DUID) is in wrong fromat. Invalid length: %s ID: %s" % (len(id.replace(":",""))*4, id))

        if (len(id.replace(":",""))%2!=0):
            raise IPValidatorException("IPv6 DHCP Unique identified (DUID) is in wrong fromat. Length is not even. ID: %s" % id)

        if not re.match(duid_pattern, id.replace(":","")):
            raise IPValidatorException("IPv6 DHCP Unique identified (DUID) is in wrong fromat. Allowed characters are: a-f, A-f, 0-9, :. ID: %s" % id)