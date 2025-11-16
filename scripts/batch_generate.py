#!/usr/bin/env python3
"""
Batch log generation script.

Generates large volumes of logs for testing SIEM systems,
log pipelines, and storage solutions.
"""

import argparse
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from log_simulator import SchemaBasedGenerator


class BatchGenerator:
    """Batch log generator for high-volume production."""

    def __init__(self, schemas_dir: Path):
        """Initialize batch generator."""
        self.schemas_dir = schemas_dir
        self.generators = {}

    def load_generator(self, log_type: str, schema_path: str):
        """Load a schema generator."""
        if log_type not in self.generators:
            full_path = self.schemas_dir / schema_path
            self.generators[log_type] = SchemaBasedGenerator(str(full_path))
        return self.generators[log_type]

    def generate_batch(
        self, config: Dict[str, Any], output_dir: Path, chunk_size: int = 10000
    ):
        """
        Generate logs in batches to avoid memory issues.

        Args:
            config: Generation configuration
            output_dir: Output directory
            chunk_size: Number of logs per file chunk
        """
        log_type = config["type"]
        total_count = config["count"]
        schema_path = config["schema"]
        scenario = config.get("scenario")
        time_spread = config.get("time_spread_hours", 24)

        print(f"\nGenerating {total_count:,} {log_type} logs...")

        # Load generator
        generator = self.load_generator(log_type, schema_path)

        # Create output directory
        output_dir.mkdir(parents=True, exist_ok=True)

        # Calculate chunks
        num_chunks = (total_count + chunk_size - 1) // chunk_size
        base_time = datetime.now() - timedelta(hours=time_spread)

        total_generated = 0
        for chunk_num in range(num_chunks):
            chunk_start = chunk_num * chunk_size
            chunk_end = min(chunk_start + chunk_size, total_count)
            chunk_count = chunk_end - chunk_start

            # Calculate time offset for this chunk
            time_offset = int((chunk_start / total_count) * (time_spread * 3600))
            chunk_base_time = base_time + timedelta(seconds=time_offset)

            # Generate chunk
            logs = generator.generate(
                count=chunk_count,
                scenario=scenario,
                base_time=chunk_base_time,
                time_spread_seconds=int(
                    (chunk_count / total_count) * (time_spread * 3600)
                ),
            )

            # Save chunk
            output_file = output_dir / f"{log_type}_chunk_{chunk_num:04d}.json"
            with open(output_file, "w") as f:
                json.dump(logs, f)

            total_generated += len(logs)
            progress = (total_generated / total_count) * 100
            print(
                f"  Progress: {total_generated:,}/{total_count:,} ({progress:.1f}%) - {output_file.name}"
            )

        print(f"✓ Completed: {total_generated:,} logs generated")

        return total_generated


def load_config(config_file: Path) -> Dict[str, Any]:
    """Load generation configuration from JSON file."""
    with open(config_file) as f:
        return json.load(f)


def create_sample_config(output_file: Path):
    """Create a sample configuration file."""
    config = {
        "batch_name": "siem_test_data",
        "description": "Sample batch generation configuration",
        "output_directory": "./generated_logs",
        "chunk_size": 10000,
        "log_sources": [
            {
                "type": "azure_ad_signin",
                "schema": "cloud_identity/azure_ad_signin.yaml",
                "count": 50000,
                "scenario": "successful_login",
                "time_spread_hours": 24,
            },
            {
                "type": "office365_audit",
                "schema": "cloud_identity/office365_audit.yaml",
                "count": 100000,
                "time_spread_hours": 24,
            },
            {
                "type": "nginx_access",
                "schema": "web_servers/nginx_access.yaml",
                "count": 1000000,
                "time_spread_hours": 24,
            },
            {
                "type": "aws_cloudtrail",
                "schema": "cloud_infrastructure/aws_cloudtrail.yaml",
                "count": 75000,
                "time_spread_hours": 24,
            },
            {
                "type": "crowdstrike_fdr",
                "schema": "security/crowdstrike_fdr.yaml",
                "count": 200000,
                "time_spread_hours": 24,
            },
        ],
    }

    with open(output_file, "w") as f:
        json.dump(config, f, indent=2)

    print(f"Sample configuration created: {output_file}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Batch log generation for high-volume testing",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Create sample configuration
  %(prog)s --create-config batch_config.json

  # Generate logs from configuration
  %(prog)s --config batch_config.json

  # Quick generation without config file
  %(prog)s --quick google_workspace 100000 --output ./logs

  # Generate with specific scenario
  %(prog)s --quick crowdstrike_fdr 50000 --scenario malware_detection
        """,
    )

    parser.add_argument(
        "--config", type=Path, metavar="FILE", help="Configuration file (JSON)"
    )

    parser.add_argument(
        "--create-config",
        type=Path,
        metavar="FILE",
        help="Create sample configuration file",
    )

    parser.add_argument(
        "--quick",
        nargs=2,
        metavar=("SCHEMA", "COUNT"),
        help="Quick generation: schema name and count",
    )

    parser.add_argument("--scenario", help="Scenario name (for --quick mode)")

    parser.add_argument(
        "--output",
        type=Path,
        default=Path("./generated_logs"),
        help="Output directory (default: ./generated_logs)",
    )

    parser.add_argument(
        "--chunk-size",
        type=int,
        default=10000,
        help="Logs per chunk file (default: 10000)",
    )

    args = parser.parse_args()

    # Handle --create-config
    if args.create_config:
        create_sample_config(args.create_config)
        return 0

    # Get schemas directory
    schemas_dir = Path(__file__).parent.parent / "src" / "log_simulator" / "schemas"

    # Initialize batch generator
    batch_gen = BatchGenerator(schemas_dir)

    # Handle --quick mode
    if args.quick:
        schema_name, count_str = args.quick
        count = int(count_str)

        # Find schema file
        schema_found = None
        for category_dir in schemas_dir.iterdir():
            if category_dir.is_dir():
                schema_file = category_dir / f"{schema_name}.yaml"
                if schema_file.exists():
                    schema_found = schema_file.relative_to(schemas_dir)
                    break

        if not schema_found:
            print(f"Error: Schema '{schema_name}' not found", file=sys.stderr)
            return 1

        config = {
            "type": schema_name,
            "schema": str(schema_found),
            "count": count,
            "scenario": args.scenario,
            "time_spread_hours": 24,
        }

        batch_gen.generate_batch(config, args.output, args.chunk_size)
        return 0

    # Handle --config mode
    if args.config:
        if not args.config.exists():
            print(
                f"Error: Configuration file not found: {args.config}", file=sys.stderr
            )
            return 1

        config = load_config(args.config)
        output_dir = Path(config.get("output_directory", "./generated_logs"))
        chunk_size = config.get("chunk_size", 10000)

        print("=" * 70)
        print(f"Batch Generation: {config['batch_name']}")
        print("=" * 70)
        print(f"Description: {config.get('description', 'N/A')}")
        print(f"Output: {output_dir}")
        print(f"Chunk size: {chunk_size:,}")
        print(f"Log sources: {len(config['log_sources'])}")
        print("=" * 70)

        total_logs = 0
        for source_config in config["log_sources"]:
            total_logs += batch_gen.generate_batch(
                source_config, output_dir / source_config["type"], chunk_size
            )

        print("\n" + "=" * 70)
        print("Batch generation completed!")
        print(f"Total logs generated: {total_logs:,}")
        print(f"Output directory: {output_dir}")
        print("=" * 70)

        return 0

    # No valid mode specified
    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
