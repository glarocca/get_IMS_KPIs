#!/usr/bin/env python3
#
#  Copyright 2024 EGI Foundation
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
import time
import warnings
warnings.filterwarnings("ignore")

from bs4 import BeautifulSoup
from datetime import date
from dateutil.parser import parse
from rich.console import Console
from rich.progress import Progress
from rich.table import Table
from utils import colourise, highlight, get_env_settings
from jirautils import getComplaints, getSLAViolations

__author__    = "Giuseppe LA ROCCA"
__email__     = "giuseppe.larocca@egi.eu"
__version__   = "$Revision: 0.8"
__date__      = "$Date: 11/07/2024 06:55:17"
__copyright__ = "Copyright (c) 2024 EGI Foundation"
__license__   = "Apache Licence v2.0"


def parsingHTML(text, find):
    ''' Parsing HTML '''

    soup = BeautifulSoup(text, "lxml")
    soup.findAll(find)
    return(soup.text)


def checkTokens(env):
    ''' Check expiration time of the PAT '''

    _confluence_url = env['CONFLUENCE_SERVER_URL'] + "rest/pat/latest/tokens"
    _jira_url = url = env['JIRA_SERVER_URL'] + "rest/pat/latest/tokens"

    confluence_headers = {
        "Accept": "Application/json",
        "Authorization": "Bearer " + env['CONFLUENCE_AUTH_TOKEN']
    }

    jira_headers = {
        "Accept": "Application/json",
        "Authorization": "Bearer " + env['JIRA_AUTH_TOKEN']
    }

    # 1. Check Confluence's PAT
    try:
         response = requests.get(_confluence_url)
    except requests.exceptions.ConnectionError:
        print("\n[%s] CONFLUENCE_SERVER_URL is *DOWN* or not responding! " %colourise("red", "ERROR"))

    else:
        print("\n[%s] CONFLUENCE_SERVER_URL is *UP* " %colourise("green", "INFO"))
        curl = requests.get(url=_confluence_url, headers=confluence_headers)
        pat = curl.json()

        if curl.status_code == 401:
           confluence_token = -1
        else:
           confluence_token = 1 # OK 

           if (env['LOG'] == "DEBUG"):
              print("[%s] The Personal Access Token (PAT) is valid!" %colourise("green", "INFO"))
              print("- Username    = %s " %pat[0]['name'])
              print("- Created at  = %s, %s" %(pat[0]['createdAt'][0:10], pat[0]['createdAt'][11:19]))
              print("- Expiring at = %s, %s" %(pat[0]['expiringAt'][0:10], pat[0]['expiringAt'][11:19]))

    # 2. Check JIRA's PAT
    try:
         response = requests.get(_jira_url)
    except requests.exceptions.ConnectionError:
        print("\n[%s] JIRA_SERVER_URL is *DOWN* or not responding! " %colourise("red", "ERROR"))
    else:  
        print("\n[%s] JIRA_SERVER_URL is *UP* " %colourise("green", "INFO"))
        curl = requests.get(url=_jira_url, headers=jira_headers)
        pat = curl.json()

        if curl.status_code == 401:
           jira_token = -1
        else:
           jira_token = 1 # OK

           if (env['LOG'] == "DEBUG"):
              print("[%s] The Personal Access Token (PAT) is valid!" %colourise("green", "INFO"))
              print("- Username    = %s " %pat[0]['name'])
              print("- Created at  = %s, %s" %(pat[0]['createdAt'][0:10], pat[0]['createdAt'][11:19]))
              print("- Expiring at = %s, %s" %(pat[0]['expiringAt'][0:10], pat[0]['expiringAt'][11:19]))

    return (confluence_token, jira_token)


def getTotalPages(env):
    ''' Return the totalPages '''
 
    _url = env['CONFLUENCE_SERVER_URL'] \
            + "rest/masterdetail/1.0/detailssummary/lines?spaceKey=" \
            + env['SPACEKEY'] \
            + "&cql=parent=+\"" \
            + env['PARENT'] + "\"" 

    headers = {
            "Accept": "Application/json",
            "Authorization": "Bearer " + env['CONFLUENCE_AUTH_TOKEN']
    }

    # Retrieve spaces that the current user has permission to view
    curl = requests.get(url=_url, headers=headers)
    customers = curl.json()

    return(customers['totalPages'])


def parsing(data, start, end):
    _tmp = data[0:start]

    try:
        # Find the last occurance of the "," string in data
        result = _tmp.rindex(",")
        _tmp = _tmp[result+1:-1]
    except:
        pass

    return(_tmp)


def scraping_data(pattern, data, prefix):
    
    tmp = 0.0
    _storages = ""
   
    # Removing prefix: 'Cloud', 'HEPSPEC', and 'Storage'
    data = data.replace("[Cloud]", "")
    data = data.replace("[HEPSPEC]", "")
    data = data.replace("[Storage]", "")
    result = re.search(pattern, data.strip(), re.IGNORECASE)

    for match in re.finditer(pattern, data.strip()):
        # Start and final index of the match 
        start = match.start()
        end = match.end()

        results = re.findall(pattern, data.strip(), re.IGNORECASE)
        #print('Match found at: [{},{}]'.format(start,end))
        tmp = parsing(data.strip(), start, end)

        if "TB" in pattern:
            if tmp:
               _storages = _storages + " " + tmp
               tmp = _storages

    return(tmp)


def parsingResources(env, details):
   
    resources = [] # Initialize the resources object
    vCPU = RAM = GPU = BS = OS = HEPSPEC = ""

    for resource in details:
        if "[Cloud]" in resource:
            if isinstance(scraping_data("vCPU", parsingHTML(resource, 'a'), "[Cloud]"), str):
               vCPU = scraping_data("vCPU", parsingHTML(resource, 'a'), "[Cloud]").strip()
            if isinstance(scraping_data("GB RAM", parsingHTML(resource, 'a'), "[Cloud]"), str):
               RAM = scraping_data("GB RAM", parsingHTML(resource, 'a'), "[Cloud]").strip()
            #if isinstance(scraping_data("vCPU", parsingHTML(resource, 'a'), "[GPU]"), str):
            #   GPU = scraping_data("card with", parsingHTML(resource, 'a'), "[GPU]").strip()
            #   print(">>> %s" %GPU) 

        if "[HEPSPEC]" in resource:
            if isinstance(scraping_data("M CPU/h", parsingHTML(resource, 'a'), "[HEPSPEC]"), str):
               HEPSPEC = scraping_data("M CPU/h", parsingHTML(resource, 'a'), "[HEPSPEC]").strip()

        if "[Storage]" in resource:
            if isinstance(scraping_data("TB", parsingHTML(resource, 'a'), "[Storage]"), str):
               storages = scraping_data("TB", parsingHTML(resource, 'p'), "[Storage]").strip()
               BS = OS = ""; i = 0
               
               #Generate a list from the given string()
               _storages = storages.split(" ")

               while i < len(_storages):
                   if _storages[i]:
                       if i == 0:
                           BS = _storages[i]
                       elif i == len(_storages)-1 and _storages[i]:
                           OS = _storages[i]
                           
                   i += 1
        
        # Creating the resource object()
        if GPU:
              resources = {
                "Cloud (vCPU cores)": vCPU,
                "RAM (GB)": RAM,
                "HEPSPEC (M CPU/h)": HEPSPEC,
                "GPU": GPU,
                "Block Storage (TB)": BS,
                "Object Storage (TB)": OS
             }
        else:
              resources = {
                "Cloud (vCPU cores)": vCPU,
                "RAM (GB)": RAM,
                "HEPSPEC (M CPU/h)": HEPSPEC,
                "Block Storage (TB)": BS,
                "Object Storage (TB)": OS
             }

    #if (env['LOG'] == "DEBUG"):
    #   print(colourise("green", "[INFO]"), \
    #           "Resources: %s, %s, %s, %s, %s" %(vCPU, RAM, HEPSPEC, BS, OS))

    return (resources, vCPU, RAM, HEPSPEC, BS, OS)     



def getKPIs(env, totalPages, total_CPU, total_RAM, total_HEPSPEC, total_Block_Storage, total_Object_Storage):
    '''  Returns the summary detail of a given spaceKey for a given period '''          

    totalCustomers = 0  # Used to count the total customers in the reporting period
    update = 0          # Used to verify whether the dict. has been updated
    index = 0 
 
    KPI_CRM_Customers_1 = 0
    KPI_CRM_Opportunities_1 = 0
    KPI_CRM_Production_1 = 0
    KPI_CRM_Supported_1 = 0
    KPI_SLM_SLA_1a = KPI_SLM_SLA_1b = 0

    # Temporary vars.
    total_CPU_local = total_RAM_local = total_HEPSPEC_local = 0
    total_Block_Storage_local = total_Object_Storage_local = 0

    # Initialize the JSON objects
    customers_list = resources = []

    KPIs = {
        "KPI:CRM:Customers.1": '0',
        "KPI:CRM:Opportunities.1": '0',
        "KPI:CRM:Production.1": '0',
        "KPI:CRM:Supported.1": '0',
        "KPI:CRM:Complains.1": '0',
        "KPI:CRM:Complains.2": '0',
        "KPI:SLM:SLA.1a": '0',
        "KPI:SLM:SLA.1b": '0',
        "KPI:SLM:SLA.2": '0'
    }

    reporting = {
       "READY FOR PRODUCTION": '0',
       "PRODUCTION": '0',
       "NEW": '0',
       "REQUIREMENTS": '0',
       "DESIGN": '0',
       "PILOT": '0',
       "PILOT EVALUATION": '0',
       "INACTIVE": '0'
    }

    for pageIndex in range(totalPages-1):
        _url = env['CONFLUENCE_SERVER_URL'] \
            + "rest/masterdetail/1.0/detailssummary/lines?spaceKey=" + env['SPACEKEY'] \
            + "&pageSize=" + str(env['PAGESIZE']) \
            + "&pageIndex=" + str(pageIndex)\
            + "&cql=parent=+\"" + env['PARENT'] + "\""
   
        headers = {
            "Accept": "Application/json",
            "Authorization": "Bearer " + env['CONFLUENCE_AUTH_TOKEN']
        }

        curl = requests.get(url=_url, headers=headers)
        customers = curl.json()
        #print(json.dumps(customers['detailLines'], indent=4, sort_keys=False))

        if curl.status_code == 200:
           
           with Progress() as progress:
              task = progress.add_task(
                     "[yellow]Parsing Customers' metadata in progress...",
                     total = 100)

              while not progress.finished:
                    progress.update(task, advance = 0.5)
                    time.sleep(0.05)

           sla_status = ""
           
           if env['DATE_TO'][5:7] == "06":
              semester = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
           else:
              semester = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", \
                          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
           
           for customer in customers['detailLines']:
               # Skip the customers: FitSM, and AoDs users
               if ("FitSM" not in customer['title']) and \
                  ("Users" not in customer['title']):
                   customer_name = customer['title'].replace("Customer: ", "")
                   details = customer['details']
                   #print(json.dumps(details, indent=4, sort_keys=False))
               
                   # Fetching the data for the reporting...
                   if (env['PARENT'] == "1867983"):
                       # (IMS) CustomersDB
                       item=parsingHTML(details[10], 'a').split()
                       _month=(parsingHTML(details[10], 'a').split()[1])
                       _year=(parsingHTML(details[10], 'a').split()[-1])
               
                   # IMPORTANT NOTE: 
                   # 1.) If the condition is '<=' historical/cumulative metrics are calculated
                   # 2.) If the condition is '==' metrics from the specified reporting period are calculated
                   if (int(_year) <= int(env['DATE_TO'][0:4]) and _month in semester):
                   #if (int(_year) == int(env['DATE_TO'][0:4]) and _month in semester):
                      #print(json.dumps(details, indent=4, sort_keys=False))
                      totalCustomers = totalCustomers + 1 
                      
                      if (env['PARENT'] == "1867983"):
                         # (IMS) CustomersDB
                         if re.search(r'\bREADY FOR PRODUCTION\b', details[11]):
                            customer_status="READY FOR PRODUCTION"
                            # Calculate the KPI:CRM.Supported.1
                            KPI_CRM_Supported_1 = KPI_CRM_Supported_1 + 1 
                            #print(customer_status,customer_name, KPI_CRM_Supported_1)
                         elif re.search(r'\bPRODUCTION\b', details[11]):
                            customer_status="PRODUCTION" 
                            # Calculate the KPI:CRM.Production.1
                            KPI_CRM_Production_1 = KPI_CRM_Production_1 + 1 
                            #print(customer_status,customer_name, KPI_CRM_Production_1)
                         elif re.search(r'\bNEW\b', details[11]):
                            customer_status="NEW" 
                            # Calculate the KPI:CRM.Opportunities.1
                            KPI_CRM_Opportunities_1 = KPI_CRM_Opportunities_1 + 1 
                            #print(customer_status,customer_name, KPI_CRM_Opportunities_1)
                         elif re.search(r'\bREQUIREMENTS\b', details[11]):
                            customer_status="REQUIREMENTS" 
                            # Calculate the KPI:CRM.Opportunities.1
                            KPI_CRM_Opportunities_1 = KPI_CRM_Opportunities_1 + 1 
                            #print(customer_status,customer_name, KPI_CRM_Opportunities_1)
                         elif re.search(r'\bDESIGN\b', details[11]):
                            customer_status="DESIGN" 
                            # Calculate the KPI:CRM.Supported.1
                            KPI_CRM_Supported_1 = KPI_CRM_Supported_1 + 1 
                            #print(customer_status,customer_name, KPI_CRM_Supported_1)
                         elif re.search(r'\bPILOT\b', details[11]):
                            customer_status="PILOT" 
                            # Calculate the KPI:CRM.Supported.1
                            KPI_CRM_Supported_1 = KPI_CRM_Supported_1 + 1 
                            #print(customer_status,customer_name, KPI_CRM_Supported_1)
                         elif re.search(r'\bPILOT EVALUATION\b', details[11]):
                            customer_status="PILOT EVALUATION"
                            # Calculate the KPI:CRM.Supported.1
                            KPI_CRM_Supported_1 = KPI_CRM_Supported_1 + 1 
                            #print(customer_status,customer_name, KPI_CRM_Supported_1)
                         else:   
                            customer_status="INACTIVE"
                            totalCustomers = totalCustomers - 1 
                        
                         # Calculate the KPI:CRM.Customers.1
                         KPI_CRM_Customers_1 = KPI_CRM_Customers_1 + 1

                         # Calculate the KPI:SLM.SLA.1
                         if re.search(r'\bFINALIZED\b', details[45]):
                            KPI_SLM_SLA_1a = KPI_SLM_SLA_1a + 1
                        
                         # Calculate the total resources allocated to the Customer
                         resources, total_CPU_local, total_RAM_local, \
                         total_HEPSPEC_local, total_Block_Storage_local, \
                         total_Object_Storage_local = parsingResources(env, details)

                         customer = {
                            "Customer Name": customer_name,
                            #"Customer Start date": parsingHTML(details[14], 'a'),
                            "Customer Start date": parsingHTML(details[10], 'a'),
                            "Customer SLA Contact": parsingHTML(details[7], 'div'),
                            "Customer Status": customer_status,
                            "SLA Status": parsingHTML(details[46], 'div'),
                            "Resources": resources
                         }

                         if (env['LOG'] == "DEBUG"):
                             print("\n[%s]" %colourise("green", "CUSTOMER"))
                             print(json.dumps(customer, indent=4, sort_keys=False))

                         customers_list.append(customer)

                         if total_CPU_local:
                            total_CPU = total_CPU + int(total_CPU_local)
                         if total_HEPSPEC_local:
                            total_HEPSPEC = total_HEPSPEC + float(total_HEPSPEC_local)
                         if total_RAM_local:
                            total_RAM = total_RAM + int(total_RAM_local)
                         if total_Block_Storage_local:
                            total_Block_Storage = total_Block_Storage + float(total_Block_Storage_local)
                         if total_Object_Storage_local:
                            total_Object_Storage = total_Object_Storage + float(total_Object_Storage_local)

                         reporting[customer_status] = int(reporting[customer_status]) + 1
                         update = 1
                    
    # Calculate the KPI:CRM.Complains.1 and KPI:CRM.Complains.2
    # Retrieve the number of total Customers Complains
    complaints = []
    KPI_CRM_Complains_1 = 0
    KPI_CRM_Complains_2 = 0
    complaints = getComplaints(env, complaints)

    if (env['LOG'] == "DEBUG"):
        if len(complaints) > 0:
           print("\n[%s] Customers *COMPLAINTS* in the reporting period (%d)" %(colourise("red", "WARNING"), len(complaints)))
           print(colourise("green", "[INFO]"), \
                "Reporting Period = %s - %s " %(env['DATE_FROM'], env['DATE_TO']))
           #print(json.dumps(complaints, indent=4, sort_keys=False))
           console = Console()
           table = Table(show_header=True, header_style="bold magenta")
           table.add_column("Issue", style="dim")
           table.add_column("URL", width=40)
           table.add_column("Status")
           table.add_column("Created")
           table.add_column("Priority")
           table.add_column("Assignee", width=30)

           for complaint in complaints:
               table.add_row(
                  complaint['Issue'],
                  complaint['URL'],
                  complaint['Status'],
                  complaint['Created'],
                  complaint['Priority'],
                  complaint['Assignee']
                  #complaint['Email']
                )
           console.print(table)

        else:
           print("\n[%s] No Customers *COMPLAINTS* in the reporting period." %colourise("green", "INFO")) 

    for complaint in complaints:
        if (complaint['Status'] == "TODO") or (complaint['Status'] == "NEW"):
            KPI_CRM_Complains_1 = KPI_CRM_Complains_1 + 1
        if (complaint['Status'] == "IN PROGRESS") or (complaint['Status'] == "ON HOLD"):
            KPI_CRM_Complains_2 = KPI_CRM_Complains_2 + 1
    
    # Calculate the KPI:SLM.SLA.2
    # Retrieve the number of SLA Violations 
    violations = []
    violations = getSLAViolations(env, violations)
    
    if (env['LOG'] == "DEBUG"):
        if len(violations) > 0:
           print("\n[%s] VO *SLA VIOLATIONS* in the reporting period (%d)" %(colourise("red", "WARNING"), len(violations)))
           print(colourise("green", "[INFO]"), \
                "Reporting Period = %s - %s " %(env['DATE_FROM'], env['DATE_TO']))

           print("Full list of VO SLA violations is here: %s" %(env['SLA_VIOLATIONS_URL']))
           #print(json.dumps(violations, indent=4, sort_keys=False))
           console = Console()
           table = Table(show_header=True, header_style="bold magenta")
           table.add_column("Issue", style="dim")
           table.add_column("URL", width=40)
           table.add_column("Status")
           table.add_column("Created")
           table.add_column("Priority")

           for violation in violations:
               table.add_row(
                  violation['Issue'],
                  violation['URL'],
                  violation['Status'],
                  violation['Created'],
                  violation['Priority']
                )
           console.print(table)

        else:   
           print("\n[%s] No *SLA VIOLATIONS* in the reporting period." %colourise("green", "INFO")) 

    # Update the KPIs for the CRM and SLM processes
    KPIs = {
        "KPI:CRM.Customers.1": KPI_CRM_Customers_1,
        "KPI:CRM.Opportunities.1": KPI_CRM_Opportunities_1,
        "KPI:CRM.Production.1": KPI_CRM_Production_1,
        "KPI:CRM.Supported.1": KPI_CRM_Supported_1,
        "KPI:CRM.Complains.1": KPI_CRM_Complains_1,
        "KPI:CRM.Complains.2": KPI_CRM_Complains_2,
        "KPI:SLM.SLA.1a": KPI_SLM_SLA_1a,
        "KPI:SLM.SLA.1b": KPI_SLM_SLA_1b,
        "KPI:SLM.SLA.2": len(violations)
    }

    return (customers_list, update, reporting, KPIs, \
            totalCustomers, total_CPU, total_RAM, total_HEPSPEC, \
            total_Block_Storage, total_Object_Storage)



def main():
    
    update = 0
    total = total_CPU = total_RAM = total_HEPSPEC = total_Block_Storage = total_Object_Storage = 0
    KPIs = {}

    # Get the user's settings
    env = get_env_settings()

    if env['LOG'] == "DEBUG":
       print(highlight("green", "\n *** [ENVIRONMENT SETTINGS] *** "))
       print(json.dumps(env, indent=4, sort_keys=False))

    print("\n[%s] Check the status of the servers and tokens " %colourise("green", "INFO"))
    confluence_token, jira_token = checkTokens(env)
       
    if (env['LOG'] == "DEBUG"):
        print("\nLog Level = %s" %colourise("cyan", env['LOG']))

    if (confluence_token > 0 and jira_token > 0):
       print("\nGenerating reporting for the EGI %s space is in progress..." %env['SPACEKEY'])
       print("This operation may take a few minutes to complete. Please wait!")

       with Progress() as progress:
            task = progress.add_task(
                   "[yellow]Parsing the CustomersDB in progress...",
                   total = 100)

            while not progress.finished:
                  progress.update(task, advance = 0.5)
                  time.sleep(0.05)
    
       # Retrieve the totalPages of a spaceKey
       totalPages = getTotalPages(env)

       # Generate reporting for a given time window
       customers_list = []
       customers_list, update, reporting, KPIs, \
               total_Customers, total_CPU, total_RAM, total_HEPSPEC, \
               total_Block_Storage, total_Object_Storage \
       = getKPIs(env, totalPages, total_CPU, total_RAM, total_HEPSPEC, total_Block_Storage, total_Object_Storage)
        
       print(highlight("green", "\n\t\t\t\t\t\t *** [SUMMARY REPORT] ***"))
       if update:
          if (env['PARENT'] == "1867983"):
              print(colourise("cyan", "\n[SPACE] (IMS) CustomersDB"))
          
          print(colourise("green", "[INFO]"), \
                "Reporting Period = %s - %s " %(env['DATE_FROM'], env['DATE_TO']))
          
          print(colourise("green", "[INFO]"), "Total Customers in the reporting period = %s" %total_Customers)
          #print(json.dumps(reporting, indent=4, sort_keys=False))

          console = Console()
          table = Table(show_header=True, header_style="bold magenta")
          table.add_column("Customer Status", style="dim", width=20)
          table.add_column("Total", justify="right")
          for key in reporting:
              table.add_row(key, str(reporting[key]))
          console.print(table)    

          if (env['PARENT'] == "1867983"):

            print(colourise("cyan", "\n[KPIs]"), "CRM/SLM KPIs in the reporting period")
            print(colourise("green", "[INFO]"), \
                 "Reporting Period = %s - %s " %(env['DATE_FROM'], env['DATE_TO']))

            console = Console()
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("KPIs", style="dim", width=23)
            table.add_column("Description", width=90)
            table.add_column("Value", justify="right")

            table.add_row(
              "KPI:CRM.Customers.1", 
              "Number of Customer DB entries that are active in any form (total, cumulative)", 
              str(KPIs['KPI:CRM.Customers.1'])
            )
            
            table.add_row(
              "KPI:CRM.Opportunities.1", 
              "Number of live Customers that are in 'NEW' or 'REQUIREMENTS' state (total, cumulative)", 
              str(KPIs['KPI:CRM.Opportunities.1'])
            )
            
            table.add_row(
              "KPI:CRM.Production.1", 
              "Number of Customers in 'PRODUCTION' state (total, cumulative)",
              str(KPIs['KPI:CRM.Production.1'])
            )

            table.add_row(
              "KPI:CRM.Supported.1", 
              "Number of Customers in 'DESIGN', 'PILOT', 'PILOT EVALUATION', 'READY FOR PRODUCTION' state (total, cumulative)",
              str(KPIs['KPI:CRM.Supported.1'])
            )

            table.add_row(
              "KPI:SLM.SLA.1a",
              "Number of active VO SLAs (total, cumulative)",
              str(KPIs['KPI:SLM.SLA.1a'])
            )
            
            table.add_row(
              "KPI:SLM.SLA.2",
              "Number of SLA violations (total, relative)",
              str(KPIs['KPI:SLM.SLA.2'])
            )

            table.add_row(
              "KPI:CRM.Complains.1",
              "Number of NEW Customer Complains (e.g.: status = TODO, NEW) (total, relative)",
              str(KPIs['KPI:CRM.Complains.1'])
            )
            
            table.add_row(
              "KPI:CRM.Complains.2",
              "Number of OPEN Complains (e.g. status = IN PROGRESS, ON HOLD) (total, relative)",
              str(KPIs['KPI:CRM.Complains.2'])
            )
            
            console.print(table)    
       
            print(colourise("cyan", "\n[SERVICEs]"), "Allocated in the reporting period")
            print(colourise("green", "[INFO]"), \
                "Reporting Period = %s - %s " %(env['DATE_FROM'], env['DATE_TO']))

            console = Console()
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("Service", style="dim")
            table.add_column("Total", justify="right")
            table.add_row("HEPSPEC (M CPU/h)", str(total_HEPSPEC))
            table.add_row("Cloud vCPU cores", str(total_CPU))
            table.add_row("RAM (GB)", str(total_RAM))
            table.add_row("Block Storage (TB)", str(total_Block_Storage))
            table.add_row("Object Storage (TB)", str(total_Object_Storage))
            console.print(table)

       else:          
          print(colourise("red", "[WARNING]"), "No report available in the selected time window.")

    else:
      if (confluence_token == -1):
         print(colourise("red", "[ERROR]"), "Personal Access Tokens *NOT* found or *NOT VALID*")
         print("Please create/update your PAT in the Confluence server: %s " %env['CONFLUENCE_SERVER_URL'])
         print("In Confluence, select your profile picture at the top right of the screen, then choose:") 
         print("Settings > Personal Access Tokens")
      if (jira_token == -1):
         print(colourise("red", "[ERROR]"), "Personal Access Tokens *NOT* found or *NOT VALID*")
         print("Please create/update your PAT in the JIRA server: %s " %env['JIRA_SERVER_URL'])

if __name__ == "__main__":
        main()

