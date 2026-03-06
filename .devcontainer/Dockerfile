FROM python:3.11-slim

# Set working directory
WORKDIR /workspace

# Install system dependencies
RUN apt-get update && apt-get install -y \
  git \
  curl \
  ca-certificates \
  nodejs \
  npm \
  libnspr4 \
  libnss3 \
  libatk1.0-0 \
  libatk-bridge2.0-0 \
  libcups2 \
  libxkbcommon0 \
  libatspi2.0-0 \
  libxdamage1 \
  libcairo2 \
  libpango-1.0-0 \
  libasound2 \
  gh \
  jq \
  ripgrep \
  && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Upgrade pip
RUN pip install --upgrade pip setuptools wheel

# Install development tools
RUN pip install \
  black \
  ruff \
  flake8 \
  mypy \
  pytest \
  pytest-cov

# Default command
CMD ["/bin/bash"]
