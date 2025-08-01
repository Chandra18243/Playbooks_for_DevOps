#!/bin/bash

PRE="/var/log/pre_upgrade_report.txt"
POST="/var/log/post_upgrade_report.txt"

echo "===== UPGRADE COMPARISON REPORT ====="

compare_section() {
  local section="$1"
  echo -e "\n=== Comparing $section ==="

  awk "/^=== $section ===/{flag=1; next} /^===/{flag=0} flag" "$PRE" | sort > /tmp/pre_$section.txt
  awk "/^=== $section ===/{flag=1; next} /^===/{flag=0} flag" "$POST" | sort > /tmp/post_$section.txt

  echo "--- Removed in Post ---"
  comm -23 /tmp/pre_$section.txt /tmp/post_$section.txt

  echo "--- Added in Post ---"
  comm -13 /tmp/pre_$section.txt /tmp/post_$section.txt
}

compare_section "Running Services"
compare_section "CPU Info"
compare_section "Disk Usage"
compare_section "Disk Info (lsblk)"

echo -e "\n===== END OF REPORT ====="
