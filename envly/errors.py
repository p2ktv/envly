from __future__ import annotations

from typing import Any


__all__ = ["EnvlyError", "MissingEnvError", "InvalidEnvError", "ValidationError"]


class EnvlyError(Exception):
    """
    Base exception for all envly errors.
    """


class MissingEnvError(EnvlyError):
    """
    Raised when a required environment variable is missing.
    """

    def __init__(self, var_name: str) -> None:
        self.var_name = var_name
        super().__init__(f"Required environment variable {var_name!r} is not missing.")


class InvalidEnvError(EnvlyError):
    """
    Raised when a value cannot be coerced to the expected type.
    """

    def __init__(
        self, var_name: str, raw_value: str, expected_type: str, reason: str = ""
    ) -> None:
        self.var_name = var_name
        self.raw_value = raw_value
        self.expected_type = expected_type
        detail = f": {reason}" if reason else ""
        super().__init__(
            f"[{var_name}] cannot coerce {raw_value!r} to {expected_type}{detail}"
        )


class ValidationError(EnvlyError):
    """
    Raised when a value fails a validator function.
    """

    def __init__(self, var_name: str, value: Any, validator_index: int) -> None:
        self.var_name = var_name
        self.value = value
        self.validator_index = validator_index
        super().__init__(
            f"[{var_name}] validation failed (validator {validator_index}) for value {value!r}."
        )
