# get_KPIs
This repository contains client to get KPIs from the EGI Integrated Management System (IMS)

## Pre-requisites

* `Python 3.10.12+` installed on your local computer
* Install pip3: `apt-get install -y python3-pip`
* Install lmxl library: `sudo pip3 install lxml`
* Install lmxl library: `sudo pip3 install beautifulsoup4`
* Install alive-progress library: `pip3 install alive-progress`

## Generate the KPIs for the reporting period

Edit the `openrc.sh`, and configure the environmental settings

```bash
#!/bin/bash

# Configure the Confluence settings
export CONFLUENCE_SERVER_URL="https://<ADD_YOUR_CONFLUENCE_SERVER_URL_HERE>"
export CONFLUENCE_AUTH_TOKEN="<ADD_YOUR_CONFLUENCE_AUTH_TOKEN_HERE>"

export SPACEKEY="IMS"
export PAGESIZE="54"
export PARENT="<ADD_THE_CONFLUENCE_SPACE>"   # IMS - Customers database

# Configure the Jira settings
export JIRA_SERVER_URL="https://<ADD_YOUR_JIRA_SERVER_URL_HERE>"
export JIRA_AUTH_TOKEN="<ADD_YOUR_JIRA_AUTH_TOKEN_HERE>"

# Project used for the Customers' complains
export COMPLAINS_PROJECTKEY="EGIREQ"

# Project used for the VO SLA violations
export SLA_VIOLATIONS_PROJECTKEY="IMSSLA"
export SLA_VIOLATIONS_ISSUETYPE="SLA Violation"
export SLA_VIOLATIONS_URL="https://confluence.egi.eu/display/IMS/SLA+Violations"

# Project used for the Service Orders
export SERVICE_ORDERS_PROJECTKEY="EOSCSO"
export SERVICE_ORDERS_ISSUETYPE="Service order"

# Enable verbose logging
# LOG=INFO, no verbose logging is 'OFF'
# LOG=DEBUG, verbose logging is 'ON'
#export LOG="INFO"
export LOG="DEBUG"

# Time window to consider for the reporting period
export DATE_FROM="2023/01"
export DATE_TO="2024/12"
```

Source the environment settings and run the client

```bash
]$ clear && source openrc.sh && python3 get_KPIs_v9.py
Log Level = DEBUG

*** [ENVIRONMENT SETTINGS] *** 
{
    "CONFLUENCE_SERVER_URL": "https://<ADD_YOUR_CONFLUENCE_SERVER_URL_HERE>",
    "CONFLUENCE_AUTH_TOKEN": "************************************",
    "SPACEKEY": "IMS",
    "PAGESIZE": "54",
    "PARENT": "1867983",
    "JIRA_SERVER_URL": "https://<ADD_YOUR_JIRA_SERVER_URL_HERE>",
    "JIRA_AUTH_TOKEN": "***************************************",
    "COMPLAINS_PROJECTKEY": "EGIREQ",
    "SLA_VIOLATIONS_PROJECTKEY": "IMSSLA",
    "SLA_VIOLATIONS_ISSUETYPE": "SLA Violation",
    "SLA_VIOLATIONS_URL": "https://confluence.egi.eu/display/IMS/SLA+Violations",
    "SERVICE_ORDERS_PROJECTKEY": "EOSCSO",
    "SERVICE_ORDERS_ISSUETYPE": "Service order",
    "PROGRESS_BAR_TITLE": "Processing",
    "PROGRESS_BAR_MAX_SIZE": "70",
    "PROGRESS_BAR_MAX_TASKS": "60",
    "PROGRESS_BAR_TYPE": "halloween",
    "PROGRESS_BAR_SPINNER_TYPE": "twirls",
    "PROGRESS_BAR_DUAL_LINE": "False",
    "PROGRESS_BAR_STATS": "True",
    "DATE_FROM": "2023/01",
    "DATE_TO": "2024/12",
    "LOG": "DEBUG"
}

[INFO] Check the status of the servers and tokens 

[DEBUG] Check the status of the Confluence and Jira servers and tokens 
Processing |🎃🎃🎃🎃🎃🎃🎃🎃🎃🎃🎃🎃🎃🎃🎃🎃🎃🎃🎃🎃🎃🎃🎃🎃🎃🎃🎃🎃🎃🎃🎃🎃🎃🎃🎃| 2/2 [100%] in 18.7s (0.07/s) 

Generating reporting for the EGI space [IMS] is in progress...
This operation may take a few minutes to complete. Please wait!
on 3: [CUSTOMER] Metadata profile:
on 3: {
          "Customer Name": "SeaDataNet (Blue-Cloud 2026)",
          "Customer Start date": "30 Mar 2021\u00a0",
          "Customer SLA Contact": "Pasquale Pagano, pasquale.pagano@isti.cnr.it",
          "Customer Status": "PRODUCTION",
          "SLA Status": "FINALIZED",
          "Resources": {
              "Cloud (vCPU cores)": "32",
              "RAM (GB)": "32",
              "HEPSPEC (M CPU/h)": "",
              "Block Storage (TB)": "25",
              "Object Storage (TB)": ""
          }
      }
on 4: [CUSTOMER] Metadata profile:
on 4: {
          "Customer Name": "DIH: OiPub",
          "Customer Start date": "07 Jul 2022\u00a0\u00a0",
          "Customer SLA Contact": "Robert Bianchi <robert@oipub.com>",
          "Customer Status": "PRODUCTION",
          "SLA Status": "DEPRECATED",
          "Resources": {
              "Cloud (vCPU cores)": "16",
              "RAM (GB)": "50",
              "HEPSPEC (M CPU/h)": "",
              "Block Storage (TB)": "7",
              "Object Storage (TB)": ""
          }
      }
[..]

on 53: 
       [WARNING] Customers *COMPLAINTS* in the reporting period (6)
on 53: [INFO]    Reporting Period = 2023/01 - 2024/12
on 53: ┏━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━┓
       ┃ Issue      ┃ URL                                 ┃ Status ┃ Created    ┃ Priority  ┃ Assignee                 ┃
       ┡━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━┩
       │ EGIREQ-155 │ https://jira.egi.eu/browse/EGIREQ-… │ DONE   │ 2024-06-14 │ CRITICAL  │ Ville Tenhunen           │
       │ EGIREQ-146 │ https://jira.egi.eu/browse/EGIREQ-… │ DONE   │ 2024-02-19 │ HIGH      │ Tiziana Ferrari          │
       │ EGIREQ-140 │ https://jira.egi.eu/browse/EGIREQ-… │ DONE   │ 2023-11-23 │ LOW       │ Andrea Manzi             │
       │ EGIREQ-136 │ https://jira.egi.eu/browse/EGIREQ-… │ DONE   │ 2023-04-06 │ MEDIUM    │ Giuseppe La Rocca        │
       │ EGIREQ-134 │ https://jira.egi.eu/browse/EGIREQ-… │ DONE   │ 2023-01-31 │ LOW       │ Valeria Ardizzone        │
       │ EGIREQ-133 │ https://jira.egi.eu/browse/EGIREQ-… │ DONE   │ 2023-01-31 │ LOW       │ Giuseppe La Rocca        │
       └────────────┴─────────────────────────────────────┴────────┴────────────┴───────────┴──────────────────────────┘

[..]
       [WARNING] VO *SLA VIOLATIONS* in the reporting period (45)
on 54: [INFO]    Reporting Period = 2023/01 - 2024/12
on 54: Full list of VO SLA violations is here: https://confluence.egi.eu/display/IMS/SLA+Violations
on 54: ┏━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━┓
       ┃ Issue      ┃ URL                                 ┃ Status ┃ Created    ┃ Priority ┃ Assignee                 ┃
       ┡━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━┩
       │ IMSSLA-371 │ https://jira.egi.eu/browse/IMSSLA-… │ DONE   │ 2024-12-12 │ LOW      │ sebastian.luna.valero@e… │
       │ IMSSLA-366 │ https://jira.egi.eu/browse/IMSSLA-… │ DONE   │ 2024-11-04 │ LOW      │ giuseppe.larocca@egi.eu  │
       │ IMSSLA-365 │ https://jira.egi.eu/browse/IMSSLA-… │ DONE   │ 2024-11-04 │ LOW      │ giuseppe.larocca@egi.eu  │
       │ IMSSLA-364 │ https://jira.egi.eu/browse/IMSSLA-… │ DONE   │ 2024-11-04 │ LOW      │ giuseppe.larocca@egi.eu  │
       │ IMSSLA-357 │ https://jira.egi.eu/browse/IMSSLA-… │ DONE   │ 2024-07-26 │ LOW      │ sebastian.luna.valero@e… │
       │ IMSSLA-355 │ https://jira.egi.eu/browse/IMSSLA-… │ DONE   │ 2024-07-05 │ LOW      │ giuseppe.larocca@egi.eu  │
       │ IMSSLA-353 │ https://jira.egi.eu/browse/IMSSLA-… │ DONE   │ 2024-06-18 │ LOW      │ alessandro.paolini@egi.… │
       │ IMSSLA-349 │ https://jira.egi.eu/browse/IMSSLA-… │ DONE   │ 2024-05-14 │ LOW      │ yin.chen@egi.eu          │
       │ IMSSLA-348 │ https://jira.egi.eu/browse/IMSSLA-… │ DONE   │ 2024-05-14 │ LOW      │ yin.chen@egi.eu          │
       │ IMSSLA-347 │ https://jira.egi.eu/browse/IMSSLA-… │ DONE   │ 2024-05-14 │ LOW      │ giuseppe.larocca@egi.eu  │
       │ IMSSLA-346 │ https://jira.egi.eu/browse/IMSSLA-… │ DONE   │ 2024-05-14 │ LOW      │ yin.chen@egi.eu          │
       │ IMSSLA-345 │ https://jira.egi.eu/browse/IMSSLA-… │ DONE   │ 2024-05-14 │ LOW      │ yin.chen@egi.eu          │
       │ IMSSLA-342 │ https://jira.egi.eu/browse/IMSSLA-… │ DONE   │ 2024-03-25 │ LOW      │ giuseppe.larocca@egi.eu  │
       │ IMSSLA-339 │ https://jira.egi.eu/browse/IMSSLA-… │ DONE   │ 2024-01-10 │ LOW      │ alessandro.paolini@egi.… │
       │ IMSSLA-338 │ https://jira.egi.eu/browse/IMSSLA-… │ DONE   │ 2024-01-10 │ LOW      │ alessandro.paolini@egi.… │
       │ IMSSLA-337 │ https://jira.egi.eu/browse/IMSSLA-… │ DONE   │ 2024-01-10 │ LOW      │ alessandro.paolini@egi.… │
       │ IMSSLA-336 │ https://jira.egi.eu/browse/IMSSLA-… │ DONE   │ 2024-01-08 │ LOW      │ giuseppe.larocca@egi.eu  │
       │ IMSSLA-332 │ https://jira.egi.eu/browse/IMSSLA-… │ DONE   │ 2023-12-15 │ LOW      │ alessandro.paolini@egi.… │
       │ IMSSLA-328 │ https://jira.egi.eu/browse/IMSSLA-… │ DONE   │ 2023-11-14 │ LOW      │ yin.chen@egi.eu          │
       │ IMSSLA-327 │ https://jira.egi.eu/browse/IMSSLA-… │ DONE   │ 2023-11-14 │ LOW      │ yin.chen@egi.eu          │
       │ IMSSLA-326 │ https://jira.egi.eu/browse/IMSSLA-… │ DONE   │ 2023-11-14 │ LOW      │ yin.chen@egi.eu          │
       │ IMSSLA-325 │ https://jira.egi.eu/browse/IMSSLA-… │ DONE   │ 2023-11-14 │ LOW      │ yin.chen@egi.eu          │
       │ IMSSLA-324 │ https://jira.egi.eu/browse/IMSSLA-… │ DONE   │ 2023-11-14 │ LOW      │ yin.chen@egi.eu          │
       │ IMSSLA-323 │ https://jira.egi.eu/browse/IMSSLA-… │ DONE   │ 2023-11-14 │ LOW      │ yin.chen@egi.eu          │
       │ IMSSLA-322 │ https://jira.egi.eu/browse/IMSSLA-… │ DONE   │ 2023-11-10 │ LOW      │ alessandro.paolini@egi.… │
       │ IMSSLA-309 │ https://jira.egi.eu/browse/IMSSLA-… │ DONE   │ 2023-08-07 │ LOW      │ alessandro.paolini@egi.… │
       │ IMSSLA-308 │ https://jira.egi.eu/browse/IMSSLA-… │ DONE   │ 2023-08-03 │ LOW      │ giuseppe.larocca@egi.eu  │
       │ IMSSLA-304 │ https://jira.egi.eu/browse/IMSSLA-… │ DONE   │ 2023-07-11 │ LOW      │ alessandro.paolini@egi.… │
       │ IMSSLA-303 │ https://jira.egi.eu/browse/IMSSLA-… │ DONE   │ 2023-07-11 │ LOW      │ alessandro.paolini@egi.… │
       │ IMSSLA-302 │ https://jira.egi.eu/browse/IMSSLA-… │ DONE   │ 2023-07-11 │ LOW      │ alessandro.paolini@egi.… │
       │ IMSSLA-301 │ https://jira.egi.eu/browse/IMSSLA-… │ DONE   │ 2023-07-11 │ LOW      │ alessandro.paolini@egi.… │
       │ IMSSLA-300 │ https://jira.egi.eu/browse/IMSSLA-… │ DONE   │ 2023-07-07 │ LOW      │ alessandro.paolini@egi.… │
       │ IMSSLA-299 │ https://jira.egi.eu/browse/IMSSLA-… │ DONE   │ 2023-07-07 │ LOW      │ alessandro.paolini@egi.… │
       │ IMSSLA-298 │ https://jira.egi.eu/browse/IMSSLA-… │ DONE   │ 2023-07-07 │ LOW      │ alessandro.paolini@egi.… │
       │ IMSSLA-287 │ https://jira.egi.eu/browse/IMSSLA-… │ DONE   │ 2023-05-26 │ LOW      │ yin.chen@egi.eu          │
       │ IMSSLA-286 │ https://jira.egi.eu/browse/IMSSLA-… │ DONE   │ 2023-05-26 │ LOW      │ alessandro.paolini@egi.… │
       │ IMSSLA-285 │ https://jira.egi.eu/browse/IMSSLA-… │ DONE   │ 2023-05-26 │ LOW      │ alessandro.paolini@egi.… │
       │ IMSSLA-283 │ https://jira.egi.eu/browse/IMSSLA-… │ DONE   │ 2023-05-08 │ LOW      │ alessandro.paolini@egi.… │
       │ IMSSLA-282 │ https://jira.egi.eu/browse/IMSSLA-… │ DONE   │ 2023-05-08 │ LOW      │ alessandro.paolini@egi.… │
       │ IMSSLA-275 │ https://jira.egi.eu/browse/IMSSLA-… │ DONE   │ 2023-01-24 │ LOW      │ alessandro.paolini@egi.… │
       │ IMSSLA-274 │ https://jira.egi.eu/browse/IMSSLA-… │ DONE   │ 2023-01-24 │ LOW      │ alessandro.paolini@egi.… │
       │ IMSSLA-273 │ https://jira.egi.eu/browse/IMSSLA-… │ DONE   │ 2023-01-24 │ LOW      │ alessandro.paolini@egi.… │
       │ IMSSLA-272 │ https://jira.egi.eu/browse/IMSSLA-… │ DONE   │ 2023-01-24 │ LOW      │ alessandro.paolini@egi.… │
       │ IMSSLA-271 │ https://jira.egi.eu/browse/IMSSLA-… │ DONE   │ 2023-01-13 │ LOW      │ alessandro.paolini@egi.… │
       │ IMSSLA-270 │ https://jira.egi.eu/browse/IMSSLA-… │ DONE   │ 2023-01-13 │ LOW      │ alessandro.paolini@egi.… │
       └────────────┴─────────────────────────────────────┴────────┴────────────┴──────────┴──────────────────────────┘
on 56: 
       						 *** [SUMMARY REPORT] ***
on 56: 
       [SPACE] (IMS) CustomersDB
on 56: [INFO]  Reporting Period = 2023/01 - 2024/12
on 56: [INFO]  Total Customers in the reporting period = 49
on 56: ┏━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━┓
       ┃ Customer Status      ┃ Total ┃
       ┡━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━┩
       │ READY FOR PRODUCTION │     2 │
       │ PRODUCTION           │    33 │
       │ NEW                  │     4 │
       │ REQUIREMENTS         │     6 │
       │ DESIGN               │     1 │
       │ PILOT                │     3 │
       │ PILOT EVALUATION     │     0 │
       │ INACTIVE             │     0 │
       └──────────────────────┴───────┘
on 57: 
       [KPIs] CRM/SLM KPIs in the reporting period
on 57: [INFO] Reporting Period = 2023/01 - 2024/12


on 58: ┏━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━┓
       ┃ KPIs                    ┃ Description                                                              ┃ Value ┃
       ┡━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━┩
       │ KPI:CRM.Customers.1     │ Number of Customer DB entries that are active in any form (total)        │    49 │
       │ KPI:CRM.Opportunities.1 │ Number of live Customers that are in 'NEW' or 'REQUIREMENTS' state       │    10 │
       │                         │ (total)                                                                  │       │
       │ KPI:CRM.Production.1    │ Number of Customers in 'PRODUCTION' state (total)                        │    33 │
       │ KPI:CRM.Supported.1     │ Number of Customers in 'DESIGN', 'PILOT', 'PILOT EVALUATION', 'READY FOR │     6 │
       │                         │ PRODUCTION' state (total)                                                │       │
       │ KPI:SLM.SLA.1a          │ Number of active VO SLAs (total)                                         │    31 │
       │ KPI:SLM.SLA.2           │ Number of SLA violations                                                 │    45 │
       │ KPI:CRM.Complains.1     │ Number of NEW Customer Complains (e.g.: status = TODO, NEW)              │     0 │
       │ KPI:CRM.Complains.2     │ Number of OPEN Complains (e.g. status = IN PROGRESS, ON HOLD)            │     0 │
       └─────────────────────────┴──────────────────────────────────────────────────────────────────────────┴───────┘
on 59: 
       [SERVICEs] Allocated in the reporting period
on 59: [INFO]     Reporting Period = 2023/01 - 2024/12
on 59: ┏━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┓
       ┃ Service             ┃   Total ┃
       ┡━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━┩
       │ HEPSPEC (M CPU/h)   │   497.0 │
       │ Cloud vCPU cores    │    3574 │
       │ RAM (GB)            │    8400 │
       │ Block Storage (TB)  │ 1552.85 │
       │ Object Storage (TB) │    70.0 │
       └─────────────────────┴─────────┘
Processing |🎃🎃🎃🎃🎃🎃🎃🎃🎃🎃🎃🎃🎃🎃🎃🎃🎃🎃🎃🎃🎃🎃🎃🎃🎃🎃🎃🎃🎃🎃🎃🎃🎃🎃🎃| 60/60 [100%] in 2:10.3 (0.46/s)
```

