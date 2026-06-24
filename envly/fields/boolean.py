from __future__ import annotations

from envly.coercion import _coerce_bool
from .var import _MISSING, Validator, EnvVar

__all__ = [
    "BoolVar",
]


def BoolVar(
    *,
    default: bool | object = _MISSING,
    validate: Validator[bool] | None = None,
    var_name: str | None = None,
) -> bool:
    """
    Represents a boolean variable in the environment.

    Parameters
    ----------
    default: :class:`bool`
        An optional default value.
    validate: :class:`Validator[bool]`
        Optional validator(s) for this variable.
    var_name: :class:`str`
        An optional name used to locate the variable in the source.
        By default it uses the class attribute name.

    Returns
    -------
    :class:`bool`
        The coerced value.
    """
    return EnvVar(
        coerce=_coerce_bool,
        default=default,
        validate=validate,
        var_name=var_name,
        type_label="bool",
    )  # type: ignore[return-value]
