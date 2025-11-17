"""Tests for CLI basic functionality and argument parsing."""

from io import StringIO
from unittest.mock import patch

import pytest

from log_simulator.cli import (
    find_schema_path,
    list_schemas,
    main,
    print_schemas,
)


def test_list_schemas_returns_dict():
    """Test that list_schemas returns a dictionary."""
    schemas = list_schemas()

    assert isinstance(schemas, dict)
    assert len(schemas) > 0


def test_list_schemas_has_expected_categories():
    """Test that list_schemas contains expected categories."""
    schemas = list_schemas()

    # Should have at least some of these categories
    expected_categories = ["cloud_identity", "security", "web_servers"]

    found_categories = [cat for cat in expected_categories if cat in schemas]
    assert len(found_categories) > 0, "Should find at least one expected category"


def test_list_schemas_category_structure():
    """Test that each category has a list of schema names."""
    schemas = list_schemas()

    for category, schema_list in schemas.items():
        assert isinstance(category, str)
        assert isinstance(schema_list, list)
        assert len(schema_list) > 0

        # Each schema should be a string
        for schema_name in schema_list:
            assert isinstance(schema_name, str)
            assert len(schema_name) > 0


def test_find_schema_path_with_full_path():
    """Test finding schema with full category/schema path."""
    path = find_schema_path("cloud_identity/google_workspace")

    assert path is not None
    assert path.exists()
    assert path.suffix == ".yaml"
    assert "google_workspace" in path.name


def test_find_schema_path_with_short_name():
    """Test finding schema with just the schema name."""
    path = find_schema_path("google_workspace")

    assert path is not None
    assert path.exists()
    assert path.suffix == ".yaml"


def test_find_schema_path_nonexistent():
    """Test finding nonexistent schema returns None."""
    path = find_schema_path("nonexistent_schema_xyz123")

    assert path is None


def test_print_schemas_output():
    """Test that print_schemas produces output."""
    output = StringIO()

    with patch("sys.stdout", output):
        print_schemas()

    result = output.getvalue()

    assert len(result) > 0
    assert "Available Schemas" in result
    assert "=" * 70 in result  # Should have separator lines


def test_print_schemas_contains_known_schemas():
    """Test that print_schemas output contains known schemas."""
    output = StringIO()

    with patch("sys.stdout", output):
        print_schemas()

    result = output.getvalue()

    # Should contain at least some known schemas
    known_schemas = ["google_workspace", "azure_ad_signin", "nginx_access"]

    found = [schema for schema in known_schemas if schema in result]
    assert len(found) > 0, "Should find at least one known schema in output"


def test_main_with_list_flag():
    """Test main() with --list flag."""
    output = StringIO()

    with patch("sys.argv", ["log-simulator", "--list"]):
        with patch("sys.stdout", output):
            exit_code = main()

    assert exit_code == 0
    result = output.getvalue()
    assert "Available Schemas" in result


def test_main_with_no_args_shows_error():
    """Test main() with no arguments shows error."""
    with patch("sys.argv", ["log-simulator"]):
        with patch("sys.stderr", StringIO()):
            with pytest.raises(SystemExit) as exc_info:
                main()

            assert exc_info.value.code == 2  # argparse error code


def test_main_with_nonexistent_schema():
    """Test main() with nonexistent schema."""
    output = StringIO()

    with patch("sys.argv", ["log-simulator", "nonexistent_xyz"]):
        with patch("sys.stderr", output):
            exit_code = main()

    assert exit_code == 1
    result = output.getvalue()
    assert "not found" in result.lower()


def test_main_generate_single_log():
    """Test generating a single log entry."""
    output = StringIO()

    with patch("sys.argv", ["log-simulator", "google_workspace"]):
        with patch("sys.stdout", output):
            exit_code = main()

    assert exit_code == 0
    result = output.getvalue()

    # Should output JSON
    assert len(result) > 0
    assert "{" in result or "[" in result  # JSON output


def test_main_generate_with_count():
    """Test generating multiple logs with --count."""
    output = StringIO()

    with patch("sys.argv", ["log-simulator", "google_workspace", "-n", "5"]):
        with patch("sys.stdout", output):
            exit_code = main()

    assert exit_code == 0
    result = output.getvalue()

    # Parse JSON to verify count
    import json

    logs = json.loads(result)
    assert len(logs) == 5


def test_main_generate_with_pretty_output():
    """Test generating logs with --pretty flag."""
    output = StringIO()

    with patch(
        "sys.argv", ["log-simulator", "google_workspace", "-n", "2", "--pretty"]
    ):
        with patch("sys.stdout", output):
            exit_code = main()

    assert exit_code == 0
    result = output.getvalue()

    # Pretty-printed JSON should have indentation
    assert "\n  " in result or "\n    " in result


def test_main_generate_with_output_file(tmp_path):
    """Test generating logs to output file."""
    output_file = tmp_path / "test_output.json"
    stderr_output = StringIO()

    with patch(
        "sys.argv",
        ["log-simulator", "google_workspace", "-n", "3", "-o", str(output_file)],
    ):
        with patch("sys.stderr", stderr_output):
            exit_code = main()

    assert exit_code == 0
    assert output_file.exists()

    # Verify file contents
    import json

    logs = json.loads(output_file.read_text())
    assert len(logs) == 3

    # Verify message to stderr
    stderr_result = stderr_output.getvalue()
    assert "Generated 3 log(s)" in stderr_result


def test_main_generate_with_scenario():
    """Test generating logs with specific scenario."""
    output = StringIO()

    with patch(
        "sys.argv", ["log-simulator", "google_workspace", "-s", "user_login_success"]
    ):
        with patch("sys.stdout", output):
            exit_code = main()

    assert exit_code == 0
    result = output.getvalue()

    # Should generate successfully
    assert len(result) > 0


def test_main_generate_with_invalid_scenario():
    """Test generating logs with invalid scenario."""
    output = StringIO()

    with patch(
        "sys.argv", ["log-simulator", "google_workspace", "-s", "invalid_scenario_xyz"]
    ):
        with patch("sys.stderr", output):
            exit_code = main()

    assert exit_code == 1
    result = output.getvalue()
    assert "scenario" in result.lower()
    assert "not found" in result.lower()


def test_main_generate_with_spread():
    """Test generating logs with time spread."""
    output = StringIO()

    with patch(
        "sys.argv", ["log-simulator", "google_workspace", "-n", "5", "--spread", "3600"]
    ):
        with patch("sys.stdout", output):
            exit_code = main()

    assert exit_code == 0
    result = output.getvalue()

    # Should generate successfully
    import json

    logs = json.loads(result)
    assert len(logs) == 5


def test_main_list_scenarios():
    """Test --list-scenarios flag."""
    output = StringIO()

    with patch("sys.argv", ["log-simulator", "google_workspace", "--list-scenarios"]):
        with patch("sys.stdout", output):
            exit_code = main()

    assert exit_code == 0
    result = output.getvalue()

    assert "Available scenarios" in result
    assert "user_login_success" in result


def test_main_show_info():
    """Test --info flag."""
    output = StringIO()

    with patch("sys.argv", ["log-simulator", "google_workspace", "--info"]):
        with patch("sys.stdout", output):
            exit_code = main()

    assert exit_code == 0
    result = output.getvalue()

    assert "Schema Information" in result
    assert "Log Type" in result
    assert "Description" in result


def test_main_output_file_creates_parent_dirs(tmp_path):
    """Test that output file creation creates parent directories."""
    output_file = tmp_path / "subdir" / "nested" / "output.json"
    stderr_output = StringIO()

    with patch(
        "sys.argv", ["log-simulator", "google_workspace", "-o", str(output_file)]
    ):
        with patch("sys.stderr", stderr_output):
            exit_code = main()

    assert exit_code == 0
    assert output_file.exists()
    assert output_file.parent.exists()


def test_main_with_full_schema_path():
    """Test using full category/schema path."""
    output = StringIO()

    with patch("sys.argv", ["log-simulator", "cloud_identity/google_workspace"]):
        with patch("sys.stdout", output):
            exit_code = main()

    assert exit_code == 0
    result = output.getvalue()

    # Should generate successfully
    import json

    logs = json.loads(result)
    assert len(logs) == 1
