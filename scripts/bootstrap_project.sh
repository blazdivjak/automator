#!/usr/bin/env bash
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
path=$(pwd) #Default path for developers and production
echo "WARNING: This script is deprecated in favor of docker containers. It may 
be removed in future releases. Please consult README for more information."
USAGE="usage: $1 [team-member | devel ]" #Usage parameters
set -e
if [ "$#" -ne 1 ];
        then echo "Invalid usage..."
        echo $USAGE
        echo ""
        exit 1
fi
if [ "$1" == "team-member" ]; then
        SETTINGS="automator.settings"

        echo "Start AMPQ service! For quick startup we recommend using docker:"
        echo "\$ docker run -d -p 5672:5672 --name rabbitmq rabbitmq"
elif [ "$1" == "devel" ]; then
        SETTINGS="automator.settings_devel"
else
        echo "Unknown parameter:  $1"
        echo $USAGE
        echo ""
        exit 2
fi

echo "VIRTUAL ENVIRONMENT: Checking if virtual environment exists"
if [ ! -f ./.venv/bin/activate ]; then
    echo "VIRTUAL ENVIRONMENT: Does not exist."
    echo "VIRTUAL ENVIRONMENT: Creating"
    pip install virtualenv        
    virtualenv -p `which python` .venv
    echo "VIRTUAL ENVIRONMENT: Created successfully"
fi
echo "VIRTUAL ENVIRONMENT: Activating"
source ./.venv/bin/activate
cd $path
# echo "GIT: Pulling latest version from github"
# git pull
echo "DEPENDENCIES: Installing Python dependencies"
pip install -r requirements.txt
echo "OpenConfig Models: Initialize"
cd $path/lib/openconfig/
./openconfig.sh
cd $path
echo "AUTOMATOR: Remove previous database"
python manage.py reset_db --noinput --settings $SETTINGS
echo "AUTOMATOR: Initialize database and importing data"
echo "AUTOMATOR: This is $1 node"
echo "AUTOMATOR: Using settings $SETTINGS"
echo "AUTOMATOR: Running Django project tests (UNIT, Database, REST, AMPQ)"
python manage.py test --noinput --settings $SETTINGS
echo "DATABASE: Initializing migrations"
python manage.py migrate --settings $SETTINGS
#echo "STATIC: Collecting static files"
#python manage.py collectstatic --noinput --settings $SETTINGS
echo "DATABASE: Creating cache table"
python manage.py createcachetable --settings $SETTINGS
# echo "DATABASE: Loading Initial data"
# echo "SET SAIL FOR ADVENTURE: Use username: admin, password: tMRAGkMDfMk3UJ2zJKgb to login in http://0.0.0.0:8000"
echo "Now create superuser: \"python manage.py createsuperuser --settings $SETTINGS\""
echo "Then start the server: \"python manage.py runserver 0.0.0.0:8000 --settings $SETTINGS\""
