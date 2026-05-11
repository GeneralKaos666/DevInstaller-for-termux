"""Platform prerequisites — Homebrew, apt, and pkg index setup."""

from udm.installer.callbacks import log
from udm.platform import command_exists, is_linux, is_mac, is_termux, run_command


def ensure_homebrew():
    """On macOS, install Homebrew if it is not present."""
    if is_mac() and not command_exists("brew"):
        log("  Homebrew not found — installing…")
        cmd = '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
        rc, out, err = run_command(cmd, timeout=300)
        if rc != 0:
            log(f"  ⚠ Homebrew install failed: {err[:200]}")
        else:
            log("  ✓ Homebrew installed.")


def ensure_apt_updated():
    """Refresh the active Linux package index once per session."""
    if not hasattr(ensure_apt_updated, "_done"):
        if is_linux() and is_termux():
            update_cmd = "pkg update -y" if command_exists("pkg") else "apt update -y"
            log("  Updating Termux package index…")
        else:
            update_cmd = "sudo apt-get update -y"
            log("  Updating apt package index…")
        run_command(update_cmd, timeout=120)
        ensure_apt_updated._done = True
