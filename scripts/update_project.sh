#!/bin/bash
echo "Updating project metadata..."

read -p "Project folder path: " path
read -p "New project name (leave blank to skip): " name
read -p "New description (leave blank to skip): " description
read -p "New author (leave blank to skip): " author
read -p "New tags (comma-separated, leave blank to skip): " tags
read -p "New progress stage (leave blank to skip): " stage

cmd="python3 -m project_tracker.cli update \"$path\""
[ -n "$name" ] && cmd+=" --name \"$name\""
[ -n "$description" ] && cmd+=" --description \"$description\""
[ -n "$author" ] && cmd+=" --author \"$author\""
[ -n "$tags" ] && cmd+=" --tags \"$tags\""
[ -n "$stage" ] && cmd+=" --stage \"$stage\""

eval $cmd
