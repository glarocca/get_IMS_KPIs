#!/bin/bash

##############################################
# Configure * C O N F L U E N C E * settings #
##############################################
export CONFLUENCE_SERVER_URL="https://<ADD_YOUR_CONFLUENCE_SERVER_URL_HERE>"
export CONFLUENCE_AUTH_TOKEN="<ADD_YOUR_CONFLUENCE_AUTH_TOKEN_HERE>"

export SPACEKEY="IMS"
export PAGESIZE="54"
export PARENT="<ADD_THE_CONFLUENCE_SPACE>"

####################################
# J I R A * environmental settings #
####################################
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

###################################################
# A L I V E ** P R O G R E S S ** S E T T I N G S #
###################################################
export PROGRESS_BAR_TITLE="Processing"
export PROGRESS_BAR_MAX_TASKS="60"
export PROGRESS_BAR_MAX_SIZE="70"
# Available bar options:
# smooth, classic, classic2, brackets,
# blocks, bubbles, solid, checks, circles,
# squares, halloween, filling, notes, ruler,
# ruler2, fish, scuba
export PROGRESS_BAR_TYPE="halloween"
export PROGRESS_BAR_DUAL_LINE="False"
# Available spinning options:
# classic, stars, twirl, twirls, horizontal, vertical, waves, waves2, waves3,
# dots, dots_waves, dots_waves2, it, ball_belt, balls_belt, triangles, brackets,
# bubbles, circles, squares, flowers, elements, loving, notes, notes2,
# arrow, arrows, arrows2, arrows_in, arrows_out, radioactive, boat,
# fish, fish2, fishes, crab, alive, wait, wait2, wait3, wait4, pulse
export PROGRESS_BAR_SPINNER_TYPE="twirls"
export PROGRESS_BAR_STATS="True"

# Enable verbose logging
# LOG=INFO, no verbose logging is 'OFF'
# LOG=DEBUG, verbose logging is 'ON'
#export LOG="INFO"
export LOG="DEBUG"

# Time window to consider for the reporting period
export DATE_FROM="2023/07"
export DATE_TO="2023/12"
