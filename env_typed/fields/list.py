from __future__ import annotations

import builtins
from typing import Callable, Any, overload

from env_typed.coercion import _make_list_coercer, _PRIMITIVE_COERCERS
from .var import _MISSING, EnvVar

__all__ = [
    "ListVar",
]


@overload
def ListVar(
    *,
    of: builtins.type[builtins.str],
    sep: str = ...,
    default: list[builtins.str] | object = ...,
    validate: Callable[[list[builtins.str]], bool]
    | tuple[Callable[[list[builtins.str]], bool], ...]
    | None = ...,
    var_name: str | None = ...,
) -> list[builtins.str]: ...


@overload
def ListVar(  # type: ignore
    *,
    of: builtins.type[builtins.int],
    sep: str = ...,
    default: list[builtins.int] | object = ...,
    validate: Callable[[list[builtins.int]], bool]
    | tuple[Callable[[list[builtins.int]], bool], ...]
    | None = ...,
    var_name: str | None = ...,
) -> list[builtins.int]: ...


@overload
def ListVar(
    *,
    of: builtins.type[builtins.float],
    sep: str = ...,
    default: list[builtins.float] | object = ...,
    validate: Callable[[list[builtins.float]], bool]
    | tuple[Callable[[list[builtins.float]], bool], ...]
    | None = ...,
    var_name: str | None = ...,
) -> list[builtins.float]: ...


@overload
def ListVar(
    *,
    of: builtins.type[builtins.bool],
    sep: str = ...,
    default: list[builtins.bool] | object = ...,
    validate: Callable[[list[builtins.bool]], bool]
    | tuple[Callable[[list[builtins.bool]], bool], ...]
    | None = ...,
    var_name: str | None = ...,
) -> list[builtins.bool]: ...


@overload
def ListVar(
    *,
    of: builtins.type[builtins.bytes],
    sep: str = ...,
    default: list[builtins.bytes] | object = ...,
    validate: Callable[[list[builtins.bytes]], bool]
    | tuple[Callable[[list[builtins.bytes]], bool], ...]
    | None = ...,
    var_name: str | None = ...,
) -> list[builtins.bytes]: ...


def ListVar(
    *,
    of: builtins.type,
    sep: str = ",",
    default: list[Any] | object = _MISSING,
    validate: Callable[[list[Any]], bool]
    | tuple[Callable[[list[Any]], bool], ...]
    | None = None,
    var_name: str | None = None,
) -> list[Any]:
    """
    Represents a list variable in the environment.

    Parameters
    ----------
    of: :class:`builtins.type`
        The type of the items in the list.
    sep: :class:`str`
        An optional seperator to use for the list.
        Defaults to `,`.
    default: :class:`list[Any]`
        An optional default value.
    validate: :class:`Validator[Any]`
        Optional validator(s) for this variable.
    var_name: :class:`str`
        An optional name used to locate the variable in the source.
        By default it uses the class attribute name.

    Returns
    -------
    :class:`list[Any]`
        The coerced value.
    """
    sub_coerce = _PRIMITIVE_COERCERS.get(of)
    if sub_coerce is None:
        supported = ", ".join(t.__name__ for t in _PRIMITIVE_COERCERS)
        raise TypeError(f"ListVar `of` must be one of: {supported}. Got {of!r}.")

    return EnvVar(
        coerce=_make_list_coercer(sub_coerce, sep),  # type: ignore[argument-type]
        default=default,
        validate=validate,  # type: ignore[argument-type]
        var_name=var_name,
        type_label=f"list[{of.__name__}]",
        extra={"of": of.__name__, "sep": sep},
    )  # type: ignore[return-value]
