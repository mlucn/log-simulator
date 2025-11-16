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
- 🔄 **Office 365** - Unified Audit Log (coming soon)
- 🔄 **Microsoft Graph API** - Audit logs (coming soon)

### Cloud Infrastructure
- 🔄 **Google Cloud Audit** - Cloud Logging format (coming soon)
- 🔄 **AWS CloudTrail** - Management events (coming soon)
- 🔄 **Azure Activity Logs** - Resource events (coming soon)

### Security Tools
- 🔄 **CrowdStrike Falcon EDR** - FDR events (coming soon)
- 🔄 **Sysmon** - Windows system monitoring (coming soon)

### Web Servers
- ✅ **Nginx** - Access logs (JSON and combined format)
- ✅ **Apache** - Access logs (coming soon)

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
# Install in editable mode
pip install -e .

# Install development dependencies
pip install pytest black ruff mypy
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

## Roadmap

### Phase 1: Foundation (Current)
- [x] Project structure and architecture
- [x] Schema-based generator
- [x] Google Workspace schema
- [x] Azure AD schema
- [x] Nginx schema
- [x] Field generators

### Phase 2: Expansion
- [ ] Office 365 Unified Audit Log
- [ ] AWS CloudTrail
- [ ] Google Cloud Audit Logs
- [ ] CrowdStrike FDR
- [ ] Apache access logs
- [ ] Template-based generation

### Phase 3: Advanced Features
- [ ] Atomic Red Team integration
- [ ] MITRE ATT&CK mapping
- [ ] Multi-log correlation scenarios
- [ ] API endpoint mocking
- [ ] CLI tool
- [ ] Web UI

### Phase 4: Enterprise Features
- [ ] Custom plugin system
- [ ] Log replay functionality
- [ ] Performance optimization
- [ ] Bulk generation (millions of logs)
- [ ] Stream to SIEM endpoints

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

```bash
# Run tests
pytest

# Run tests with coverage
pytest --cov=src/log_simulator --cov-report=html

# Format code
black src/ tests/

# Lint code
ruff check src/ tests/

# Type check
mypy src/
```

## License

See [LICENSE](LICENSE) file for details.

## Resources

- [CLAUDE.md](CLAUDE.md) - AI assistant development guide
- [docs/SAMPLE_LOG_RESOURCES.md](docs/SAMPLE_LOG_RESOURCES.md) - Sample log sources and resources
- [Atomic Red Team](https://github.com/redcanaryco/atomic-red-team) - Attack simulation framework
- [Elastic Common Schema](https://www.elastic.co/guide/en/ecs/current/index.html) - ECS documentation
- [MITRE ATT&CK](https://attack.mitre.org/) - ATT&CK framework

## Acknowledgments

- Inspired by the need for realistic test data in security operations
- Built to complement Atomic Red Team for comprehensive security testing
- Thanks to the open-source SIEM and security communities

---

**Status**: Early development - Active development in progress

**Version**: 0.1.0

**Author**: mlucn

**Repository**: https://github.com/mlucn/log-simulator
