from __future__ import annotations

import re

from env_typed.coercion import _make_regex_coercer
from .var import _MISSING, Validator, EnvVar

__all__ = [
    "RegexVar",
]


def RegexVar(
    pattern: str | re.Pattern[str],
    *,
    default: str | object = _MISSING,
    validate: Validator[str] | None = None,
    var_name: str | None = None,
) -> str:
    """
    Represents a RegEx-parsed variable in the environment.

    Parameters
    ----------
    pattern: :class:`str | re.Pattern[str]`
        RegEx pattern used for the validation.
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
    compiled = re.compile(pattern) if isinstance(pattern, str) else pattern
    return EnvVar(
        coerce=_make_regex_coercer(compiled),
        default=default,
        validate=validate,
        var_name=var_name,
        type_label="regex",
        extra={"pattern": compiled.pattern},
    )  # type: ignore[return-value]
