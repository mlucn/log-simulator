#!/usr/bin/env python3
"""
Command-line interface for log-simulator.

Provides an easy-to-use CLI for generating logs from schemas.
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Optional

from .generators.schema_generator import SchemaBasedGenerator


def list_schemas() -> dict[str, list[str]]:
    """List all available schemas organized by category."""
    schemas_dir = Path(__file__).parent / "schemas"
    schemas: dict[str, list[str]] = {}

    if not schemas_dir.exists():
        return schemas

    # Walk through the schemas directory recursively
    for schema_file in schemas_dir.rglob("*.yaml"):
        # Get relative path from schemas_dir
        rel_path = schema_file.relative_to(schemas_dir)

        # Get category (top-level directory name)
        if len(rel_path.parts) > 1:
            category = rel_path.parts[0]
        else:
            category = "other"

        # Get schema name (relative path without .yaml extension)
        schema_name = str(rel_path.with_suffix(""))

        # Add to category
        if category not in schemas:
            schemas[category] = []
        schemas[category].append(schema_name)

    return schemas


def print_schemas():
    """Print all available schemas."""
    schemas = list_schemas()

    print("\nAvailable Schemas:")
    print("=" * 70)

    for category, schema_list in sorted(schemas.items()):
        print(f"\n{category.replace('_', ' ').title()}:")
        for schema in sorted(schema_list):
            print(f"  - {schema}")

    print("\n" + "=" * 70)


def find_schema_path(schema_name: str) -> Optional[Path]:
    """
    Find the full path to a schema file by name.

    Supports multiple formats:
    - Relative path: "google_workspace/admin" -> cloud_identity/google_workspace/admin.yaml
    - Full path: "cloud_identity/google_workspace/admin" -> cloud_identity/google_workspace/admin.yaml
    - Simple name: "nginx_access" -> web_servers/nginx_access.yaml
    """
    schemas_dir = Path(__file__).parent / "schemas"

    if not schemas_dir.exists():
        return None

    # Remove .yaml extension if present
    if schema_name.endswith(".yaml"):
        schema_name = schema_name[:-5]

    # Try direct path first (e.g., "cloud_identity/google_workspace/admin")
    schema_path = schemas_dir / f"{schema_name}.yaml"
    if schema_path.exists():
        return schema_path

    # Search recursively for matching schema
    # This allows "google_workspace/admin" to find "cloud_identity/google_workspace/admin.yaml"
    for schema_file in schemas_dir.rglob("*.yaml"):
        rel_path = schema_file.relative_to(schemas_dir)
        schema_full_name = str(rel_path.with_suffix(""))

        # Check if the schema_name matches the end of the full path
        # This allows both "admin" and "google_workspace/admin" to match
        if schema_full_name == schema_name or schema_full_name.endswith(f"/{schema_name}"):
            return schema_file

    return None


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Generate simulated logs from schema definitions",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # List all available schemas
  %(prog)s --list

  # Generate Google Workspace admin logs
  %(prog)s google_workspace/admin -n 10

  # Generate Drive logs with external sharing scenario
  %(prog)s google_workspace/drive -n 5 --scenario file_share_external

  # Generate login logs with time spread
  %(prog)s google_workspace/login -n 100 --spread 3600 -o login_logs.json

  # List scenarios for a specific schema
  %(prog)s google_workspace/admin --list-scenarios

  # Generate Azure AD logs with specific scenario
  %(prog)s azure_ad_signin -n 5 --scenario failed_login_mfa_required

  # Pretty-print output
  %(prog)s office365_audit -n 3 --pretty
        """,
    )

    parser.add_argument(
        "schema",
        nargs="?",
        help="Schema name (e.g., google_workspace, azure_ad_signin)",
    )

    parser.add_argument(
        "-l", "--list", action="store_true", help="List all available schemas"
    )

    parser.add_argument(
        "-n",
        "--count",
        type=int,
        default=1,
        help="Number of log entries to generate (default: 1)",
    )

    parser.add_argument("-s", "--scenario", help="Scenario name from schema (optional)")

    parser.add_argument(
        "--spread",
        type=int,
        default=0,
        metavar="SECONDS",
        help="Spread logs over N seconds (default: 0)",
    )

    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        metavar="FILE",
        help="Output file (default: stdout)",
    )

    parser.add_argument(
        "-p", "--pretty", action="store_true", help="Pretty-print JSON output"
    )

    parser.add_argument(
        "--list-scenarios",
        action="store_true",
        help="List scenarios available in the schema",
    )

    parser.add_argument("--info", action="store_true", help="Show schema information")

    args = parser.parse_args()

    # Handle --list flag
    if args.list:
        print_schemas()
        return 0

    # Require schema if not listing
    if not args.schema:
        parser.error("schema is required (use --list to see available schemas)")

    # Find schema file
    schema_path = find_schema_path(args.schema)
    if not schema_path:
        print(f"Error: Schema '{args.schema}' not found", file=sys.stderr)
        print("\nUse --list to see available schemas", file=sys.stderr)
        return 1

    # Initialize generator
    try:
        generator = SchemaBasedGenerator(str(schema_path))
    except Exception as e:
        print(f"Error loading schema: {e}", file=sys.stderr)
        return 1

    # Handle --info flag
    if args.info:
        info = generator.get_schema_info()
        print("\nSchema Information:")
        print("=" * 70)
        print(f"Log Type: {info['log_type']}")
        print(f"Description: {info['description']}")
        print(f"Schema Version: {info['schema_version']}")
        print(f"Output Format: {info['output_format']}")
        print(f"Scenarios: {len(info['available_scenarios'])}")
        print("=" * 70)
        return 0

    # Handle --list-scenarios flag
    if args.list_scenarios:
        scenarios = generator.list_scenarios()
        print(f"\nAvailable scenarios for '{args.schema}':")
        print("=" * 70)
        for scenario in scenarios:
            print(f"  - {scenario}")
        print("=" * 70)
        return 0

    # Validate scenario if provided
    if args.scenario:
        scenarios = generator.list_scenarios()
        if args.scenario not in scenarios:
            print(f"Error: Scenario '{args.scenario}' not found", file=sys.stderr)
            print(f"\nAvailable scenarios: {', '.join(scenarios)}", file=sys.stderr)
            return 1

    # Generate logs
    try:
        logs = generator.generate(
            count=args.count, scenario=args.scenario, time_spread_seconds=args.spread
        )
    except Exception as e:
        print(f"Error generating logs: {e}", file=sys.stderr)
        return 1

    # Format output
    if args.pretty:
        output = json.dumps(logs, indent=2)
    else:
        output = json.dumps(logs)

    # Write output
    if args.output:
        try:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(output)
            print(f"Generated {len(logs)} log(s) -> {args.output}", file=sys.stderr)
        except Exception as e:
            print(f"Error writing to file: {e}", file=sys.stderr)
            return 1
    else:
        print(output)

    return 0


if __name__ == "__main__":
    sys.exit(main())
