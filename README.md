# Cloud Service Manager

A unified CLI application to discover and manage cloud resources across AWS, Azure, and Google Cloud Platform.

## Features

- **Multi-Cloud Support**: AWS, Azure, GCP
- **Service Discovery**: List all compute instances across providers
- **Multiple Output Formats**: JSON, Table, CSV
- **Unified Interface**: Single CLI for all cloud providers
- **Credential Management**: Support for native cloud authentication

## Quick Start

### Prerequisites

- Docker and Docker Compose
- VS Code with Remote Containers extension
- Cloud provider credentials (optional, for actual cloud integration)

### Development Setup

1. **Clone the repository**

```bash
git clone <repository-url>
cd CloudServiceManager
```

2. **Open in Dev Container**

- In VS Code, use the Remote Containers extension
- Click the green remote indicator (bottom-left)
- Select "Reopen in Container"

3. **Install dependencies** (automatic in container)

```bash
pip install -r requirements.txt
```

4. **Configure cloud credentials**
   See [SETUP.md](docs/SETUP.md) for detailed instructions.

## Usage

### List all cloud services

```bash
python -m src.cli.main list-services
```

### List services from a specific provider

```bash
python -m src.cli.main list-services --provider aws
python -m src.cli.main list-services --provider gcp --format json
```

### Filter by region

```bash
python -m src.cli.main list-services --provider aws --region us-east-1
```

### Output formats

```bash
# Table (default)
python -m src.cli.main list-services --format table

# JSON
python -m src.cli.main list-services --format json

# CSV
python -m src.cli.main list-services --format csv
```

See [API_DESIGN.md](docs/03_API_DESIGN.md) for complete CLI documentation.

## Documentation

### 📚 Documentation Structure

This project maintains **dual-language documentation**:

- **`/docs`** - English documentation (optimized for AI agents)
- **`/docs_ja`** - Japanese documentation (for human developers)

### 📖 Reading Guide

**For AI Agents and New Developers**, read documentation in this order:

1. **[docs/01_PREREQUISITES.md](docs/01_PREREQUISITES.md)** ⚠️ **READ FIRST**
   - Prerequisites, constraints, critical technical decisions
   
2. **[docs/02_PROJECT_PLAN.md](docs/02_PROJECT_PLAN.md)**
   - Project overview, architecture, roadmap
   
3. **[docs/03_API_DESIGN.md](docs/03_API_DESIGN.md)**
   - CLI command specifications, API design
   
4. **[docs/04_SETUP.md](docs/04_SETUP.md)**
   - Development environment setup procedures
   
5. **[docs/05_DEVELOPMENT_CHECKLIST.md](docs/05_DEVELOPMENT_CHECKLIST.md)**
   - Development progress tracking

See **[docs/00_README_DOCS.md](docs/00_README_DOCS.md)** for complete documentation guide.

### 📝 Documentation Policy

- **English First**: All documentation in `/docs` must be in **English** (for AI agent comprehension)
- **Japanese Mirror**: `/docs_ja` contains Japanese translations (for human developers)
- **Synchronization Required**: When updating documentation, **both versions must be updated**
- **Consistency**: Maintain consistent structure and content across both versions

## Project Structure

```
CloudServiceManager/
├── docs/                   # Documentation (English, for AI agents)
│   ├── 00_README_DOCS.md  # Documentation guide
│   ├── 01_PREREQUISITES.md # Prerequisites and constraints
│   ├── 02_PROJECT_PLAN.md  # Project overview and roadmap
│   ├── 03_API_DESIGN.md    # CLI design and API documentation
│   ├── 04_SETUP.md         # Development setup guide
│   └── 05_DEVELOPMENT_CHECKLIST.md # Development checklist
├── docs_ja/                # Documentation (Japanese, for humans)
│   └── (Same structure as docs/)
├── .devcontainer/
│   ├── Dockerfile          # Dev container image definition
│   └── devcontainer.json   # Dev container configuration
├── src/
│   └── cli/
│       ├── main.py         # CLI entry point
│       ├── models/         # Data models
│       └── providers/      # Cloud provider implementations
│           ├── aws.py
│           ├── gcp.py
│           └── azure.py
├── tests/                  # Unit tests
├── requirements.txt        # Python dependencies
├── pytest.ini             # Pytest configuration
└── README.md              # This file
```

## Development

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test file
pytest tests/test_aws_provider.py

# Verbose output
pytest -v
```

### Code Quality

```bash
# Format code
black src/

# Lint
flake8 src/

# Type check
mypy src/
```

## Architecture

### Provider Pattern

Each cloud provider implements a consistent interface:

- `list_services()`: Fetch all services from the provider
- `get_service()`: Get a specific service by ID

### Data Flow

```
CLI Command
    ↓
Provider Manager
    ↓
Cloud Provider (AWS/GCP/Azure)
    ↓
Cloud APIs
    ↓
Data Aggregation
    ↓
Output Formatter (JSON/Table/CSV)
    ↓
User
```

## Future Roadmap

### Phase 2: Web Application

- Convert CLI backend to FastAPI
- Build React frontend
- Add authentication (OAuth2)
- Persistent storage with database

### Phase 3: Advanced Features

- Real-time monitoring
- Resource cost analysis
- Automated actions (start/stop/delete)
- Multi-account management
- Custom dashboards

## Contributing

1. Create a feature branch
2. Make your changes
3. Ensure tests pass and code quality checks pass
4. Submit a pull request

### Development Guidelines

- Write tests for new features
- Maintain >80% code coverage
- Follow PEP 8 style guide
- Document public APIs
- Update relevant documentation

## Documentation

- [Project Plan](docs/PROJECT_PLAN.md) - Detailed project overview
- [Setup Guide](docs/SETUP.md) - Development environment setup
- [API Design](docs/API_DESIGN.md) - CLI design and usage

## Troubleshooting

### Container Issues

- Ensure Docker daemon is running
- Delete .devcontainer volume: `docker volume prune`
- Rebuild container: Reopen in Container

### Credential Issues

- Verify environment variables are set correctly
- Check credential file permissions
- See [SETUP.md](docs/SETUP.md) for provider-specific setup

## License

MIT License

## Contact

For questions or issues, please create a GitHub issue.
