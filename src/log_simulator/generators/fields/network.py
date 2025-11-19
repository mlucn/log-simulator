"""
Network-related field generators.
"""

import random

from .base import BaseFieldGenerator


class NetworkGenerator(BaseFieldGenerator):
    """Generators for network-related fields (IPs, URLs, etc)."""

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
