"""
Pydantic models for log schema validation.
"""

from typing import Any, Optional, Union

from pydantic import BaseModel, ConfigDict, field_validator


class FieldSpec(BaseModel):
    """Specification for a single log field."""

    type: str
    required: bool = False
    description: Optional[str] = None
    default: Optional[Any] = None
    generator: Optional[str] = None
    params: Optional[dict[str, Any]] = None
    values: Optional[list[Any]] = None  # For enum
    distribution: Optional[dict[Union[str, int], float]] = None  # For weighted choice
    fields: Optional[dict[str, "FieldSpec"]] = None  # For object type
    item: Optional["FieldSpec"] = None  # For array type
    min_items: Optional[int] = 1
    max_items: Optional[int] = 3
    value: Optional[Any] = None  # For constant type
    format: Optional[str] = None  # For datetime
    ecs_field: Optional[str] = None  # For ECS mapping

    model_config = ConfigDict(extra="allow")

    @field_validator("type")
    @classmethod
    def validate_type(cls, v: str) -> str:
        allowed_types = {
            "string",
            "integer",
            "float",
            "boolean",
            "datetime",
            "uuid",
            "ipv4",
            "email",
            "enum",
            "object",
            "array",
            "constant",
        }
        if v not in allowed_types:
            raise ValueError(f"Invalid field type: {v}. Must be one of {allowed_types}")
        return v


class ScenarioSpec(BaseModel):
    """Specification for a generation scenario."""

    # Scenarios are flexible dictionaries of overrides
    # We use a custom root type or just allow extra fields
    model_config = ConfigDict(extra="allow")


class CorrelationRule(BaseModel):
    """Rule for correlating fields across logs."""

    field: str
    scope: str
    description: Optional[str] = None
    correlation_with: Optional[str] = None


class LogSchema(BaseModel):
    """Top-level log schema definition."""

    schema_version: str
    log_type: str
    description: Optional[str] = None
    output_format: str = "json"
    ecs_compatible: bool = False
    fields: dict[str, FieldSpec]
    scenarios: Optional[dict[str, dict[str, Any]]] = None
    correlation: Optional[list[CorrelationRule]] = None

    model_config = ConfigDict(extra="allow")
