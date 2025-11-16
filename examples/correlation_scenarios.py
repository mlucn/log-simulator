#!/usr/bin/env python3
"""
Example: Multi-log correlation scenarios.

This script demonstrates generating correlated logs across multiple
systems to simulate realistic user activity and attack scenarios.
"""

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from log_simulator import SchemaBasedGenerator


class CorrelatedScenarioGenerator:
    """Generate correlated logs across multiple log sources."""

    def __init__(self):
        """Initialize generators for different log sources."""
        schemas_dir = (Path(__file__).parent.parent / 'src' /
                      'log_simulator' / 'schemas')

        # Initialize generators
        self.azure_ad = SchemaBasedGenerator(
            str(schemas_dir / 'cloud_identity' / 'azure_ad_signin.yaml')
        )
        self.office365 = SchemaBasedGenerator(
            str(schemas_dir / 'cloud_identity' / 'office365_audit.yaml')
        )
        self.crowdstrike = SchemaBasedGenerator(
            str(schemas_dir / 'security' / 'crowdstrike_fdr.yaml')
        )
        self.aws = SchemaBasedGenerator(
            str(schemas_dir / 'cloud_infrastructure' / 'aws_cloudtrail.yaml')
        )

    def scenario_normal_workday(self, username="john.doe@company.com"):
        """
        Generate logs for a normal user workday.

        Timeline:
        - 08:00: User logs into Azure AD
        - 08:05: User accesses Office 365 (Outlook, Teams)
        - 09:00-17:00: Various file access and email activity
        - 17:30: User logs out
        """
        print("\n" + "=" * 70)
        print("Scenario: Normal Workday")
        print("=" * 70)

        base_time = datetime.now().replace(hour=8, minute=0, second=0)
        all_logs = []

        # 08:00 - Azure AD login
        print("\n08:00 - User logs in (Azure AD)")
        login = self.azure_ad.generate(
            count=1,
            scenario='successful_login',
            base_time=base_time
        )[0]
        all_logs.append(('azure_ad', login))
        print(f"  ✓ Azure AD sign-in: {login['userPrincipalName']}")

        # 08:05 - Office 365 activities
        print("\n08:05-09:00 - Office 365 activity")
        activities = self.office365.generate(
            count=5,
            base_time=base_time + timedelta(minutes=5),
            time_spread_seconds=3300  # 55 minutes
        )
        for activity in activities:
            all_logs.append(('office365', activity))
            print(f"  ✓ {activity['Operation']}: {activity['Workload']}")

        # Throughout day - File access
        print("\n09:00-17:00 - File and email activity")
        file_ops = self.office365.generate(
            count=20,
            scenario='file_accessed',
            base_time=base_time + timedelta(hours=1),
            time_spread_seconds=28800  # 8 hours
        )
        for op in file_ops:
            all_logs.append(('office365', op))

        print(f"  ✓ Generated {len(file_ops)} file operations")

        return all_logs

    def scenario_security_incident(self):
        """
        Generate logs for a security incident.

        Attack chain:
        1. Initial phishing email opened
        2. Malicious PowerShell execution
        3. Credential dumping attempt
        4. Lateral movement
        5. C2 communication
        """
        print("\n" + "=" * 70)
        print("Scenario: Security Incident (Attack Chain)")
        print("=" * 70)

        base_time = datetime.now()
        all_logs = []

        # Step 1: Email access (phishing)
        print("\n[T1566] Step 1: Phishing email opened")
        email = self.office365.generate(
            count=1,
            scenario='mailbox_accessed',
            base_time=base_time
        )[0]
        all_logs.append(('office365', email))
        print(f"  ✓ MailItemsAccessed: {email['UserId']}")

        # Step 2: Malicious PowerShell execution
        print("\n[T1059.001] Step 2: Suspicious PowerShell execution")
        powershell = self.crowdstrike.generate(
            count=1,
            scenario='suspicious_process',
            base_time=base_time + timedelta(minutes=2)
        )[0]
        all_logs.append(('crowdstrike', powershell))
        print(f"  ✓ {powershell['event_simpleName']}: Severity {powershell['Severity']}")

        # Step 3: Credential dumping
        print("\n[T1003.001] Step 3: Credential dumping attempt")
        cred_dump = self.crowdstrike.generate(
            count=1,
            scenario='malware_detection',
            base_time=base_time + timedelta(minutes=5)
        )[0]
        all_logs.append(('crowdstrike', cred_dump))
        print(f"  ✓ {cred_dump['DetectName']}: Severity {cred_dump['Severity']}")

        # Step 4: Lateral movement
        print("\n[T1021.002] Step 4: Lateral movement (SMB)")
        lateral = self.crowdstrike.generate(
            count=1,
            scenario='lateral_movement',
            base_time=base_time + timedelta(minutes=10)
        )[0]
        all_logs.append(('crowdstrike', lateral))
        print(f"  ✓ Network connection to port {lateral['RemotePort']}")

        # Step 5: C2 communication
        print("\n[T1071] Step 5: Command and Control communication")
        c2 = self.crowdstrike.generate(
            count=3,
            scenario='c2_communication',
            base_time=base_time + timedelta(minutes=15),
            time_spread_seconds=300
        )
        for log in c2:
            all_logs.append(('crowdstrike', log))
        print(f"  ✓ {len(c2)} C2 connections detected")

        print("\n" + "=" * 70)
        print(f"Total logs generated: {len(all_logs)}")
        print("=" * 70)

        return all_logs

    def scenario_cloud_resource_access(self):
        """
        Generate logs for cloud resource access scenario.

        Timeline:
        1. User logs into Azure AD
        2. Assumes AWS role
        3. Creates EC2 instances
        4. Accesses S3 buckets
        5. Modifies security groups
        """
        print("\n" + "=" * 70)
        print("Scenario: Cloud Resource Access")
        print("=" * 70)

        base_time = datetime.now()
        all_logs = []

        # Step 1: Azure AD login
        print("\nStep 1: Azure AD authentication")
        azure_login = self.azure_ad.generate(
            count=1,
            scenario='successful_login',
            base_time=base_time
        )[0]
        all_logs.append(('azure_ad', azure_login))
        print(f"  ✓ User signed in: {azure_login['userPrincipalName']}")

        # Step 2: AWS role assumption
        print("\nStep 2: AWS role assumption")
        assume_role = self.aws.generate(
            count=1,
            scenario='assume_role',
            base_time=base_time + timedelta(minutes=1)
        )[0]
        all_logs.append(('aws', assume_role))
        print(f"  ✓ AssumeRole: {assume_role['userIdentity']['type']}")

        # Step 3: EC2 operations
        print("\nStep 3: EC2 instance operations")
        ec2_ops = self.aws.generate(
            count=3,
            scenario='ec2_instance_launch',
            base_time=base_time + timedelta(minutes=5),
            time_spread_seconds=180
        )
        for op in ec2_ops:
            all_logs.append(('aws', op))
        print(f"  ✓ {len(ec2_ops)} EC2 operations")

        # Step 4: S3 operations
        print("\nStep 4: S3 bucket access")
        s3_ops = self.aws.generate(
            count=10,
            scenario='s3_object_upload',
            base_time=base_time + timedelta(minutes=10),
            time_spread_seconds=600
        )
        for op in s3_ops:
            all_logs.append(('aws', op))
        print(f"  ✓ {len(s3_ops)} S3 operations")

        # Step 5: Security group modification
        print("\nStep 5: Security group modification")
        sg_mod = self.aws.generate(
            count=1,
            scenario='security_group_modified',
            base_time=base_time + timedelta(minutes=20)
        )[0]
        all_logs.append(('aws', sg_mod))
        print(f"  ✓ Security group modified in {sg_mod['awsRegion']}")

        print("\n" + "=" * 70)
        print(f"Total logs generated: {len(all_logs)}")
        print("=" * 70)

        return all_logs

    def save_scenario(self, logs, output_file):
        """Save scenario logs to file."""
        output = {
            'generated_at': datetime.now().isoformat(),
            'total_logs': len(logs),
            'logs_by_source': {},
            'timeline': []
        }

        # Organize by source
        for source, log in logs:
            if source not in output['logs_by_source']:
                output['logs_by_source'][source] = []
            output['logs_by_source'][source].append(log)

            # Add to timeline
            output['timeline'].append({
                'source': source,
                'log': log
            })

        # Save to file
        with open(output_file, 'w') as f:
            json.dump(output, f, indent=2)

        print(f"\n✓ Saved to {output_file}")


def main():
    """Run correlation scenario examples."""
    print("=" * 70)
    print("Multi-Log Correlation Scenarios")
    print("=" * 70)

    generator = CorrelatedScenarioGenerator()

    # Scenario 1: Normal workday
    workday_logs = generator.scenario_normal_workday()
    generator.save_scenario(workday_logs, 'scenario_normal_workday.json')

    # Scenario 2: Security incident
    incident_logs = generator.scenario_security_incident()
    generator.save_scenario(incident_logs, 'scenario_security_incident.json')

    # Scenario 3: Cloud access
    cloud_logs = generator.scenario_cloud_resource_access()
    generator.save_scenario(cloud_logs, 'scenario_cloud_access.json')

    print("\n" + "=" * 70)
    print("All scenarios completed!")
    print("=" * 70)
    print("\nGenerated files:")
    print("  - scenario_normal_workday.json")
    print("  - scenario_security_incident.json")
    print("  - scenario_cloud_access.json")


if __name__ == '__main__':
    main()
