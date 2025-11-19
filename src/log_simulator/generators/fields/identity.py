"""
Identity-related field generators.
"""

import random
import string
from typing import Optional

from .base import BaseFieldGenerator


class IdentityGenerator(BaseFieldGenerator):
    """Generators for identity-related fields (users, emails, etc)."""

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
