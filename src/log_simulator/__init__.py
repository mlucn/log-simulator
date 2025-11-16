"""
log-simulator: Generate simulated logs and mock up endpoints.

A Python tool for generating realistic log data for testing, development,
and security research purposes.
"""

__version__ = "0.2.0"
__author__ = "mlucn"

from .generators.schema_generator import SchemaBasedGenerator
from .generators.template_generator import TemplateBasedGenerator

__all__ = ['SchemaBasedGenerator', 'TemplateBasedGenerator']
