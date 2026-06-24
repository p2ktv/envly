from __future__ import annotations

from envly.coercion import _coerce_int
from .var import _MISSING, Validator, EnvVar

__all__ = [
    "IntVar",
]


def IntVar(
    *,
    default: int | object = _MISSING,
    validate: Validator[int] | None = None,
    var_name: str | None = None,
) -> int:
    """
    Represents an integer variable in the environment.

    Parameters
    ----------
    default: :class:`int`
        An optional default value.
    validate: :class:`Validator[int]`
        Optional validator(s) for this variable.
    var_name: :class:`str`
        An optional name used to locate the variable in the source.
        By default it uses the class attribute name.

    Returns
    -------
    :class:`int`
        The coerced value.
    """
    return EnvVar(
        coerce=_coerce_int,
        default=default,
        validate=validate,
        var_name=var_name,
        type_label="int",
    )  # type: ignore[return-value]
