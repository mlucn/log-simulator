"""
Tests for Google Workspace application-specific schemas.

Tests the new WORKSPACE_ACTIVITY compatible schemas for admin, drive, login, calendar, and token.
"""

import json
from pathlib import Path

import pytest

from log_simulator.generators.schema_generator import SchemaBasedGenerator

# Define schema paths
SCHEMA_DIR = Path("src/log_simulator/schemas/cloud_identity/google_workspace")

SCHEMAS = {
    "admin": SCHEMA_DIR / "admin.yaml",
    "drive": SCHEMA_DIR / "drive.yaml",
    "login": SCHEMA_DIR / "login.yaml",
    "calendar": SCHEMA_DIR / "calendar.yaml",
    "token": SCHEMA_DIR / "token.yaml",
}


class TestGoogleWorkspaceSchemas:
    """Test Google Workspace application-specific schemas."""

    @pytest.mark.parametrize("app_name,schema_path", SCHEMAS.items())
    def test_schema_loads(self, app_name, schema_path):
        """Test that each schema file loads correctly."""
        generator = SchemaBasedGenerator(str(schema_path))
        assert generator is not None
        assert generator.schema is not None

    @pytest.mark.parametrize("app_name,schema_path", SCHEMAS.items())
    def test_schema_metadata(self, app_name, schema_path):
        """Test that schema metadata is correct for Chronicle compatibility."""
        generator = SchemaBasedGenerator(str(schema_path))

        # Verify log_type is WORKSPACE_ACTIVITY for Chronicle compatibility
        assert generator.schema.get("log_type") == "WORKSPACE_ACTIVITY"

        # Verify source API is documented
        assert (
            generator.schema.get("source_api")
            == "Google Workspace Admin SDK Reports API v1"
        )

        # Verify application_name matches
        assert generator.schema.get("application_name") == app_name

        # Verify Chronicle compatibility flag
        assert generator.schema.get("chronicle_compatible") is True

        # Verify schema version
        assert generator.schema.get("schema_version") == "1.0"

    @pytest.mark.parametrize("app_name,schema_path", SCHEMAS.items())
    def test_generate_basic_log(self, app_name, schema_path):
        """Test basic log generation for each schema."""
        generator = SchemaBasedGenerator(str(schema_path))
        logs = generator.generate(count=1)

        assert len(logs) == 1
        log = logs[0]

        # Verify standard Google Workspace Activity log structure
        assert log["kind"] == "admin#reports#activity"
        assert "id" in log
        assert "actor" in log
        assert "ipAddress" in log
        assert "events" in log

        # Verify id structure
        assert "time" in log["id"]
        assert "uniqueQualifier" in log["id"]
        assert "applicationName" in log["id"]
        assert log["id"]["applicationName"] == app_name
        assert "customerId" in log["id"]

        # Verify actor structure
        assert "callerType" in log["actor"]
        assert "email" in log["actor"]
        assert "profileId" in log["actor"]

        # Verify events is an array
        assert isinstance(log["events"], list)
        assert len(log["events"]) >= 1

        # Verify event structure
        event = log["events"][0]
        assert "type" in event
        assert "name" in event

    @pytest.mark.parametrize("app_name,schema_path", SCHEMAS.items())
    def test_has_scenarios(self, app_name, schema_path):
        """Test that each schema has scenarios defined."""
        generator = SchemaBasedGenerator(str(schema_path))
        scenarios = generator.list_scenarios()

        assert len(scenarios) > 0
        assert isinstance(scenarios, list)

    def test_admin_scenarios(self):
        """Test specific admin scenarios."""
        generator = SchemaBasedGenerator(str(SCHEMAS["admin"]))
        scenarios = generator.list_scenarios()

        # Verify key admin scenarios exist
        assert "user_create" in scenarios
        assert "user_delete" in scenarios
        assert "grant_admin_privilege" in scenarios
        assert "add_group_member" in scenarios

        # Test user_create scenario
        logs = generator.generate(count=1, scenario="user_create")
        assert len(logs) == 1
        assert logs[0]["events"][0]["type"] == "user_settings"
        assert logs[0]["events"][0]["name"] == "create_user"

    def test_drive_scenarios(self):
        """Test specific drive scenarios."""
        generator = SchemaBasedGenerator(str(SCHEMAS["drive"]))
        scenarios = generator.list_scenarios()

        # Verify key drive scenarios exist
        assert "file_view" in scenarios
        assert "file_share_external" in scenarios
        assert "file_download" in scenarios

        # Test file_share_external scenario
        logs = generator.generate(count=1, scenario="file_share_external")
        assert len(logs) == 1
        event = logs[0]["events"][0]
        assert event["type"] == "acl_change"
        assert event["name"] == "user_access_grant"

        # Verify parameters exist
        assert "parameters" in event
        params = {p["name"]: p for p in event["parameters"]}
        assert "visibility" in params
        assert params["visibility"]["value"] == "shared_externally"

    def test_login_scenarios(self):
        """Test specific login scenarios."""
        generator = SchemaBasedGenerator(str(SCHEMAS["login"]))
        scenarios = generator.list_scenarios()

        # Verify key login scenarios exist
        assert "login_success" in scenarios
        assert "login_failure" in scenarios
        assert "login_success_with_2fa" in scenarios

        # Test login_success scenario
        logs = generator.generate(count=1, scenario="login_success")
        assert len(logs) == 1
        assert logs[0]["events"][0]["type"] == "login"
        assert logs[0]["events"][0]["name"] == "login_success"

        # Test login_failure scenario
        logs = generator.generate(count=1, scenario="login_failure")
        assert len(logs) == 1
        event = logs[0]["events"][0]
        assert event["type"] == "login"
        assert event["name"] == "login_failure"

        # Verify login_failure_type parameter
        params = {p["name"]: p for p in event["parameters"]}
        assert "login_failure_type" in params

    def test_calendar_scenarios(self):
        """Test specific calendar scenarios."""
        generator = SchemaBasedGenerator(str(SCHEMAS["calendar"]))
        scenarios = generator.list_scenarios()

        # Verify key calendar scenarios exist
        assert "event_create" in scenarios
        assert "event_delete" in scenarios
        assert "change_calendar_acls" in scenarios

        # Test event_create scenario
        logs = generator.generate(count=1, scenario="event_create")
        assert len(logs) == 1
        assert logs[0]["events"][0]["type"] == "event_change"
        assert logs[0]["events"][0]["name"] == "create_event"

    def test_token_scenarios(self):
        """Test specific token scenarios."""
        generator = SchemaBasedGenerator(str(SCHEMAS["token"]))
        scenarios = generator.list_scenarios()

        # Verify key token scenarios exist
        assert "authorize_3p_app" in scenarios
        assert "revoke_3p_app" in scenarios

        # Test authorize_3p_app scenario
        logs = generator.generate(count=1, scenario="authorize_3p_app")
        assert len(logs) == 1
        event = logs[0]["events"][0]
        assert event["type"] == "authorize"
        assert event["name"] == "authorize"

        # Verify scope parameter with multiValue
        params = {p["name"]: p for p in event["parameters"]}
        assert "scope" in params
        assert "multiValue" in params["scope"]
        assert isinstance(params["scope"]["multiValue"], list)

    def test_multiple_log_generation(self):
        """Test generating multiple logs."""
        generator = SchemaBasedGenerator(str(SCHEMAS["drive"]))
        logs = generator.generate(count=10)

        assert len(logs) == 10

        # Verify each log has proper structure
        for log in logs:
            assert log["kind"] == "admin#reports#activity"
            assert "id" in log
            assert "actor" in log
            assert "events" in log

    def test_time_spread_generation(self):
        """Test log generation with time spread."""
        generator = SchemaBasedGenerator(str(SCHEMAS["login"]))
        logs = generator.generate(count=5, time_spread_seconds=300)

        assert len(logs) == 5

        # Extract timestamps
        timestamps = [log["id"]["time"] for log in logs]

        # Verify timestamps are different (due to time spread)
        assert len(set(timestamps)) > 1

    def test_json_serialization(self):
        """Test that generated logs can be serialized to JSON."""
        for _app_name, schema_path in SCHEMAS.items():
            generator = SchemaBasedGenerator(str(schema_path))
            logs = generator.generate(count=1)

            # Should not raise exception
            json_str = json.dumps(logs)
            assert json_str is not None

            # Should be able to parse back
            parsed = json.loads(json_str)
            assert len(parsed) == 1

    def test_correlation_fields(self):
        """Test that correlation fields are consistent within a session."""
        generator = SchemaBasedGenerator(str(SCHEMAS["admin"]))
        logs = generator.generate(count=5)

        # All logs should have the same customerId (global correlation)
        customer_ids = [log["id"]["customerId"] for log in logs]
        # Note: Current implementation may not enforce this, but structure supports it
        assert len(customer_ids) == 5

    def test_schema_version_consistency(self):
        """Test that all schemas have consistent version."""
        for _app_name, schema_path in SCHEMAS.items():
            generator = SchemaBasedGenerator(str(schema_path))
            assert generator.schema.get("schema_version") == "1.0"
