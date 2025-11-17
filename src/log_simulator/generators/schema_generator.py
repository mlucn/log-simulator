"""
Schema-based log generator.

This module generates logs based on YAML schema definitions.
"""

import json
import random
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional, cast

import yaml

from ..utils.field_generators import FieldGenerator


class SchemaBasedGenerator:
    """Generate logs based on schema definitions."""

    def __init__(self, schema_path: str):
        """
        Initialize generator with a schema file.

        Args:
            schema_path: Path to YAML schema file
        """
        self.schema_path = Path(schema_path)
        self.schema = self._load_schema()
        self.field_gen = FieldGenerator()
        self.correlation_state: dict[str, Any] = {}  # Store correlated values

    def _load_schema(self) -> dict[str, Any]:
        """Load and parse the YAML schema file."""
        with open(self.schema_path) as f:
            return cast(dict[str, Any], yaml.safe_load(f))

    def generate(
        self,
        count: int = 1,
        scenario: Optional[str] = None,
        base_time: Optional[datetime] = None,
        time_spread_seconds: int = 0,
    ) -> list[dict[str, Any]]:
        """
        Generate log entries based on the schema.

        Args:
            count: Number of log entries to generate
            scenario: Optional scenario name from schema
            base_time: Base timestamp (defaults to now)
            time_spread_seconds: Spread logs over this many seconds

        Returns:
            List of generated log dictionaries
        """
        if base_time is None:
            base_time = datetime.now(timezone.utc)

        logs = []
        scenario_overrides = {}

        # Get scenario overrides if specified
        if scenario and "scenarios" in self.schema:
            if scenario in self.schema["scenarios"]:
                scenario_overrides = self.schema["scenarios"][scenario]
            else:
                available = ", ".join(self.schema["scenarios"].keys())
                raise ValueError(
                    f"Scenario '{scenario}' not found. Available: {available}"
                )

        for i in range(count):
            # Calculate time offset for this log
            if time_spread_seconds > 0:
                time_offset = int((i / count) * time_spread_seconds)
            else:
                time_offset = 0

            log_entry = self._generate_single(
                scenario_overrides, base_time, time_offset
            )
            logs.append(log_entry)

        return logs

    def _generate_single(
        self, overrides: dict[str, Any], base_time: datetime, time_offset: int
    ) -> dict[str, Any]:
        """Generate a single log entry."""
        result = {}
        fields = self.schema.get("fields", {})

        for field_name, field_spec in fields.items():
            result[field_name] = self._generate_field(
                field_name, field_spec, base_time, time_offset, overrides, field_name
            )

        return result

    def _get_nested_override(
        self, overrides: dict[str, Any], field_path: str
    ) -> Optional[Any]:
        """Get override value for a potentially nested field."""
        if field_path in overrides:
            return overrides[field_path]

        # Check for nested overrides (e.g., "status.errorCode")
        for key, value in overrides.items():
            if key == field_path:
                return value

        return None

    def _generate_field(
        self,
        field_name: str,
        field_spec: dict[str, Any],
        base_time: datetime,
        time_offset: int,
        overrides: Optional[dict[str, Any]] = None,
        field_path: str = "",
    ) -> Any:
        """Generate a single field value based on its specification."""
        if overrides is None:
            overrides = {}

        # Check if this exact field has an override
        if field_path in overrides:
            return overrides[field_path]

        field_type = field_spec.get("type")
        required = field_spec.get("required", False)

        # Handle optional fields
        if not required and random.random() > 0.7:
            return field_spec.get("default", None)

        # Handle different field types
        if field_type == "constant":
            return field_spec["value"]

        elif field_type == "datetime":
            return self.field_gen.datetime_iso8601(base_time, time_offset)

        elif field_type == "uuid":
            return self.field_gen.uuid4()

        elif field_type == "string":
            return self._generate_string_field(field_spec)

        elif field_type == "email":
            return self.field_gen.email()

        elif field_type == "ipv4":
            return self.field_gen.ipv4()

        elif field_type == "integer":
            return self._generate_integer_field(field_spec)

        elif field_type == "float":
            return self._generate_float_field(field_spec)

        elif field_type == "boolean":
            return self._generate_boolean_field(field_spec)

        elif field_type == "enum":
            return self._generate_enum_field(field_spec)

        elif field_type == "object":
            return self._generate_object_field(
                field_spec, base_time, time_offset, overrides, field_path
            )

        elif field_type == "array":
            return self._generate_array_field(
                field_spec, base_time, time_offset, overrides, field_path
            )

        else:
            # Default to string
            return f"field_{field_name}"

    def _generate_string_field(self, field_spec: dict[str, Any]) -> str:
        """Generate a string field value."""
        generator = field_spec.get("generator", "default")

        if generator == "number_string":
            params = field_spec.get("params", {})
            length = params.get("length", 16)
            return self.field_gen.number_string(length)

        elif generator == "custom_id":
            params = field_spec.get("params", {})
            prefix = params.get("prefix", "")
            length = params.get("length", 8)
            return self.field_gen.custom_id(prefix, length)

        elif generator == "full_name":
            return self.field_gen.full_name()

        elif generator == "username":
            return self.field_gen.username()

        elif generator == "user_agent":
            return self.field_gen.user_agent()

        elif generator == "uri_path":
            return self.field_gen.uri_path()

        elif generator == "city":
            return self.field_gen.city()

        elif generator == "state":
            return self.field_gen.state()

        elif generator == "country_code":
            return self.field_gen.country_code()

        elif generator == "device_name":
            return self.field_gen.device_name()

        elif generator == "email_subject":
            return self.field_gen.email_subject()

        elif generator == "filename":
            return self.field_gen.filename()

        elif generator == "referer":
            return self.field_gen.referer()

        elif generator == "process_name":
            return self.field_gen.process_name()

        elif generator == "command_line":
            return self.field_gen.command_line()

        elif generator == "sha256":
            return self.field_gen.sha256()

        elif generator == "md5":
            return self.field_gen.md5()

        elif generator == "domain_name":
            return self.field_gen.domain_name()

        elif generator == "file_path":
            return self.field_gen.file_path()

        elif generator == "detection_name":
            return self.field_gen.detection_name()

        elif generator == "registry_key":
            return self.field_gen.registry_key()

        elif generator == "aws_user_agent":
            return self.field_gen.aws_user_agent()

        elif generator == "aws_principal_id":
            return self.field_gen.aws_principal_id()

        elif generator == "aws_arn":
            return self.field_gen.aws_arn()

        elif generator == "aws_account_id":
            return self.field_gen.aws_account_id()

        elif generator == "aws_resource_arn":
            return self.field_gen.aws_resource_arn()

        elif generator == "gcp_project_id":
            return self.field_gen.gcp_project_id()

        elif generator == "gcp_resource_name":
            return self.field_gen.gcp_resource_name()

        elif generator == "sysmon_guid":
            return self.field_gen.sysmon_guid()

        elif generator == "windows_image_path":
            return self.field_gen.windows_image_path()

        elif generator == "windows_user":
            return self.field_gen.windows_user()

        elif generator == "sysmon_hashes":
            return self.field_gen.sysmon_hashes()

        else:
            return str(field_spec.get("default", "default_value"))

    def _generate_integer_field(self, field_spec: dict[str, Any]) -> int:
        """Generate an integer field value."""
        field_spec.get("default", 0)
        params = field_spec.get("params", {})

        min_val = params.get("min", 0)
        max_val = params.get("max", 1000)

        if "distribution" in field_spec:
            # Use specific distribution from field spec
            return cast(int, self.field_gen.weighted_choice(field_spec["distribution"]))

        return random.randint(min_val, max_val)

    def _generate_float_field(self, field_spec: dict[str, Any]) -> float:
        """Generate a float field value."""
        params = field_spec.get("params", {})
        generator = field_spec.get("generator", "uniform")

        min_val = params.get("min", 0.0)
        max_val = params.get("max", 1.0)

        if generator == "request_time":
            mean = params.get("mean", 0.150)
            return self.field_gen.request_time(min_val, max_val, mean)

        return round(random.uniform(min_val, max_val), 3)

    def _generate_boolean_field(self, field_spec: dict[str, Any]) -> bool:
        """Generate a boolean field value."""
        if "distribution" in field_spec:
            dist = field_spec["distribution"]
            true_prob = dist.get(True, 0.5)
            return self.field_gen.boolean(true_prob)

        return random.choice([True, False])

    def _generate_enum_field(self, field_spec: dict[str, Any]) -> Any:
        """Generate an enum field value."""
        values = field_spec.get("values", [])

        if not values:
            return field_spec.get("default", None)

        # Check for distribution
        if "distribution" in field_spec:
            return self.field_gen.weighted_choice(field_spec["distribution"])

        # Otherwise random choice
        return random.choice(values)

    def _generate_object_field(
        self,
        field_spec: dict[str, Any],
        base_time: datetime,
        time_offset: int,
        overrides: Optional[dict[str, Any]] = None,
        parent_path: str = "",
    ) -> dict[str, Any]:
        """Generate an object (nested) field value."""
        if overrides is None:
            overrides = {}

        result = {}
        nested_fields = field_spec.get("fields", {})

        for nested_name, nested_spec in nested_fields.items():
            # Build the full path for nested fields (e.g., "id.applicationName")
            nested_path = f"{parent_path}.{nested_name}" if parent_path else nested_name

            result[nested_name] = self._generate_field(
                nested_name, nested_spec, base_time, time_offset, overrides, nested_path
            )

        return result

    def _generate_array_field(
        self,
        field_spec: dict[str, Any],
        base_time: datetime,
        time_offset: int,
        overrides: Optional[dict[str, Any]] = None,
        parent_path: str = "",
    ) -> list[Any]:
        """Generate an array field value."""
        if overrides is None:
            overrides = {}

        # Check if the entire array is overridden
        if parent_path in overrides:
            return cast(list[Any], overrides[parent_path])

        min_items = field_spec.get("min_items", 1)
        max_items = field_spec.get("max_items", 3)
        item_spec = field_spec.get("item", {})

        count = random.randint(min_items, max_items)
        result = []

        for _ in range(count):
            if item_spec.get("type") == "object":
                item_value = self._generate_object_field(
                    item_spec, base_time, time_offset, overrides, parent_path
                )
            else:
                item_value = self._generate_field(
                    "array_item",
                    item_spec,
                    base_time,
                    time_offset,
                    overrides,
                    parent_path,
                )
            result.append(item_value)

        return result

    def generate_to_json(
        self, count: int = 1, scenario: Optional[str] = None, pretty: bool = False
    ) -> str:
        """
        Generate logs and return as JSON string.

        Args:
            count: Number of logs to generate
            scenario: Optional scenario name
            pretty: Pretty-print JSON

        Returns:
            JSON string
        """
        logs = self.generate(count, scenario)

        if pretty:
            return json.dumps(logs, indent=2)
        else:
            return json.dumps(logs)

    def list_scenarios(self) -> list[str]:
        """List available scenarios in the schema."""
        return list(self.schema.get("scenarios", {}).keys())

    def get_schema_info(self) -> dict[str, Any]:
        """Get schema metadata."""
        return {
            "log_type": self.schema.get("log_type"),
            "description": self.schema.get("description"),
            "schema_version": self.schema.get("schema_version"),
            "output_format": self.schema.get("output_format"),
            "available_scenarios": self.list_scenarios(),
        }
