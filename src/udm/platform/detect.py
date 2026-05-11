"""OS detection utilities."""

import os
import platform
from pathlib import Path

TERMUX_PREFIX = "/data/data/com.termux/files/usr"


def detect_os() -> str:
    """Return 'Windows', 'Linux', or 'Darwin' (macOS)."""
    system = platform.system()
    if system == "Android":
        return "Linux"
    return system


def is_windows() -> bool:
    return detect_os() == "Windows"


def is_linux() -> bool:
    return detect_os() == "Linux"


def is_mac() -> bool:
    return detect_os() == "Darwin"


def is_termux() -> bool:
    """Return True when running inside a Termux userland."""
    prefix = os.environ.get("PREFIX", "")
    return is_linux() and (
        "TERMUX_VERSION" in os.environ
        or prefix.startswith(TERMUX_PREFIX)
        or (Path(TERMUX_PREFIX) / "bin" / "pkg").exists()
    )


def termux_prefix() -> str:
    """Return the active Termux prefix."""
    return os.environ.get("PREFIX", TERMUX_PREFIX)


def os_label() -> str:
    """Return a human-friendly OS name."""
    if is_termux():
        return "Termux (Android)"
    mapping = {"Windows": "Windows", "Linux": "Linux", "Darwin": "macOS"}
    return mapping.get(detect_os(), detect_os())
