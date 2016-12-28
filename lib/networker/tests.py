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

import unittest
import ipaddress
from validator import IPValidator
from validator import IPValidatorException

class TestNetworkerMethods(unittest.TestCase):

    def test_class_init(self):

        a = IPValidator(network_ip="193.2.1.0",
                        network_mask=24)
        b = IPValidator(network_ip="193.2.1.0")
        c = IPValidator(network_mask=24)

        self.assertIsInstance(a, IPValidator)
        self.assertIsInstance(b, IPValidator)
        self.assertIsInstance(c, IPValidator)

    def test_get_netmask(self):

        v = IPValidator(network_ip="193.2.1.0",
                        network_mask=24)

        self.assertEqual(v.get_netmask(), ipaddress.ip_network(unicode('193.2.1.0/24')).netmask)

    def test_is_ipv4(self):

        v = IPValidator(network_ip="193.2.1.0",
                        network_mask=24)

        self.assertTrue(v.is_ipv4())

    def test_is_ipv6(self):

        v = IPValidator(network_ip="2001:db8::",
                        network_mask=64)

        self.assertTrue(v.is_ipv6())

    def test_validate_ip_is_in_subnet(self):

        v = IPValidator(network_ip="193.2.1.0",
                        network_mask=24)

        self.assertTrue(v.validate_ip_is_in_subnet(unicode("193.2.1.1")))

        with self.assertRaises(IPValidatorException) as exception:
            v.validate_ip_is_in_subnet(unicode("193.3.1.1"))

        self.assertEqual(str(exception.exception), "IP: 193.3.1.1 is not a member of subnet 193.2.1.0/24")

    def test_validate_range(self):

        v = IPValidator(network_ip="193.2.1.0",
                        network_mask=24)

        self.assertTrue(v.validate_range(start=unicode("193.2.1.100"),
                                         stop=unicode("193.2.1.200"),
                                         router=unicode("193.2.1.1")))

        with self.assertRaises(IPValidatorException) as exception:
            v.validate_range(start=unicode("193.2.1.1"),
                             stop=unicode("193.2.1.200"),
                             router=unicode("193.2.1.1"))
        self.assertEqual(str(exception.exception), "Router IP: 193.2.1.1 is included in range: 193.2.1.1-193.2.1.200")

        with self.assertRaises(IPValidatorException) as exception:
            v.validate_range(start=unicode("193.2.1.100"),
                             stop=unicode("193.3.1.200"),
                             router=unicode("193.2.1.1"))
        self.assertEqual(str(exception.exception), "Range start: 193.2.1.100 or stop: 193.3.1.200 is not a member of subnet 193.2.1.0/24 or start>stop.")


    def test_validate_range_overlap(self):
        v = IPValidator(network_ip="193.2.1.0",
                        network_mask=24)

        self.assertTrue(v.validate_range(start=unicode("193.2.1.100"),
                                         stop=unicode("193.2.1.200"),
                                         router=unicode("193.2.1.1")))

        with self.assertRaises(IPValidatorException) as exception:
            v.validate_range_overlap([{'range_start': '193.2.1.1',
                                     'range_stop': '193.2.1.100'},
                                      {'range_start': '193.2.1.50',
                                       'range_stop': '193.2.1.150'}]),

        self.assertEqual(str(exception.exception), "Ranges for subnet overlap. Range1: 193.2.1.1 - 193.2.1.100 Range2: 193.2.1.50 - 193.2.1.150")


    def test_validate_ip_in_allowed_class(self):
        v = IPValidator(network_ip="193.2.1.0",
                        network_mask=24)

        self.assertIsNone(v.validate_ip_in_allowed_class())

    def test_validate_mac(self):
        v = IPValidator()

        self.assertTrue(v.validate_mac("b8:e8:56:49:e4:48"))

        with self.assertRaises(IPValidatorException) as exception:
            v.validate_mac("00:01:00:06:46:e2:f8:c2:00:08:74:da:ab:6z"),

        self.assertEqual(str(exception.exception),
                         "MAC address is in invalid format. MAC: 00:01:00:06:46:e2:f8:c2:00:08:74:da:ab:6z")

    def test_validate_duid(self):
        v = IPValidator()

        self.assertIsNone(v.validate_duid("00:01:00:06:46:e2:f8:c2:00:08:74:da:ab:64"))

        with self.assertRaises(IPValidatorException) as exception:
            v.validate_duid("00:01:00:06:46:e2:f8:c2:00:08:74:da:ab:6z"),

        self.assertEqual(str(exception.exception),
                         "IPv6 DHCP Unique identified (DUID) is in wrong fromat. Allowed characters are: a-f, A-f, 0-9, :. ID: 00:01:00:06:46:e2:f8:c2:00:08:74:da:ab:6z")

if __name__ == '__main__':
    unittest.main()