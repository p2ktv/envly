from __future__ import annotations

import os
import pathlib


__all__ = ["_load_env_file"]


def _load_env_file(env_path: str | pathlib.Path) -> None:
    """
    Loads a .env file into :attr:`os.environ`.

    If param:`env_path` has no directory component, searches upward
    from cwd through parent directories until the file is found or the
    filesystem root is reached.

    Supports:
        - KEY=VALUE
        - KEY="VALUE"
        - KEY='VALUE'
        - export KEY=VALUE
        - inline comments

    Parameters
    ----------
    env_path: :class:`str` | :class:`pathlib.Path`
        The path to check.
    """
    path = pathlib.Path(env_path)

    # Search upward from cwd
    if path.parent == pathlib.Path("."):
        current = pathlib.Path.cwd()
        while True:
            candidate = current / path
            if candidate.is_file():
                path = candidate
                break
            parent = current.parent
            if parent == current:
                return  # reached filesystem root
            current = parent

    if not path.is_file():
        return

    with path.open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()

            # Skip blank lines and comments
            if not line or line.startswith("#"):
                continue

            if line.startswith("export "):
                line = line[7:].lstrip()

            # Every line must contain '='
            if "=" not in line:
                continue

            key, _, raw_value = line.partition("=")
            key = key.strip()
            value = _parse_value(raw_value)

            if key and key not in os.environ:
                os.environ[key] = value


def _parse_value(raw: str) -> str:
    """
    Strips quotes and inline comments from a raw .env value.

    Parameters
    ----------
    raw: :class:`str`
        The raw .env value.

    Returns
    -------
    :class:`str`
        The parsed value.
    """
    raw = raw.strip()

    if raw and raw[0] in ('"', "'"):
        quote = raw[0]
        closing = raw.find(quote, 1)
        if closing != -1:
            return raw[1:closing]

    # Strip inline comment (unqouted)
    comment_idx = raw.find(" #")
    if comment_idx != -1:
        raw = raw[:comment_idx]

    return raw.strip()
