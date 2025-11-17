"""Main FastAPI application."""

from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from .config import get_settings
from .middleware.rate_limit import limiter
from .routes import generate_router, health_router, schemas_router

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    print(f"Starting {settings.app_name} v{settings.version}")
    print(f"Schemas directory: {settings.schemas_dir}")
    print(f"Rate limiting: {'enabled' if settings.rate_limit_enabled else 'disabled'}")

    yield

    # Shutdown
    print("Shutting down...")


# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    description="""
    Generate realistic synthetic log data for testing, development, and security research.

    ## Features

    * **Multiple Log Formats**: Support for cloud services, web servers, and security tools
    * **Schema-Based**: Flexible YAML schema definitions
    * **Realistic Data**: Built-in generators for IPs, emails, timestamps, UUIDs, and more
    * **Scenarios**: Pre-built scenarios for common use cases
    * **Field Overrides**: Customize specific fields as needed
    * **Time-Series**: Generate logs spread over time ranges

    ## Rate Limits

    - Schema discovery: 10 requests/minute
    - Log generation: 5 requests/minute

    ## Quick Start

    1. List available schemas: `GET /api/v1/schemas`
    2. Get schema details: `GET /api/v1/schemas/{schema_name}`
    3. Generate logs: `POST /api/v1/generate`
    """,
    lifespan=lifespan,
    docs_url=f"{settings.api_prefix}/docs",
    redoc_url=f"{settings.api_prefix}/redoc",
    openapi_url=f"{settings.api_prefix}/openapi.json",
)

# Add rate limiting
if settings.rate_limit_enabled:
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=settings.cors_credentials,
    allow_methods=settings.cors_methods,
    allow_headers=settings.cors_headers,
)


# Error handlers
@app.exception_handler(404)
async def not_found_handler(request: Request, exc: Exception):
    """Handle 404 errors."""
    return JSONResponse(
        status_code=404,
        content={
            "error": "Not Found",
            "message": str(exc),
            "detail": "The requested resource was not found",
        },
    )


@app.exception_handler(500)
async def internal_error_handler(request: Request, exc: Exception):
    """Handle 500 errors."""
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": "An unexpected error occurred",
            "detail": str(exc) if settings.debug else None,
        },
    )


# Include routers with rate limiting decorators
@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": settings.app_name,
        "version": settings.version,
        "docs": f"{settings.api_prefix}/docs",
        "schemas": f"{settings.api_prefix}/schemas",
    }


# Include routers
app.include_router(health_router, prefix=settings.api_prefix)
app.include_router(schemas_router, prefix=settings.api_prefix)
app.include_router(generate_router, prefix=settings.api_prefix)
