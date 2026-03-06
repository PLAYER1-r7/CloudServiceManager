#!/bin/bash
#
# API Smoke Test Script
# Tests core API endpoints and functionality for manual verification
#
# Usage:
#   ./scripts/test_api_smoke.sh [BASE_URL] [API_KEY]
#
# Examples:
#   ./scripts/test_api_smoke.sh                              # Test localhost:8000
#   ./scripts/test_api_smoke.sh http://localhost:8000        # Specify base URL
#   ./scripts/test_api_smoke.sh http://localhost:8000 secret # With API key
#

# Configuration
BASE_URL="${1:-http://localhost:8000}"
API_KEY="${2:-}"
FAILED_TESTS=0
PASSED_TESTS=0

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Helper functions
print_header() {
    echo -e "\n${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}"
}

print_test() {
    echo -e "\n${YELLOW}Test: $1${NC}"
}

print_success() {
    echo -e "${GREEN}✓ PASS${NC}: $1"
    ((PASSED_TESTS++))
}

print_failure() {
    echo -e "${RED}✗ FAIL${NC}: $1"
    ((FAILED_TESTS++))
}

make_request() {
    local method="$1"
    local endpoint="$2"
    local expected_status="$3"
    local description="$4"
    
    local url="${BASE_URL}${endpoint}"
    
    echo "  → ${method} ${endpoint}"
    
    # Make request and save to temp files
    local temp_body=$(mktemp)
    local http_code
    
    if [ -n "$API_KEY" ]; then
        http_code=$(curl -s -w "%{http_code}" -X "$method" "$url" \
            -H "X-API-Key: $API_KEY" \
            -o "$temp_body" 2>/dev/null)
    else
        http_code=$(curl -s -w "%{http_code}" -X "$method" "$url" \
            -o "$temp_body" 2>/dev/null)
    fi
    
    local body=$(cat "$temp_body")
    rm -f "$temp_body"
    
    if [ "$http_code" = "$expected_status" ]; then
        print_success "$description (HTTP $http_code)"
        if [ -n "$body" ] && [ "$body" != "null" ] && [ ${#body} -lt 300 ]; then
            echo "  Response: $body"
        elif [ -n "$body" ]; then
            echo "  Response: ${body:0:200}..."
        fi
        return 0
    else
        print_failure "$description (Expected HTTP $expected_status, got $http_code)"
        if [ -n "$body" ] && [ ${#body} -lt 500 ]; then
            echo "  Response: $body"
        fi
        return 1
    fi
}

validate_json_field() {
    local json="$1"
    local field="$2"
    local description="$3"
    
    local value=$(echo "$json" | grep -o "\"$field\"" || true)
    
    if [ -n "$value" ]; then
        print_success "$description"
        return 0
    else
        print_failure "$description"
        return 1
    fi
}

# Start tests
print_header "API Smoke Test Suite"
echo "Base URL: $BASE_URL"
if [ -n "$API_KEY" ]; then
    echo "API Key: ********"
else
    echo "API Key: Not configured (testing without authentication)"
fi

# Test 1: Health Check
print_header "1. Health Check"
print_test "GET /health"
make_request "GET" "/health" 200 "Health endpoint returns 200 OK"

# Test 2: Basic Service Listing
print_header "2. Service Listing"
print_test "GET /services (no parameters)"
make_request "GET" "/services" 200 "List all services without parameters"

print_test "GET /services?limit=5"
make_request "GET" "/services?limit=5" 200 "List services with limit=5"

print_test "GET /services?limit=3&offset=2"
make_request "GET" "/services?limit=3&offset=2" 200 "List services with pagination (limit=3, offset=2)"

# Test 3: Filtering
print_header "3. Filtering"
print_test "GET /services?status=running"
make_request "GET" "/services?status=running" 200 "Filter by status=running"

print_test "GET /services?status=stopped"
make_request "GET" "/services?status=stopped" 200 "Filter by status=stopped"

print_test "GET /services?service_type=compute"
make_request "GET" "/services?service_type=compute" 200 "Filter by service_type=compute"

print_test "GET /services?service_type=storage"
make_request "GET" "/services?service_type=storage" 200 "Filter by service_type=storage"

print_test "GET /services?status=running&service_type=compute"
make_request "GET" "/services?status=running&service_type=compute" 200 "Filter by status=running and service_type=compute"

# Test 4: Sorting
print_header "4. Sorting"
print_test "GET /services?sort_by=name"
make_request "GET" "/services?sort_by=name" 200 "Sort by name"

print_test "GET /services?sort_by=created_at"
make_request "GET" "/services?sort_by=created_at" 200 "Sort by created_at"

print_test "GET /services?sort_by=status"
make_request "GET" "/services?sort_by=status" 200 "Sort by status"

print_test "GET /services?sort_by=provider"
make_request "GET" "/services?sort_by=provider" 200 "Sort by provider"

# Test 5: Combined Parameters
print_header "5. Combined Parameters"
print_test "GET /services?status=running&sort_by=name&limit=10"
make_request "GET" "/services?status=running&sort_by=name&limit=10" 200 "Combine filtering, sorting, and pagination"

# Test 6: Get Single Service
print_header "6. Single Service Retrieval"
print_test "GET /services/aws/test-service-1"
if make_request "GET" "/services/aws/test-service-1" 200 "Get specific service (aws/test-service-1)"; then
    : # Success
else
    echo "  Note: Service might not exist, trying alternative..."
    make_request "GET" "/services/aws/any-service" 404 "Non-existent service returns 404" || true
fi

# Test 7: Error Handling
print_header "7. Error Handling"
print_test "GET /services?limit=invalid"
make_request "GET" "/services?limit=invalid" 422 "Invalid limit parameter returns 422"

print_test "GET /services?offset=invalid"
make_request "GET" "/services?offset=invalid" 422 "Invalid offset parameter returns 422"

print_test "GET /services?sort_by=invalid_field"
make_request "GET" "/services?sort_by=invalid_field" 422 "Invalid sort_by parameter returns 422"

print_test "GET /services?status=invalid_status"
make_request "GET" "/services?status=invalid_status" 422 "Invalid status value returns 422"

print_test "GET /services/invalid_provider/test"
make_request "GET" "/services/invalid_provider/test" 400 "Invalid provider returns 400"

# Test 8: API Documentation
print_header "8. API Documentation"
print_test "GET /docs"
response=$(curl -s -o /dev/null -w "%{http_code}" "${BASE_URL}/docs")
if [ "$response" -eq 200 ]; then
    print_success "OpenAPI documentation accessible at /docs"
else
    print_failure "OpenAPI documentation not accessible (HTTP $response)"
fi

print_test "GET /openapi.json"
make_request "GET" "/openapi.json" 200 "OpenAPI schema available at /openapi.json"

# Test 9: CORS Headers (if applicable)
print_header "9. CORS Headers"
print_test "OPTIONS /services"
response=$(curl -s -o /dev/null -w "%{http_code}" -X OPTIONS "${BASE_URL}/services")
if [ "$response" -eq 200 ]; then
    print_success "CORS preflight request handled"
else
    echo "  Note: CORS test returned HTTP $response (may be expected)"
fi

# Summary
print_header "Test Summary"
TOTAL_TESTS=$((PASSED_TESTS + FAILED_TESTS))
echo -e "Total Tests: $TOTAL_TESTS"
echo -e "${GREEN}Passed: $PASSED_TESTS${NC}"
echo -e "${RED}Failed: $FAILED_TESTS${NC}"

if [ $FAILED_TESTS -eq 0 ]; then
    echo -e "\n${GREEN}✓ All tests passed!${NC}\n"
    exit 0
else
    echo -e "\n${RED}✗ Some tests failed!${NC}\n"
    exit 1
fi
