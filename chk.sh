#!/bin/bash

# Shell script to run the Python script recursively on all XML files in ~/dumps

# Define the directory to search in
SEARCH_DIR="$HOME/dumps"

# Define the Python script
PYTHON_SCRIPT="check_xml_integrity.py"

# Function to run the Python script on an XML file
run_script() {
    local file=$1
    python3 "$PYTHON_SCRIPT" "$file"
}

# Export the function so it can be used with find
export -f run_script
export PYTHON_SCRIPT

# Find all XML files in the SEARCH_DIR and run the Python script on each
find "$SEARCH_DIR" -type f -name "*.xml" -exec bash -c 'run_script "$0"' {} \;
