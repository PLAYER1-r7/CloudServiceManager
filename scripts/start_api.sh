#!/bin/bash
# Start the FastAPI development server for Cloud Service Manager Phase 2 Web API

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Get the script directory and project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo -e "${GREEN}Starting Cloud Service Manager API Server...${NC}"
echo ""
echo "API will be available at: http://localhost:8000"
echo "Interactive docs (Swagger): http://localhost:8000/docs"
echo "Alternative docs (ReDoc): http://localhost:8000/redoc"
echo ""
echo -e "${YELLOW}Press Ctrl+C to stop the server${NC}"
echo ""

# Change to project root
cd "$PROJECT_ROOT"

# Check if uvicorn is installed
if ! command -v uvicorn &> /dev/null && ! python -m uvicorn --help &> /dev/null 2>&1; then
    echo "Error: uvicorn is not installed."
    echo "Install it with: pip install uvicorn"
    exit 1
fi

# Start the server
# Use --reload for development (auto-reload on code changes)
# Use --host 0.0.0.0 to allow external connections (useful in containers)
uvicorn src.api.main:app \
    --reload \
    --host 0.0.0.0 \
    --port 8000 \
    --log-level info
