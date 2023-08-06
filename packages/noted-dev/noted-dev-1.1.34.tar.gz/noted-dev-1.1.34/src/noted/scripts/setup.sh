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
TRANSFERS_DIR="$HOME/noted/transfers"

NOTED_CONFIG_FILE_DIR="src/noted/config/config-example.yaml"
NOTED_SENSE1_FILE_DIR="src/noted/sense-o/sense-provision.sh"
NOTED_SENSE2_FILE_DIR="src/noted/sense-o/sense-cancel.sh"
NOTED_SENSE3_FILE_DIR="src/noted/sense-o/sense_util.py"

create_folders(){
    echo "Creating folders for NOTED."
    mkdir -p $MAIN_DIR
    mkdir -p $LOGS_DIR
    mkdir -p $QUERY_DIR
    mkdir -p $SENSE_DIR
    mkdir -p $CONFIG_DIR
    mkdir -p $TRANSFERS_DIR
}

copy_config_files(){
    echo "Copying configuration files for NOTED."
    cp $NOTED_CONFIG_FILE_DIR $CONFIG_DIR
    cp $NOTED_SENSE1_FILE_DIR $SENSE_DIR
    cp $NOTED_SENSE2_FILE_DIR $SENSE_DIR
    cp $NOTED_SENSE3_FILE_DIR $SENSE_DIR
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
    echo "Finished setup for NOTED."
    noted -h
    echo "\nFinished the installation of NOTED: a framework to optimise network traffic via the analysis of data from File Transfer Services.\n"
    exit 0
fi
