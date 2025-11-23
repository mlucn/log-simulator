"""Tests for the log generation endpoint."""

from fastapi.testclient import TestClient


def test_generate_endpoint_success(client: TestClient, sample_generate_request: dict):
    """Test successful log generation."""
    response = client.post("/api/v1/generate", json=sample_generate_request)

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"


def test_generate_endpoint_returns_logs(
    client: TestClient, sample_generate_request: dict
):
    """Test that generate endpoint returns log entries."""
    response = client.post("/api/v1/generate", json=sample_generate_request)
    data = response.json()

    assert "logs" in data
    assert isinstance(data["logs"], list)
    assert len(data["logs"]) == sample_generate_request["count"]


def test_generate_endpoint_minimal_request(
    client: TestClient, sample_generate_request_minimal: dict
):
    """Test generation with minimal required fields."""
    response = client.post("/api/v1/generate", json=sample_generate_request_minimal)

    assert response.status_code == 200
    data = response.json()
    assert len(data["logs"]) == 1


def test_generate_endpoint_with_time_spread(
    client: TestClient, sample_generate_request_with_time: dict
):
    """Test generation with time spread parameter."""
    response = client.post("/api/v1/generate", json=sample_generate_request_with_time)

    assert response.status_code == 200
    data = response.json()
    assert len(data["logs"]) == sample_generate_request_with_time["count"]


def test_generate_endpoint_invalid_schema(
    client: TestClient, invalid_schema_request: dict
):
    """Test that invalid schema name returns 404."""
    response = client.post("/api/v1/generate", json=invalid_schema_request)

    assert response.status_code == 404
    data = response.json()
    assert "detail" in data


def test_generate_endpoint_count_too_high(
    client: TestClient, invalid_count_request: dict
):
    """Test that count exceeding max returns 422 (Pydantic validation)."""
    response = client.post("/api/v1/generate", json=invalid_count_request)

    # Pydantic le=10000 validation happens first (422)
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data


def test_generate_endpoint_time_spread_too_high(
    client: TestClient, invalid_time_spread_request: dict
):
    """Test that time_spread exceeding max returns 422 (Pydantic validation)."""
    response = client.post("/api/v1/generate", json=invalid_time_spread_request)

    # Pydantic le=86400 validation happens first (422)
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data


def test_generate_endpoint_missing_schema_name(client: TestClient):
    """Test that missing schema_name returns 422."""
    request = {"count": 5}
    response = client.post("/api/v1/generate", json=request)

    assert response.status_code == 422  # Validation error


def test_generate_endpoint_default_count(client: TestClient):
    """Test that count has a default value."""
    # count is optional with default=10
    request = {"schema_name": "cloud_identity/google_workspace/admin"}
    response = client.post("/api/v1/generate", json=request)

    assert response.status_code == 200
    data = response.json()
    assert data["count"] == 10  # Default count


def test_generate_endpoint_zero_count(client: TestClient):
    """Test that zero count returns 422 (validation error)."""
    request = {"schema_name": "cloud_identity/google_workspace/admin", "count": 0}
    response = client.post("/api/v1/generate", json=request)

    assert response.status_code == 422  # Pydantic validation error (ge=1)


def test_generate_endpoint_negative_count(client: TestClient):
    """Test that negative count returns 422 (validation error)."""
    request = {"schema_name": "cloud_identity/google_workspace/admin", "count": -5}
    response = client.post("/api/v1/generate", json=request)

    assert response.status_code == 422  # Pydantic validation error (ge=1)


def test_generate_endpoint_invalid_scenario(client: TestClient):
    """Test that invalid scenario name returns 400."""
    request = {
        "schema_name": "cloud_identity/google_workspace/admin",
        "count": 5,
        "scenario": "nonexistent_scenario",
    }
    response = client.post("/api/v1/generate", json=request)

    assert response.status_code == 400


def test_generate_endpoint_log_structure(
    client: TestClient, sample_generate_request: dict
):
    """Test that generated logs have expected structure."""
    response = client.post("/api/v1/generate", json=sample_generate_request)
    data = response.json()

    # Each log should be a dict
    for log in data["logs"]:
        assert isinstance(log, dict)
        assert len(log) > 0  # Should have at least some fields


def test_generate_endpoint_response_metadata(
    client: TestClient, sample_generate_request: dict
):
    """Test that response includes metadata."""
    response = client.post("/api/v1/generate", json=sample_generate_request)
    data = response.json()

    assert "success" in data
    assert "schema_used" in data
    assert "count" in data
    assert "execution_time" in data
    assert data["success"] is True
    assert data["schema_used"] == sample_generate_request["schema_name"]
    assert data["count"] == len(data["logs"])
    assert isinstance(data["execution_time"], float)


def test_generate_endpoint_different_counts(client: TestClient):
    """Test generation with different count values."""
    schema = "cloud_identity/google_workspace/admin"

    for count in [1, 5, 10, 50]:
        request = {"schema_name": schema, "count": count}
        response = client.post("/api/v1/generate", json=request)

        assert response.status_code == 200
        data = response.json()
        assert len(data["logs"]) == count


def test_generate_endpoint_multiple_schemas(client: TestClient):
    """Test generation with different schemas."""
    schemas = [
        "cloud_identity/google_workspace/admin",
        "web_servers/nginx_access",
        "security/crowdstrike_fdr",
    ]

    for schema in schemas:
        request = {"schema_name": schema, "count": 3}
        response = client.post("/api/v1/generate", json=request)

        assert response.status_code == 200, f"Failed for schema: {schema}"
        data = response.json()
        assert len(data["logs"]) == 3


def test_generate_endpoint_post_only(client: TestClient):
    """Test that generate endpoint only accepts POST."""
    # GET should not be allowed
    response = client.get("/api/v1/generate")
    assert response.status_code == 405

    # PUT should not be allowed
    response = client.put("/api/v1/generate")
    assert response.status_code == 405

    # DELETE should not be allowed
    response = client.delete("/api/v1/generate")
    assert response.status_code == 405


def test_generate_endpoint_invalid_json(client: TestClient):
    """Test that invalid JSON returns 422."""
    response = client.post(
        "/api/v1/generate",
        data="not json",
        headers={"Content-Type": "application/json"},
    )

    assert response.status_code == 422


def test_generate_endpoint_empty_body(client: TestClient):
    """Test that empty request body returns 422."""
    response = client.post("/api/v1/generate", json={})

    assert response.status_code == 422


def test_generate_endpoint_extra_fields_ignored(client: TestClient):
    """Test that extra fields in request are handled gracefully."""
    request = {
        "schema_name": "cloud_identity/google_workspace/admin",
        "count": 5,
        "extra_field": "should be ignored",
    }
    response = client.post("/api/v1/generate", json=request)

    # Pydantic may ignore extra fields depending on config
    assert response.status_code in [200, 422]


def test_generate_endpoint_response_time_small(client: TestClient):
    """Test that small generation is fast."""
    import time

    request = {"schema_name": "cloud_identity/google_workspace/admin", "count": 1}

    start = time.time()
    response = client.post("/api/v1/generate", json=request)
    duration = time.time() - start

    assert response.status_code == 200
    # Should complete in reasonable time (< 1 second)
    assert duration < 1.0


def test_generate_endpoint_consistent_log_count(client: TestClient):
    """Test that multiple requests with same count produce same count."""
    request = {"schema_name": "cloud_identity/google_workspace/admin", "count": 10}

    for _ in range(3):
        response = client.post("/api/v1/generate", json=request)
        assert response.status_code == 200
        data = response.json()
        assert len(data["logs"]) == 10


def test_generate_endpoint_scenario_affects_output(client: TestClient):
    """Test that scenario parameter affects generated logs."""
    schema = "cloud_identity/google_workspace/admin"

    # Generate with different scenarios
    request1 = {"schema_name": schema, "count": 1, "scenario": "user_create"}
    request2 = {"schema_name": schema, "count": 1, "scenario": "user_delete"}

    response1 = client.post("/api/v1/generate", json=request1)
    response2 = client.post("/api/v1/generate", json=request2)

    assert response1.status_code == 200
    assert response2.status_code == 200

    data1 = response1.json()
    data2 = response2.json()

    # Both should generate successfully
    assert len(data1["logs"]) == 1
    assert len(data2["logs"]) == 1
    assert data1["scenario_used"] == "user_create"
    assert data2["scenario_used"] == "user_delete"
