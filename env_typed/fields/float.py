from __future__ import annotations

from env_typed.coercion import _coerce_float
from .var import _MISSING, Validator, EnvVar

__all__ = [
    "FloatVar",
]


def FloatVar(
    *,
    default: float | object = _MISSING,
    validate: Validator[float] | None = None,
    var_name: str | None = None,
) -> float:
    """
    Represents a floating integer variable in the environment.

    Parameters
    ----------
    default: :class:`float`
        An optional default value.
    validate: :class:`Validator[float]`
        Optional validator(s) for this variable.
    var_name: :class:`str`
        An optional name used to locate the variable in the source.
        By default it uses the class attribute name.

    Returns
    -------
    :class:`float`
        The coerced value.
    """
    return EnvVar(
        coerce=_coerce_float,
        default=default,
        validate=validate,
        var_name=var_name,
        type_label="float",
    )  # type: ignore[return-value]
