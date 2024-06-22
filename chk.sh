#!/bin/bash

# run check_xml_inegrity.py on subfolders

# Specify folders to ignore (comma-separated list)
IGNORE_FOLDERS="snap,scratch"

# Function to check if a folder should be ignored
should_ignore_folder() {
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
find_xml_files() {
    local folder="$1"
    find "$folder" -type f -name '*.xml' -not -path '*/\.*' | while IFS= read -r xml_file; do
        echo ""
        python3 checkxml.py "$xml_file"
    done
}

# Main script logic
for folder in */; do
    folder_name=$(basename "$folder")
    if should_ignore_folder "$folder_name"; then
        continue
    fi
    find_xml_files "$folder"
done
