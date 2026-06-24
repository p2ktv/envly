from __future__ import annotations

__all__ = ["SecretStr"]


class SecretStr(str):
    """
    A :class:`str` subclass whose :meth:`__repr__` and :meth:`__str__`
    redact the value.

    The raw string is still accessible via :meth:`str(secret)` only
    if explicitly called by :meth:`reveal()`.
    """

    def __repr__(self) -> str:
        return "SecretStr('**redacted**')"

    def __str__(self) -> str:
        return "**redacted**"

    def reveal(self) -> str:
        """
        Returns the actual secret value.

        Returns
        -------
        :class:`str`
            The actual value.
        """
        return str.__str__(self)
