"""Response models for API endpoints."""

from typing import Any, Optional

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    """Health check response."""

    status: str = Field(..., description="Health status")
    version: str = Field(..., description="API version")
    schemas_available: int = Field(..., description="Number of available schemas")


class SchemaInfoResponse(BaseModel):
    """Schema information response."""

    schema_name: str = Field(..., description="Schema name")
    log_type: str = Field(..., description="Log type identifier")
    description: str = Field(..., description="Schema description")
    output_format: str = Field(..., description="Output format (json, text, etc.)")
    available_scenarios: list[str] = Field(
        ..., description="List of available scenarios"
    )
    field_count: int = Field(..., description="Number of fields in schema")


class SchemaListResponse(BaseModel):
    """List of available schemas."""

    schemas: dict[str, list[str]] = Field(
        ..., description="Schemas organized by category"
    )
    total_count: int = Field(..., description="Total number of schemas")


class GenerateResponse(BaseModel):
    """Log generation response."""

    success: bool = Field(..., description="Whether generation was successful")
    count: int = Field(..., description="Number of logs generated")
    execution_time: float = Field(..., description="Execution time in seconds")
    logs: list[dict[str, Any]] = Field(..., description="Generated log entries")
    schema_used: str = Field(..., description="Schema that was used")
    scenario_used: Optional[str] = Field(
        default=None, description="Scenario that was used (if any)"
    )


class ErrorResponse(BaseModel):
    """Error response."""

    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Error message")
    detail: Optional[str] = Field(default=None, description="Additional error details")
