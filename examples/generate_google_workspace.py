#!/usr/bin/env python3
"""
Example: Generate Google Workspace audit logs.

This script demonstrates how to use the schema-based generator
to create Google Workspace audit log entries.
"""

import json
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from log_simulator import SchemaBasedGenerator


def main():
    """Generate Google Workspace logs with different scenarios."""

    # Path to the Google Workspace schema
    schema_path = Path(__file__).parent.parent / 'src' / 'log_simulator' / 'schemas' / 'cloud_identity' / 'google_workspace.yaml'

    # Initialize the generator
    generator = SchemaBasedGenerator(str(schema_path))

    # Print schema information
    print("=" * 70)
    print("Google Workspace Log Generator")
    print("=" * 70)
    info = generator.get_schema_info()
    print(f"Log Type: {info['log_type']}")
    print(f"Description: {info['description']}")
    print(f"Schema Version: {info['schema_version']}")
    print(f"\nAvailable Scenarios:")
    for scenario in info['available_scenarios']:
        print(f"  - {scenario}")
    print("=" * 70)
    print()

    # Example 1: Generate a single default log
    print("Example 1: Single default log")
    print("-" * 70)
    logs = generator.generate(count=1)
    print(json.dumps(logs[0], indent=2))
    print()

    # Example 2: Generate drive file access logs
    print("\nExample 2: Drive file access (scenario)")
    print("-" * 70)
    logs = generator.generate(count=1, scenario='drive_file_access')
    print(json.dumps(logs[0], indent=2))
    print()

    # Example 3: Generate successful login
    print("\nExample 3: User login success (scenario)")
    print("-" * 70)
    logs = generator.generate(count=1, scenario='user_login_success')
    print(json.dumps(logs[0], indent=2))
    print()

    # Example 4: Generate failed login
    print("\nExample 4: User login failure (scenario)")
    print("-" * 70)
    logs = generator.generate(count=1, scenario='user_login_failure')
    print(json.dumps(logs[0], indent=2))
    print()

    # Example 5: Generate admin user creation
    print("\nExample 5: Admin user creation (scenario)")
    print("-" * 70)
    logs = generator.generate(count=1, scenario='admin_user_create')
    print(json.dumps(logs[0], indent=2))
    print()

    # Example 6: Generate multiple logs spread over time
    print("\nExample 6: Multiple logs over 60 seconds")
    print("-" * 70)
    logs = generator.generate(
        count=5,
        scenario='user_login_success',
        time_spread_seconds=60
    )
    for i, log in enumerate(logs, 1):
        print(f"Log {i} - Timestamp: {log['id']['time']}")
    print()

    # Example 7: Save logs to file
    print("\nExample 7: Save 10 logs to file")
    print("-" * 70)
    output_file = Path(__file__).parent / 'google_workspace_logs.json'
    logs = generator.generate(count=10, time_spread_seconds=300)

    with open(output_file, 'w') as f:
        json.dump(logs, f, indent=2)

    print(f"Generated {len(logs)} logs and saved to: {output_file}")
    print(f"File size: {output_file.stat().st_size} bytes")
    print()

    print("=" * 70)
    print("Examples completed!")
    print("=" * 70)


if __name__ == '__main__':
    main()
