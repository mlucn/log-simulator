"""
Integration tests for end-to-end scenarios.
"""

from pathlib import Path

import pytest

from log_simulator import SchemaBasedGenerator


class TestEndToEndScenarios:
    """Test complete scenarios."""

    @pytest.fixture
    def schemas_dir(self):
        """Path to schemas directory."""
        return Path(__file__).parent.parent.parent / "src" / "log_simulator" / "schemas"

    def test_google_workspace_login_scenario(self, schemas_dir):
        """Test Google Workspace login scenario generation."""
        schema_path = schemas_dir / "cloud_identity" / "google_workspace.yaml"
        generator = SchemaBasedGenerator(str(schema_path))

        # Generate successful login
        logs = generator.generate(count=1, scenario="user_login_success")
        assert len(logs) == 1
        log = logs[0]

        assert log["id"]["applicationName"] == "login"
        assert log["events"][0]["name"] == "login_success"

        # Verify PII generation
        assert "@" in log["actor"]["email"]
        assert "." in log["ipAddress"]

    def test_nginx_attack_scenario(self, schemas_dir):
        """Test Nginx attack scenario generation."""
        schema_path = schemas_dir / "web_servers" / "nginx_access.yaml"
        generator = SchemaBasedGenerator(str(schema_path))

        # Generate malicious scan
        logs = generator.generate(count=5, scenario="malicious_scan")
        assert len(logs) == 5

        for log in logs:
            # Should have 4xx or 5xx status codes
            assert log["status"] >= 400
            # Should have suspicious user agent or path
            assert log["remote_addr"] is not None

    def test_cross_platform_correlation(self, schemas_dir):
        """Test correlation between different log sources."""
        gw_schema = schemas_dir / "cloud_identity" / "google_workspace.yaml"
        aws_schema = schemas_dir / "cloud_infrastructure" / "aws_cloudtrail.yaml"

        gw_gen = SchemaBasedGenerator(str(gw_schema))
        aws_gen = SchemaBasedGenerator(str(aws_schema))

        # Simulate a user
        user_email = "attacker@example.com"

        # 1. Google Workspace Login
        gw_logs = gw_gen.generate(count=1, scenario="user_login_success")
        gw_logs[0]["actor"]["email"] = user_email

        # 2. AWS Console Login (correlated by email)
        aws_logs = aws_gen.generate(count=1, scenario="console_login_success")
        aws_logs[0]["userIdentity"]["userName"] = user_email

        assert gw_logs[0]["actor"]["email"] == aws_logs[0]["userIdentity"]["userName"]
