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

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'i%-*tr5a+u5myg4q$zm1eb-yn$t508(r6nkapue_4bh7ps*o@d'

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'guardian',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_swagger',
    'api',
    'authentication',
    'inventory',
    'tenants',
    'dhcp'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'automator.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'automator.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'automator.sqlite3'),
    }
}

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'guardian.backends.ObjectPermissionBackend',
)

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

#LANGUAGE_CODE = 'sl-si'

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Ljubljana'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_ROOT = 'staticfiles/'
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    'static/',
)

#-----------------------------------------------
#AUTOMATOR ENGINE
#-----------------------------------------------
AUTOMATOR_ENABLE = True

#-----------------------------------------------
#SWAGGER
#-----------------------------------------------

SWAGGER_SETTINGS = {
    "exclude_namespaces": ["inventory"],    #  List URL namespaces to ignore
}

#-----------------------------------------------
#Ansible
#-----------------------------------------------
ANSIBLE = {
    'ENVIRONMENT': 'develop',
    'PATH': 'ansible/',
    'CONFIG_FILE': 'ansible.cfg',
    'INVENTORY_NAME': 'develop',
    'HOST_VARS': 'host_vars/',
    'FACTS_PATH': 'gathered_facts/',
    'INTERFACE_MAP': {
        'ethernetCsmacd': ['ethernet', 'eth', 'ge', 'gi'],
        'propVirtual': ['vlan'],
        'softwareLoopback': ['lo', 'Loopback', 'loopback'],
        'l2vlan' : ['GigabitEthernet0/1.501'], #todo write regex or smtin :D
        'tunnel': ['gre']
    }
}

#-----------------------------------------------
#DHCP Service
#-----------------------------------------------
DHCP_SERVICE = {
    'HOSTS' : ['vm1.hodor.arnes.si'],
    'INVENTORY_NAME': 'infrastructure',
}
#-----------------------------------------------
#AMQP
#-----------------------------------------------
BROKER_URL = 'amqp://guest@gateway//'
BACKEND_URL = 'amqp://guest@gateway//'
#: Only add pickle to this list if your broker is secured
#: from unwanted access (see userguide/security.html)
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

# some tasks can only run one instance at a time
CELERY_LOCK_EXPIRE = 10

CELERY_TIMER = 10

