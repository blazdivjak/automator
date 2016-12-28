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

import requests
import json

class APIClientException(Exception):
    pass

class APIClient():

    """
    ArnesAAI API Client to connect to ArnesAAI API Services Orchy and with APIS database
    """

    def __init__(self, username, password, api_url="https://orchy-test.aai.arnes.si/api/", verify=False, page_size=9999):

        """
        Initialization here
        :param username: username to access API
        :param password: password to access API
        :param page_size: API pagination support. specify how many entries per page will be displayed
        :param api_url: api url
        :param verify: verify SSL cert (set to false for development environment or if cert is selfsigned, set to true for production)
        """

        self.api_url = api_url
        self.username=username
        self.password=password
        self.auth=(self.username, self.password) #Support for BASIC authentication used on APIS APIs
        self.token = ""
        self.headers={'Content-Type' : 'application/json; charset=utf-8',
                      'Accept' : 'application/json'}
        self.page_size=page_size
        self.verify=verify
        self.timeout=90

    def authenticate(self, url="token/"):

        """
        Authenticate and get token we will use for all api requests. Use this only if token authentication is used. Else it is not needed.
        :param url: url for authentication API
        :return:
        """

        payload = {'username': self.username,
                   'password' : self.password}

        r = requests.post("%s%s" % (self.api_url,
                                    url),
                                    payload,
                                    verify=self.verify,
                                    timeout=self.timeout)

        if r.status_code==200:

            self.token=json.loads(r.text)['token']
            self.headers['Authorization'] = 'Token %s' %(self.token)

        elif r.status_code==400:
            raise Exception("Exception authenticating to API. Details: %s" % (r.text))

        else:
            raise Exception("Exception authenticating to API. Unhandled error. Code: %s Details: %s" % (r.status_code, r.text))

    #Getters
    #All getters supported by ArnesAAI API
    #List of all possible getter urls can be found on
    #https://orchy-test.aai.arnes.si/api/
    def getter(self, url=None, parameters={}):

        """
        API getter, gets information about entries in database
        :param parameters: parameters in dict format {} e.g. {'organization':'2'} -> get all entities for organization with ID:2
        :param url: entity model API url. url can include entity ID to get specific entity information
        :return: python list object with results
        """

        payload=parameters
        payload['page_size']=self.page_size

        r = requests.get("%s%s" % (self.api_url, url), headers=self.headers, params=payload,verify=self.verify, auth=self.auth, timeout=self.timeout)
        r.encoding='utf-8'

        if r.status_code==200:

            result = json.loads(r.text, encoding='utf-8')

            return result

        else:
            raise APIClientException("Exception executing getter API call on URL: %s%s Details: %s" % (self.api_url, url, r.text))

    def setter(self, url=None, id=None, parameters={}):

        """
        API setter, adds or modifys entry in database
        :param url: url for entities to modify
        :param id: resource ID if we modify
        :param parameters: API call payload
        :return: python list object with results
        """

        payload=parameters

        if id!=None:
            r = requests.put("%s%s%s/" % (self.api_url, url, str(id)), headers=self.headers, data=json.dumps(payload),verify=self.verify, timeout=self.timeout)
            r.encoding='utf-8'
        elif id==None:
            r = requests.post("%s%s" % (self.api_url, url), headers=self.headers, data=json.dumps(payload),verify=self.verify, timeout=self.timeout)
            r.encoding='utf-8'

        if r.status_code in [200, 201, 202, 203,204,205,206]:
            return json.loads(r.text)
        else:
            result={}
            result["error"]="Exception executing setter API call"
            result["url"]="%s%s%s" % (self.api_url, url, id)
            result["code"]=r.status_code
            result["message"]=r.text

            raise APIClientException(json.dumps(result, indent=4, encoding='utf-8'))

    def deletter(self, url=None, id=None):

        """
        Delete selected entity
        :param id:
        :return: True if object wass deleted else it raises exception
        """

        r = requests.delete("%s%s%s/" % (self.api_url, url, id), headers=self.headers, verify=self.verify, timeout=self.timeout)
        r.encoding='utf-8'

        if r.status_code in [200, 201, 202, 203,204,205,206]:

            return True

        else:
            raise APIClientException("Exception executing deletter API call on URL: %s%s%s/ StatusCode: %s Details: %s" % (self.api_url, url,id, r.status_code, r.text))