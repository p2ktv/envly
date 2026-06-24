from __future__ import annotations

from env_typed.coercion import _coerce_str
from .var import _MISSING, Validator, EnvVar

__all__ = [
    "StringVar",
]


def StringVar(
    *,
    default: str | object = _MISSING,
    validate: Validator[str] | None = None,
    var_name: str | None = None,
    secret: bool = False,
) -> str:
    """
    Represents a string variable in the environment.

    Parameters
    ----------
    default: :class:`str`
        An optional default value.
    validate: :class:`Validator[str]`
        Optional validator(s) for this variable.
    var_name: :class:`str`
        An optional name used to locate the variable in the source.
        By default it uses the class attribute name.
    secret: :class:`bool`
        Whether to hide the value when displaying the variable
        inside the code. Defaults to `False`.

    Returns
    -------
    :class:`str`
        The coerced value.
    """
    return EnvVar(
        coerce=_coerce_str,
        default=default,
        validate=validate,
        var_name=var_name,
        secret=secret,
        type_label="SecretStr" if secret else "str",
    )  # type: ignore[return-value]
