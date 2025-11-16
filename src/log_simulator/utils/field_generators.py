"""
Field generators for creating realistic log data.

This module provides various generators for common log fields like
timestamps, UUIDs, IP addresses, emails, etc.
"""

import random
import string
import uuid
from datetime import datetime, timedelta
from typing import Any, Optional


class FieldGenerator:
    """Base class for field generators with reusable utilities."""

    @staticmethod
    def uuid4() -> str:
        """Generate a random UUID v4."""
        return str(uuid.uuid4())

    @staticmethod
    def datetime_iso8601(
        base_time: Optional[datetime] = None,
        offset_seconds: int = 0
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
            base_time = datetime.utcnow()

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
            domain = random.choice([
                "example.com",
                "company.com",
                "organization.org",
                "business.net"
            ])

        first_names = [
            "john", "jane", "alice", "bob", "charlie", "david", "emma",
            "frank", "grace", "henry", "isabel", "jack", "kate", "liam"
        ]
        last_names = [
            "smith", "johnson", "williams", "brown", "jones", "garcia",
            "miller", "davis", "rodriguez", "martinez", "hernandez"
        ]

        first = random.choice(first_names)
        last = random.choice(last_names)

        formats = [
            f"{first}.{last}",
            f"{first}{last}",
            f"{first[0]}{last}",
            f"{first}.{last}{random.randint(1, 99)}"
        ]

        return f"{random.choice(formats)}@{domain}"

    @staticmethod
    def full_name() -> str:
        """Generate a random full name."""
        first_names = [
            "John", "Jane", "Alice", "Bob", "Charlie", "David", "Emma",
            "Frank", "Grace", "Henry", "Isabel", "Jack", "Kate", "Liam",
            "Maria", "Noah", "Olivia", "Peter", "Quinn", "Rachel"
        ]
        last_names = [
            "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia",
            "Miller", "Davis", "Rodriguez", "Martinez", "Hernandez",
            "Wilson", "Anderson", "Taylor", "Thomas", "Moore"
        ]

        return f"{random.choice(first_names)} {random.choice(last_names)}"

    @staticmethod
    def username() -> str:
        """Generate a random username."""
        adjectives = ["cool", "fast", "smart", "bright", "bold", "quick"]
        nouns = ["tiger", "eagle", "fox", "wolf", "bear", "lion"]
        return f"{random.choice(adjectives)}{random.choice(nouns)}{random.randint(1, 999)}"

    @staticmethod
    def number_string(length: int = 16) -> str:
        """
        Generate a random string of digits.

        Args:
            length: Number of digits

        Returns:
            String of random digits
        """
        return ''.join(random.choices(string.digits, k=length))

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
        random_part = ''.join(
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
            "Mozilla/5.0 (Linux; Android 13; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36"
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
            "/docs/readme.html"
        ]
        return random.choice(paths)

    @staticmethod
    def http_status() -> int:
        """Generate an HTTP status code with realistic distribution."""
        # Weighted distribution
        statuses = [200] * 75 + [301] * 5 + [302] * 3 + [304] * 4 + \
                   [400] * 2 + [401] * 2 + [403] * 2 + [404] * 5 + [500] * 2
        return random.choice(statuses)

    @staticmethod
    def city() -> str:
        """Generate a random city name."""
        cities = [
            "New York", "Los Angeles", "Chicago", "Houston", "Phoenix",
            "Philadelphia", "San Antonio", "San Diego", "Dallas", "San Jose",
            "London", "Paris", "Tokyo", "Sydney", "Toronto", "Berlin",
            "Singapore", "Mumbai", "Dubai", "Amsterdam"
        ]
        return random.choice(cities)

    @staticmethod
    def state() -> str:
        """Generate a random US state."""
        states = [
            "California", "Texas", "Florida", "New York", "Pennsylvania",
            "Illinois", "Ohio", "Georgia", "North Carolina", "Michigan"
        ]
        return random.choice(states)

    @staticmethod
    def country_code() -> str:
        """Generate a random ISO country code."""
        countries = [
            "US", "GB", "CA", "AU", "DE", "FR", "JP", "IN", "BR", "MX",
            "IT", "ES", "NL", "SE", "SG", "AE", "CN", "KR", "RU", "ZA"
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
    def request_time(min_time: float = 0.001, max_time: float = 30.0, mean: float = 0.150) -> float:
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
