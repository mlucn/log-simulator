"""Tests for the schemas endpoint."""

from fastapi.testclient import TestClient


def test_schemas_endpoint_success(client: TestClient):
    """Test that schemas endpoint returns 200 OK."""
    response = client.get("/api/v1/schemas")

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"


def test_schemas_endpoint_returns_dict(client: TestClient):
    """Test that schemas endpoint returns schema data."""
    response = client.get("/api/v1/schemas")
    data = response.json()

    assert isinstance(data, dict)
    assert "schemas" in data
    assert "total_count" in data
    assert isinstance(data["schemas"], dict)
    assert data["total_count"] > 0  # Should have at least one schema


def test_schemas_endpoint_schema_structure(client: TestClient):
    """Test that schemas are organized by category."""
    response = client.get("/api/v1/schemas")
    data = response.json()

    schemas = data["schemas"]

    # Check that categories exist
    assert isinstance(schemas, dict)
    assert len(schemas) > 0

    # Check structure of each category
    for category, schema_list in schemas.items():
        assert isinstance(category, str)
        assert isinstance(schema_list, list)
        assert len(schema_list) > 0

        # Each schema should be a string path
        for schema_name in schema_list:
            assert isinstance(schema_name, str)
            assert "/" in schema_name  # Should be in format category/name


def test_schemas_endpoint_has_expected_schemas(client: TestClient):
    """Test that endpoint returns known schemas."""
    response = client.get("/api/v1/schemas")
    data = response.json()

    # Flatten all schemas from all categories
    all_schemas = []
    for category_schemas in data["schemas"].values():
        all_schemas.extend(category_schemas)

    # Check for at least some expected schemas
    expected_schemas = [
        "cloud_identity/google_workspace",
        "security/crowdstrike_fdr",
        "web_servers/nginx_access",
    ]

    for expected in expected_schemas:
        assert expected in all_schemas, f"Schema {expected} not found in response"


def test_schemas_endpoint_total_count(client: TestClient):
    """Test that total_count matches actual number of schemas."""
    response = client.get("/api/v1/schemas")
    data = response.json()

    # Count total schemas
    total = sum(len(schemas) for schemas in data["schemas"].values())

    assert data["total_count"] == total


def test_schemas_endpoint_no_authentication(client: TestClient):
    """Test that schemas endpoint doesn't require authentication."""
    response = client.get("/api/v1/schemas")
    assert response.status_code == 200


def test_schemas_endpoint_get_only(client: TestClient):
    """Test that schemas endpoint only accepts GET."""
    # POST should not be allowed
    response = client.post("/api/v1/schemas")
    assert response.status_code == 405

    # PUT should not be allowed
    response = client.put("/api/v1/schemas")
    assert response.status_code == 405

    # DELETE should not be allowed
    response = client.delete("/api/v1/schemas")
    assert response.status_code == 405


def test_schemas_endpoint_consistent_results(client: TestClient):
    """Test that schemas endpoint returns consistent results."""
    # Make two requests
    response1 = client.get("/api/v1/schemas")
    response2 = client.get("/api/v1/schemas")

    assert response1.status_code == 200
    assert response2.status_code == 200

    # Results should be identical
    assert response1.json() == response2.json()


def test_schemas_endpoint_specific_schema_info(client: TestClient):
    """Test getting info about a specific schema."""
    # This tests the detail endpoint for a single schema
    response = client.get("/api/v1/schemas/cloud_identity/google_workspace")

    assert response.status_code == 200
    data = response.json()

    # Check schema info structure
    assert "schema_name" in data
    assert "log_type" in data
    assert "description" in data
    assert "available_scenarios" in data
    assert data["schema_name"] == "cloud_identity/google_workspace"
    assert isinstance(data["available_scenarios"], list)
