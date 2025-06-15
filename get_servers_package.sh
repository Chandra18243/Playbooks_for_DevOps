#!/bin/bash

# Check argument
if [ $# -ne 1 ]; then
    echo "Usage: $0 <package_name>"
    exit 1
fi

PACKAGE_NAME="$1"
REPORT_DIR="/var/opt/ansible/reports"
OUTPUT_DIR="/tmp/servers"
INSTALLED_FILE="${OUTPUT_DIR}/${PACKAGE_NAME}_installed"
NOT_INSTALLED_FILE="${OUTPUT_DIR}/${PACKAGE_NAME}_not_installed"

# Prepare output directory and clean files
mkdir -p "$OUTPUT_DIR"
> "$INSTALLED_FILE"
> "$NOT_INSTALLED_FILE"

COUNT=0
TOTAL=0

# Loop through all server JSON files
for file in "$REPORT_DIR"/*.json; do
    SERVER_NAME=$(basename "$file" .json)
    ((TOTAL++))

    if jq -e --arg pkg "$PACKAGE_NAME" '.[] | select(.name == $pkg)' "$file" > /dev/null 2>&1; then
        echo "$SERVER_NAME" >> "$INSTALLED_FILE"
        ((COUNT++))
    else
        echo "$SERVER_NAME" >> "$NOT_INSTALLED_FILE"
    fi
done

# Summary
echo "Package: $PACKAGE_NAME"
echo "Total servers checked: $TOTAL"
echo "Servers with package installed: $COUNT"
echo "List saved to: $INSTALLED_FILE"
echo "Servers without package: $((TOTAL - COUNT))"
echo "List saved to: $NOT_INSTALLED_FILE"
