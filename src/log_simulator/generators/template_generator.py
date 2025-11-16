"""
Template-based log generator.

This module generates logs based on real log templates, allowing for
realistic log generation with variable substitution.
"""

import json
import random
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Optional, cast

from ..utils.field_generators import FieldGenerator


class TemplateBasedGenerator:
    """Generate logs based on templates extracted from real logs."""

    def __init__(self, template_dir: Optional[str] = None):
        """
        Initialize generator with a template directory.

        Args:
            template_dir: Path to directory containing log templates
        """
        if template_dir:
            self.template_dir = Path(template_dir)
        else:
            # Default to templates directory in package
            self.template_dir = Path(__file__).parent.parent / "templates"

        self.field_gen = FieldGenerator()
        self.variable_pattern = re.compile(r"\{\{(\w+)\}\}")

    def list_templates(self, category: Optional[str] = None) -> list[str]:
        """
        List available templates.

        Args:
            category: Optional category filter (e.g., 'security', 'cloud')

        Returns:
            List of template file names
        """
        if category:
            search_dir = self.template_dir / category
        else:
            search_dir = self.template_dir

        if not search_dir.exists():
            return []

        templates = []
        for template_file in search_dir.rglob("*.json"):
            rel_path = template_file.relative_to(self.template_dir)
            templates.append(str(rel_path))

        return sorted(templates)

    def load_template(self, template_path: str) -> dict[str, Any]:
        """
        Load a template file.

        Args:
            template_path: Path to template file (relative to template_dir)

        Returns:
            Template dictionary
        """
        full_path = self.template_dir / template_path

        if not full_path.exists():
            raise FileNotFoundError(f"Template not found: {template_path}")

        with open(full_path) as f:
            return cast(dict[str, Any], json.load(f))

    def _substitute_variables(
        self, value: Any, base_time: Optional[datetime] = None, offset_seconds: int = 0
    ) -> Any:
        """
        Substitute template variables with generated values.

        Args:
            value: Template value (can be string, dict, list, etc.)
            base_time: Base timestamp for datetime generation
            offset_seconds: Offset from base time

        Returns:
            Value with substituted variables
        """
        if base_time is None:
            base_time = datetime.utcnow()

        if isinstance(value, str):
            # Find and replace all variables
            def replace_variable(match):
                var_name = match.group(1)
                return self._generate_variable(var_name, base_time, offset_seconds)

            return self.variable_pattern.sub(replace_variable, value)

        elif isinstance(value, dict):
            return {
                key: self._substitute_variables(val, base_time, offset_seconds)
                for key, val in value.items()
            }

        elif isinstance(value, list):
            return [
                self._substitute_variables(item, base_time, offset_seconds)
                for item in value
            ]

        else:
            return value

    def _generate_variable(
        self, var_name: str, base_time: datetime, offset_seconds: int
    ) -> str:
        """
        Generate value for a template variable.

        Args:
            var_name: Variable name from template
            base_time: Base timestamp
            offset_seconds: Time offset

        Returns:
            Generated value as string
        """
        # Timestamp variables
        if var_name in ["timestamp", "utc_time", "event_time"]:
            return self.field_gen.datetime_iso8601(base_time, offset_seconds)

        # ID variables
        elif var_name in ["uuid", "event_id", "record_id", "id"]:
            return self.field_gen.uuid4()

        elif var_name in ["process_id", "pid"]:
            return str(random.randint(100, 65535))

        elif var_name in ["thread_id", "tid"]:
            return str(random.randint(1, 10000))

        # Network variables
        elif var_name in ["ip", "source_ip", "remote_ip"]:
            return self.field_gen.ipv4()

        elif var_name in ["port", "source_port", "remote_port"]:
            return str(random.randint(1024, 65535))

        # User variables
        elif var_name in ["username", "user"]:
            return self.field_gen.username()

        elif var_name in ["email", "user_email"]:
            return self.field_gen.email()

        # File/Process variables
        elif var_name in ["filename", "file_name"]:
            return self.field_gen.filename()

        elif var_name in ["file_path", "path"]:
            return self.field_gen.file_path()

        elif var_name in ["process_name", "image_name"]:
            return self.field_gen.process_name()

        elif var_name in ["command_line", "cmdline"]:
            return self.field_gen.command_line()

        # Hash variables
        elif var_name in ["sha256", "hash_sha256"]:
            return self.field_gen.sha256()

        elif var_name in ["md5", "hash_md5"]:
            return self.field_gen.md5()

        # Host variables
        elif var_name in ["hostname", "computer_name"]:
            return self.field_gen.device_name()

        elif var_name in ["domain", "domain_name"]:
            return self.field_gen.domain_name()

        # Numbers
        elif var_name.endswith("_number"):
            return str(random.randint(1, 1000000))

        # Default: return placeholder
        else:
            return f"{{{{unknown:{var_name}}}}}"

    def generate_from_template(
        self,
        template_path: str,
        count: int = 1,
        base_time: Optional[datetime] = None,
        time_spread_seconds: int = 0,
    ) -> list[dict[str, Any]]:
        """
        Generate logs from a template.

        Args:
            template_path: Path to template file
            count: Number of logs to generate
            base_time: Base timestamp
            time_spread_seconds: Spread logs over this many seconds

        Returns:
            List of generated log dictionaries
        """
        template = self.load_template(template_path)

        if base_time is None:
            base_time = datetime.utcnow()

        logs = []
        for i in range(count):
            # Calculate time offset
            if time_spread_seconds > 0:
                offset = int((i / count) * time_spread_seconds)
            else:
                offset = 0

            # Generate log with variable substitution
            log = self._substitute_variables(template, base_time, offset)
            logs.append(log)

        return logs

    def generate_attack_scenario(
        self,
        techniques: list[str],
        count_per_technique: int = 5,
        template_category: str = "security",
        time_spread_seconds: int = 300,
    ) -> list[dict[str, Any]]:
        """
        Generate logs for an attack scenario using multiple techniques.

        Args:
            techniques: List of MITRE ATT&CK technique IDs (e.g., ['T1059.001'])
            count_per_technique: Number of logs per technique
            template_category: Template category to search
            time_spread_seconds: Total time spread for all logs

        Returns:
            List of generated logs in chronological order
        """
        all_logs = []
        base_time = datetime.utcnow()

        total_logs = len(techniques) * count_per_technique
        log_index = 0

        for technique in techniques:
            # Find template for this technique
            template_pattern = f"**/*{technique}*.json"
            matching_templates = list(
                (self.template_dir / template_category).glob(template_pattern)
            )

            if not matching_templates:
                print(f"Warning: No template found for {technique}")
                continue

            # Use first matching template
            template_path = matching_templates[0].relative_to(self.template_dir)

            # Generate logs for this technique
            for _i in range(count_per_technique):
                offset = int((log_index / total_logs) * time_spread_seconds)
                log = self._substitute_variables(
                    self.load_template(str(template_path)), base_time, offset
                )

                # Add metadata
                log["_metadata"] = {
                    "technique": technique,
                    "log_index": log_index,
                    "template": str(template_path),
                }

                all_logs.append(log)
                log_index += 1

        # Sort by timestamp if present
        if all_logs and "timestamp" in all_logs[0]:
            all_logs.sort(key=lambda x: x.get("timestamp", ""))

        return all_logs

    def generate_to_json(
        self, template_path: str, count: int = 1, pretty: bool = False
    ) -> str:
        """
        Generate logs and return as JSON string.

        Args:
            template_path: Path to template file
            count: Number of logs to generate
            pretty: Pretty-print JSON

        Returns:
            JSON string
        """
        logs = self.generate_from_template(template_path, count)

        if pretty:
            return json.dumps(logs, indent=2)
        else:
            return json.dumps(logs)

    def save_to_file(
        self, template_path: str, output_file: str, count: int = 1, pretty: bool = False
    ):
        """
        Generate logs and save to file.

        Args:
            template_path: Path to template file
            output_file: Output file path
            count: Number of logs to generate
            pretty: Pretty-print JSON
        """
        json_str = self.generate_to_json(template_path, count, pretty)

        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json_str)

        print(f"Generated {count} log(s) -> {output_file}")
