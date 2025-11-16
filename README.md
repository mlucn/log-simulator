# log-simulator

**Generate simulated logs and mock up endpoints for testing, development, and security research.**

A Python-based tool that generates realistic, configurable log data across multiple formats and platforms. Perfect for testing SIEM systems, developing log parsers, security research, and load testing.

## Features

- 🎯 **Schema-Based Generation**: Define log structures in YAML for flexible, maintainable log generation
- 🌐 **Multi-Platform Support**: Generate logs for cloud services, web servers, and security tools
- 📊 **Realistic Data**: Built-in field generators for IPs, emails, timestamps, UUIDs, and more
- 🎬 **Pre-Built Scenarios**: Common use cases like successful logins, failed authentications, attacks
- 🔗 **Data Correlation**: Maintain relationships between fields (same user across multiple logs)
- ⚡ **Flexible Output**: JSON, traditional log formats, ECS-compatible outputs
- 🔐 **Security-Focused**: Designed with MITRE ATT&CK and Atomic Red Team integration in mind

## Supported Log Formats

### Cloud Identity & Access
- ✅ **Google Workspace** - Audit logs from Admin SDK Reports API
- ✅ **Azure AD / Microsoft Entra ID** - Sign-in and audit logs
- ✅ **Office 365** - Unified Audit Log with Exchange, SharePoint, Teams events
- ✅ **Microsoft Graph API** - Audit logs (via Azure AD schema)

### Cloud Infrastructure
- ✅ **Google Cloud Audit** - Cloud Logging format with compute, storage, IAM
- ✅ **AWS CloudTrail** - Management events including IAM, EC2, S3
- 🔄 **Azure Activity Logs** - Resource events (coming soon)

### Security Tools
- ✅ **CrowdStrike Falcon EDR** - FDR events with MITRE ATT&CK mapping
- ✅ **Sysmon** - Windows system monitoring (Events 1, 3, 7, 8, 10, 11, 12, 13, 22, 23)
- 🔄 **Windows Event Logs** - Security, System, Application (coming soon)

### Web Servers
- ✅ **Nginx** - Access logs (JSON and combined format)
- ✅ **Apache** - Access logs (Common and combined formats)

## Installation

### Prerequisites
- Python 3.9 or higher
- pip

### Install Dependencies

```bash
# Clone the repository
git clone https://github.com/mlucn/log-simulator.git
cd log-simulator

# Install required packages
pip install -r requirements.txt
```

### Development Installation

```bash
# Install in editable mode with dev dependencies
pip install -e ".[dev]"

# Install type stubs for YAML
pip install types-PyYAML

# Set up pre-commit hooks (recommended)
pre-commit install
```

## Quick Start

### Basic Usage

```python
from log_simulator import SchemaBasedGenerator

# Initialize generator with a schema
generator = SchemaBasedGenerator('src/log_simulator/schemas/cloud_identity/google_workspace.yaml')

# Generate a single log
logs = generator.generate(count=1)
print(logs[0])

# Generate logs with a specific scenario
logs = generator.generate(count=5, scenario='user_login_failure')

# Generate logs spread over time (5 logs over 60 seconds)
logs = generator.generate(count=5, time_spread_seconds=60)
```

### Command Line Examples

```bash
# Run the Google Workspace example
python examples/generate_google_workspace.py

# Generate and save logs to a file
python examples/generate_google_workspace.py > output.json
```

## Usage Examples

### Example 1: Google Workspace Login Activity

```python
from log_simulator import SchemaBasedGenerator
import json

generator = SchemaBasedGenerator(
    'src/log_simulator/schemas/cloud_identity/google_workspace.yaml'
)

# List available scenarios
print("Available scenarios:", generator.list_scenarios())

# Generate successful login
login_success = generator.generate(count=1, scenario='user_login_success')
print(json.dumps(login_success[0], indent=2))

# Generate failed login attempts
login_failures = generator.generate(count=3, scenario='user_login_failure')
```

### Example 2: Azure AD Sign-ins with Risk Detection

```python
generator = SchemaBasedGenerator(
    'src/log_simulator/schemas/cloud_identity/azure_ad_signin.yaml'
)

# Generate normal successful logins
normal_logins = generator.generate(count=10, scenario='successful_login')

# Generate risky login blocked by conditional access
risky_login = generator.generate(count=1, scenario='risky_login_blocked')

# Generate MFA-required failure
mfa_failures = generator.generate(count=2, scenario='failed_login_mfa_required')
```

### Example 3: Nginx Access Logs

```python
generator = SchemaBasedGenerator(
    'src/log_simulator/schemas/web_servers/nginx_access.yaml'
)

# Generate normal traffic
normal_traffic = generator.generate(count=100, time_spread_seconds=300)

# Generate attack patterns
sql_injection = generator.generate(count=5, scenario='malicious_scan')
ddos_pattern = generator.generate(count=50, scenario='ddos_pattern')
```

### Example 4: Time-Series Log Generation

```python
from datetime import datetime, timedelta

# Generate logs for the past hour
base_time = datetime.utcnow() - timedelta(hours=1)
logs = generator.generate(
    count=60,
    base_time=base_time,
    time_spread_seconds=3600  # Spread across 1 hour
)
```

## Project Structure

```
log-simulator/
├── src/
│   └── log_simulator/
│       ├── generators/          # Log generation engines
│       │   └── schema_generator.py
│       ├── schemas/             # YAML schema definitions
│       │   ├── cloud_identity/
│       │   │   ├── google_workspace.yaml
│       │   │   └── azure_ad_signin.yaml
│       │   ├── cloud_infrastructure/
│       │   ├── security/
│       │   └── web_servers/
│       │       └── nginx_access.yaml
│       ├── templates/           # Real log samples (templates)
│       │   └── (organized by category)
│       └── utils/               # Utility functions
│           └── field_generators.py
├── tests/                       # Test suite
│   ├── unit/
│   └── integration/
├── examples/                    # Usage examples
│   └── generate_google_workspace.py
├── docs/                        # Documentation
│   ├── SAMPLE_LOG_RESOURCES.md
│   └── CLAUDE.md
├── requirements.txt             # Dependencies
└── README.md
```

## Schema Definition

Schemas are defined in YAML format. Here's a simple example:

```yaml
schema_version: "1.0"
log_type: "example_log"
description: "Example log schema"
output_format: "json"

fields:
  timestamp:
    type: "datetime"
    format: "iso8601"
    required: true

  user_id:
    type: "uuid"
    generator: "uuid4"
    required: true

  action:
    type: "enum"
    values:
      - "login"
      - "logout"
      - "view"
    distribution:
      login: 0.4
      logout: 0.4
      view: 0.2

scenarios:
  successful_action:
    action: "login"
    status: "success"
```

See existing schemas in `src/log_simulator/schemas/` for complete examples.

## Advanced Features

### Template-Based Generation

Use real log samples as templates for even more realistic log generation:

```python
from log_simulator import TemplateBasedGenerator

# Initialize with template directory
generator = TemplateBasedGenerator('templates/security')

# Generate from template
logs = generator.generate_from_template(
    template_path='crowdstrike/T1059.001_powershell.json',
    count=100
)

# Generate attack scenario
attack_logs = generator.generate_attack_scenario(
    techniques=['T1059.001', 'T1003.001', 'T1547.001'],
    count_per_technique=10
)
```

See [Atomic Red Team Integration Guide](docs/ATOMIC_RED_TEAM_INTEGRATION.md) for creating templates from real security tool logs.

### Multi-Log Correlation

Generate correlated logs across multiple systems:

```bash
# Run correlation scenario examples
python examples/correlation_scenarios.py
```

Scenarios include:
- **Normal Workday**: User login, Office 365 activity, file access
- **Security Incident**: Complete attack chain from phishing to C2
- **Cloud Resource Access**: Azure AD → AWS role assumption → EC2/S3 operations

### Batch Generation

Generate millions of logs efficiently:

```bash
# Create configuration
python scripts/batch_generate.py --create-config batch_config.json

# Generate from config
python scripts/batch_generate.py --config batch_config.json

# Quick generation
python scripts/batch_generate.py --quick crowdstrike_fdr 1000000 --output ./logs
```

Batch generation automatically:
- Splits output into manageable chunks (default: 10,000 logs/file)
- Distributes logs across time ranges
- Handles memory efficiently for large volumes
- Supports multiple log sources in parallel

## Roadmap

### Phase 1: Foundation ✅ COMPLETED
- [x] Project structure and architecture
- [x] Schema-based generator
- [x] Google Workspace schema
- [x] Azure AD schema
- [x] Nginx schema
- [x] Field generators (30+)

### Phase 2: Expansion ✅ COMPLETED
- [x] Office 365 Unified Audit Log
- [x] AWS CloudTrail
- [x] Google Cloud Audit Logs
- [x] CrowdStrike FDR
- [x] Apache access logs
- [x] Sysmon
- [x] Template-based generation
- [x] CLI tool
- [x] Batch generation

### Phase 3: Advanced Features ✅ COMPLETED
- [x] Atomic Red Team integration (documented)
- [x] MITRE ATT&CK mapping (in schemas)
- [x] Multi-log correlation scenarios
- [x] Setup.py for pip installation
- [x] Unit tests (40+ test cases)
- [ ] API endpoint mocking (coming soon)
- [ ] Web UI (coming soon)

### Phase 4: Enterprise Features (Next)
- [ ] Custom plugin system
- [ ] Log replay functionality
- [ ] Performance optimization
- [ ] Stream to SIEM endpoints
- [ ] Kubernetes deployment
- [ ] Docker containers

## Use Cases

- **SIEM Testing**: Generate realistic logs to test detection rules and correlation logic
- **Parser Development**: Create sample data for developing and testing log parsers
- **Security Research**: Generate attack patterns for research and analysis
- **Load Testing**: Test log ingestion pipelines with high-volume data
- **Training**: Create datasets for security training and education
- **Development**: Mock log sources during application development

## Integration with Atomic Red Team

This project is designed to complement [Atomic Red Team](https://github.com/redcanaryco/atomic-red-team):

1. **Execute ART tests** in a sandboxed environment
2. **Capture real logs** generated by security tools
3. **Extract patterns** and create templates
4. **Generate similar logs** at scale using log-simulator
5. **Map to MITRE ATT&CK** techniques for comprehensive testing

See [docs/SAMPLE_LOG_RESOURCES.md](docs/SAMPLE_LOG_RESOURCES.md) for detailed resources.

## Contributing

Contributions are welcome! Areas where you can help:

- Add new log format schemas
- Contribute sample log templates
- Improve field generators
- Add test coverage
- Documentation improvements
- Bug fixes

Please see [CLAUDE.md](CLAUDE.md) for development guidelines.

## Development

### Running Tests

```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=src/log_simulator --cov-report=html

# Run specific test file
pytest tests/unit/test_schema_generator.py -v
```

### Code Quality

```bash
# Format code with black
black src/ tests/

# Lint with ruff (auto-fix issues)
ruff check src/ tests/ --fix

# Type check with mypy
mypy src/

# Run all quality checks
black src/ tests/ && ruff check src/ tests/ && mypy src/ && pytest
```

### Pre-commit Hooks

Pre-commit hooks automatically run quality checks before each commit:

```bash
# Install hooks (one-time setup)
pre-commit install

# Run manually on all files
pre-commit run --all-files

# Skip hooks if needed (not recommended)
git commit --no-verify
```

The hooks will automatically:
- Format code with Black
- Lint with Ruff (and auto-fix)
- Type-check with Mypy
- Check for trailing whitespace, large files, etc.

### Continuous Integration

The project uses GitHub Actions to run tests on every push and pull request:

- ✅ Tests run on Python 3.9, 3.10, 3.11, and 3.12
- ✅ Code coverage reported to Codecov
- ✅ Linting and type checking enforced
- ✅ All checks must pass before merging

View test results and coverage at: https://github.com/mlucn/log-simulator/actions

## License

See [LICENSE](LICENSE) file for details.

## Resources

### Documentation
- [CLAUDE.md](CLAUDE.md) - AI assistant development guide
- [docs/ATOMIC_RED_TEAM_INTEGRATION.md](docs/ATOMIC_RED_TEAM_INTEGRATION.md) - Complete guide for ART integration
- [docs/SAMPLE_LOG_RESOURCES.md](docs/SAMPLE_LOG_RESOURCES.md) - Sample log sources and resources

### Example Scripts
- [examples/generate_google_workspace.py](examples/generate_google_workspace.py) - Google Workspace examples
- [examples/generate_cloudtrail.py](examples/generate_cloudtrail.py) - AWS CloudTrail examples
- [examples/generate_crowdstrike.py](examples/generate_crowdstrike.py) - CrowdStrike FDR examples
- [examples/correlation_scenarios.py](examples/correlation_scenarios.py) - Multi-log correlation
- [scripts/batch_generate.py](scripts/batch_generate.py) - High-volume batch generation

### External Resources
- [Atomic Red Team](https://github.com/redcanaryco/atomic-red-team) - Attack simulation framework
- [Elastic Common Schema](https://www.elastic.co/guide/en/ecs/current/index.html) - ECS documentation
- [MITRE ATT&CK](https://attack.mitre.org/) - ATT&CK framework
- [Splunk Attack Data](https://github.com/splunk/attack_data) - Real attack datasets

## Acknowledgments

- Inspired by the need for realistic test data in security operations
- Built to complement Atomic Red Team for comprehensive security testing
- Thanks to the open-source SIEM and security communities

---

**Status**: Production-ready - Phases 1-3 complete!

**Version**: 0.2.0

**Features**:
- 9 log format schemas
- 35+ field generators
- Template-based generation
- CLI tool
- Batch generation (millions of logs)
- Multi-log correlation
- 40+ unit tests
- Atomic Red Team integration guide

**Author**: mlucn

**Repository**: https://github.com/mlucn/log-simulator
