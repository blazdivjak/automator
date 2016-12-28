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

import subprocess
from lib.toolson.utils import write

class AnsibleLayerException(Exception):
    pass

class AnsibleHostException(Exception):
    pass

class Ansible():

    """
    Ansible automation engine interaction
    """

    def __init__(self, inventory="develop", ansible_path="ansible/"):

        """
        Initialize Ansible automation engine interaction class. Can be used to execute playbooks and get back information
        :param inventory: Sets which inventory file to use. Before production use dynamic inventory in Ansible.
        """

        self.inventory = inventory
        self.ansible_path = ansible_path

    def playbook(self, playbook_name=None, limit="all"):

        """
        Execute ansible playbook using python code and store results
        Example usage using ansible-playbook in any directory
        ansible-playbook Dropbox/Study/Magistrska/git/automator/ansible/get_facts.yml --inventory-file=Dropbox/Study/Magistrska/git/automator/ansible/develop --limit lab
        :param playbook_name: name of playbook to execute
        :param limit: limit playbook execution to specific hosts or group of hosts
        :return:
        """

        p = subprocess.Popen(["ansible-playbook",
                              "%s/%s" % (self.ansible_path, playbook_name),
                              "--inventory-file",
                              "%s%s" % (self.ansible_path, self.inventory),
                              "--limit",
                              limit],
                              stdout = subprocess.PIPE,
                              stderr = subprocess.PIPE)

        st_out, st_err = p.communicate()
        if "ERROR" in st_err:
            raise AnsibleLayerException("Exception occurred inside Ansible automation layer. Either problem with configuration or playbooks. Exception details:\n%s" % st_err)

        if "failed=1" in st_out or "fatal" in st_out:
            raise AnsibleHostException("Failed processing one or more hosts. Please check retry file for details. Exception details:\n%s" % st_out)

    def write_configuration(self, target_file=None, configuration_content=None):

        """
        Write configuration from database to .YAML representation for Ansible. Store it into target_file inside Ansible
        :param target_file: Target file inside Ansible playbook directory, for example: host_vars/host.arnes.si, groups_vars/lab ...
        :param configuration_content: Configuration content, should be in YAML format or we'll try to convert it
        :return: None if successful, else error
        """

        write(configuration_content,self.ansible_path,target_file)

    def _commit(self, comment):

        """
        Asuming Ansible directory is a git repository, we can commit recently changed configuration into git after chaning.
        :param comment: Make a meaningfull commit.
        :return: None
        """

        raise NotImplementedError

    def _get_retry_list(self):

        """
        Get list of hosts with failed processing.
        :return:
        """

        raise NotImplementedError