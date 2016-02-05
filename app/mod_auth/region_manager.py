#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Copyright 2014 Telefónica Investigación y Desarrollo, S.A.U
#
# This file is part of FI-WARE project.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
#
# You may obtain a copy of the License at:
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#
# See the License for the specific language governing permissions and
# limitations under the License.
#
# For those usages not covered by the Apache version 2.0 License please
# contact with opensource@tid.es
#

# Import flask dependencies
from flask import abort, Response

from app.settings.log import logger
from functools import wraps
from app.mod_auth.AuthorizationManager import AuthorizationManager
from app.settings import settings
import requests
import json
from app.settings.settings import CONTENT_TYPE
import httplib

__author__ = 'fla'


class region():
    regions = []
    ERROR_MESSAGE = '{ "error": { "message": "Bad region", "code": 410 } }'

    def __init__(self):
        """
        Contructor of the class region
        """
        # Get the region list
        # GET http://cloud.lab.fiware.org:4730/v3/OS-EP-FILTER/endpoint_groups

        if not self.regions:
            a = AuthorizationManager(identity_url=settings.OPENSTACK_URL, api_version=settings.AUTH_API_V2)

            # Get the Admin token to validate the access_token
            adm_token = a.get_auth_token(settings.ADM_USER, settings.ADM_PASS, settings.ADM_TENANT_ID,
                                         tenant_name=settings.ADM_TENANT_NAME,
                                         user_domain_name=settings.USER_DOMAIN_NAME)

            s = requests.Session()
            s.headers.update({'X-Auth-Token': adm_token})

            response = s.get('http://cloud.lab.fiware.org:4730/v3/OS-EP-FILTER/endpoint_groups')

            r = json.loads(response.text)

            endpoint_groups = r['endpoint_groups']

            for i in range (0, len(endpoint_groups)):
                # If the specific endpoint_groups has not a filters, it is not a correct
                # region and we discard it.
                region_filter = endpoint_groups[i]['filters']
                if region_filter and 'region_id' in region_filter:
                    self.regions.append(region_filter['region_id'])

            print self.regions

    def validate_region(self, region_name):
        """
        Validate if region_name is a name that can be found
        in the Keystone component.
        :param region_name: The name of the region.
        :return: True if it is correct or false otherwise.
        """
        return region_name in self.regions


def check_region(func):
    """
    Decorator that checks that requested region is a real region
    that exists in keystone.

    :param func:
    :return:
    """

    @wraps(func)
    def _wrap(*args, **kwargs):
        region_name = kwargs['regionid']

        region_management = region()

        logger.info("Checking region: {}...".format(region_name))

        result = region_management.validate_region(region_name)

        if result:
            return func(*args, **kwargs)
        else:
            abort(Response(response=region_management.ERROR_MESSAGE,
                           status=httplib.GONE,
                           content_type=CONTENT_TYPE))

    return _wrap
