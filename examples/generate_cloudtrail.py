#!/usr/bin/env python3
"""
Example: Generate AWS CloudTrail logs.

This script demonstrates generating AWS CloudTrail events including
console logins, API calls, and security-relevant actions.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from log_simulator import SchemaBasedGenerator


def main():
    """Generate AWS CloudTrail logs with various scenarios."""

    schema_path = (
        Path(__file__).parent.parent
        / "src"
        / "log_simulator"
        / "schemas"
        / "cloud_infrastructure"
        / "aws_cloudtrail.yaml"
    )

    generator = SchemaBasedGenerator(str(schema_path))

    print("=" * 70)
    print("AWS CloudTrail Log Generator")
    print("=" * 70)
    print()

    # Example 1: Console login
    print("Example 1: Successful console login")
    print("-" * 70)
    logs = generator.generate(count=1, scenario="console_login_success")
    print(json.dumps(logs[0], indent=2))
    print()

    # Example 2: EC2 instance launch
    print("\nExample 2: EC2 instance launch")
    print("-" * 70)
    logs = generator.generate(count=1, scenario="ec2_instance_launch")
    print(json.dumps(logs[0], indent=2))
    print()

    # Example 3: S3 operations
    print("\nExample 3: S3 bucket policy change (security event)")
    print("-" * 70)
    logs = generator.generate(count=1, scenario="s3_bucket_policy_change")
    print(json.dumps(logs[0], indent=2))
    print()

    # Example 4: IAM activity
    print("\nExample 4: IAM user created")
    print("-" * 70)
    logs = generator.generate(count=1, scenario="iam_user_created")
    print(json.dumps(logs[0], indent=2))
    print()

    # Example 5: Security group modification
    print("\nExample 5: Security group rule added")
    print("-" * 70)
    logs = generator.generate(count=1, scenario="security_group_modified")
    print(json.dumps(logs[0], indent=2))
    print()

    # Example 6: Generate activity log over time
    print("\nExample 6: Simulated 1-hour activity (10 events)")
    print("-" * 70)
    logs = generator.generate(count=10, time_spread_seconds=3600)
    for i, log in enumerate(logs, 1):
        print(
            f"{i}. {log['eventTime']} - {log['eventName']} by {log['userIdentity']['type']}"
        )
    print()

    print("=" * 70)
    print("Examples completed!")
    print("=" * 70)


if __name__ == "__main__":
    main()
