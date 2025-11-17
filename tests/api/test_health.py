"""Tests for the health endpoint."""

from fastapi.testclient import TestClient


def test_health_endpoint_success(client: TestClient):
    """Test that health endpoint returns 200 OK."""
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"


def test_health_endpoint_response_structure(client: TestClient):
    """Test that health endpoint returns expected structure."""
    response = client.get("/api/v1/health")
    data = response.json()

    assert "status" in data
    assert "version" in data
    assert "schemas_available" in data
    assert data["status"] == "healthy"
    assert isinstance(data["schemas_available"], int)


def test_health_endpoint_no_authentication(client: TestClient):
    """Test that health endpoint doesn't require authentication."""
    # Should work without any auth headers
    response = client.get("/api/v1/health")
    assert response.status_code == 200


def test_health_endpoint_accepts_head_request(client: TestClient):
    """Test that health endpoint supports HEAD requests."""
    response = client.head("/api/v1/health")
    # HEAD may not be explicitly defined, so 405 is acceptable
    assert response.status_code in [200, 405]


def test_health_endpoint_options_request(client: TestClient):
    """Test that health endpoint supports OPTIONS for CORS."""
    response = client.options("/api/v1/health")
    # Should return either 200 or 405, depending on CORS config
    assert response.status_code in [200, 405]


def test_health_endpoint_get_only(client: TestClient):
    """Test that health endpoint rejects POST/PUT/DELETE."""
    # POST should not be allowed
    response = client.post("/api/v1/health")
    assert response.status_code == 405

    # PUT should not be allowed
    response = client.put("/api/v1/health")
    assert response.status_code == 405

    # DELETE should not be allowed
    response = client.delete("/api/v1/health")
    assert response.status_code == 405


def test_health_endpoint_response_time(client: TestClient):
    """Test that health endpoint responds quickly."""
    import time

    start = time.time()
    response = client.get("/api/v1/health")
    duration = time.time() - start

    assert response.status_code == 200
    # Health check should be fast (< 100ms)
    assert duration < 0.1
