#!/bin/bash
echo "Searching projects..."

read -p "Base folder path: " base_path
read -p "Filter by tag (leave blank to skip): " tag
read -p "Filter by stage (leave blank to skip): " stage
read -p "Filter by author (leave blank to skip): " author

cmd="python3 -m tracklet.cli search \"$base_path\""
[ -n "$tag" ] && cmd+=" --tag \"$tag\""
[ -n "$stage" ] && cmd+=" --stage \"$stage\""
[ -n "$author" ] && cmd+=" --author \"$author\""

eval $cmd
