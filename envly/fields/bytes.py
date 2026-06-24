from __future__ import annotations

from envly.coercion import _coerce_bytes
from .var import _MISSING, Validator, EnvVar

__all__ = [
    "BytesVar",
]


def BytesVar(
    *,
    default: bytes | object = _MISSING,
    validate: Validator[bytes] | None = None,
    var_name: str | None = None,
) -> bytes:
    """
    Represents a bytes variable in the environment.

    Parameters
    ----------
    default: :class:`bytes`
        An optional default value.
    validate: :class:`Validator[bytes]`
        Optional validator(s) for this variable.
    var_name: :class:`str`
        An optional name used to locate the variable in the source.
        By default it uses the class attribute name.

    Returns
    -------
    :class:`bytes`
        The coerced value.
    """
    return EnvVar(
        coerce=_coerce_bytes,
        default=default,
        validate=validate,
        var_name=var_name,
        type_label="bytes",
    )  # type: ignore[return-value]
