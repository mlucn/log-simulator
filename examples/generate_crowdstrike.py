#!/usr/bin/env python3
"""
Example: Generate CrowdStrike FDR logs.

This script demonstrates generating CrowdStrike Falcon Data Replicator
events including process activity, network connections, and detections.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from log_simulator import SchemaBasedGenerator


def main():
    """Generate CrowdStrike FDR logs with various scenarios."""

    schema_path = (Path(__file__).parent.parent / 'src' / 'log_simulator' /
                  'schemas' / 'security' / 'crowdstrike_fdr.yaml')

    generator = SchemaBasedGenerator(str(schema_path))

    print("=" * 70)
    print("CrowdStrike Falcon Data Replicator (FDR) Log Generator")
    print("=" * 70)
    print()

    # Example 1: Normal process
    print("Example 1: Normal process execution")
    print("-" * 70)
    logs = generator.generate(count=1, scenario='normal_process')
    print(json.dumps(logs[0], indent=2))
    print()

    # Example 2: Network connection
    print("\nExample 2: Outbound network connection")
    print("-" * 70)
    logs = generator.generate(count=1, scenario='network_connection')
    print(json.dumps(logs[0], indent=2))
    print()

    # Example 3: Malware detection
    print("\nExample 3: Malware detection (HIGH severity)")
    print("-" * 70)
    logs = generator.generate(count=1, scenario='malware_detection')
    print(json.dumps(logs[0], indent=2))
    print()

    # Example 4: Suspicious process
    print("\nExample 4: Suspicious PowerShell execution")
    print("-" * 70)
    logs = generator.generate(count=1, scenario='suspicious_process')
    print(json.dumps(logs[0], indent=2))
    print()

    # Example 5: Lateral movement
    print("\nExample 5: Potential lateral movement (SMB)")
    print("-" * 70)
    logs = generator.generate(count=1, scenario='lateral_movement')
    print(json.dumps(logs[0], indent=2))
    print()

    # Example 6: Command and Control
    print("\nExample 6: Suspicious C2 communication")
    print("-" * 70)
    logs = generator.generate(count=1, scenario='c2_communication')
    print(json.dumps(logs[0], indent=2))
    print()

    # Example 7: Simulate attack chain
    print("\nExample 7: Attack chain simulation (10 events over 5 minutes)")
    print("-" * 70)
    scenarios = [
        'suspicious_process',
        'registry_modification',
        'network_connection',
        'lateral_movement',
        'c2_communication'
    ]

    attack_logs = []
    for scenario in scenarios * 2:  # Repeat twice to get 10 events
        logs = generator.generate(count=1, scenario=scenario)
        attack_logs.extend(logs)

    for i, log in enumerate(attack_logs, 1):
        event_name = log['event_simpleName']
        tactic = log.get('Tactic', 'N/A')
        severity = log.get('Severity', 'N/A')
        print(f"{i}. {event_name} - Tactic: {tactic}, Severity: {severity}")
    print()

    print("=" * 70)
    print("Examples completed!")
    print("=" * 70)
    print("\nNote: These are simulated logs for testing purposes.")
    print("Use with Atomic Red Team for realistic attack scenarios.")


if __name__ == '__main__':
    main()
