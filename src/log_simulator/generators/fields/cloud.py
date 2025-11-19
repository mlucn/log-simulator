"""
Cloud-related field generators.
"""

import random
import string

from .base import BaseFieldGenerator


class CloudGenerator(BaseFieldGenerator):
    """Generators for cloud-related fields (AWS, GCP, etc)."""

    @staticmethod
    def aws_user_agent() -> str:
        """Generate a random AWS user agent."""
        agents = [
            "aws-cli/2.13.25 Python/3.11.5 Linux/5.15.0 exe/x86_64.ubuntu.22",
            "aws-sdk-go/1.44.327 (go1.20.7; linux; amd64)",
            "Boto3/1.28.55 Python/3.11.5 Linux/5.15.0",
            "aws-sdk-java/2.20.140 Linux/5.15.0",
            "[S3Console/0.4]",
            "console.amazonaws.com",
            "AWS Internal",
        ]
        return random.choice(agents)

    @staticmethod
    def aws_principal_id() -> str:
        """Generate a random AWS principal ID."""
        prefix = random.choice(["AIDAI", "AROA", "AGPA"])
        suffix = "".join(random.choices(string.ascii_uppercase + string.digits, k=17))
        return f"{prefix}{suffix}"

    @staticmethod
    def aws_account_id() -> str:
        """Generate a random AWS account ID (12 digits)."""
        return "".join(random.choices(string.digits, k=12))

    @staticmethod
    def aws_arn() -> str:
        """Generate a random AWS ARN."""
        account_id = CloudGenerator.aws_account_id()
        resource_types = [
            ("iam", "user", "username"),
            ("iam", "role", "rolename"),
            ("s3", "", "bucket-name"),
            ("ec2", "instance", "i-"),
            ("lambda", "function", "function-name"),
        ]
        service, res_type, prefix = random.choice(resource_types)

        if res_type:
            if prefix.startswith("i-"):
                resource = (
                    f"{prefix}{''.join(random.choices(string.hexdigits.lower(), k=17))}"
                )
                return f"arn:aws:{service}:us-east-1:{account_id}:{res_type}/{resource}"
            else:
                resource = f"{prefix}{random.randint(1, 9999)}"
                return f"arn:aws:{service}::{account_id}:{res_type}/{resource}"
        else:
            return f"arn:aws:{service}:::{prefix}{random.randint(1000, 9999)}"

    @staticmethod
    def aws_resource_arn() -> str:
        """Generate a random AWS resource ARN."""
        return CloudGenerator.aws_arn()

    @staticmethod
    def gcp_project_id() -> str:
        """Generate a random GCP project ID."""
        adjective = random.choice(["bright", "cool", "fast", "smart", "quick"])
        noun = random.choice(["cloud", "data", "app", "service", "platform"])
        number = random.randint(100, 999)
        return f"{adjective}-{noun}-{number}"

    @staticmethod
    def gcp_resource_name() -> str:
        """Generate a random GCP resource name."""
        project_id = CloudGenerator.gcp_project_id()
        resource_types = [
            ("instances", "instance-"),
            ("buckets", "bucket-"),
            ("serviceAccounts", "sa-"),
        ]
        res_type, prefix = random.choice(resource_types)
        resource_id = f"{prefix}{random.randint(1000, 9999)}"

        if res_type == "instances":
            zone = random.choice(["us-central1-a", "us-east1-b", "europe-west1-c"])
            return f"projects/{project_id}/zones/{zone}/{res_type}/{resource_id}"
        else:
            return f"projects/{project_id}/{res_type}/{resource_id}"
