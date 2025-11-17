"""Request models for API endpoints."""

from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, Field, field_validator


class FieldOverride(BaseModel):
    """Field override specification."""

    path: str = Field(
        ..., description="Dot-notation path to field (e.g., 'user.email')"
    )
    value: Any = Field(..., description="Value to override the field with")


class GenerateRequest(BaseModel):
    """Request model for log generation."""

    schema_name: str = Field(
        ...,
        description="Schema name (e.g., 'cloud_identity/google_workspace')",
        examples=["cloud_identity/google_workspace"],
    )

    count: int = Field(
        default=10, ge=1, le=10000, description="Number of logs to generate"
    )

    scenario: Optional[str] = Field(
        default=None, description="Scenario name to use (optional)"
    )

    base_time: Optional[datetime] = Field(
        default=None, description="Base timestamp for logs (defaults to now)"
    )

    time_spread_seconds: Optional[int] = Field(
        default=None,
        ge=0,
        le=86400,
        description="Spread logs over this many seconds",
    )

    overrides: dict[str, Any] = Field(
        default_factory=dict,
        description="Field overrides as key-value pairs (dot notation)",
    )

    pretty: bool = Field(default=False, description="Pretty-print JSON output")

    @field_validator("schema_name")
    @classmethod
    def validate_schema_name(cls, v: str) -> str:
        """Validate schema name format."""
        # Remove .yaml extension if present
        if v.endswith(".yaml"):
            v = v[:-5]
        return v

    class Config:
        """Pydantic config."""

        json_schema_extra = {
            "example": {
                "schema_name": "cloud_identity/google_workspace",
                "count": 5,
                "scenario": "user_login_success",
                "time_spread_seconds": 300,
                "overrides": {
                    "actor.email": "test@example.com",
                    "ipAddress": "192.168.1.100",
                },
                "pretty": True,
            }
        }
