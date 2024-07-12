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

import json
import re
import requests
import urllib.parse
import warnings
warnings.filterwarnings("ignore")
from datetime import date
from dateutil.parser import parse
from utils import colourise

__author__    = "Giuseppe LA ROCCA"
__email__     = "giuseppe.larocca@egi.eu"
__version__   = "$Revision: 0.4"
__date__      = "$Date: 26/09/2023 11:58:27"
__copyright__ = "Copyright (c) 2023 EGI Foundation"
__license__   = "Apache Licence v2.0"


def getServiceOrders(env, orders):
    ''' Return the list of service orders '''

    start = (env['DATE_FROM'].replace("/", "-")) + "-01"
    end = (env['DATE_TO'].replace("/", "-")) + "-01"

    _url = env['JIRA_SERVER_URL'] \
            + "rest/api/latest/search?jql=project=" \
            + env['SERVICE_ORDERS_PROJECTKEY'] \
            + "&created>=" + start \
            + "&created<=" + end 
            #+ " ORDER BY priority DESC, updated DESC"

    headers = {
            "Accept": "Application/json",
            "Authorization": "Bearer " + env['JIRA_AUTH_TOKEN']
    }

   
    curl = requests.get(url=_url, headers=headers)
    orders = curl.json()

    return(orders['issues'])


def getComplaints(env, complaints):
    ''' Return the list of Customer Complaints '''

    _issues = complaints = []

    start = (env['DATE_FROM'].replace("/", "-")) + "-01"
    end = (env['DATE_TO'].replace("/", "-")) + "-01"

    _url = env['JIRA_SERVER_URL'] \
            + "rest/api/latest/search?jql=project=" \
            + env['COMPLAINTS_PROJECTKEY'] \
            + "&maxResults=500" \
            + "&resolution=All" \
            + "&Complaint=Yes" \
            + "&created>=" + start \
            + "&created<=" + end \
            + " ORDER BY priority DESC"

    headers = {
            "Accept": "Application/json",
            "Authorization": "Bearer " + env['JIRA_AUTH_TOKEN']
    }
 
    curl = requests.get(url=_url, headers=headers)
    issues = curl.json()

    for issue in issues['issues']:
        if issue['fields']['status']['name']:
           # customfield_12409 = Complaint
           if issue['fields']['customfield_12409']:
              if "Yes" in (issue['fields']['customfield_12409']['value']):
                 _month = issue['fields']['created'][5:7]
                 _year = issue['fields']['created'][0:4]
        
                 if int(_year) >= int(env['DATE_FROM'][0:4]) and \
                    int(_year) <= int(env['DATE_TO'][0:4]):
                    if int(_month) >= int(env['DATE_FROM'][5:7]):
                        details = getComplaintDetails(env, issue['key'])
                        complaints.append(details)
    
    return(complaints)



def getComplaintDetails(env, issue):
    ''' Retrieve the details for a given customer complaint (issue) '''

    _url = env['JIRA_SERVER_URL'] + "rest/api/latest/issue/" + issue

    headers = {
       "Accept": "Application/json",
       "Authorization": "Bearer " + env['JIRA_AUTH_TOKEN']
    }

    curl = requests.get(url=_url, headers=headers)
    issue_details = curl.json()

    details = []

    details = {
             "Issue": issue,
             "URL": env['JIRA_SERVER_URL'] + "browse/" + issue,
             "Status": issue_details['fields']['status']['name'].upper(),
             "Created": issue_details['fields']['created'][0:10],
             "Priority": issue_details['fields']['priority']['name'].upper(),
             "Assignee": issue_details['fields']['assignee']['displayName'],
             "Email": issue_details['fields']['assignee']['emailAddress'],
             "Complaint": issue_details['fields']['customfield_12409']['value']
    }

    return (details)


def getSLAViolations(env, violations):
    ''' Retrieve the SLA violations in the reporting period ''' 

    _issues = []
    
    start = (env['DATE_FROM'].replace("/", "-")) + "-01"
    end = (env['DATE_TO'].replace("/", "-")) + "-31"

    _url = env['JIRA_SERVER_URL'] \
            + "rest/api/latest/search?jql=project=" \
            + env['SLA_VIOLATIONS_PROJECTKEY'] \
            + "&maxResults=500" \
            + "&issueType=" + env['SLA_VIOLATIONS_ISSUETYPE'] \
            + "&resolution=Unresolved" \
            + "&created>=" + start \
            + "&created<=" + end \
            + " ORDER BY priority DESC, updated DESC"

    headers = {
        "Accept": "Application/json",
        "Authorization": "Bearer " + env['JIRA_AUTH_TOKEN']
    }

    curl = requests.get(url=_url, headers=headers)
    issues = curl.json()

    for issue in issues['issues']:
        if env['SLA_VIOLATIONS_ISSUETYPE'] in (issue['fields']['issuetype']['name']):
            if ((issue['fields']['created'] >= start) and
                (issue['fields']['created'] < end)):
               _issues.append(issue['key'])
               #print(issue['key'], issue['fields']['created'])

    if len(_issues):
       for issue in _issues:
           violations = getSLAViolationsDetails(env, issue, violations)

    return(violations)


def getSLAViolationsDetails(env, issue, violations):
    ''' Retrieve details for a given SLA violation (issue) '''

    _url = env['JIRA_SERVER_URL'] + "rest/api/latest/issue/" + issue

    headers = {
        "Accept": "Application/json",
        "Authorization": "Bearer " + env['JIRA_AUTH_TOKEN']
    }

    curl = requests.get(url=_url, headers=headers)
    issue_details = curl.json()

    if issue_details['fields']['status']['name']:
       _year = issue_details['fields']['created'][0:4]
       _month = issue_details['fields']['created'][5:7]

       #print(_year, _month)

       if (int(_year) == int(env['DATE_TO'][0:4]) and \
           int(_month) <= int(env['DATE_TO'][5:7])):

           violation = {
                "Issue": issue,
                "URL": env['JIRA_SERVER_URL'] + "browse/" + issue,
                "Status": issue_details['fields']['status']['name'].upper(),
                "Created": issue_details['fields']['created'][0:10],
                "Priority": issue_details['fields']['priority']['name'].upper()
           }

           violations.append(violation)

    return (violations)       

