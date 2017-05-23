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

import os
import unittest
from django.core.mail import outbox
from notifications import send_error_message
from notifications import send_notification_message
from utils import read
from utils import write
import test_settings

class TestToolsonMethods(unittest.TestCase):


    def test_send_error_message(self):

        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'test_settings')

        self.assertIsNone(send_error_message(node="BACKEND-TEST",
                                             module="TEST",
                                             action="Test action",
                                             error_description="Test error",
                                             message="Exception occurred building Test",
                                             mail_from='noreply@arnes.si',
                                             mail_to=["test@arnes.si"]))

        self.assertIn("[BACKEND-TEST] TEST > Test action > Exception occurred building Test", outbox[-1].subject)
        self.assertIn("noreply@arnes.si", outbox[-1].from_email)
        self.assertEqual(["test@arnes.si"], outbox[-1].to)
        self.assertIn("[BACKEND-TEST] TEST > Test action", outbox[-1].subject)
        self.assertIn("Action: Test action", outbox[-1].body)
        self.assertIn("Message:\nTest error", outbox[-1].body)


    def test_send_notification_message(self):

        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'test_settings')

        self.assertIsNone(send_notification_message(node="BACKEND-TEST",
                                                    module="TEST",
                                                    organization="Akademska in raziskovalna mreža Slovenije",
                                                    action="Entity added",
                                                    message="Federation: %s EntityID: %s" % ("ArnesAAI", "https://idp.aai.arnes.si/idp/test/"),
                                                    user="blaz",
                                                    mail_from='noreply@arnes.si',
                                                    mail_to=["test@arnes.si"]))

        self.assertIn("[BACKEND-TEST] TEST > Entity added > Federation: ArnesAAI EntityID: https://idp.aai.arnes.si/idp/test/", outbox[-1].subject)
        self.assertIn("noreply@arnes.si", outbox[-1].from_email)
        self.assertEqual(["test@arnes.si"], outbox[-1].to)
        self.assertIn("[BACKEND-TEST] TEST > Entity added", outbox[-1].subject)
        self.assertIn("Organization: Akademska in raziskovalna mreža Slovenije", outbox[-1].body)
        self.assertIn("Action: Entity added", outbox[-1].body)
        self.assertIn("Message:\nFederation: ArnesAAI EntityID: https://idp.aai.arnes.si/idp/test/", outbox[-1].body)
        self.assertIn("User: blaz", outbox[-1].body)


if __name__ == '__main__':
    unittest.main()
