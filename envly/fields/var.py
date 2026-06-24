from __future__ import annotations

import pathlib
from typing import Any, Callable, Generic, TypeVar, overload, override, final

from envly.errors import EnvError
from envly.types import SecretStr

__all__ = ["EnvVar"]

T = TypeVar("T", str, int, float, bool, bytes, pathlib.Path, SecretStr)

# Type definition for a validator, which can be either
# a single callable or a tuple of callable.
# Each validator receives the coerced value and returns True if valid.
Validator = Callable[[T], bool] | tuple[Callable[[T], bool], ...]

# Special sentinel annotating a missing value
_MISSING: Any = object()


@final
class EnvVar(Generic[T]):
    """
    Descriptor that reads, coerces, and validates a
    single environment variable.

    This class is not constructed directly, since the
    default approach is done through the typed factory
    functions.

    Parameters
    ----------
    coerce: :class:`Callable[[str, str], T]`
        The function used to coerce the value.
    default: :class:`T`
        An optional default value.
    validate: :class:`Validator[T]`
        Optional validators for this variable.
        Can be specificed using a single callable or
        a tuple of callables, where each validator
        has to return `True` in order to be fully validated.
    var_name: :class:`str`
        An optional name used to locate the variable in the source.
        By default it uses the class attribute name.
    secret: :class:`bool`
        Can be used in strings to hide their value in the class
        representation. Defaults to `False`.
    """

    # Filled in by the metaclass when it registers this field.
    _attr_name: str

    def __init__(
        self,
        *,
        coerce: Callable[[str, str], T],
        default: T | object = _MISSING,
        validate: Validator[T] | None = None,
        var_name: str | None = None,
        secret: bool = False,
        # Metadata carried for :func:`schema()`
        type_label: str = "str",
        extra: dict[str, Any] | None = None,
    ) -> None:
        self._coerce = coerce
        self.default = default
        self.var_name = var_name
        self.secret = secret
        self.type_label = type_label
        self.extra: dict[str, Any] = extra or {}
        self._validators: tuple[Callable[[T], bool], ...] = (
            (validate,) if callable(validate) else tuple(validate or ())
        )

    @overload
    def __get__(self, obj: None, objtype: type) -> "EnvVar[T]": ...
    @overload
    def __get__(self, obj: object, objtype: type) -> T: ...

    def __get__(
        self, obj: object | None, objtype: type | None = None
    ) -> "EnvVar[T] | T":
        if obj is None:
            return self

        try:
            return obj.__dict__[self._attr_name]
        except KeyError:
            raise AttributeError(self._attr_name) from None

    def __set__(self, obj: object, value: Any) -> None:
        raise AttributeError("Env configs are immutable after construction")

    def __set_name__(self, owner: type, name: str) -> None:
        self._attr_name = name

    def resolve(self, source: dict[str, str], effective_name: str) -> T:
        """
        Read from `effective_name` from `source`, coerce, optionally
        wrap as :class:`SecretStr`, validate, and return the
        final value.

        Parameters
        ----------
        source: :class:`dict[str, str]`
            The source to read the value from.
        effective_name: :class:`str`
            The env var key after prefix expansion.

        Returns
        -------
        :class:`T`
            The final value.

        Raises
        ------
        :class:`EnvError`
            If the value couldn't be resolved.
        """
        if effective_name in source:
            value: T = self._coerce(effective_name, source[effective_name])
            if self.secret:
                value = SecretStr(value)  # type: ignore
        elif self.default is not _MISSING:
            return self.default  # type: ignore[return-value]
        else:
            raise EnvError(
                f"Required environment variable {effective_name!r} is missing."
            )

        self._run_validators(effective_name, value)
        return value

    def _run_validators(self, var_name: str, value: T) -> None:
        for i, validator in enumerate(self._validators, start=1):
            try:
                ok = validator(value)
            except Exception as exc:
                raise EnvError(
                    f"[{var_name}] validator {i} raised an exception: {exc}"
                ) from exc

            if not ok:
                raise EnvError(
                    f"[{var_name}] validation failed (validator {i}) for value {value!r}."
                )

    @override
    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}("
            f"type={self.type_label!r}, "
            f"var_name={self.var_name!r}, "
            f"default={self.default!r}, "
            f"secret={self.secret}, ",
            f"validators={len(self._validators)})",
        )
