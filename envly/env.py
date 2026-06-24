from __future__ import annotations

import os
import dotenv
from typing import Any, ClassVar, TypedDict, override

from envly.fields import EnvVar, _MISSING

__all__ = ["Environment"]


class FieldSchema(TypedDict, total=False):
    """
    Schema for an environment variable
    """

    attr: str  # Python attribute name
    env_var: str  # Actual env var key (combined with prefix)
    type: str  # Human-readable type label
    required: bool  # True when no default is set
    default: Any  # Omitted when required=True
    secret: bool  # True when value is redacted in repr
    extra: dict[str, Any]  # Type-specific metadata


class _EnvironmentMeta(type):
    """
    Metaclass that discovers :class:`EnvVar` descriptors on the class
    body and stores them in :attr:`__env_vars__` for use during
    instantiation.

    Accepts an optional `prefix` keyword argument on the class definition.
    """

    __env_vars__: dict[str, EnvVar[Any]]
    __env_prefix__: str

    def __new__(
        mcs,
        name: str,
        bases: tuple[type, ...],
        namespace: dict[str, Any],
        prefix: str = "",
        **kwargs: Any,
    ) -> "_EnvironmentMeta":
        env_vars: dict[str, EnvVar[Any]] = {}

        for base in bases:
            if hasattr(base, "__env_vars__"):
                env_vars.update(base.__env_vars__)

        for attr, value in namespace.items():
            if isinstance(value, EnvVar):
                env_vars[attr] = value

        cls = super().__new__(mcs, name, bases, namespace, **kwargs)
        cls.__env_vars__ = env_vars  # type: ignore[attr-defined]
        cls.__env_prefix__ = prefix  # type: ignore[attr-defined]
        return cls

    # We need to forward the keyword so Python doesn't complain
    # about unexpected kwargs.
    def __init_subclass__(cls, prefix: str = "", **kwargs: Any) -> None:
        return super().__init_subclass__(**kwargs)


class Environment(metaclass=_EnvironmentMeta):
    """
    Base class for environment configurations.

    Usage
    -----
    ```py
        class MyEnv(Environment):
            HOST = StringVar()
            PORT = IntVar(default=8080)
            TIMEOUT: float = FloatVar(default=30.0, validate=lambda x: x > 0)

        env = MyEnv()
    ```

    Parameters
    ----------
    env_path: :class:`str`
        The path to the the environment file.
        By default this is the `.env` in the folder root.
    source: :class:`dict[str, str]`
        Override the environment source (defaults to :attr:`os.environ`).
        This is especially useful in a testing environment.
    """

    __env_vars__: ClassVar[dict[str, EnvVar[Any]]]
    __env_prefix__: ClassVar[str]

    def __init__(
        self, env_path: str = ".env", source: dict[str, str] | None = None
    ) -> None:
        if not source and env_path:
            self._load_env_file(env_path)

        _source: dict[str, str] = os.environ if source is None else source  # type: ignore[assignment]
        prefix = type(self).__env_prefix__
        instance_dict: dict[str, Any] = self.__dict__  # type: ignore[assignment]

        for attr, var in type(self).__env_vars__.items():
            effective = var.var_name if var.var_name else f"{prefix}{attr}"
            instance_dict[attr] = var.resolve(_source, effective)

    def __setattr__(self, name: str, value: Any) -> None:
        raise AttributeError(
            f"{type(self).__name__} instances are immutable after construction."
        )

    @override
    def __repr__(self) -> str:
        pairs = ", ".join(f"{k}={getattr(self, k)!r}" for k in type(self).__env_vars__)
        return f"{type(self).__name__}({pairs})"

    @staticmethod
    def _load_env_file(env_path: str) -> None:
        if not os.path.isfile(env_path):
            env_path = dotenv.find_dotenv(env_path, usecwd=True)
            if not env_path:
                return
        dotenv.load_dotenv(env_path)

    @classmethod
    def schema(cls) -> list[FieldSchema]:
        """
        Returns a description of every declared field.

        Each entry is a :class:`FieldSchema` TypedDict with the keys:
            - `attr`
            - `env_var`
            - `type`
            - `required`
            - `secret`
            - `default` (optional, omitted when required)
            - `extra` (type-specific medatata)

        Example
        -------
        ```py
            for field in MyEnv.schema():
                print(field["env_var"], "->", field["type"])
        ```
        """
        prefix = cls.__env_prefix__
        result: list[FieldSchema] = []

        for (
            attr,
            var,
        ) in cls.__env_vars__.items():
            effective = var.var_name if var.var_name else f"{prefix}{attr}"
            required = var.default is _MISSING

            entry: FieldSchema = {
                "attr": attr,
                "env_var": effective,
                "type": var.type_label,
                "required": required,
                "secret": var.secret,
                "extra": var.extra,
            }
            if not required:
                entry["default"] = var.default

            result.append(entry)

        return result
