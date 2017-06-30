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

# Automator container image

FROM centos:7
LABEL version="0.1"

# variables
ENV automator_dir /opt/automator
ENV settings automator.settings

# install dependencies
RUN yum install -y \
	python-setuptools \
	gcc \
	python-devel \
	mysql-devel \
	git 
# Ansible on CentOS 7:
# yum install -y openssl-devel

# mount project
VOLUME [$automator_dir]
ADD . $automator_dir

# set workdir
WORKDIR $automator_dir

RUN easy_install pip
RUN pip install -r requirements.txt

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
