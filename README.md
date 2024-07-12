# get_KPIs
This repository contains client to get KPIs from the EGI Integrated Management System (IMS)

## Pre-requisites

* `Python 3.10.12+` installed on your local computer
* Install pip3: `apt-get install -y python3-pip`
* Install lmxl library: `sudo pip3 install lxml`
* Install lmxl library: `sudo pip3 install beautifulsoup4`

## Generate the KPIs for the reporting period

Edit the `openrc.sh`, and configure the environmental settings

```bash
#!/bin/bash

# Configure the Confluence settings
export CONFLUENCE_SERVER_URL="https://confluence.egi.eu/"
export CONFLUENCE_AUTH_TOKEN="<ADD_YOUR_CONFLUENCE_AUTH_TOKEN_HERE>"

export SPACEKEY="IMS"
export PAGESIZE="54"
export PARENT="<ADD_THE_CONFLUENCE_SPACE>"   # IMS - Customers database

# Configure the Jira settings
export JIRA_SERVER_URL="https://jira.egi.eu/"
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
export DATE_FROM="2023/07"
export DATE_TO="2023/12"
```

Source the environment settings and run the client

```bash
Configuring environment settings in progress...
This operation may take some time to complete. Please wait!


- Environment settings:
{
    "CONFLUENCE_SERVER_URL": "https://confluence.egi.eu/",
    "CONFLUENCE_AUTH_TOKEN": "************************************",
    "SPACEKEY": "IMS",
    "PAGESIZE": "54",
    "PARENT": "1867983",
    "JIRA_SERVER_URL": "https://jira.egi.eu/",
    "JIRA_AUTH_TOKEN": "***************************************",
    "COMPLAINS_PROJECTKEY": "EGIREQ",
    "SLA_VIOLATIONS_PROJECTKEY": "IMSSLA",
    "SLA_VIOLATIONS_ISSUETYPE": "SLA Violation",
    "SLA_VIOLATIONS_URL": "https://confluence.egi.eu/display/IMS/SLA+Violations",
    "SERVICE_ORDERS_PROJECTKEY": "EOSCSO",
    "SERVICE_ORDERS_ISSUETYPE": "Service order",
    "DATE_FROM": "2023/07",
    "DATE_TO": "2023/12",
    "LOG": "DEBUG"
}

[INFO] Check the status of the servers and tokens 

[INFO] CONFLUENCE_SERVER_URL is *UP* 
[INFO] The Personal Access Token (PAT) is valid!
- Username    = glarocca_token 
- Created at  = 2023-10-26, 08:20:27
- Expiring at = 2024-10-25, 08:20:27

[INFO] JIRA_SERVER_URL is *UP* 
[INFO] The Personal Access Token (PAT) is valid!
- Username    = glarocca_JIRA 
- Created at  = 2023-10-26, 08:21:58
- Expiring at = 2024-10-25, 08:21:58

Log Level = DEBUG

Generating reporting for the EGI IMS space is in progress...
This operation may take a few minutes to complete. Please wait!
Parsing the CustomersDB in progress... ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00
Parsing Customers' metadata in progress... ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00

[INFO] Resources: 354, 708, 443, 10, 
{
    "Customer Name": "BioMed (LSGC)",
    "Customer Start date": "02 Mar 2015\u00a0",
    "Customer SLA Contact": "Sorina Pop",
    "Customer Status": "PRODUCTION",
    "SLA Status": "3. Medical and Health Sciences3.1 Basic medicine3.2 Clincal medicine",
    "Resources": {
        "Cloud (vCPU cores)": "354",
        "RAM (GB)": "708",
        "HEPSPEC (M CPU/h)": "443",
        "Block Storage (TB)": "10",
        "Object Storage (TB)": ""
    }
}
[..]

[INFO] Resources: , , , , 
{
    "Customer Name": "TANGO",
    "Customer Start date": "19 Feb 2023\u00a0",
    "Customer SLA Contact": "",
    "Customer Status": "REQUIREMENTS",
    "SLA Status": "",
    "Resources": {
        "Cloud (vCPU cores)": "",
        "RAM (GB)": "",
        "HEPSPEC (M CPU/h)": "",
        "Block Storage (TB)": "",
        "Object Storage (TB)": ""
    }
}

[WARNING] Customers *COMPLAINS* in the reporting period
[INFO] Reporting Period = 2023.07-12 
┏━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Issue      ┃ URL                                      ┃ Status      ┃ Created    ┃ Priority ┃ Assignee                       ┃
┡━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ EGIREQ-140 │ https://jira.egi.eu/browse/EGIREQ-140    │ IN PROGRESS │ 2023-11-23 │ LOW      │ Andrea Manzi                   │
│ EGIREQ-136 │ https://jira.egi.eu/browse/EGIREQ-136    │ DONE        │ 2023-04-06 │ MEDIUM   │ Giuseppe La Rocca              │
│ EGIREQ-134 │ https://jira.egi.eu/browse/EGIREQ-134    │ DONE        │ 2023-01-31 │ LOW      │ Valeria Ardizzone              │
│ EGIREQ-133 │ https://jira.egi.eu/browse/EGIREQ-133    │ DONE        │ 2023-01-31 │ LOW      │ Giuseppe La Rocca              │
└────────────┴──────────────────────────────────────────┴─────────────┴────────────┴──────────┴────────────────────────────────┘

┏━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━┓
┃ Issue      ┃ URL                                      ┃ Status ┃ Created    ┃ Priority ┃
┡━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━┩
│ IMSSLA-332 │ https://jira.egi.eu/browse/IMSSLA-332    │ DONE   │ 2023-12-15 │ LOW      │
│ IMSSLA-328 │ https://jira.egi.eu/browse/IMSSLA-328    │ DONE   │ 2023-11-14 │ LOW      │
│ IMSSLA-327 │ https://jira.egi.eu/browse/IMSSLA-327    │ DONE   │ 2023-11-14 │ LOW      │
│ IMSSLA-326 │ https://jira.egi.eu/browse/IMSSLA-326    │ DONE   │ 2023-11-14 │ LOW      │
│ IMSSLA-325 │ https://jira.egi.eu/browse/IMSSLA-325    │ DONE   │ 2023-11-14 │ LOW      │
│ IMSSLA-324 │ https://jira.egi.eu/browse/IMSSLA-324    │ DONE   │ 2023-11-14 │ LOW      │
│ IMSSLA-323 │ https://jira.egi.eu/browse/IMSSLA-323    │ DONE   │ 2023-11-14 │ LOW      │
│ IMSSLA-322 │ https://jira.egi.eu/browse/IMSSLA-322    │ DONE   │ 2023-11-10 │ LOW      │
│ IMSSLA-309 │ https://jira.egi.eu/browse/IMSSLA-309    │ DONE   │ 2023-08-07 │ LOW      │
│ IMSSLA-308 │ https://jira.egi.eu/browse/IMSSLA-308    │ DONE   │ 2023-08-03 │ LOW      │
│ IMSSLA-304 │ https://jira.egi.eu/browse/IMSSLA-304    │ DONE   │ 2023-07-11 │ LOW      │
│ IMSSLA-303 │ https://jira.egi.eu/browse/IMSSLA-303    │ DONE   │ 2023-07-11 │ LOW      │
│ IMSSLA-302 │ https://jira.egi.eu/browse/IMSSLA-302    │ DONE   │ 2023-07-11 │ LOW      │
│ IMSSLA-301 │ https://jira.egi.eu/browse/IMSSLA-301    │ DONE   │ 2023-07-11 │ LOW      │
│ IMSSLA-300 │ https://jira.egi.eu/browse/IMSSLA-300    │ DONE   │ 2023-07-07 │ LOW      │
│ IMSSLA-299 │ https://jira.egi.eu/browse/IMSSLA-299    │ DONE   │ 2023-07-07 │ LOW      │
│ IMSSLA-298 │ https://jira.egi.eu/browse/IMSSLA-298    │ DONE   │ 2023-07-07 │ LOW      │
└────────────┴──────────────────────────────────────────┴────────┴────────────┴──────────┘

						*** [ SUMMARY REPORT ] ***
[SPACE] (IMS) CustomersDB
[INFO] Reporting Period = 2023.07-12 
[INFO] Total Customers in the reporting period = 51
┏━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━┓
┃ Customer Status      ┃ Total ┃
┡━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━┩
│ READY FOR PRODUCTION │     4 │
│ PRODUCTION           │    38 │
│ NEW                  │     1 │
│ REQUIREMENTS         │     4 │
│ DESIGN               │     1 │
│ PILOT                │     3 │
│ PILOT EVALUATION     │     0 │
└──────────────────────┴───────┘

[KPIs] CRM/SLM KPIs in the reporting period
[INFO] Reporting Period = 2023.07-12 
┏━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━┓
┃ KPIs                    ┃ Description                                                                                ┃ Value ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━┩
│ KPI:CRM.Customers.1     │ Number of Customer DB entries that are active in any form (cumulative)                     │    51 │
│ KPI:CRM.Opportunities.1 │ Number of live Customers that are in 'NEW' or 'REQUIREMENTS' state (total, cumulative)     │     5 │
│ KPI:CRM.Production.1    │ Number of Customers in 'PRODUCTION' state (total, cumulative)                              │    37 │
│ KPI:CRM.Supported.1     │ Number of Customers in 'DESIGN', 'PILOT', 'PILOT EVALUATION', 'READY FOR PRODUCTION' state │     7 │
│                         │ (total, cumulative)                                                                        │       │
│ KPI:SLM.SLA.1a          │ Number of active VO SLAs (total, cumulative)                                               │     0 │
│ KPI:SLM.SLA.2           │ Number of SLA violations (relative)                                                        │    17 │
│ KPI:CRM.Complains.1     │ Number of NEW Customer Complains (e.g.: status = TODO, NEW) (relative)                     │     0 │
│ KPI:CRM.Complains.2     │ Number of OPEN Complains (e.g. status = IN PROGRESS, ON HOLD) (relative)                   │     1 │
└─────────────────────────┴────────────────────────────────────────────────────────────────────────────────────────────┴───────┘

[CAPACITY] Allocated in the reporting period
[INFO] Reporting Period = 2023.07-12 
┏━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┓
┃ Capacity            ┃   Total ┃
┡━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━┩
│ HEPSPEC (M CPU/h)   │   497.0 │
│ Cloud vCPU cores    │    4527 │
│ RAM (GB)            │    6912 │
│ Block Storage (TB)  │ 1608.65 │
│ Object Storage (TB) │    70.0 │
└─────────────────────┴─────────┘
```

