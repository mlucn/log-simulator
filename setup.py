#!/usr/bin/env python3
"""Setup script for log-simulator."""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text() if readme_file.exists() else ""

# Read requirements
requirements_file = Path(__file__).parent / "requirements.txt"
if requirements_file.exists():
    requirements = [
        line.strip()
        for line in requirements_file.read_text().splitlines()
        if line.strip() and not line.startswith('#')
    ]
else:
    requirements = ['PyYAML>=6.0.1']

setup(
    name="log-simulator",
    version="0.1.0",
    author="mlucn",
    description="Generate simulated logs and mock up endpoints",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mlucn/log-simulator",
    project_urls={
        "Bug Tracker": "https://github.com/mlucn/log-simulator/issues",
        "Documentation": "https://github.com/mlucn/log-simulator",
        "Source Code": "https://github.com/mlucn/log-simulator",
    },
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    package_data={
        "log_simulator": [
            "schemas/**/*.yaml",
            "templates/**/*",
        ],
    },
    include_package_data=True,
    python_requires=">=3.9",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.0.0",
            "ruff>=0.1.0",
            "mypy>=1.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "log-simulator=log_simulator.cli:main",
            "logsim=log_simulator.cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Information Technology",
        "Topic :: Software Development :: Testing",
        "Topic :: System :: Logging",
        "Topic :: Security",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    keywords="logging, simulation, testing, siem, security, logs, generator",
)
