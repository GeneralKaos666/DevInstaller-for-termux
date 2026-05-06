"""OS and runtime detection utilities."""

import os
import platform


def detect_os() -> str:
    """Return the platform.system() value for the current runtime."""
    return platform.system()


def is_windows() -> bool:
    return detect_os() == "Windows"


def is_linux() -> bool:
    return detect_os() in {"Linux", "Android"}


def is_mac() -> bool:
    return detect_os() == "Darwin"


def is_termux() -> bool:
    """Return True when running inside Termux."""
    prefix = os.environ.get("PREFIX", "")
    return is_linux() and (
        "com.termux" in prefix
        or "TERMUX_VERSION" in os.environ
        or prefix.endswith("/com.termux/files/usr")
    )


def has_graphical_display() -> bool:
    """Return True if the current session exposes a GUI display."""
    if is_windows():
        return True
    if is_mac():
        return True
    return bool(os.environ.get("DISPLAY") or os.environ.get("WAYLAND_DISPLAY"))


def os_label() -> str:
    """Return a human-friendly OS name."""
    if is_termux():
        return "Termux"
    mapping = {
        "Windows": "Windows",
        "Linux": "Linux",
        "Android": "Android",
        "Darwin": "macOS",
    }
    return mapping.get(detect_os(), detect_os())
