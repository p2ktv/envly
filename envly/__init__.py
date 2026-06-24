"""
Minimal, type-safe environment variable validation for Python.

:license: MIT, see LICENSE for more details.
"""

from envly.env import Environment, FieldSchema
from envly.errors import EnvlyError, InvalidEnvError, MissingEnvError, ValidationError
from envly.fields import (
    EnvVar,
    BoolVar,
    FloatVar,
    IntVar,
    StringVar,
    EmailVar,
    RegexVar,
    EnumVar,
    PathVar,
    BytesVar,
    JsonVar,
    ListVar,
)
from envly.types import SecretStr

__all__ = [
    "Environment",
    "FieldSchema",
    "EnvlyError",
    "MissingEnvError",
    "InvalidEnvError",
    "ValidationError",
    "EnvVar",
    "SecretStr",
    "StringVar",
    "IntVar",
    "FloatVar",
    "BoolVar",
    "EmailVar",
    "RegexVar",
    "EnumVar",
    "PathVar",
    "BytesVar",
    "JsonVar",
    "ListVar",
]

__version__ = "0.1.3"
