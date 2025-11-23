#!/usr/bin/env python3
"""
Example: Generate Google Workspace Drive Activity Logs

This example demonstrates how to generate Drive file activity logs
compatible with Google SecOps Chronicle WORKSPACE_ACTIVITY parser.

Use cases:
- Data Loss Prevention (DLP) monitoring
- External file sharing detection
- Insider threat detection
- File access anomaly detection
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
    schema_path = "src/log_simulator/schemas/cloud_identity/google_workspace/drive.yaml"
    generator = SchemaBasedGenerator(schema_path)

    print("=" * 70)
    print("Google Workspace Drive Activity Log Generator")
    print("=" * 70)
    print(f"Log Type: {generator.schema.get('log_type')}")
    print(f"Application: {generator.schema.get('application_name')}")
    print()

    # Example 1: DLP - External File Sharing Detection
    print("-" * 70)
    print("Example 1: DLP - External File Sharing Detection")
    print("-" * 70)

    external_shares = generator.generate(count=10, scenario="file_share_external")
    print(f"✓ Generated {len(external_shares)} external file sharing events")
    print(f"\nSample external share event:")
    print(json.dumps(external_shares[0], indent=2))
    print()

    # Example 2: Public File Exposure Risk
    print("-" * 70)
    print("Example 2: Public File Exposure Risk")
    print("-" * 70)

    public_shares = generator.generate(count=5, scenario="file_share_public")
    print(f"✓ Generated {len(public_shares)} public file sharing events")
    print(f"\nSample public share event:")
    print(json.dumps(public_shares[0], indent=2))
    print()

    # Example 3: Normal File Activity
    print("-" * 70)
    print("Example 3: Normal File Activity Pattern")
    print("-" * 70)

    normal_activity = []
    normal_activity.extend(generator.generate(count=50, scenario="file_view"))
    normal_activity.extend(generator.generate(count=20, scenario="file_edit"))
    normal_activity.extend(generator.generate(count=10, scenario="file_create"))
    normal_activity.extend(generator.generate(count=5, scenario="file_download"))

    print(f"✓ Generated {len(normal_activity)} normal file activity events")
    print(f"  - Views: 50")
    print(f"  - Edits: 20")
    print(f"  - Creates: 10")
    print(f"  - Downloads: 5")
    print()

    # Example 4: Suspicious Activity - Mass Downloads
    print("-" * 70)
    print("Example 4: Suspicious Activity - Mass Downloads")
    print("-" * 70)

    # Simulate mass downloads in short time window (potential data exfiltration)
    base_time = datetime.now() - timedelta(minutes=30)
    mass_downloads = generator.generate(
        count=50,
        scenario="file_download",
        base_time=base_time,
        time_spread_seconds=300,  # 5 minutes
    )

    print(f"✓ Generated {len(mass_downloads)} download events in 5-minute window")
    print(f"  (Potential data exfiltration pattern)")
    print()

    # Example 5: File Lifecycle Events
    print("-" * 70)
    print("Example 5: File Lifecycle Events")
    print("-" * 70)

    lifecycle_logs = []
    lifecycle_logs.extend(generator.generate(count=10, scenario="file_create"))
    lifecycle_logs.extend(generator.generate(count=15, scenario="file_edit"))
    lifecycle_logs.extend(generator.generate(count=5, scenario="file_share_with_user"))
    lifecycle_logs.extend(generator.generate(count=3, scenario="file_delete"))

    print(f"✓ Generated {len(lifecycle_logs)} file lifecycle events")
    print()

    # Example 6: Permission Changes
    print("-" * 70)
    print("Example 6: Permission Changes")
    print("-" * 70)

    permission_logs = []
    permission_logs.extend(generator.generate(count=8, scenario="file_share_with_user"))
    permission_logs.extend(
        generator.generate(count=3, scenario="file_remove_permission")
    )
    permission_logs.extend(
        generator.generate(count=2, scenario="file_change_permission")
    )

    print(f"✓ Generated {len(permission_logs)} permission change events")
    print(f"\nSample permission grant:")
    print(json.dumps(permission_logs[0], indent=2))
    print()

    # Save to file
    output_file = "workspace_drive_logs.json"
    all_logs = (
        external_shares
        + public_shares
        + normal_activity
        + mass_downloads
        + lifecycle_logs
        + permission_logs
    )

    with open(output_file, "w") as f:
        json.dump(all_logs, f, indent=2)

    print("=" * 70)
    print(f"✅ Generated {len(all_logs)} total Drive activity logs")
    print(f"✅ Saved to: {output_file}")
    print()
    print("Use Cases Covered:")
    print("  ✓ DLP - External sharing detection")
    print("  ✓ Public file exposure monitoring")
    print("  ✓ Mass download detection (data exfiltration)")
    print("  ✓ File lifecycle tracking")
    print("  ✓ Permission change auditing")
    print("=" * 70)


if __name__ == "__main__":
    main()
