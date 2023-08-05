#!/usr/bin/env bash

# Usage: 
# sh src/noted/scripts/setup.sh [action]
# Actions:
# setup: Setup NOTED, create the folder structure
# package [package_name]: Package all Python packages in the repository and copy them to the directory specified as the local package index location. If package_name is provided, only the requested package is packaged.

MAIN_DIR="$HOME/noted"
LOGS_DIR="$HOME/noted/logs"
QUERY_DIR="$HOME/noted/query"
SENSE_DIR="$HOME/noted/sense-o"
CONFIG_DIR="$HOME/noted/config"
PARAMS_DIR="$HOME/noted/params"
TRANSFERS_DIR="$HOME/noted/transfers"

NOTED_CONFIG_FILE_DIR="src/noted/config/config-example.yaml"
NOTED_PARAMS_FILE_DIR="src/noted/params/params.ini"
NOTED_SENSE1_FILE_DIR="src/noted/sense-o/sense-provision.sh"
NOTED_SENSE2_FILE_DIR="src/noted/sense-o/sense-cancel.sh"

function create_folders(){
    echo "Creating folders for NOTED."
    mkdir -p $MAIN_DIR
    mkdir -p $LOGS_DIR
    mkdir -p $QUERY_DIR
    mkdir -p $SENSE_DIR
    mkdir -p $CONFIG_DIR
    mkdir -p $PARAMS_DIR
    mkdir -p $TRANSFERS_DIR
}

function copy_config_files(){
    echo "Copying configuration files for NOTED."
    cp $NOTED_CONFIG_FILE_DIR $CONFIG_DIR
    cp $NOTED_PARAMS_FILE_DIR $PARAMS_DIR
    cp $NOTED_SENSE1_FILE_DIR $SENSE_DIR
    cp $NOTED_SENSE2_FILE_DIR $SENSE_DIR
}

function set_authentication_token(){
    PARAMS="$PARAMS_DIR/params.ini"
    echo "\nPlease, enter your authentication token:"
    read auth_token
    echo "" >> "$PARAMS"
    echo "[AUTH TOKEN]" >> "$PARAMS"
    echo "; Authorization token to access CERN Grafana Proxy [UNIQUE TOKEN FOR THE USER]" >> "$PARAMS"
    echo "auth_token = $auth_token" >> "$PARAMS"
    echo "" >> "$PARAMS"
    echo "[CMD]" >> "$PARAMS"
    echo "; Curl command to query in elastic search" >> "$PARAMS"
    #echo "cmd = curl -s -X POST \"\$${FTS PARAMETERS:url_fts_raw_queue}\" -H \"Authorization: Bearer \$${AUTH TOKEN:auth_token}\" -H 'Content-Type: application/json' --data-binary \"@\$${QUERY PARAMETERS:filename_src_query}\"" >> "$PARAMS"
    echo "cmd = curl -s -X POST \"\${FTS PARAMETERS:url_fts_raw_queue}\" -H \"Authorization: Bearer \${AUTH TOKEN:auth_token}\" -H 'Content-Type: application/json' --data-binary \"@\${QUERY PARAMETERS:filename_src_query}\"" >> "$PARAMS"
    echo "" >> "$PARAMS"
}

# ==============================================================================
# main
# ==============================================================================

if [[ $1 ]]; then
    ACTION="$1"
fi

if [[ $ACTION == "setup" ]]; then
    echo "Starting setup for NOTED."
    create_folders
    copy_config_files
    set_authentication_token
    echo "Finished setup for NOTED."
    noted -h
    echo "\nFinished the installation of NOTED: a framework to optimise network traffic via the analysis of data from File Transfer Services.\n"
    exit 0
fi
