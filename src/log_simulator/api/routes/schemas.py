"""Schema discovery endpoints."""

from pathlib import Path
from typing import Union

from fastapi import APIRouter, Depends, HTTPException

from ...generators.schema_generator import SchemaBasedGenerator
from ..config import Settings, get_settings
from ..models import SchemaInfoResponse, SchemaListResponse

router = APIRouter(prefix="/schemas", tags=["schemas"])


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
        if schema_full_name == schema_name or schema_full_name.endswith(f"/{schema_name}"):
            return schema_file

    # If not found, raise error
    raise HTTPException(
        status_code=404,
        detail=f"Schema '{schema_name}' not found. Use /schemas to list available schemas.",
    )


@router.get("", response_model=SchemaListResponse)
async def list_schemas(
    settings: Settings = Depends(get_settings),
) -> SchemaListResponse:
    """
    List all available log schemas.

    Returns schemas organized by category (e.g., cloud_identity, security, etc.)
    """
    schemas_dir = settings.schemas_dir
    schemas: dict[str, list[str]] = {}

    if not schemas_dir.exists():
        return SchemaListResponse(schemas={}, total_count=0)

    # Walk through the schemas directory
    for schema_file in schemas_dir.rglob("*.yaml"):
        # Get relative path from schemas_dir
        rel_path = schema_file.relative_to(schemas_dir)

        # Get category (parent directory name)
        if len(rel_path.parts) > 1:
            category = rel_path.parts[0]
        else:
            category = "other"

        # Get schema name (without .yaml)
        schema_name = str(rel_path.with_suffix(""))

        # Add to category
        if category not in schemas:
            schemas[category] = []
        schemas[category].append(schema_name)

    # Sort categories and schemas within each category
    schemas = {k: sorted(v) for k, v in sorted(schemas.items())}

    total = sum(len(v) for v in schemas.values())

    return SchemaListResponse(schemas=schemas, total_count=total)


@router.get("/{schema_name:path}", response_model=SchemaInfoResponse)
async def get_schema_info(
    schema_name: str, settings: Settings = Depends(get_settings)
) -> SchemaInfoResponse:
    """
    Get detailed information about a specific schema.

    Returns schema metadata including available scenarios and field count.
    """
    schemas_dir = settings.schemas_dir

    # Find the schema file
    schema_path = _find_schema_path(schema_name, schemas_dir)

    # Load schema using generator
    try:
        generator = SchemaBasedGenerator(str(schema_path))
        info = generator.get_schema_info()

        return SchemaInfoResponse(
            schema_name=schema_name,
            log_type=info["log_type"],
            description=info.get("description", "No description available"),
            output_format=info.get("output_format", "json"),
            available_scenarios=info.get("available_scenarios", []),
            field_count=len(info.get("fields", {})),
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error loading schema: {str(e)}"
        ) from e


@router.get("/{schema_name:path}/scenarios")
async def list_scenarios(
    schema_name: str, settings: Settings = Depends(get_settings)
) -> dict[str, Union[str, list[str]]]:
    """
    List available scenarios for a specific schema.

    Returns a list of scenario names that can be used with this schema.
    """
    schemas_dir = settings.schemas_dir

    # Find the schema file
    schema_path = _find_schema_path(schema_name, schemas_dir)

    # Load schema using generator
    try:
        generator = SchemaBasedGenerator(str(schema_path))
        scenarios = generator.list_scenarios()

        return {"schema": schema_name, "scenarios": scenarios}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error loading schema: {str(e)}"
        ) from e
