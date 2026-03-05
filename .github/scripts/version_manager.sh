#!/bin/bash
# Version Manager - Track versioning and commit history
# Usage: bash .github/scripts/version_manager.sh [check|record]

set -e

PROJECT_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$PROJECT_ROOT"

# Color codes
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Get current git info
COMMIT_COUNT=$(git rev-list --count HEAD)
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
LATEST_COMMIT=$(git log -1 --pretty=format:"%h - %s")
LATEST_TAG=$(git describe --tags --always 2>/dev/null || echo "no tags")

# Read version from config.py
BASE_VERSION=$(grep "^BASE_VERSION" config.py | grep -oP '"\K[^"]+')
CURRENT_VERSION="${BASE_VERSION}.${COMMIT_COUNT}"

echo -e "${BLUE}=== Version Manager ===${NC}\n"
echo -e "${GREEN}Current Status:${NC}"
echo "  Version:      ${BLUE}${CURRENT_VERSION}${NC}"
echo "  Base:         ${BASE_VERSION}"
echo "  Commits:      ${COMMIT_COUNT}"
echo "  Branch:       ${CURRENT_BRANCH}"
echo "  Latest:       ${LATEST_COMMIT}"
echo "  Latest Tag:   ${LATEST_TAG}"

# Check function
if [ "$1" = "check" ]; then
  PYTHON_VERSION=$(python3 -c "from config import VERSION; print(VERSION)")
  if [ "$PYTHON_VERSION" = "$CURRENT_VERSION" ]; then
    echo -e "\n${GREEN}✅ Version is consistent (${PYTHON_VERSION})${NC}"
    exit 0
  else
    echo -e "\n${YELLOW}⚠️  Version mismatch!${NC}"
    echo "  Expected: ${CURRENT_VERSION}"
    echo "  Actual:   ${PYTHON_VERSION}"
    exit 1
  fi
fi

# Record function
if [ "$1" = "record" ]; then
  RECORD_FILE="docs/VERSION_HISTORY.md"
  
  if [ ! -f "$RECORD_FILE" ]; then
    cat > "$RECORD_FILE" << 'EOF'
# Version History & Commit Records

This document tracks the version releases and associated commit counts.

## Version Timeline

| Version | Commits | Branch | Date | Notes |
|---------|---------|--------|------|-------|
EOF
  fi
  
  # Append new record
  NOW=$(date '+%Y-%m-%d %H:%M:%S')
  echo "| ${CURRENT_VERSION} | ${COMMIT_COUNT} | ${CURRENT_BRANCH} | ${NOW} | ${LATEST_COMMIT} |" >> "$RECORD_FILE"
  
  echo -e "\n${GREEN}✅ Version record saved to ${RECORD_FILE}${NC}"
  exit 0
fi

# Default: show help
if [ -z "$1" ]; then
  echo -e "\n${YELLOW}Usage:${NC}"
  echo "  bash .github/scripts/version_manager.sh check    # Check version consistency"
  echo "  bash .github/scripts/version_manager.sh record   # Record version in history"
fi
