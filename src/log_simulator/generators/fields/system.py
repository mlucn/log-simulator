"""
System-related field generators.
"""

import random
import string

from .base import BaseFieldGenerator


class SystemGenerator(BaseFieldGenerator):
    """Generators for system-related fields (processes, files, registry)."""

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
    def sysmon_guid() -> str:
        """Generate a Sysmon-style GUID."""
        # Format: {XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX}
        return "{" + BaseFieldGenerator.uuid4().upper() + "}"

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
        md5 = SystemGenerator.md5()
        sha256 = SystemGenerator.sha256()
        return f"MD5={md5},SHA256={sha256}"

    @staticmethod
    def device_name() -> str:
        """Generate a random device name."""
        prefixes = ["DESKTOP", "LAPTOP", "MOBILE", "WORKSTATION"]
        return f"{random.choice(prefixes)}-{random.choice(string.ascii_uppercase)}{random.randint(1000, 9999)}"

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
