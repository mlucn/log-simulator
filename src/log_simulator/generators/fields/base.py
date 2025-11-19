"""
Base class for field generators.
"""

import random
import uuid
from datetime import datetime, timedelta, timezone
from typing import Any, Optional


class BaseFieldGenerator:
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
