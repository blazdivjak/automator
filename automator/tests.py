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

from django.test import TestCase
import socket
import unittest
from kombu import Connection
from django.conf import settings
import os
os.environ['DJANGO_SETTINGS_MODULE']="automator.settings"

def test_celery_connection():

    try:

        conn = Connection(settings.BROKER_URL)
        conn.ensure_connection(max_retries=3)

    except socket.error:
        raise RuntimeError("Failed to connect to RabbitMQ instance at {}".format(settings.BROKER_URL))


class TestBackendMethods(unittest.TestCase):

    def test_celery(self):

        self.assertIsNone(test_celery_connection())


if __name__ == '__main__':
    unittest.main()

