#!/bin/bash

# Define paths and hostname
PRE="/var/log/pre_upgrade_report.txt"
POST="/var/log/post_upgrade_report.txt"
HOST=$(hostname)
CHANGED_LOG="/var/tmp/${HOST}_changed.log"
UNCHANGED_LOG="/var/tmp/${HOST}_unchanged.log"

# Clear previous logs
> "$CHANGED_LOG"
> "$UNCHANGED_LOG"

# Comparison function
compare_section() {
  local section="$1"
  local pre_tmp="/tmp/pre_${section}.txt"
  local post_tmp="/tmp/post_${section}.txt"

  awk "/^=== $section ===/{flag=1; next} /^===/{flag=0} flag" "$PRE" | sort > "$pre_tmp"
  awk "/^=== $section ===/{flag=1; next} /^===/{flag=0} flag" "$POST" | sort > "$post_tmp"

  if diff -q "$pre_tmp" "$post_tmp" > /dev/null; then
    echo -e "=== $section (No Changes) ===" >> "$UNCHANGED_LOG"
    cat "$pre_tmp" >> "$UNCHANGED_LOG"
    echo -e "\n" >> "$UNCHANGED_LOG"
  else
    echo -e "=== $section (Changed) ===" >> "$CHANGED_LOG"
    echo "--- Removed in Post ---" >> "$CHANGED_LOG"
    comm -23 "$pre_tmp" "$post_tmp" >> "$CHANGED_LOG"
    echo "--- Added in Post ---" >> "$CHANGED_LOG"
    comm -13 "$pre_tmp" "$post_tmp" >> "$CHANGED_LOG"
    echo -e "\n" >> "$CHANGED_LOG"
  fi

  rm -f "$pre_tmp" "$post_tmp"
}

# Run comparison for each section
echo "===== UPGRADE COMPARISON REPORT: $HOST =====" >> "$CHANGED_LOG"
echo "===== UPGRADE COMPARISON REPORT: $HOST =====" >> "$UNCHANGED_LOG"

for section in "Running Services" "CPU Info" "Disk Usage" "Disk Info (lsblk)"; do
  compare_section "$section"
done

echo "Report generated:"
echo "➤ Changed:   $CHANGED_LOG"
echo "➤ Unchanged: $UNCHANGED_LOG"
