from __future__ import annotations

import pathlib
import re
import urllib.parse
from typing import Callable, Any

from env_typed.errors import EnvError


_BOOL_TRUE = frozenset({"1", "true", "yes", "on"})
_BOOL_FALSE = frozenset({"0", "false", "no", "off"})

_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def _coerce_str(name: str, raw: str) -> str:
    return raw


def _coerce_int(name: str, raw: str) -> int:
    try:
        return int(raw)
    except ValueError:
        raise EnvError(f"[{name}] expected an integer, got {raw!r}") from None


def _coerce_float(name: str, raw: str) -> float:
    try:
        return float(raw)
    except ValueError:
        raise EnvError(f"[{name}] expected a float, got {raw!r}") from None


def _coerce_bool(name: str, raw: str) -> bool:
    lower = raw.strip().lower()
    if lower in _BOOL_TRUE:
        return True
    if lower in _BOOL_FALSE:
        return False
    raise EnvError(
        f"[{name}] expected a boolean (true/false/1/0/yes/no/on/off), got {raw!r}"
    )


def _coerce_bytes(name: str, raw: str) -> bytes:
    try:
        value = raw.lower().removeprefix("0x")
        if len(value) % 2:
            value = "0" + value
        return bytes.fromhex(value)
    except Exception as exc:
        raise EnvError(f"[{name}] expected bytes, got {raw!r}") from exc


def _coerce_url(name: str, raw: str) -> str:
    parsed = urllib.parse.urlparse(raw)
    if not parsed.scheme or not parsed.netloc:
        raise EnvError(
            f"[{name}] expected a valid URL with scheme and host, got {raw!r}"
        )
    return raw


def _coerce_path(name: str, raw: str) -> pathlib.Path:
    return pathlib.Path(raw)


def _coerce_email(name: str, raw: str) -> str:
    if not _EMAIL_RE.match(raw):
        raise EnvError(f"[{name}] expected a valid email address, got {raw!r}")
    return raw


def _make_enum_coercer(choices: tuple[str, ...]) -> Callable[[str, str], str]:
    choice_set = frozenset(choices)

    def _coerce_enum(name: str, raw) -> str:
        if raw not in choice_set:
            formatted = ", ".join(repr(c) for c in choices)
            raise EnvError(f"[{name}] expected one of {formatted}, got {raw!r}")
        return raw

    return _coerce_enum


def _make_regex_coercer(pattern: str | re.Pattern[str]) -> Callable[[str, str], str]:
    compiled = re.compile(pattern) if isinstance(pattern, str) else pattern

    def _coerce_regex(name: str, raw: str) -> str:
        if not compiled.fullmatch(raw):
            raise EnvError(
                f"[{name}] value {raw!r} does not match pattern {compiled.pattern!r}"
            )
        return raw

    return _coerce_regex


def _make_json_coercer(type_check: type | None) -> Callable[[str, str], Any]:
    import json

    def _coerce_json(name: str, raw: str) -> Any:
        try:
            value = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise EnvError(f"[{name}] invalid JSON: {exc}") from None
        if type_check is not None and not isinstance(value, type_check):
            raise EnvError(
                f"[{name}] expected JSON root to be {type_check.__name__}, got {type(value).__name__}"
            )
        return value

    return _coerce_json


def _make_list_coercer(
    sub_coerce: Callable[[str, str], Any], sep: str
) -> Callable[[str, str], list[Any]]:
    def _coerce_list(name: str, raw: str) -> list[Any]:
        return [
            sub_coerce(f"{name}[{i}]", item.strip())
            for i, item in enumerate(raw.split(sep))
        ]

    return _coerce_list


_PRIMITIVE_COERCERS: dict[type, Callable[[str, str], Any]] = {
    str: _coerce_str,
    int: _coerce_int,
    float: _coerce_float,
    bool: _coerce_bool,
    bytes: _coerce_bytes,
}
