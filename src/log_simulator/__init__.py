"""
log-simulator: Generate simulated logs and mock up endpoints.

A Python tool for generating realistic log data for testing, development,
and security research purposes.
"""

__version__ = "0.1.0"
__author__ = "mlucn"

from .generators.schema_generator import SchemaBasedGenerator

__all__ = ['SchemaBasedGenerator']
