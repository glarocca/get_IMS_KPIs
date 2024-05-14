#!/usr/bin/env python3
#
#  Copyright 2023 EGI Foundation
# 
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#

import configparser
import os
import string


__author__    = "Giuseppe LA ROCCA"
__email__     = "giuseppe.larocca@egi.eu"
__version__   = "$Revision: 0.7"
__date__      = "$Date: 18/08/2023 11:58:27"
__copyright__ = "Copyright (c) 2023 EGI Foundation"
__license__   = "Apache Licence v2.0"


def load_settings(file):
    ''' Load settings from file '''

    fd=open(file, "r")
    participants = fd.readlines()
    return participants


def store_settings(participants, file):
    ''' Store settings (list) to file '''

    with open(file, 'w') as fd:
        for participant in participants:
              fd.write("%s" % participant)


def colourise(colour, text):
    ''' Colourise - colours text in shell. '''
    ''' Returns plain if colour doesn't exist '''

    if colour == "black":
        return "\033[1;30m" + str(text) + "\033[1;m"
    if colour == "red":
        return "\033[1;31m" + str(text) + "\033[1;m"
    if colour == "green":
        return "\033[1;32m" + str(text) + "\033[1;m"
    if colour == "yellow":
        return "\033[1;33m" + str(text) + "\033[1;m"
    if colour == "blue":
        return "\033[1;34m" + str(text) + "\033[1;m"
    if colour == "magenta":
        return "\033[1;35m" + str(text) + "\033[1;m"
    if colour == "cyan":
        return "\033[1;36m" + str(text) + "\033[1;m"
    if colour == "gray":
        return "\033[1;37m" + str(text) + "\033[1;m"
    return str(text)


def highlight(colour, text):
    ''' Highlight - highlights text in shell. '''
    ''' Returns plain if colour doesn't exist. '''

    if colour == "black":
        return "\033[1;40m" + str(text) + "\033[1;m"
    if colour == "red":
        return "\033[1;41m" + str(text) + "\033[1;m"
    if colour == "green":
        return "\033[1;42m" + str(text) + "\033[1;m"
    if colour == "yellow":
        return "\033[1;43m" + str(text) + "\033[1;m"
    if colour == "blue":
        return "\033[1;44m" + str(text) + "\033[1;m"
    if colour == "magenta":
        return "\033[1;45m" + str(text) + "\033[1;m"
    if colour == "cyan":
        return "\033[1;46m" + str(text) + "\033[1;m"
    if colour == "gray":
        return "\033[1;47m" + str(text) + "\033[1;m"
    return str(text)


def get_env_settings():
        ''' Reading profile settings from env '''

        d = {}
        try:
           d['CONFLUENCE_SERVER_URL'] = os.environ['CONFLUENCE_SERVER_URL']
           d['CONFLUENCE_AUTH_TOKEN'] = os.environ['CONFLUENCE_AUTH_TOKEN']
           d['SPACEKEY'] = os.environ['SPACEKEY']
           d['PAGESIZE'] = os.environ['PAGESIZE']
           d['PARENT'] = os.environ['PARENT']
           
           d['JIRA_SERVER_URL'] = os.environ['JIRA_SERVER_URL']
           d['JIRA_AUTH_TOKEN'] = os.environ['JIRA_AUTH_TOKEN']
           d['COMPLAINS_PROJECTKEY'] = os.environ['COMPLAINS_PROJECTKEY']

           d['SLA_VIOLATIONS_PROJECTKEY'] = os.environ['SLA_VIOLATIONS_PROJECTKEY']
           d['SLA_VIOLATIONS_ISSUETYPE'] = os.environ['SLA_VIOLATIONS_ISSUETYPE']
           d['SLA_VIOLATIONS_URL'] = os.environ['SLA_VIOLATIONS_URL']
           
           d['SERVICE_ORDERS_PROJECTKEY'] = os.environ['SERVICE_ORDERS_PROJECTKEY']
           d['SERVICE_ORDERS_ISSUETYPE'] = os.environ['SERVICE_ORDERS_ISSUETYPE']
           
           d['DATE_FROM'] = os.environ['DATE_FROM']
           d['DATE_TO'] = os.environ['DATE_TO']
           d['LOG'] = os.environ['LOG']

        except:
          print(colourise("red", "ERROR: os.environment settings not found!"))
        
        return d

