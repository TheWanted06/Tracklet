#!/bin/bash
echo "Initializing project metadata..."

read -p "Project folder path: " path
read -p "Project name: " name
read -p "Description: " description
read -p "Author: " author
read -p "Tags (comma-separated): " tags
read -p "Progress stage (default: WIP): " stage

stage=${stage:-WIP}

python3 -m project_tracker.cli init "$path" --name "$name" --description "$description" --author "$author" --tags "$tags" --stage "$stage"
