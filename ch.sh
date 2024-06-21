#!/bin/bash

# Specify folders to ignore (comma-separated list)
IGNORE_FOLDERS="snap,scratch"

# Function to check if a folder should be ignored
function should_ignore_folder {
    local folder_name="$1"
    local ignore_list="$IGNORE_FOLDERS"
    IFS=',' read -ra ignore_array <<< "$ignore_list"
    for ignore_folder in "${ignore_array[@]}"; do
        if [ "$folder_name" = "$ignore_folder" ]; then
            return 0
        fi
    done
    return 1
}

# Function to find XML files in a folder
function find_xml_files {
    local folder="$1"
    local indent="$2"
    local xml_files=$(find "$folder" -type f -name '*.xml' -not -path '*/\.*')

    if [ -z "$xml_files" ]; then
        echo "${indent}No XML files found."
    else
        for xml_file in $xml_files; do
            echo ""
            python3 checkxml.py "$xml_file"
        done
    fi
}

# Main script logic
for folder in */; do
    folder_name=$(basename "$folder")
    if should_ignore_folder "$folder_name"; then
        continue
    fi
    find_xml_files "$folder"
done
