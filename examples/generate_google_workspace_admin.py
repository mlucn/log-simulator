#!/usr/bin/env python3
"""
Example: Generate Google Workspace Admin Activity Logs

This example demonstrates how to generate admin console activity logs
compatible with Google SecOps Chronicle WORKSPACE_ACTIVITY parser.

Use cases:
- User provisioning/deprovisioning monitoring
- Admin privilege escalation detection
- Group membership changes
- Security policy modifications
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from log_simulator.generators.schema_generator import SchemaBasedGenerator


def main():
    # Initialize generator
    schema_path = "src/log_simulator/schemas/cloud_identity/google_workspace/admin.yaml"
    generator = SchemaBasedGenerator(schema_path)

    print("=" * 70)
    print("Google Workspace Admin Activity Log Generator")
    print("=" * 70)
    print(f"Log Type: {generator.schema.get('log_type')}")
    print(f"Application: {generator.schema.get('application_name')}")
    print(f"Chronicle Compatible: {generator.schema.get('chronicle_compatible')}")
    print()

    # List available scenarios
    print("Available Scenarios:")
    scenarios = generator.list_scenarios()
    for i, scenario in enumerate(scenarios, 1):
        print(f"  {i}. {scenario}")
    print()

    # Example 1: User Management Activities
    print("-" * 70)
    print("Example 1: User Management Activities")
    print("-" * 70)

    user_activities = [
        ("user_create", 3),
        ("user_suspend", 1),
        ("user_delete", 2),
    ]

    all_logs = []
    for scenario, count in user_activities:
        logs = generator.generate(count=count, scenario=scenario)
        all_logs.extend(logs)
        print(f"✓ Generated {count} {scenario} event(s)")

    print(f"\nSample user_create event:")
    user_create_logs = [
        log for log in all_logs if log["events"][0]["name"] == "create_user"
    ]
    if user_create_logs:
        print(json.dumps(user_create_logs[0], indent=2))
    print()

    # Example 2: Admin Privilege Changes
    print("-" * 70)
    print("Example 2: Admin Privilege Escalation Monitoring")
    print("-" * 70)

    privilege_logs = generator.generate(count=5, scenario="grant_admin_privilege")
    print(f"✓ Generated {len(privilege_logs)} admin privilege grants")
    print(f"\nSample event:")
    print(json.dumps(privilege_logs[0], indent=2))
    print()

    # Example 3: Group Management
    print("-" * 70)
    print("Example 3: Group Management Activities")
    print("-" * 70)

    group_logs = []
    group_logs.extend(generator.generate(count=2, scenario="group_create"))
    group_logs.extend(generator.generate(count=5, scenario="add_group_member"))
    group_logs.extend(generator.generate(count=2, scenario="remove_group_member"))

    print(f"✓ Generated {len(group_logs)} group management events")
    print()

    # Example 4: Security Settings Changes
    print("-" * 70)
    print("Example 4: Security Settings Changes")
    print("-" * 70)

    security_logs = []
    security_logs.extend(generator.generate(count=2, scenario="change_2sv_settings"))
    security_logs.extend(generator.generate(count=1, scenario="change_password_policy"))

    print(f"✓ Generated {len(security_logs)} security setting change events")
    print(f"\nSample 2FA settings change:")
    if security_logs:
        print(json.dumps(security_logs[0], indent=2))
    print()

    # Example 5: Time-series generation (spread over 1 hour)
    print("-" * 70)
    print("Example 5: Time-series Activity (1 hour span)")
    print("-" * 70)

    base_time = datetime.now() - timedelta(hours=1)
    time_series_logs = generator.generate(
        count=20,
        scenario="user_create",
        base_time=base_time,
        time_spread_seconds=3600,  # 1 hour
    )

    print(f"✓ Generated {len(time_series_logs)} events spread over 1 hour")
    print(f"  First event time: {time_series_logs[0]['id']['time']}")
    print(f"  Last event time: {time_series_logs[-1]['id']['time']}")
    print()

    # Save to file
    output_file = "workspace_admin_logs.json"
    all_combined_logs = (
        all_logs + privilege_logs + group_logs + security_logs + time_series_logs
    )

    with open(output_file, "w") as f:
        json.dump(all_combined_logs, f, indent=2)

    print("=" * 70)
    print(f"✅ Generated {len(all_combined_logs)} total admin activity logs")
    print(f"✅ Saved to: {output_file}")
    print("=" * 70)


if __name__ == "__main__":
    main()
