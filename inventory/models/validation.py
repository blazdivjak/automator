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

from django.core.exceptions import ValidationError
from lib.networker.validator import IPValidator
import re

def validate_special_characters(value):

    if re.match("[a-zA-Z0-9\.\-\_]*$", value) is None:
        raise ValidationError("Invalid characters. Allowed characters: a-z, A-Z, 0-9, _, -, .")

def validate_mac(value):

    try:

        validator = IPValidator()
        validator.validate_mac(value)

    except Exception as e:
        raise ValidationError(e)

def validate_interface_type(interface_id):

    pass

def validate_inventory_number(value):

    raise NotImplementedError

def validate_serial_number(value):

    raise NotImplementedError

def ip_validator(value):

    try:
        v = IPValidator(network_ip=value)
        v.validate_ip_in_allowed_class()

    except Exception as detail:
        raise ValidationError(detail)