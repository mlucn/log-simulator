"""Health check endpoints."""

from fastapi import APIRouter, Depends

from ..config import Settings, get_settings
from ..models import HealthResponse

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
async def health_check(settings: Settings = Depends(get_settings)) -> HealthResponse:
    """
    Health check endpoint.

    Returns the API status, version, and number of available schemas.
    """
    # Count available schemas
    schemas_dir = settings.schemas_dir
    schema_count = 0

    if schemas_dir.exists():
        schema_count = len(list(schemas_dir.rglob("*.yaml")))

    return HealthResponse(
        status="healthy", version=settings.version, schemas_available=schema_count
    )
