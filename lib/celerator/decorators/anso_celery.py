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

import logging
from functools import wraps
from celery import shared_task
from ..utils import task_already_exists

logging = logging.getLogger('tasks')

def shared_task_with_locking(func):

    @shared_task(bind=True)
    @wraps(func)
    def _decorated(*args, **kwargs):

        self = args[0]

        if task_already_exists(task_type=self.name, task_kwargs=kwargs, attributes_to_check=kwargs.keys()):
            return "Task with equal parameters detected in queue. Nothing to do."
        else:
            return func(*args, **kwargs)

    return _decorated
