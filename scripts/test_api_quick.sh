#!/bin/bash
#
# Quick API Smoke Test
# Minimal smoke test for quick verification
#

BASE_URL="${1:-http://localhost:8000}"
PASSED=0
FAILED=0

GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

test_endpoint() {
    local method="$1"
    local endpoint="$2"
    local expected="$3"
    local name="$4"
    
    printf "%-60s" "$name..."
    http_code=$(curl -s -o /dev/null -w "%{http_code}" -X "$method" "${BASE_URL}${endpoint}")
    
    if [ "$http_code" = "$expected" ]; then
        echo -e " ${GREEN}✓ PASS${NC} (HTTP $http_code)"
        ((PASSED++))
    else
        echo -e " ${RED}✗ FAIL${NC} (Expected $expected, got $http_code)"
        ((FAILED++))
    fi
}

echo -e "${BLUE}Quick API Smoke Test${NC}"
echo "Base URL: $BASE_URL"
echo ""

# Core tests
test_endpoint "GET" "/health" "200" "Health check"
test_endpoint "GET" "/services" "200" "List all services"
test_endpoint "GET" "/services?limit=5" "200" "List with pagination"
test_endpoint "GET" "/services?status=running" "200" "Filter by status"
test_endpoint "GET" "/services?sort_by=name" "200" "Sort by name"
test_endpoint "GET" "/openapi.json" "200" "OpenAPI spec"

# Error handling
test_endpoint "GET" "/services?limit=invalid" "422" "Invalid limit parameter"
test_endpoint "GET" "/services/invalid_provider/test" "400" "Invalid provider"

# Summary
echo ""
echo -e "${BLUE}Summary:${NC} $((PASSED + FAILED)) tests"
echo -e "${GREEN}Passed:${NC} $PASSED"
echo -e "${RED}Failed:${NC} $FAILED"

[ $FAILED -eq 0 ] && exit 0 || exit 1
