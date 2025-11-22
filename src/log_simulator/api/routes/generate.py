"""Log generation endpoints."""

import time
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException

from ...generators.schema_generator import SchemaBasedGenerator
from ..config import Settings, get_settings
from ..models import GenerateRequest, GenerateResponse

router = APIRouter(prefix="/generate", tags=["generate"])


def _find_schema_path(schema_name: str, schemas_dir: Path) -> Path:
    """
    Find the full path to a schema file.

    Supports multiple formats:
    - Relative path: "google_workspace/admin" -> cloud_identity/google_workspace/admin.yaml
    - Full path: "cloud_identity/google_workspace/admin" -> cloud_identity/google_workspace/admin.yaml
    - Simple name: "nginx_access" -> web_servers/nginx_access.yaml
    """
    # Remove .yaml extension if present
    if schema_name.endswith(".yaml"):
        schema_name = schema_name[:-5]

    # Try direct path first (e.g., "cloud_identity/google_workspace/admin")
    schema_path = schemas_dir / f"{schema_name}.yaml"
    if schema_path.exists():
        return schema_path

    # Search recursively for matching schema
    # This allows "google_workspace/admin" to find "cloud_identity/google_workspace/admin.yaml"
    for schema_file in schemas_dir.rglob("*.yaml"):
        rel_path = schema_file.relative_to(schemas_dir)
        schema_full_name = str(rel_path.with_suffix(""))

        # Check if the schema_name matches the end of the full path
        # This allows both "admin" and "google_workspace/admin" to match
        if schema_full_name == schema_name or schema_full_name.endswith(
            f"/{schema_name}"
        ):
            return schema_file

    # If not found, raise error
    raise HTTPException(
        status_code=404,
        detail=f"Schema '{schema_name}' not found. Use /schemas to list available schemas.",
    )


@router.post("", response_model=GenerateResponse)
async def generate_logs(
    request: GenerateRequest,
    settings: Settings = Depends(get_settings),
) -> GenerateResponse:
    """
    Generate synthetic log entries based on a schema.

    This endpoint generates realistic log data according to the specified schema.
    You can optionally:
    - Use predefined scenarios
    - Override specific fields
    - Spread logs over a time range
    - Control output formatting

    Rate limit: 5 requests per minute per IP
    """
    # Validate count against max
    if request.count > settings.max_log_count:
        raise HTTPException(
            status_code=400,
            detail=f"Count exceeds maximum allowed ({settings.max_log_count})",
        )

    # Validate time_spread if provided
    if (
        request.time_spread_seconds
        and request.time_spread_seconds > settings.max_time_spread
    ):
        raise HTTPException(
            status_code=400,
            detail=f"Time spread exceeds maximum allowed ({settings.max_time_spread} seconds)",
        )

    # Find schema file
    schemas_dir = settings.schemas_dir
    schema_path = _find_schema_path(request.schema_name, schemas_dir)

    # Generate logs
    try:
        start_time = time.time()

        generator = SchemaBasedGenerator(str(schema_path))

        logs = generator.generate(
            count=request.count,
            scenario=request.scenario,
            base_time=request.base_time,
            time_spread_seconds=request.time_spread_seconds or 0,
        )

        # Apply field overrides if provided
        if request.overrides:
            for log in logs:
                for field_path, value in request.overrides.items():
                    # Split path and navigate to set the value
                    parts = field_path.split(".")
                    target = log
                    for part in parts[:-1]:
                        if part not in target:
                            target[part] = {}
                        target = target[part]
                    target[parts[-1]] = value

        execution_time = time.time() - start_time

        return GenerateResponse(
            success=True,
            count=len(logs),
            execution_time=round(execution_time, 3),
            logs=logs,
            schema_used=request.schema_name,
            scenario_used=request.scenario,
        )

    except ValueError as e:
        # Handle validation errors (e.g., invalid scenario)
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        # Handle unexpected errors
        raise HTTPException(
            status_code=500, detail=f"Error generating logs: {str(e)}"
        ) from e
