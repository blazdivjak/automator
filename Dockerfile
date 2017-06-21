# Automator container image

# Requirements:
# - RabbitMQ server

LABEL version="0.1"

FROM centos:7

# variables
ENV automator_dir /opt/automator
ENV settings automator.settings

# mount project
VOLUME [$automator_dir]
ADD . $automator_dir

# set workdir
WORKDIR ${automator_dir}

# install dependencies
RUN yum install -y \
python-setuptools \
gcc \
python-devel \
mysql-devel \
git 
RUN easy_install pip
RUN pip install -r requirements.txt

# prepare environment
RUN cd ${automator_dir}
RUN python manage.py reset_db --noinput --settings $settings
RUN python manage.py migrate --settings $settings
RUN python manage.py createcachetable --settings $settings
RUN python manage.py test --settings $settings

CMD cd lib/openconfig/ && ./openconfig.sh & python manage.py runserver 0.0.0.0:8000
