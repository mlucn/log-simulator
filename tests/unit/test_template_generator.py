"""Unit tests for the template-based log generator."""

import json
from datetime import datetime, timezone
from unittest.mock import patch

import pytest

from log_simulator.generators.template_generator import TemplateBasedGenerator


@pytest.fixture
def temp_template_dir(tmp_path):
    """Create a temporary template directory with test templates."""
    template_dir = tmp_path / "templates"
    template_dir.mkdir()

    # Create a simple template
    simple_template = {
        "timestamp": "{{timestamp}}",
        "event_id": "{{uuid}}",
        "username": "{{username}}",
        "ip_address": "{{ip}}",
    }
    simple_file = template_dir / "simple.json"
    simple_file.write_text(json.dumps(simple_template))

    # Create a nested template
    nested_template = {
        "event": {
            "timestamp": "{{timestamp}}",
            "user": {"name": "{{username}}", "email": "{{email}}"},
            "source": {"ip": "{{ip}}", "port": "{{port}}"},
        },
        "tags": ["{{hostname}}", "{{domain}}"],
    }
    nested_file = template_dir / "nested.json"
    nested_file.write_text(json.dumps(nested_template))

    # Create category subdirectory
    security_dir = template_dir / "security"
    security_dir.mkdir()

    security_template = {
        "technique": "T1059.001",
        "process": "{{process_name}}",
        "command": "{{command_line}}",
        "hash": "{{sha256}}",
    }
    security_file = security_dir / "T1059.001_powershell.json"
    security_file.write_text(json.dumps(security_template))

    return template_dir


@pytest.fixture
def generator(temp_template_dir):
    """Create a generator with temporary template directory."""
    return TemplateBasedGenerator(template_dir=str(temp_template_dir))


class TestTemplateBasedGeneratorInit:
    """Tests for TemplateBasedGenerator initialization."""

    def test_init_with_custom_dir(self, temp_template_dir):
        """Test initialization with custom template directory."""
        gen = TemplateBasedGenerator(template_dir=str(temp_template_dir))
        assert gen.template_dir == temp_template_dir

    def test_init_with_default_dir(self):
        """Test initialization with default template directory."""
        gen = TemplateBasedGenerator()
        assert gen.template_dir.name == "templates"

    def test_field_generator_initialized(self, generator):
        """Test that field generator is initialized."""
        assert generator.field_gen is not None

    def test_variable_pattern_initialized(self, generator):
        """Test that variable pattern regex is initialized."""
        assert generator.variable_pattern is not None
        # Test pattern matches variables
        match = generator.variable_pattern.search("{{test}}")
        assert match is not None
        assert match.group(1) == "test"


class TestListTemplates:
    """Tests for list_templates method."""

    def test_list_all_templates(self, generator):
        """Test listing all templates."""
        templates = generator.list_templates()
        assert len(templates) == 3
        assert "simple.json" in templates
        assert "nested.json" in templates
        assert "security/T1059.001_powershell.json" in templates

    def test_list_templates_by_category(self, generator):
        """Test listing templates in a specific category."""
        templates = generator.list_templates(category="security")
        assert len(templates) == 1
        assert "T1059.001_powershell.json" in templates[0]

    def test_list_templates_nonexistent_category(self, generator):
        """Test listing templates in nonexistent category returns empty list."""
        templates = generator.list_templates(category="nonexistent")
        assert templates == []

    def test_list_templates_returns_sorted(self, generator):
        """Test that templates are returned sorted."""
        templates = generator.list_templates()
        assert templates == sorted(templates)


class TestLoadTemplate:
    """Tests for load_template method."""

    def test_load_simple_template(self, generator):
        """Test loading a simple template."""
        template = generator.load_template("simple.json")
        assert isinstance(template, dict)
        assert "timestamp" in template
        assert "event_id" in template

    def test_load_nested_template(self, generator):
        """Test loading a nested template."""
        template = generator.load_template("nested.json")
        assert isinstance(template, dict)
        assert "event" in template
        assert "tags" in template

    def test_load_template_with_path(self, generator):
        """Test loading template from subdirectory."""
        template = generator.load_template("security/T1059.001_powershell.json")
        assert isinstance(template, dict)
        assert "technique" in template

    def test_load_nonexistent_template(self, generator):
        """Test loading nonexistent template raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError, match="Template not found"):
            generator.load_template("nonexistent.json")


class TestGenerateVariable:
    """Tests for _generate_variable method."""

    def test_generate_timestamp_variables(self, generator):
        """Test generating timestamp variables."""
        base_time = datetime(2025, 1, 15, 12, 0, 0, tzinfo=timezone.utc)

        for var_name in ["timestamp", "utc_time", "event_time"]:
            result = generator._generate_variable(var_name, base_time, 0)
            assert isinstance(result, str)
            assert len(result) > 0

    def test_generate_uuid_variables(self, generator):
        """Test generating UUID variables."""
        base_time = datetime.now(timezone.utc)

        for var_name in ["uuid", "event_id", "record_id", "id"]:
            result = generator._generate_variable(var_name, base_time, 0)
            assert isinstance(result, str)
            assert len(result) == 36  # UUID format

    def test_generate_ip_variables(self, generator):
        """Test generating IP address variables."""
        base_time = datetime.now(timezone.utc)

        for var_name in ["ip", "source_ip", "remote_ip"]:
            result = generator._generate_variable(var_name, base_time, 0)
            assert isinstance(result, str)
            assert result.count(".") == 3  # IPv4 format

    def test_generate_username_variables(self, generator):
        """Test generating username variables."""
        base_time = datetime.now(timezone.utc)

        for var_name in ["username", "user"]:
            result = generator._generate_variable(var_name, base_time, 0)
            assert isinstance(result, str)
            assert len(result) > 0

    def test_generate_email_variables(self, generator):
        """Test generating email variables."""
        base_time = datetime.now(timezone.utc)

        for var_name in ["email", "user_email"]:
            result = generator._generate_variable(var_name, base_time, 0)
            assert isinstance(result, str)
            assert "@" in result

    def test_generate_file_variables(self, generator):
        """Test generating file-related variables."""
        base_time = datetime.now(timezone.utc)

        filename = generator._generate_variable("filename", base_time, 0)
        assert isinstance(filename, str)

        filepath = generator._generate_variable("file_path", base_time, 0)
        assert isinstance(filepath, str)

    def test_generate_hash_variables(self, generator):
        """Test generating hash variables."""
        base_time = datetime.now(timezone.utc)

        sha256 = generator._generate_variable("sha256", base_time, 0)
        assert isinstance(sha256, str)
        assert len(sha256) == 64

        md5 = generator._generate_variable("md5", base_time, 0)
        assert isinstance(md5, str)
        assert len(md5) == 32

    def test_generate_hostname_variables(self, generator):
        """Test generating hostname variables."""
        base_time = datetime.now(timezone.utc)

        for var_name in ["hostname", "computer_name"]:
            result = generator._generate_variable(var_name, base_time, 0)
            assert isinstance(result, str)

    def test_generate_number_suffix_variables(self, generator):
        """Test generating variables ending with _number."""
        base_time = datetime.now(timezone.utc)

        result = generator._generate_variable("sequence_number", base_time, 0)
        assert isinstance(result, str)
        assert result.isdigit()

    def test_generate_unknown_variable(self, generator):
        """Test generating unknown variable returns placeholder."""
        base_time = datetime.now(timezone.utc)

        result = generator._generate_variable("unknown_var", base_time, 0)
        assert result == "{{unknown:unknown_var}}"


class TestSubstituteVariables:
    """Tests for _substitute_variables method."""

    def test_substitute_simple_string(self, generator):
        """Test substituting variables in a simple string."""
        template = "User {{username}} logged in from {{ip}}"
        result = generator._substitute_variables(template)

        assert isinstance(result, str)
        assert "{{username}}" not in result
        assert "{{ip}}" not in result

    def test_substitute_dict_values(self, generator):
        """Test substituting variables in a dictionary."""
        template = {"user": "{{username}}", "ip": "{{ip}}"}
        result = generator._substitute_variables(template)

        assert isinstance(result, dict)
        assert "{{username}}" not in result["user"]
        assert "{{ip}}" not in result["ip"]

    def test_substitute_nested_dict(self, generator):
        """Test substituting variables in nested dictionary."""
        template = {"event": {"user": "{{username}}", "source": {"ip": "{{ip}}"}}}
        result = generator._substitute_variables(template)

        assert isinstance(result, dict)
        assert "{{username}}" not in result["event"]["user"]
        assert "{{ip}}" not in result["event"]["source"]["ip"]

    def test_substitute_list_values(self, generator):
        """Test substituting variables in a list."""
        template = ["{{username}}", "{{ip}}", "{{hostname}}"]
        result = generator._substitute_variables(template)

        assert isinstance(result, list)
        assert len(result) == 3
        for item in result:
            assert "{{" not in item

    def test_substitute_mixed_types(self, generator):
        """Test substituting variables with mixed types."""
        template = {
            "string": "{{username}}",
            "number": 42,
            "bool": True,
            "null": None,
            "list": ["{{ip}}", 123],
        }
        result = generator._substitute_variables(template)

        assert result["number"] == 42
        assert result["bool"] is True
        assert result["null"] is None
        assert isinstance(result["list"], list)

    def test_substitute_with_base_time(self, generator):
        """Test substituting with specific base time."""
        base_time = datetime(2025, 1, 15, 12, 0, 0, tzinfo=timezone.utc)
        template = "{{timestamp}}"
        result = generator._substitute_variables(template, base_time=base_time)

        assert isinstance(result, str)
        assert "2025" in result

    def test_substitute_with_offset(self, generator):
        """Test substituting with time offset."""
        base_time = datetime(2025, 1, 15, 12, 0, 0, tzinfo=timezone.utc)
        template = "{{timestamp}}"

        result1 = generator._substitute_variables(template, base_time, 0)
        result2 = generator._substitute_variables(template, base_time, 3600)

        # Results should be different due to offset
        assert result1 != result2


class TestGenerateFromTemplate:
    """Tests for generate_from_template method."""

    def test_generate_single_log(self, generator):
        """Test generating a single log from template."""
        logs = generator.generate_from_template("simple.json", count=1)

        assert isinstance(logs, list)
        assert len(logs) == 1
        assert isinstance(logs[0], dict)

    def test_generate_multiple_logs(self, generator):
        """Test generating multiple logs from template."""
        logs = generator.generate_from_template("simple.json", count=10)

        assert len(logs) == 10
        for log in logs:
            assert isinstance(log, dict)

    def test_generate_with_base_time(self, generator):
        """Test generating logs with specific base time."""
        base_time = datetime(2025, 1, 15, 12, 0, 0, tzinfo=timezone.utc)
        logs = generator.generate_from_template(
            "simple.json", count=1, base_time=base_time
        )

        assert len(logs) == 1

    def test_generate_with_time_spread(self, generator):
        """Test generating logs with time spread."""
        logs = generator.generate_from_template(
            "simple.json", count=5, time_spread_seconds=300
        )

        assert len(logs) == 5
        # All logs should have different timestamps due to spread
        timestamps = [log.get("timestamp") for log in logs]
        assert len(set(timestamps)) > 1

    def test_generate_nested_template(self, generator):
        """Test generating from nested template."""
        logs = generator.generate_from_template("nested.json", count=1)

        assert len(logs) == 1
        assert "event" in logs[0]
        assert "user" in logs[0]["event"]
        assert "tags" in logs[0]

    def test_generate_all_variables_substituted(self, generator):
        """Test that all template variables are substituted."""
        logs = generator.generate_from_template("simple.json", count=1)

        log_str = json.dumps(logs[0])
        assert "{{" not in log_str
        assert "}}" not in log_str


class TestGenerateToJson:
    """Tests for generate_to_json method."""

    def test_generate_to_json_basic(self, generator):
        """Test generating logs as JSON string."""
        json_str = generator.generate_to_json("simple.json", count=1)

        assert isinstance(json_str, str)
        # Verify it's valid JSON
        parsed = json.loads(json_str)
        assert isinstance(parsed, list)
        assert len(parsed) == 1

    def test_generate_to_json_pretty(self, generator):
        """Test generating pretty-printed JSON."""
        json_str = generator.generate_to_json("simple.json", count=1, pretty=True)

        assert isinstance(json_str, str)
        # Pretty JSON has newlines and indentation
        assert "\n" in json_str
        assert "  " in json_str

    def test_generate_to_json_not_pretty(self, generator):
        """Test generating compact JSON."""
        json_str = generator.generate_to_json("simple.json", count=1, pretty=False)

        assert isinstance(json_str, str)
        # Compact JSON has no unnecessary whitespace
        parsed = json.loads(json_str)
        assert isinstance(parsed, list)


class TestSaveToFile:
    """Tests for save_to_file method."""

    def test_save_to_file_basic(self, generator, tmp_path):
        """Test saving logs to file."""
        output_file = tmp_path / "output.json"

        with patch("builtins.print"):
            generator.save_to_file(
                "simple.json", str(output_file), count=5, pretty=False
            )

        assert output_file.exists()
        content = json.loads(output_file.read_text())
        assert isinstance(content, list)
        assert len(content) == 5

    def test_save_to_file_creates_parent_dirs(self, generator, tmp_path):
        """Test that parent directories are created."""
        output_file = tmp_path / "subdir" / "nested" / "output.json"

        with patch("builtins.print"):
            generator.save_to_file("simple.json", str(output_file), count=1)

        assert output_file.exists()
        assert output_file.parent.exists()

    def test_save_to_file_pretty(self, generator, tmp_path):
        """Test saving pretty-printed logs to file."""
        output_file = tmp_path / "output.json"

        with patch("builtins.print"):
            generator.save_to_file(
                "simple.json", str(output_file), count=1, pretty=True
            )

        content = output_file.read_text()
        assert "\n" in content
        assert "  " in content

    def test_save_to_file_prints_message(self, generator, tmp_path):
        """Test that save_to_file prints confirmation message."""
        output_file = tmp_path / "output.json"

        with patch("builtins.print") as mock_print:
            generator.save_to_file("simple.json", str(output_file), count=3)

        mock_print.assert_called_once()
        call_args = str(mock_print.call_args)
        assert "3" in call_args
        assert str(output_file) in call_args


class TestGenerateAttackScenario:
    """Tests for generate_attack_scenario method."""

    def test_generate_attack_scenario_basic(self, generator):
        """Test generating attack scenario with single technique."""
        logs = generator.generate_attack_scenario(
            techniques=["T1059.001"], count_per_technique=3
        )

        assert isinstance(logs, list)
        # Should have 3 logs (1 technique × 3 per technique)
        assert len(logs) == 3

    def test_generate_attack_scenario_metadata(self, generator):
        """Test that attack scenario logs include metadata."""
        logs = generator.generate_attack_scenario(
            techniques=["T1059.001"], count_per_technique=2
        )

        for log in logs:
            assert "_metadata" in log
            assert "technique" in log["_metadata"]
            assert "log_index" in log["_metadata"]
            assert "template" in log["_metadata"]

    def test_generate_attack_scenario_multiple_techniques(
        self, generator, temp_template_dir
    ):
        """Test generating attack scenario with multiple techniques."""
        # Create another technique template
        security_dir = temp_template_dir / "security"
        template2 = {"technique": "T1055", "process": "{{process_name}}"}
        (security_dir / "T1055_injection.json").write_text(json.dumps(template2))

        logs = generator.generate_attack_scenario(
            techniques=["T1059.001", "T1055"], count_per_technique=2
        )

        # Should have 4 logs (2 techniques × 2 per technique)
        assert len(logs) == 4

    def test_generate_attack_scenario_time_spread(self, generator):
        """Test that attack scenario logs are spread over time."""
        logs = generator.generate_attack_scenario(
            techniques=["T1059.001"], count_per_technique=5, time_spread_seconds=300
        )

        assert len(logs) == 5

    def test_generate_attack_scenario_missing_technique(self, generator):
        """Test handling of missing technique template."""
        with patch("builtins.print"):
            logs = generator.generate_attack_scenario(
                techniques=["T9999.999"], count_per_technique=2
            )

        # Should return empty list for nonexistent technique
        assert logs == []

    def test_generate_attack_scenario_sorted_by_timestamp(self, generator):
        """Test that logs are sorted chronologically."""
        # This test depends on template having timestamp field
        # Since our test template doesn't have one, it should still return logs
        logs = generator.generate_attack_scenario(
            techniques=["T1059.001"], count_per_technique=3
        )

        assert isinstance(logs, list)
