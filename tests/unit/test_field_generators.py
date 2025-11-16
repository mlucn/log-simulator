"""Unit tests for field generators."""

import re
from datetime import datetime

import pytest

from log_simulator.utils.field_generators import FieldGenerator


class TestFieldGenerator:
    """Test FieldGenerator class."""

    def test_uuid4(self):
        """Test UUID generation."""
        uuid = FieldGenerator.uuid4()
        assert isinstance(uuid, str)
        assert len(uuid) == 36
        # UUID format: 8-4-4-4-12
        assert re.match(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', uuid)

    def test_datetime_iso8601(self):
        """Test ISO 8601 timestamp generation."""
        timestamp = FieldGenerator.datetime_iso8601()
        assert isinstance(timestamp, str)
        # Check format: YYYY-MM-DDTHH:MM:SS.sssZ
        assert re.match(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z$', timestamp)

    def test_datetime_iso8601_with_offset(self):
        """Test ISO 8601 timestamp with offset."""
        base_time = datetime(2025, 1, 1, 12, 0, 0)
        timestamp = FieldGenerator.datetime_iso8601(base_time, offset_seconds=60)
        assert '2025-01-01T12:01:00' in timestamp

    def test_ipv4(self):
        """Test IPv4 address generation."""
        ip = FieldGenerator.ipv4()
        assert isinstance(ip, str)
        parts = ip.split('.')
        assert len(parts) == 4
        for part in parts:
            assert 0 <= int(part) <= 255

    def test_ipv4_internal(self):
        """Test internal IPv4 address generation."""
        ip = FieldGenerator.ipv4(internal=True)
        assert isinstance(ip, str)
        # Should be in private ranges
        assert (ip.startswith('10.') or
                ip.startswith('192.168.') or
                (ip.startswith('172.') and 16 <= int(ip.split('.')[1]) <= 31))

    def test_email(self):
        """Test email generation."""
        email = FieldGenerator.email()
        assert isinstance(email, str)
        assert '@' in email
        parts = email.split('@')
        assert len(parts) == 2
        assert len(parts[0]) > 0  # username
        assert '.' in parts[1]     # domain with TLD

    def test_email_custom_domain(self):
        """Test email with custom domain."""
        email = FieldGenerator.email(domain='test.com')
        assert email.endswith('@test.com')

    def test_full_name(self):
        """Test full name generation."""
        name = FieldGenerator.full_name()
        assert isinstance(name, str)
        parts = name.split(' ')
        assert len(parts) >= 2  # First and last name

    def test_username(self):
        """Test username generation."""
        username = FieldGenerator.username()
        assert isinstance(username, str)
        assert len(username) > 3

    def test_number_string(self):
        """Test number string generation."""
        num_str = FieldGenerator.number_string(length=10)
        assert isinstance(num_str, str)
        assert len(num_str) == 10
        assert num_str.isdigit()

    def test_custom_id(self):
        """Test custom ID generation."""
        custom_id = FieldGenerator.custom_id(prefix='TEST', length=8)
        assert custom_id.startswith('TEST')
        assert len(custom_id) == 12  # prefix + 8 chars

    def test_user_agent(self):
        """Test user agent generation."""
        ua = FieldGenerator.user_agent()
        assert isinstance(ua, str)
        assert len(ua) > 10
        assert 'Mozilla' in ua or 'Chrome' in ua or 'Safari' in ua or 'Firefox' in ua

    def test_uri_path(self):
        """Test URI path generation."""
        path = FieldGenerator.uri_path()
        assert isinstance(path, str)
        assert path.startswith('/')

    def test_http_status(self):
        """Test HTTP status code generation."""
        status = FieldGenerator.http_status()
        assert isinstance(status, int)
        assert status in [200, 301, 302, 304, 400, 401, 403, 404, 500]

    def test_city(self):
        """Test city generation."""
        city = FieldGenerator.city()
        assert isinstance(city, str)
        assert len(city) > 0

    def test_country_code(self):
        """Test country code generation."""
        code = FieldGenerator.country_code()
        assert isinstance(code, str)
        assert len(code) == 2
        assert code.isupper()

    def test_latitude(self):
        """Test latitude generation."""
        lat = FieldGenerator.latitude()
        assert isinstance(lat, float)
        assert -90 <= lat <= 90

    def test_longitude(self):
        """Test longitude generation."""
        lon = FieldGenerator.longitude()
        assert isinstance(lon, float)
        assert -180 <= lon <= 180

    def test_boolean(self):
        """Test boolean generation."""
        # Test default
        result = FieldGenerator.boolean()
        assert isinstance(result, bool)

        # Test with probability
        result = FieldGenerator.boolean(true_probability=1.0)
        assert result is True

        result = FieldGenerator.boolean(true_probability=0.0)
        assert result is False

    def test_weighted_choice(self):
        """Test weighted choice."""
        distribution = {'a': 1.0, 'b': 0.0}
        result = FieldGenerator.weighted_choice(distribution)
        assert result == 'a'

    def test_body_bytes(self):
        """Test body bytes generation."""
        size = FieldGenerator.body_bytes()
        assert isinstance(size, int)
        assert size >= 0

    def test_request_time(self):
        """Test request time generation."""
        time = FieldGenerator.request_time()
        assert isinstance(time, float)
        assert time >= 0.001

    def test_filename(self):
        """Test filename generation."""
        filename = FieldGenerator.filename()
        assert isinstance(filename, str)
        assert '.' in filename  # Should have extension

    def test_process_name(self):
        """Test process name generation."""
        process = FieldGenerator.process_name()
        assert isinstance(process, str)
        assert len(process) > 0

    def test_sha256(self):
        """Test SHA256 hash generation."""
        hash_val = FieldGenerator.sha256()
        assert isinstance(hash_val, str)
        assert len(hash_val) == 64
        assert re.match(r'^[0-9a-f]{64}$', hash_val)

    def test_md5(self):
        """Test MD5 hash generation."""
        hash_val = FieldGenerator.md5()
        assert isinstance(hash_val, str)
        assert len(hash_val) == 32
        assert re.match(r'^[0-9a-f]{32}$', hash_val)

    def test_domain_name(self):
        """Test domain name generation."""
        domain = FieldGenerator.domain_name()
        assert isinstance(domain, str)
        assert '.' in domain

    def test_aws_account_id(self):
        """Test AWS account ID generation."""
        account_id = FieldGenerator.aws_account_id()
        assert isinstance(account_id, str)
        assert len(account_id) == 12
        assert account_id.isdigit()

    def test_aws_arn(self):
        """Test AWS ARN generation."""
        arn = FieldGenerator.aws_arn()
        assert isinstance(arn, str)
        assert arn.startswith('arn:aws:')

    def test_gcp_project_id(self):
        """Test GCP project ID generation."""
        project_id = FieldGenerator.gcp_project_id()
        assert isinstance(project_id, str)
        assert '-' in project_id  # Should have hyphens
