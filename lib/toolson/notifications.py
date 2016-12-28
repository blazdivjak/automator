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

from datetime import datetime
from django.core.mail import send_mail

def send_error_message(node="BACKEND-TEST",
                       module="No orchestration system module specified. Please check orchestration system configuration.",
                       action="No Action specified. Please check orchestration system configuration.",
                       message="No message specified. Please check orchestration system configuration.",
                       error_description="No error specified. Please check orchestration system configuration.",
                       mail_from='noreply@arnes.si',
                       mail_to=[]):
    """
    Send error message to email. Specify manage command name where error occurred and error description. This method
    is used for management commands only.
    :param node: orchestration system node using this lib
    :param module: module from orchestration system sending this notification
    :param action: action used
    :param error_description: error string
    :param mail_form: mail from address
    :param mail_to: mail to addresses in array
    :return: None
    """
    try:

        subject = "[%s] %s > %s > %s" % (node, module, action, message)
        message = "[%s] %s > %s\nDate: %s\nAction: %s\nMessage:\n%s" % (node, module, action, datetime.now(), action, error_description)

        send_mail(subject, message, mail_from, mail_to, fail_silently=True)        

    except Exception:
        raise
        #pass

def send_notification_message(node="BACKEND-TEST",
                              module="No orchestration system module specified. Please check orchestration system configuration.",
                              action="No Action specified. Please check orchestration system configuration.",
                              organization="No organization specified. Please check orchestration system configuration.",
                              message="No message specified. Please check orchestration system configuration.",
                              user="User updating was not specified. Please check orchestration system configuration",
                              mail_from='noreply@arnes.si',
                              mail_to=[]):
    """
    Send notification message when something updates
    :param node: orchestration system node using this lib
    :param module: module from orchestration system sending this notification
    :param action: action used
    :param entity: entity modified (eg. idpaas, dhcpaas, mds entity)
    :param mail_form: mail from address
    :param mail_to: mail to addresses in array
    :return: None
    """

    try:
        subject = "[%s] %s > %s > %s" % (node, module, action, message)
        message = "[%s] %s > %s\nDate: %s\nOrganization: %s\nAction: %s\nMessage:\n%s\nUser: %s" % (node, module, action, datetime.now(), organization, action, message, user)

        send_mail(subject, message, mail_from, mail_to, fail_silently=True)

    except Exception as detail:
        raise
        #pass

