"""
Field generators for creating realistic log data.

This module provides various generators for common log fields like
timestamps, UUIDs, IP addresses, emails, etc.
"""

import random
import string
import uuid
from datetime import datetime, timedelta, timezone
from typing import Any, Optional


class FieldGenerator:
    """Base class for field generators with reusable utilities."""

    @staticmethod
    def uuid4() -> str:
        """Generate a random UUID v4."""
        return str(uuid.uuid4())

    @staticmethod
    def datetime_iso8601(
        base_time: Optional[datetime] = None, offset_seconds: int = 0
    ) -> str:
        """
        Generate an ISO 8601 formatted timestamp.

        Args:
            base_time: Base datetime to use (defaults to now)
            offset_seconds: Seconds to offset from base_time

        Returns:
            ISO 8601 formatted timestamp string
        """
        if base_time is None:
            base_time = datetime.now(timezone.utc)

        timestamp = base_time + timedelta(seconds=offset_seconds)
        return timestamp.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

    @staticmethod
    def ipv4(internal: bool = False) -> str:
        """
        Generate a random IPv4 address.

        Args:
            internal: If True, generate RFC 1918 private IP

        Returns:
            IPv4 address string
        """
        if internal:
            # Generate private IP (10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16)
            choice = random.choice(["10", "172", "192"])
            if choice == "10":
                return f"10.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}"
            elif choice == "172":
                return f"172.{random.randint(16, 31)}.{random.randint(0, 255)}.{random.randint(1, 254)}"
            else:
                return f"192.168.{random.randint(0, 255)}.{random.randint(1, 254)}"
        else:
            # Generate public IP (avoiding reserved ranges)
            return f"{random.randint(1, 223)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}"

    @staticmethod
    def email(domain: Optional[str] = None) -> str:
        """
        Generate a random email address.

        Args:
            domain: Email domain (defaults to example.com)

        Returns:
            Email address string
        """
        if domain is None:
            domain = random.choice(
                ["example.com", "company.com", "organization.org", "business.net"]
            )

        first_names = [
            "john",
            "jane",
            "alice",
            "bob",
            "charlie",
            "david",
            "emma",
            "frank",
            "grace",
            "henry",
            "isabel",
            "jack",
            "kate",
            "liam",
        ]
        last_names = [
            "smith",
            "johnson",
            "williams",
            "brown",
            "jones",
            "garcia",
            "miller",
            "davis",
            "rodriguez",
            "martinez",
            "hernandez",
        ]

        first = random.choice(first_names)
        last = random.choice(last_names)

        formats = [
            f"{first}.{last}",
            f"{first}{last}",
            f"{first[0]}{last}",
            f"{first}.{last}{random.randint(1, 99)}",
        ]

        return f"{random.choice(formats)}@{domain}"

    @staticmethod
    def full_name() -> str:
        """Generate a random full name."""
        first_names = [
            "John",
            "Jane",
            "Alice",
            "Bob",
            "Charlie",
            "David",
            "Emma",
            "Frank",
            "Grace",
            "Henry",
            "Isabel",
            "Jack",
            "Kate",
            "Liam",
            "Maria",
            "Noah",
            "Olivia",
            "Peter",
            "Quinn",
            "Rachel",
        ]
        last_names = [
            "Smith",
            "Johnson",
            "Williams",
            "Brown",
            "Jones",
            "Garcia",
            "Miller",
            "Davis",
            "Rodriguez",
            "Martinez",
            "Hernandez",
            "Wilson",
            "Anderson",
            "Taylor",
            "Thomas",
            "Moore",
        ]

        return f"{random.choice(first_names)} {random.choice(last_names)}"

    @staticmethod
    def username() -> str:
        """Generate a random username."""
        adjectives = ["cool", "fast", "smart", "bright", "bold", "quick"]
        nouns = ["tiger", "eagle", "fox", "wolf", "bear", "lion"]
        return (
            f"{random.choice(adjectives)}{random.choice(nouns)}{random.randint(1, 999)}"
        )

    @staticmethod
    def number_string(length: int = 16) -> str:
        """
        Generate a random string of digits.

        Args:
            length: Number of digits

        Returns:
            String of random digits
        """
        return "".join(random.choices(string.digits, k=length))

    @staticmethod
    def custom_id(prefix: str = "", length: int = 8) -> str:
        """
        Generate a custom ID with prefix.

        Args:
            prefix: ID prefix
            length: Length of random part (alphanumeric)

        Returns:
            Custom ID string
        """
        random_part = "".join(
            random.choices(string.ascii_uppercase + string.digits, k=length)
        )
        return f"{prefix}{random_part}"

    @staticmethod
    def user_agent() -> str:
        """Generate a random user agent string."""
        browsers = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (Linux; Android 13; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
        ]
        return random.choice(browsers)

    @staticmethod
    def uri_path() -> str:
        """Generate a random URI path."""
        paths = [
            "/",
            "/index.html",
            "/about.html",
            "/api/v1/users",
            "/api/v1/data",
            "/api/v2/search",
            "/static/css/style.css",
            "/static/js/app.js",
            "/images/logo.png",
            "/dashboard",
            "/profile",
            "/settings",
            "/login",
            "/logout",
            "/docs/readme.html",
        ]
        return random.choice(paths)

    @staticmethod
    def http_status() -> int:
        """Generate an HTTP status code with realistic distribution."""
        # Weighted distribution
        statuses = (
            [200] * 75
            + [301] * 5
            + [302] * 3
            + [304] * 4
            + [400] * 2
            + [401] * 2
            + [403] * 2
            + [404] * 5
            + [500] * 2
        )
        return random.choice(statuses)

    @staticmethod
    def city() -> str:
        """Generate a random city name."""
        cities = [
            "New York",
            "Los Angeles",
            "Chicago",
            "Houston",
            "Phoenix",
            "Philadelphia",
            "San Antonio",
            "San Diego",
            "Dallas",
            "San Jose",
            "London",
            "Paris",
            "Tokyo",
            "Sydney",
            "Toronto",
            "Berlin",
            "Singapore",
            "Mumbai",
            "Dubai",
            "Amsterdam",
        ]
        return random.choice(cities)

    @staticmethod
    def state() -> str:
        """Generate a random US state."""
        states = [
            "California",
            "Texas",
            "Florida",
            "New York",
            "Pennsylvania",
            "Illinois",
            "Ohio",
            "Georgia",
            "North Carolina",
            "Michigan",
        ]
        return random.choice(states)

    @staticmethod
    def country_code() -> str:
        """Generate a random ISO country code."""
        countries = [
            "US",
            "GB",
            "CA",
            "AU",
            "DE",
            "FR",
            "JP",
            "IN",
            "BR",
            "MX",
            "IT",
            "ES",
            "NL",
            "SE",
            "SG",
            "AE",
            "CN",
            "KR",
            "RU",
            "ZA",
        ]
        return random.choice(countries)

    @staticmethod
    def latitude() -> float:
        """Generate a random latitude."""
        return round(random.uniform(-90, 90), 6)

    @staticmethod
    def longitude() -> float:
        """Generate a random longitude."""
        return round(random.uniform(-180, 180), 6)

    @staticmethod
    def device_name() -> str:
        """Generate a random device name."""
        prefixes = ["DESKTOP", "LAPTOP", "MOBILE", "WORKSTATION"]
        return f"{random.choice(prefixes)}-{random.choice(string.ascii_uppercase)}{random.randint(1000, 9999)}"

    @staticmethod
    def boolean(true_probability: float = 0.5) -> bool:
        """
        Generate a random boolean value.

        Args:
            true_probability: Probability of True (0.0 to 1.0)

        Returns:
            Random boolean
        """
        return random.random() < true_probability

    @staticmethod
    def weighted_choice(distribution: dict) -> Any:
        """
        Choose a value based on weighted distribution.

        Args:
            distribution: Dict mapping values to weights (probabilities)

        Returns:
            Randomly chosen value based on weights
        """
        values = list(distribution.keys())
        weights = list(distribution.values())
        return random.choices(values, weights=weights, k=1)[0]

    @staticmethod
    def body_bytes(min_bytes: int = 0, max_bytes: int = 5000000) -> int:
        """
        Generate response body size in bytes with log-normal distribution.

        Args:
            min_bytes: Minimum size
            max_bytes: Maximum size

        Returns:
            Random byte count
        """
        # Log-normal distribution favors smaller sizes
        value = int(random.lognormvariate(7, 2))
        return max(min_bytes, min(value, max_bytes))

    @staticmethod
    def request_time(
        min_time: float = 0.001, max_time: float = 30.0, mean: float = 0.150
    ) -> float:
        """
        Generate request processing time with log-normal distribution.

        Args:
            min_time: Minimum time in seconds
            max_time: Maximum time in seconds
            mean: Mean time in seconds

        Returns:
            Random processing time
        """
        # Log-normal distribution
        import math

        mu = math.log(mean)
        sigma = 1.0
        value = random.lognormvariate(mu, sigma)
        return round(max(min_time, min(value, max_time)), 3)

    @staticmethod
    def email_subject() -> str:
        """Generate a random email subject line."""
        subjects = [
            "Project Update",
            "Meeting Tomorrow",
            "Q4 Report",
            "Action Required",
            "Weekly Status",
            "Follow Up",
            "Question about the proposal",
            "Budget Review",
            "Team Lunch",
            "Important Announcement",
            "Schedule Change",
            "Document Review",
            "Approval Needed",
            "Thank You",
            "Next Steps",
            "Quarterly Results",
            "Policy Update",
            "Training Session",
            "Feedback Request",
            "System Maintenance",
        ]
        return random.choice(subjects)

    @staticmethod
    def filename() -> str:
        """Generate a random filename."""
        names = [
            "report",
            "document",
            "presentation",
            "spreadsheet",
            "budget",
            "proposal",
            "summary",
            "analysis",
            "data",
            "meeting_notes",
            "project_plan",
            "requirements",
            "spec",
        ]
        extensions = [
            ".docx",
            ".xlsx",
            ".pptx",
            ".pdf",
            ".txt",
            ".csv",
            ".json",
            ".xml",
            ".zip",
            ".png",
        ]
        name = random.choice(names)
        ext = random.choice(extensions)

        # Sometimes add date or version
        if random.random() < 0.3:
            suffix = f"_{random.choice(['2024', '2025', 'Q4', 'final', 'v2', 'draft'])}"
            return f"{name}{suffix}{ext}"
        return f"{name}{ext}"

    @staticmethod
    def referer() -> str:
        """Generate a random HTTP referer."""
        if random.random() < 0.3:
            return "-"  # No referer

        domains = ["example.com", "google.com", "github.com", "stackoverflow.com"]
        paths = ["/", "/search", "/dashboard", "/docs", "/api"]
        domain = random.choice(domains)
        path = random.choice(paths)
        return f"https://{domain}{path}"

    @staticmethod
    def process_name() -> str:
        """Generate a random process name."""
        processes = [
            "chrome.exe",
            "firefox.exe",
            "msedge.exe",
            "explorer.exe",
            "svchost.exe",
            "System",
            "cmd.exe",
            "powershell.exe",
            "notepad.exe",
            "Teams.exe",
            "Outlook.exe",
            "Excel.exe",
            "Word.exe",
            "java.exe",
            "python.exe",
            "node.exe",
            "code.exe",
            "slack.exe",
            "zoom.exe",
        ]
        return random.choice(processes)

    @staticmethod
    def command_line() -> str:
        """Generate a random command line."""
        commands = [
            '"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe" --type=renderer',
            "C:\\Windows\\System32\\svchost.exe -k NetworkService",
            "powershell.exe -NoProfile -Command Get-Process",
            'cmd.exe /c "dir C:\\Users"',
            '"C:\\Program Files\\Microsoft Office\\Office16\\OUTLOOK.EXE"',
            "python.exe script.py --verbose",
            "node.exe server.js",
            '"C:\\Windows\\Explorer.EXE"',
            "notepad.exe C:\\Users\\user\\Documents\\file.txt",
        ]
        return random.choice(commands)

    @staticmethod
    def sha256() -> str:
        """Generate a random SHA256 hash."""
        return "".join(random.choices("0123456789abcdef", k=64))

    @staticmethod
    def md5() -> str:
        """Generate a random MD5 hash."""
        return "".join(random.choices("0123456789abcdef", k=32))

    @staticmethod
    def domain_name() -> str:
        """Generate a random domain name."""
        domains = [
            "example.com",
            "test.com",
            "sample.org",
            "demo.net",
            "google.com",
            "microsoft.com",
            "amazon.com",
            "github.com",
            "api.service.com",
            "cdn.example.net",
            "mail.company.com",
            "update.vendor.com",
            "download.software.org",
        ]
        return random.choice(domains)

    @staticmethod
    def file_path() -> str:
        """Generate a random Windows file path."""
        paths = [
            "C:\\Users\\user\\Documents\\report.docx",
            "C:\\Users\\user\\Downloads\\setup.exe",
            "C:\\Windows\\System32\\config\\system",
            "C:\\Program Files\\Application\\app.exe",
            "C:\\Users\\Public\\Desktop\\file.txt",
            "C:\\Temp\\output.log",
            "C:\\ProgramData\\vendor\\data.json",
            "C:\\Users\\user\\AppData\\Local\\Temp\\tmp.dat",
            "D:\\Projects\\source\\main.py",
        ]
        return random.choice(paths)

    @staticmethod
    def detection_name() -> str:
        """Generate a random security detection name."""
        detections = [
            "Suspicious PowerShell Execution",
            "Malicious Process Detected",
            "Credential Dumping Attempt",
            "Lateral Movement Activity",
            "Ransomware Behavior",
            "Privilege Escalation",
            "Malware Communication",
            "Suspicious Network Connection",
            "File Encryption Activity",
            "Registry Persistence",
            "Suspicious Script Execution",
            "Command and Control Traffic",
        ]
        return random.choice(detections)

    @staticmethod
    def registry_key() -> str:
        """Generate a random Windows registry key."""
        keys = [
            "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run",
            "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\RunOnce",
            "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run",
            "HKLM\\SYSTEM\\CurrentControlSet\\Services",
            "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows",
            "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer",
            "HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion",
        ]
        return random.choice(keys)

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
    def aws_arn() -> str:
        """Generate a random AWS ARN."""
        account_id = FieldGenerator.aws_account_id()
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
    def aws_account_id() -> str:
        """Generate a random AWS account ID (12 digits)."""
        return "".join(random.choices(string.digits, k=12))

    @staticmethod
    def aws_resource_arn() -> str:
        """Generate a random AWS resource ARN."""
        return FieldGenerator.aws_arn()

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
        project_id = FieldGenerator.gcp_project_id()
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

    @staticmethod
    def sysmon_guid() -> str:
        """Generate a Sysmon-style GUID."""
        # Format: {XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX}
        return "{" + FieldGenerator.uuid4().upper() + "}"

    @staticmethod
    def windows_image_path() -> str:
        """Generate a random Windows executable path."""
        paths = [
            "C:\\Windows\\System32\\cmd.exe",
            "C:\\Windows\\System32\\powershell.exe",
            "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe",
            "C:\\Windows\\explorer.exe",
            "C:\\Windows\\System32\\svchost.exe",
            "C:\\Windows\\System32\\rundll32.exe",
            "C:\\Windows\\System32\\wscript.exe",
            "C:\\Windows\\System32\\cscript.exe",
            "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
            "C:\\Program Files\\Microsoft Office\\Office16\\EXCEL.EXE",
            "C:\\Program Files\\Microsoft Office\\Office16\\WINWORD.EXE",
            "C:\\Program Files\\Microsoft Office\\Office16\\OUTLOOK.EXE",
            "C:\\Windows\\System32\\msiexec.exe",
            "C:\\Windows\\System32\\reg.exe",
            "C:\\Windows\\System32\\net.exe",
        ]
        return random.choice(paths)

    @staticmethod
    def windows_user() -> str:
        """Generate a Windows user in DOMAIN\\User format."""
        domains = ["WORKSTATION", "CORP", "DOMAIN", "NT AUTHORITY"]
        users = ["user", "admin", "Administrator", "SYSTEM", "service_account"]
        return f"{random.choice(domains)}\\{random.choice(users)}"

    @staticmethod
    def sysmon_hashes() -> str:
        """Generate Sysmon-style hash string."""
        md5 = FieldGenerator.md5()
        sha256 = FieldGenerator.sha256()
        return f"MD5={md5},SHA256={sha256}"
