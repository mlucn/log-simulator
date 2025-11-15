# CLAUDE.md - AI Assistant Guide for log-simulator

## Project Overview

**log-simulator** is a Python-based tool designed to generate simulated logs and mock up endpoints. This project is in its early development stage.

### Repository Information
- **Primary Language**: Python
- **Project Type**: Log simulation and endpoint mocking tool
- **Current Status**: Initial development stage
- **Git Branch Strategy**: Feature branches prefixed with `claude/`

## Current Codebase Structure

```
log-simulator/
├── .git/                 # Git repository data
├── .gitignore           # Python-focused gitignore
├── LICENSE              # Project license
└── README.md            # Basic project description
```

### Project State
This is a greenfield project with minimal initial setup. The codebase currently contains only foundational files and is ready for active development.

## Recommended Project Structure

As development progresses, the following structure is recommended:

```
log-simulator/
├── src/                 # Source code
│   └── log_simulator/   # Main package
│       ├── __init__.py
│       ├── generators/  # Log generation modules
│       ├── endpoints/   # Endpoint mocking modules
│       └── utils/       # Utility functions
├── tests/               # Test suite
│   ├── unit/
│   └── integration/
├── docs/                # Documentation
├── examples/            # Usage examples
├── scripts/             # Development/deployment scripts
├── .gitignore
├── README.md
├── LICENSE
├── pyproject.toml       # Python project configuration
├── requirements.txt     # Dependencies (or use pyproject.toml)
└── setup.py            # Package installation (or use pyproject.toml)
```

## Development Conventions

### Python Standards

1. **Python Version**: Specify minimum Python version (recommend 3.9+)
2. **Code Style**:
   - Follow PEP 8 style guide
   - Use type hints for function signatures
   - Maximum line length: 88 characters (Black formatter default)
3. **Formatting**: Use Black for code formatting
4. **Linting**: Use Ruff or Flake8 for linting
5. **Type Checking**: Use mypy for static type checking

### Package Management

Options for dependency management (choose one):
- **pyproject.toml** (recommended modern approach)
- **requirements.txt** (traditional approach)
- **Poetry** (comprehensive dependency management)
- **UV** (fast Python package installer)

### Code Organization

1. **Modules**: Organize code into logical modules (generators, endpoints, utils)
2. **Naming Conventions**:
   - Files/modules: `snake_case.py`
   - Classes: `PascalCase`
   - Functions/variables: `snake_case`
   - Constants: `UPPER_SNAKE_CASE`
3. **Docstrings**: Use Google-style or NumPy-style docstrings

### Testing Strategy

1. **Framework**: pytest (recommended)
2. **Coverage**: Aim for >80% code coverage
3. **Test Structure**:
   - Unit tests for individual functions/classes
   - Integration tests for endpoint mocking
   - Example tests for log generation patterns
4. **Test Files**: Mirror source structure in `tests/` directory

## AI Assistant Guidelines

### When Adding Features

1. **Plan First**: Use TodoWrite to break down complex features into steps
2. **Structure Check**:
   - Create appropriate module structure if it doesn't exist
   - Follow the recommended project structure above
3. **Dependencies**:
   - Add new dependencies to `requirements.txt` or `pyproject.toml`
   - Document why each dependency is needed
4. **Testing**:
   - Write tests alongside implementation
   - Ensure all tests pass before committing

### Code Quality Practices

1. **Type Safety**:
   - Add type hints to all function signatures
   - Use `from typing import` for complex types
2. **Error Handling**:
   - Use specific exception types
   - Provide informative error messages
   - Document exceptions in docstrings
3. **Documentation**:
   - Add docstrings to all public functions and classes
   - Update README.md when adding major features
   - Include usage examples for new functionality
4. **Security**:
   - Avoid command injection vulnerabilities
   - Validate all user inputs
   - Don't hardcode sensitive data (use environment variables)
   - Be cautious with file operations and path traversal

### Git Workflow

1. **Branches**:
   - Develop on feature branches (prefix: `claude/`)
   - Current branch: `claude/claude-md-mi0vl9kfb3ey0k39-019vUpEWQ1AJnKAemvGXgj42`
2. **Commits**:
   - Write clear, descriptive commit messages
   - Use conventional commit format when possible:
     - `feat:` for new features
     - `fix:` for bug fixes
     - `docs:` for documentation
     - `test:` for tests
     - `refactor:` for refactoring
3. **Pushing**:
   - Always use `git push -u origin <branch-name>`
   - Retry on network errors with exponential backoff

### Log Simulator Specific Conventions

Since this is a log simulation tool, keep these domain-specific guidelines in mind:

1. **Log Formats**:
   - Support common log formats (JSON, syslog, Apache, etc.)
   - Make formats configurable and extensible
2. **Endpoint Mocking**:
   - Use standard HTTP libraries (requests, httpx, or built-in http.server)
   - Support various HTTP methods and response codes
   - Allow customizable response payloads
3. **Configuration**:
   - Use YAML or JSON for configuration files
   - Support CLI arguments for quick testing
   - Provide sensible defaults
4. **Performance**:
   - Consider async/await for concurrent operations
   - Allow rate limiting for log generation
   - Implement efficient file I/O for large log volumes

### Pre-Implementation Checklist

Before implementing new features:

- [ ] Understand the requirement clearly
- [ ] Check if similar functionality exists
- [ ] Plan the module/file structure
- [ ] Identify required dependencies
- [ ] Consider error cases and edge conditions
- [ ] Plan the test strategy
- [ ] Use TodoWrite for complex multi-step tasks

### Post-Implementation Checklist

After implementing features:

- [ ] All code has type hints
- [ ] All public functions have docstrings
- [ ] Tests are written and passing
- [ ] No security vulnerabilities introduced
- [ ] Dependencies are documented
- [ ] README updated if needed
- [ ] Code follows PEP 8 / Black formatting
- [ ] Changes are committed with clear messages

## Common Commands

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

# Install in development mode
pip install -e .

# Install dependencies
pip install -r requirements.txt
```

## Environment Setup

When setting up the development environment:

1. Create virtual environment: `python -m venv .venv`
2. Activate: `source .venv/bin/activate` (Linux/Mac) or `.venv\Scripts\activate` (Windows)
3. Install dependencies: `pip install -r requirements.txt`
4. Install dev dependencies: `pip install pytest black ruff mypy`

## Key Files to Watch

As development progresses, pay attention to:

- **pyproject.toml** or **setup.py**: Package configuration
- **requirements.txt**: Dependencies
- **.env.example**: Example environment variables (if created)
- **CONTRIBUTING.md**: Contribution guidelines (if created)
- **docs/**: Documentation files

## Questions to Clarify Before Major Changes

When implementing significant features, consider clarifying:

1. **Target Use Cases**: Who will use this tool and how?
2. **Log Volume**: What scale of log generation is expected?
3. **Endpoint Types**: What kinds of endpoints need mocking (REST, GraphQL, gRPC)?
4. **Output Formats**: Where should logs be written (file, stdout, network)?
5. **Configuration**: How should users configure the tool (CLI, config file, programmatic)?

## Notes for AI Assistants

- This is a new project with minimal existing code - you have flexibility in architecture decisions
- Prioritize clean, maintainable code over complex optimizations initially
- Document architectural decisions in code comments or separate docs
- Consider creating a CLI interface early for easy testing
- Think about both library usage and standalone tool usage patterns
- Always ask for clarification on ambiguous requirements before implementation

---

**Last Updated**: 2025-11-15
**Repository**: mlucn/log-simulator
**Branch**: claude/claude-md-mi0vl9kfb3ey0k39-019vUpEWQ1AJnKAemvGXgj42
