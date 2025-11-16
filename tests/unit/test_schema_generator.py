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
            Path(__file__).parent.parent.parent /
            'src' / 'log_simulator' / 'schemas' /
            'cloud_identity' / 'google_workspace.yaml'
        )
        return str(schema_path)

    @pytest.fixture
    def generator(self, google_workspace_schema):
        """Create a generator instance."""
        return SchemaBasedGenerator(google_workspace_schema)

    def test_load_schema(self, generator):
        """Test schema loading."""
        assert generator.schema is not None
        assert 'log_type' in generator.schema
        assert generator.schema['log_type'] == 'google_workspace_audit'

    def test_get_schema_info(self, generator):
        """Test getting schema information."""
        info = generator.get_schema_info()
        assert info['log_type'] == 'google_workspace_audit'
        assert 'description' in info
        assert 'available_scenarios' in info
        assert len(info['available_scenarios']) > 0

    def test_list_scenarios(self, generator):
        """Test listing scenarios."""
        scenarios = generator.list_scenarios()
        assert isinstance(scenarios, list)
        assert 'user_login_success' in scenarios
        assert 'user_login_failure' in scenarios

    def test_generate_single_log(self, generator):
        """Test generating a single log."""
        logs = generator.generate(count=1)
        assert len(logs) == 1
        log = logs[0]

        # Check required fields
        assert 'kind' in log
        assert 'id' in log
        assert 'actor' in log
        assert 'ipAddress' in log
        assert 'events' in log

    def test_generate_multiple_logs(self, generator):
        """Test generating multiple logs."""
        logs = generator.generate(count=5)
        assert len(logs) == 5

        # Each log should be unique
        ids = [log['id']['uniqueQualifier'] for log in logs]
        assert len(set(ids)) == 5

    def test_generate_with_scenario(self, generator):
        """Test generating logs with a scenario."""
        logs = generator.generate(count=1, scenario='user_login_success')
        assert len(logs) == 1
        log = logs[0]

        # Check scenario-specific fields
        assert log['id']['applicationName'] == 'login'
        assert log['events'][0]['type'] == 'login'
        assert log['events'][0]['name'] == 'login_success'

    def test_generate_with_invalid_scenario(self, generator):
        """Test generating with invalid scenario raises error."""
        with pytest.raises(ValueError, match="Scenario .* not found"):
            generator.generate(count=1, scenario='nonexistent_scenario')

    def test_generate_to_json(self, generator):
        """Test generating logs as JSON string."""
        json_str = generator.generate_to_json(count=2)
        assert isinstance(json_str, str)
        assert json_str.startswith('[')
        assert json_str.endswith(']')

    def test_generate_to_json_pretty(self, generator):
        """Test generating pretty-printed JSON."""
        json_str = generator.generate_to_json(count=1, pretty=True)
        assert isinstance(json_str, str)
        # Pretty-printed JSON should have newlines
        assert '\n' in json_str

    def test_time_spread(self, generator):
        """Test generating logs with time spread."""
        logs = generator.generate(count=3, time_spread_seconds=60)
        assert len(logs) == 3

        # Timestamps should be different
        timestamps = [log['id']['time'] for log in logs]
        assert len(set(timestamps)) >= 2  # At least 2 different timestamps
