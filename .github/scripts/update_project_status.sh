#!/bin/bash
# GitHub Projectのステータス更新スクリプト
# Usage: bash .github/scripts/update_project_status.sh <ISSUE_NUMBER> <STATUS>
# Example: bash .github/scripts/update_project_status.sh 6 "In progress"

set -e

ISSUE_NUM=$1
STATUS=$2

if [ -z "$ISSUE_NUM" ] || [ -z "$STATUS" ]; then
  echo "Usage: $0 <ISSUE_NUMBER> <STATUS>"
  echo "STATUS: Backlog | Ready | In progress | In review | Done"
  exit 1
fi

# Project and Field IDs (CloudServiceManager Project #1)
PROJECT_ID="PVT_kwHOBs4glc4BQ4Vr"
STATUS_FIELD_ID="PVTSSF_lAHOBs4glc4BQ4Vrzg-32gc"

# Status option IDs
declare -A STATUS_IDS=(
  ["Backlog"]="f75ad846"
  ["Ready"]="61e4505c"
  ["In progress"]="47fc9ee4"
  ["In review"]="df73e18b"
  ["Done"]="98236657"
)

# Get status option ID
STATUS_OPTION_ID="${STATUS_IDS[$STATUS]}"

if [ -z "$STATUS_OPTION_ID" ]; then
  echo "❌ Error: Invalid status '$STATUS'"
  echo "Valid statuses: Backlog, Ready, In progress, In review, Done"
  exit 1
fi

# Get Project Item ID for the issue
echo "🔍 Finding Issue #$ISSUE_NUM in project..."
ITEM_ID=$(gh project item-list 1 --owner PLAYER1-r7 --format json | \
  jq -r ".items[] | select(.content.number == $ISSUE_NUM) | .id")

if [ -z "$ITEM_ID" ]; then
  echo "❌ Error: Issue #$ISSUE_NUM not found in project"
  exit 1
fi

echo "📝 Item ID: $ITEM_ID"

# Update status
echo "📌 Updating status to: $STATUS"
gh project item-edit \
  --project-id "$PROJECT_ID" \
  --id "$ITEM_ID" \
  --field-id "$STATUS_FIELD_ID" \
  --single-select-option-id "$STATUS_OPTION_ID"

# Verify update
CURRENT_STATUS=$(gh project item-list 1 --owner PLAYER1-r7 --format json | \
  jq -r ".items[] | select(.content.number == $ISSUE_NUM) | .status")

echo "✅ Issue #$ISSUE_NUM → $CURRENT_STATUS"
