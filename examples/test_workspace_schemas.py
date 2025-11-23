#!/usr/bin/env python3
"""
Quick validation script for Google Workspace application-specific schemas.

This script tests that all schemas load correctly and can generate basic logs.
"""

import json
from pathlib import Path

# Add src to path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from log_simulator.generators.schema_generator import SchemaBasedGenerator


def test_schema(schema_path, app_name):
    """Test a single schema."""
    print(f"\n{'='*60}")
    print(f"Testing {app_name} schema")
    print(f"{'='*60}")

    try:
        # Load schema
        generator = SchemaBasedGenerator(str(schema_path))
        print(f"✓ Schema loaded successfully")

        # Check metadata
        info = generator.get_schema_info()
        print(f"✓ Log type: {generator.schema.get('log_type')}")
        print(f"✓ Application: {generator.schema.get('application_name')}")
        print(f"✓ Source API: {generator.schema.get('source_api')}")

        # List scenarios
        scenarios = generator.list_scenarios()
        print(f"✓ Found {len(scenarios)} scenarios")
        print(f"  First 5 scenarios: {scenarios[:5]}")

        # Generate a log
        logs = generator.generate(count=1)
        print(f"✓ Generated {len(logs)} log(s)")

        # Verify structure
        log = logs[0]
        assert log["kind"] == "admin#reports#activity"
        assert log["id"]["applicationName"] == app_name
        assert "actor" in log
        assert "events" in log
        print(f"✓ Log structure verified")

        # Generate with first scenario
        if scenarios:
            scenario_logs = generator.generate(count=1, scenario=scenarios[0])
            print(f"✓ Generated log with scenario '{scenarios[0]}'")

            # Show sample
            print(f"\nSample log (scenario: {scenarios[0]}):")
            print(json.dumps(scenario_logs[0], indent=2)[:500] + "...")

        print(f"\n✅ {app_name.upper()} PASSED")
        return True

    except Exception as e:
        print(f"\n❌ {app_name.upper()} FAILED: {e}")
        import traceback

        traceback.print_exc()
        return False


def main():
    """Run all schema tests."""
    print("=" * 60)
    print("Google Workspace Schema Validation")
    print("=" * 60)

    schema_dir = (
        Path(__file__).parent.parent
        / "src"
        / "log_simulator"
        / "schemas"
        / "cloud_identity"
        / "google_workspace"
    )

    schemas = {
        "admin": schema_dir / "admin.yaml",
        "drive": schema_dir / "drive.yaml",
        "login": schema_dir / "login.yaml",
        "calendar": schema_dir / "calendar.yaml",
        "token": schema_dir / "token.yaml",
    }

    results = {}
    for app_name, schema_path in schemas.items():
        if not schema_path.exists():
            print(
                f"\n❌ {app_name.upper()} FAILED: Schema file not found at {schema_path}"
            )
            results[app_name] = False
            continue

        results[app_name] = test_schema(schema_path, app_name)

    # Summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    passed = sum(1 for v in results.values() if v)
    total = len(results)

    for app_name, passed_test in results.items():
        status = "✅ PASSED" if passed_test else "❌ FAILED"
        print(f"{app_name.upper()}: {status}")

    print(f"\n{passed}/{total} schemas passed")

    if passed == total:
        print("\n🎉 All schemas validated successfully!")
        return 0
    else:
        print(f"\n⚠️  {total - passed} schema(s) failed validation")
        return 1


if __name__ == "__main__":
    exit(main())
