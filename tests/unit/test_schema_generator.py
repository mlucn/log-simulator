"""Unit tests for schema-based generator."""

from pathlib import Path

import pytest

from log_simulator.generators.schema_generator import SchemaBasedGenerator


class TestSchemaBasedGenerator:
    """Test SchemaBasedGenerator class."""

    @pytest.fixture
    def google_workspace_schema(self):
        """Path to Google Workspace schema."""
        schema_path = (
            Path(__file__).parent.parent.parent
            / "src"
            / "log_simulator"
            / "schemas"
            / "cloud_identity"
            / "google_workspace.yaml"
        )
        return str(schema_path)

    @pytest.fixture
    def generator(self, google_workspace_schema):
        """Create a generator instance."""
        return SchemaBasedGenerator(google_workspace_schema)

    def test_load_schema(self, generator):
        """Test schema loading."""
        assert generator.schema is not None
        assert "log_type" in generator.schema
        assert generator.schema["log_type"] == "google_workspace_audit"

    def test_get_schema_info(self, generator):
        """Test getting schema information."""
        info = generator.get_schema_info()
        assert info["log_type"] == "google_workspace_audit"
        assert "description" in info
        assert "available_scenarios" in info
        assert len(info["available_scenarios"]) > 0

    def test_list_scenarios(self, generator):
        """Test listing scenarios."""
        scenarios = generator.list_scenarios()
        assert isinstance(scenarios, list)
        assert "user_login_success" in scenarios
        assert "user_login_failure" in scenarios

    def test_generate_single_log(self, generator):
        """Test generating a single log."""
        logs = generator.generate(count=1)
        assert len(logs) == 1
        log = logs[0]

        # Check required fields
        assert "kind" in log
        assert "id" in log
        assert "actor" in log
        assert "ipAddress" in log
        assert "events" in log

    def test_generate_multiple_logs(self, generator):
        """Test generating multiple logs."""
        logs = generator.generate(count=5)
        assert len(logs) == 5

        # Each log should be unique
        ids = [log["id"]["uniqueQualifier"] for log in logs]
        assert len(set(ids)) == 5

    def test_generate_with_scenario(self, generator):
        """Test generating logs with a scenario."""
        logs = generator.generate(count=1, scenario="user_login_success")
        assert len(logs) == 1
        log = logs[0]

        # Check scenario-specific fields
        assert log["id"]["applicationName"] == "login"
        assert log["events"][0]["type"] == "login"
        assert log["events"][0]["name"] == "login_success"

    def test_generate_with_invalid_scenario(self, generator):
        """Test generating with invalid scenario raises error."""
        with pytest.raises(ValueError, match="Scenario .* not found"):
            generator.generate(count=1, scenario="nonexistent_scenario")

    def test_generate_to_json(self, generator):
        """Test generating logs as JSON string."""
        json_str = generator.generate_to_json(count=2)
        assert isinstance(json_str, str)
        assert json_str.startswith("[")
        assert json_str.endswith("]")

    def test_generate_to_json_pretty(self, generator):
        """Test generating pretty-printed JSON."""
        json_str = generator.generate_to_json(count=1, pretty=True)
        assert isinstance(json_str, str)
        # Pretty-printed JSON should have newlines
        assert "\n" in json_str

    def test_time_spread(self, generator):
        """Test generating logs with time spread."""
        logs = generator.generate(count=3, time_spread_seconds=60)
        assert len(logs) == 3

        # Timestamps should be different
        timestamps = [log["id"]["time"] for log in logs]
        assert len(set(timestamps)) >= 2  # At least 2 different timestamps

    def test_generate_with_scenario_overrides(self, generator):
        """Test that scenario overrides work correctly."""
        # Test user_login_failure scenario which has specific overrides
        logs = generator.generate(count=1, scenario="user_login_failure")
        assert len(logs) == 1
        log = logs[0]

        # Verify scenario-specific values
        assert log["id"]["applicationName"] == "login"
        assert log["events"][0]["type"] == "login"
        assert log["events"][0]["name"] == "login_failure"

    def test_nested_override(self, generator):
        """Test _get_nested_override method."""
        overrides = {"ipAddress": "10.0.0.1", "status.errorCode": "UNAUTHORIZED"}

        # Test direct field override
        result = generator._get_nested_override(overrides, "ipAddress")
        assert result == "10.0.0.1"

        # Test nested field override
        result = generator._get_nested_override(overrides, "status.errorCode")
        assert result == "UNAUTHORIZED"

        # Test missing field
        result = generator._get_nested_override(overrides, "nonexistent")
        assert result is None

    def test_generate_field_with_overrides(self, google_workspace_schema):
        """Test _generate_field with overrides."""
        gen = SchemaBasedGenerator(google_workspace_schema)
        from datetime import datetime, timezone

        base_time = datetime.now(timezone.utc)

        field_spec = {"type": "string", "generator": "username"}
        overrides = {"username": "custom_user"}

        # With override
        result = gen._generate_field(
            "username", field_spec, base_time, 0, overrides, "username"
        )
        assert result == "custom_user"

    def test_boolean_field_with_distribution(self, google_workspace_schema):
        """Test generating boolean field with distribution."""
        gen = SchemaBasedGenerator(google_workspace_schema)

        field_spec = {
            "type": "boolean",
            "distribution": {True: 1.0, False: 0.0},  # Always true
        }

        result = gen._generate_boolean_field(field_spec)
        assert result is True

    def test_boolean_field_without_distribution(self, google_workspace_schema):
        """Test generating boolean field without distribution."""
        gen = SchemaBasedGenerator(google_workspace_schema)

        field_spec = {"type": "boolean"}
        result = gen._generate_boolean_field(field_spec)
        assert isinstance(result, bool)

    def test_enum_field_empty_values(self, google_workspace_schema):
        """Test generating enum field with empty values list."""
        gen = SchemaBasedGenerator(google_workspace_schema)

        field_spec = {"type": "enum", "values": [], "default": "default_value"}

        result = gen._generate_enum_field(field_spec)
        assert result == "default_value"

    def test_object_field_generation(self, google_workspace_schema):
        """Test _generate_object_field method."""
        gen = SchemaBasedGenerator(google_workspace_schema)
        from datetime import datetime, timezone

        base_time = datetime.now(timezone.utc)

        field_spec = {
            "type": "object",
            "fields": {
                "name": {"type": "string", "generator": "username"},
                "email": {"type": "string", "generator": "email"},
            },
        }

        result = gen._generate_object_field(field_spec, base_time, 0)
        assert isinstance(result, dict)
        assert "name" in result
        assert "email" in result

    def test_field_generator_coverage(self, google_workspace_schema):
        """Test various field generator calls."""
        gen = SchemaBasedGenerator(google_workspace_schema)
        from datetime import datetime, timezone

        base_time = datetime.now(timezone.utc)

        generators_to_test = [
            "uuid",
            "full_name",
            "username",
            "user_agent",
            "uri_path",
            "city",
            "state",
            "country_code",
            "device_name",
            "email_subject",
            "filename",
            "referer",
            "process_name",
            "command_line",
            "sha256",
            "md5",
            "domain_name",
            "file_path",
            "detection_name",
            "registry_key",
            "aws_user_agent",
            "aws_principal_id",
            "aws_arn",
            "aws_account_id",
            "aws_resource_arn",
            "gcp_project_id",
            "gcp_resource_name",
            "sysmon_guid",
            "windows_image_path",
            "windows_user",
            "sysmon_hashes",
        ]

        for generator in generators_to_test:
            field_spec = {"type": "string", "generator": generator, "required": True}
            result = gen._generate_field(f"test_{generator}", field_spec, base_time, 0)
            assert result is not None
            assert isinstance(result, str)
