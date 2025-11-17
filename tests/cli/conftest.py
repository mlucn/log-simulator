"""Pytest fixtures for CLI tests."""

import sys

import pytest


@pytest.fixture
def temp_output_file(tmp_path):
    """Create a temporary output file path."""
    return tmp_path / "output.json"


@pytest.fixture
def mock_argv():
    """Context manager to mock sys.argv for CLI tests."""

    class MockArgv:
        def __init__(self):
            self.original_argv = None

        def __enter__(self):
            self.original_argv = sys.argv.copy()
            return self

        def __exit__(self, *args):
            sys.argv = self.original_argv

        def set(self, args):
            """Set sys.argv to given args."""
            sys.argv = ["log-simulator"] + args

    return MockArgv()


@pytest.fixture
def sample_schema_name():
    """Sample schema name that exists."""
    return "google_workspace"


@pytest.fixture
def sample_full_schema_name():
    """Sample full schema path."""
    return "cloud_identity/google_workspace"


@pytest.fixture
def nonexistent_schema():
    """Schema name that doesn't exist."""
    return "nonexistent_schema_xyz"
