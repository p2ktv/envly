from __future__ import annotations

import builtins
from typing import Callable, Any

from envly.coercion import _make_json_coercer
from .var import _MISSING, EnvVar

__all__ = [
    "JsonVar",
]


def JsonVar(
    *,
    type: builtins.type | None = None,
    default: Any = _MISSING,
    validate: Callable[[Any], bool] | tuple[Callable[[Any], bool], ...] | None = None,
    var_name: str | None = None,
) -> Any:
    """
    Represents a JSON variable in the environment.

    Parameters
    ----------
    type: :class:`builtins.type`
        Requires the root to be of this type.
    default: :class:`Any`
        An optional default value.
    validate: :class:`Validator[Any]`
        Optional validator(s) for this variable.
    var_name: :class:`str`
        An optional name used to locate the variable in the source.
        By default it uses the class attribute name.

    Returns
    -------
    :class:`Any`
        The coerced value.
    """
    return EnvVar(
        coerce=_make_json_coercer(type),
        default=default,
        validate=validate,
        var_name=var_name,
        type_label="json",
        extra={"type": type.__name__ if type is not None else None},
    )  # type: ignore[return-value]
