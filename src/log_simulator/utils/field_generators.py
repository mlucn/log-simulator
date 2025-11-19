"""
Field generators for creating realistic log data.

This module provides various generators for common log fields like
timestamps, UUIDs, IP addresses, emails, etc.

DEPRECATED: This class is now a facade for the specialized generators in
src/log_simulator/generators/fields/. Please use those directly in new code.
"""

from ..generators.fields.base import BaseFieldGenerator
from ..generators.fields.cloud import CloudGenerator
from ..generators.fields.identity import IdentityGenerator
from ..generators.fields.network import NetworkGenerator
from ..generators.fields.system import SystemGenerator


class FieldGenerator:
    """
    Base class for field generators with reusable utilities.
    Acts as a facade for specialized generators.
    """

    # Base
    uuid4 = staticmethod(BaseFieldGenerator.uuid4)
    datetime_iso8601 = staticmethod(BaseFieldGenerator.datetime_iso8601)
    boolean = staticmethod(BaseFieldGenerator.boolean)
    weighted_choice = staticmethod(BaseFieldGenerator.weighted_choice)

    # Identity
    email = staticmethod(IdentityGenerator.email)
    full_name = staticmethod(IdentityGenerator.full_name)
    username = staticmethod(IdentityGenerator.username)
    number_string = staticmethod(IdentityGenerator.number_string)
    custom_id = staticmethod(IdentityGenerator.custom_id)

    # Network
    ipv4 = staticmethod(NetworkGenerator.ipv4)
    user_agent = staticmethod(NetworkGenerator.user_agent)
    uri_path = staticmethod(NetworkGenerator.uri_path)
    http_status = staticmethod(NetworkGenerator.http_status)
    referer = staticmethod(NetworkGenerator.referer)
    domain_name = staticmethod(NetworkGenerator.domain_name)
    request_time = staticmethod(NetworkGenerator.request_time)
    body_bytes = staticmethod(NetworkGenerator.body_bytes)

    # Cloud
    aws_user_agent = staticmethod(CloudGenerator.aws_user_agent)
    aws_principal_id = staticmethod(CloudGenerator.aws_principal_id)
    aws_account_id = staticmethod(CloudGenerator.aws_account_id)
    aws_arn = staticmethod(CloudGenerator.aws_arn)
    aws_resource_arn = staticmethod(CloudGenerator.aws_resource_arn)
    gcp_project_id = staticmethod(CloudGenerator.gcp_project_id)
    gcp_resource_name = staticmethod(CloudGenerator.gcp_resource_name)

    # System
    process_name = staticmethod(SystemGenerator.process_name)
    command_line = staticmethod(SystemGenerator.command_line)
    sha256 = staticmethod(SystemGenerator.sha256)
    md5 = staticmethod(SystemGenerator.md5)
    file_path = staticmethod(SystemGenerator.file_path)
    detection_name = staticmethod(SystemGenerator.detection_name)
    registry_key = staticmethod(SystemGenerator.registry_key)
    sysmon_guid = staticmethod(SystemGenerator.sysmon_guid)
    windows_image_path = staticmethod(SystemGenerator.windows_image_path)
    windows_user = staticmethod(SystemGenerator.windows_user)
    sysmon_hashes = staticmethod(SystemGenerator.sysmon_hashes)
    device_name = staticmethod(SystemGenerator.device_name)
    city = staticmethod(SystemGenerator.city)
    state = staticmethod(SystemGenerator.state)
    country_code = staticmethod(SystemGenerator.country_code)
    latitude = staticmethod(SystemGenerator.latitude)
    longitude = staticmethod(SystemGenerator.longitude)
    email_subject = staticmethod(SystemGenerator.email_subject)
    filename = staticmethod(SystemGenerator.filename)
