"""Admin / privilege helpers."""

import os
import shutil
import sys

from udm.platform.detect import is_termux, is_windows


def is_admin() -> bool:
    """Return True if the process has elevated privileges."""
    if is_windows():
        try:
            import ctypes

            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        except Exception:
            return False
    else:
        return os.geteuid() == 0


def request_admin():
    """Relaunch the current script with admin / root privileges."""
    if is_windows():
        import ctypes

        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(sys.argv), None, 1
        )
        sys.exit(0)
    if is_termux():
        raise RuntimeError("Privilege escalation is not supported on Termux.")
    if os.geteuid() == 0:
        return
    for launcher in ("pkexec", "sudo"):
        if shutil.which(launcher):
            os.execvp(launcher, [launcher, sys.executable, *sys.argv])
    raise RuntimeError("No supported privilege escalation helper was found.")
