"""Platform-specific utilities."""

from udm.platform.admin import is_admin, request_admin
from udm.platform.command import command_exists, run_command
from udm.platform.detect import (
    detect_os,
    is_linux,
    is_mac,
    is_termux,
    is_windows,
    os_label,
    termux_prefix,
)
from udm.platform.path import add_to_path, resolve_env_path

__all__ = [
    "detect_os",
    "is_windows",
    "is_linux",
    "is_mac",
    "is_termux",
    "os_label",
    "termux_prefix",
    "is_admin",
    "request_admin",
    "add_to_path",
    "resolve_env_path",
    "run_command",
    "command_exists",
]
