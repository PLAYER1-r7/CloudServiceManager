"""
Configuration for development environment.
"""

import os
import subprocess
from pathlib import Path


def get_commit_count():
    """Get the current commit count from git."""
    try:
        count = subprocess.run(
            ["git", "rev-list", "--count", "HEAD"],
            cwd=Path(__file__).parent,
            capture_output=True,
            text=True,
            check=True
        )
        return count.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "0"


# Application version (W.X.Y.Z format)
# Z = commit count
BASE_VERSION = "1.0.2"
COMMIT_COUNT = get_commit_count()
VERSION = f"{BASE_VERSION}.{COMMIT_COUNT}"

# Project root directory
PROJECT_ROOT = Path(__file__).parent.parent

# Source directory
SRC_DIR = PROJECT_ROOT / "src"

# Tests directory
TESTS_DIR = PROJECT_ROOT / "tests"

# Docs directory
DOCS_DIR = PROJECT_ROOT / "docs"

# Python environment
PYTHON_ENV = os.getenv("VIRTUAL_ENV", "/opt/venv")

# Development settings
DEBUG = os.getenv("DEBUG", "false").lower() == "true"

# Cloud provider configuration
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
GCP_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT", None)
AZURE_SUBSCRIPTION_ID = os.getenv("AZURE_SUBSCRIPTION_ID", None)
