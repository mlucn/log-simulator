"""Pytest fixtures for API tests."""

import pytest
from fastapi.testclient import TestClient

from log_simulator.api.main import app


@pytest.fixture
def client() -> TestClient:
    """Create a FastAPI test client."""
    return TestClient(app)


@pytest.fixture
def sample_generate_request() -> dict:
    """Sample valid generate request payload."""
    return {
        "schema_name": "cloud_identity/google_workspace",
        "count": 5,
        "scenario": "user_login_success",
    }


@pytest.fixture
def sample_generate_request_minimal() -> dict:
    """Minimal valid generate request payload."""
    return {
        "schema_name": "cloud_identity/google_workspace",
        "count": 1,
    }


@pytest.fixture
def sample_generate_request_with_time() -> dict:
    """Generate request with time parameters."""
    return {
        "schema_name": "cloud_identity/google_workspace",
        "count": 10,
        "time_spread_seconds": 3600,
    }


@pytest.fixture
def invalid_schema_request() -> dict:
    """Request with invalid schema name."""
    return {
        "schema_name": "nonexistent/schema",
        "count": 5,
    }


@pytest.fixture
def invalid_count_request() -> dict:
    """Request with invalid count (too high)."""
    return {
        "schema_name": "cloud_identity/google_workspace",
        "count": 20000,  # Exceeds default max of 10000
    }


@pytest.fixture
def invalid_time_spread_request() -> dict:
    """Request with invalid time spread."""
    return {
        "schema_name": "cloud_identity/google_workspace",
        "count": 5,
        "time_spread_seconds": 100000,  # Exceeds default max of 86400
    }
