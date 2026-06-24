from __future__ import annotations

from envly.coercion import _make_enum_coercer
from .var import _MISSING, Validator, EnvVar

__all__ = [
    "EnumVar",
]


def EnumVar(
    *choices: str,
    default: str | object = _MISSING,
    validate: Validator[str] | None = None,
    var_name: str | None = None,
) -> str:
    """
    Represents an enum variable in the environment.

    Parameters
    ----------
    choices: :class:`str`
        List of valid options for the variable.
    default: :class:`str`
        An optional default value.
    validate: :class:`Validator[str]`
        Optional validator(s) for this variable.
    var_name: :class:`str`
        An optional name used to locate the variable in the source.
        By default it uses the class attribute name.

    Returns
    -------
    :class:`str`
        The coerced value.
    """
    if not choices:
        raise TypeError("EnumVar requires at least once choice.")

    return EnvVar(
        coerce=_make_enum_coercer(choices),
        default=default,
        validate=validate,
        var_name=var_name,
        type_label="enum",
        extra={"choices": list(choices)},
    )  # type: ignore[return-value]
