"""
Configuration for development environment.
"""

import os
from pathlib import Path

# Application version (W.X.Y.Z format)
VERSION = "1.0.0.3"

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
