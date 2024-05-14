#!/bin/bash

##############################################
# Configure * C O N F L U E N C E * settings #
##############################################
export CONFLUENCE_SERVER_URL="https://confluence.egi.eu/"
export CONFLUENCE_AUTH_TOKEN="<ADD_YOUR_CONFLUENCE_AUTH_TOKEN_HERE>"

export SPACEKEY="IMS"
export PAGESIZE="54"
export PARENT="<ADD_THE_CONFLUENCE_SPACE>"

####################################
# J I R A * environmental settings #
####################################
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
