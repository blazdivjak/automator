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

def write(config, path, output_filename):

    """
    Write data stored in config to file
    :param config: configuration stored in memory
    :param path: path to folder
    :param output_filename: filename we will store in
    """

    with open(path+output_filename, 'w') as f:
        f.write(config)

def read(file):

    """
    Read data from file
    :param file: file path
    :return: file content
    """

    with open(file, 'r') as f:
        read_data = f.read()

    return read_data