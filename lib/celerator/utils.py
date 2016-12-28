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

from django.core.cache import cache
from celery import Celery
import os
#from arnesaai.celery import app
import json


def task_already_exists(task_type='acl.tasks.device_build_policy',
                        task_kwargs=None,
                        attributes_to_check=['device', 'policy']):

    """
    Check if task you are trying to add into celery already exists there and its waiting to be processed. Only add if task does not exist.
    At this time its required for all fields to have INT values. In most cases database IDs.
    If we dont have any tasks we just return False. Otherwise we process tasks on all workers and return True if we find one tasks that has all attributes
    equal to task we are adding. In case one attribute is not equal we stop checking and continue with the next task. If len(tasks)==0 we just return false.
    :param task_type: which task type we are checking
    :param new_task: kwarg arguments for new task
    :return: True/False
    """

    #Find settings from environment or use defaults
    if os.environ.has_key('BROKER_URL'):
        broker = os.environ['BROKER_URL']
    else:
        broker = "amqp://guest@localhost//"

    if os.environ.has_key('BACKEND_URL'):
        backend = os.environ['BACKEND_URL']
    else:
        backend = "amqp://guest@localhost//"


    app = Celery(os.environ['DJANGO_SETTINGS_MODULE'].split(".")[0], broker=broker, backend=backend)

    # two tasks can call this function at the same time and i.scheduled() is slow. this results in duplicate tasks

    lock_id = '{0}-lock-{1}'.format(task_type, '_'.join([str(value) for key,value in task_kwargs.items()]))

    # cache.add fails if if the key already exists
    acquire_lock = lambda: cache.add(lock_id, 'true', 10)
    # memcache delete is very slow, but we have to use it to take
    # advantage of using add() for atomic locking
    release_lock = lambda: cache.delete(lock_id)

    if not acquire_lock():
        # the same kind of task is already being processed, no need to check again
        return True
    else:
        i = app.control.inspect()
        workers = i.scheduled()
        tasks_are_equal = False

        #Detect if command is being executed with workers stopped
        if workers == None:
            return tasks_are_equal

        for worker, tasks in workers.items():

            for task in tasks:

                tasks_are_equal = False

                existing_task_kwargs=json.loads(str(task['request']['kwargs']).replace("'", '"').replace("u",""))

                if task['request']['name'] == task_type:

                    #Check all specified attributes
                    for attribute in attributes_to_check:
                        if existing_task_kwargs[attribute] == task_kwargs[attribute]:
                            tasks_are_equal = True
                        else:
                            tasks_are_equal = False
                            break

                if tasks_are_equal:
                    release_lock()
                    return True

        release_lock()
        return tasks_are_equal