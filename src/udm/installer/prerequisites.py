"""Platform prerequisites — Homebrew and apt-get update."""

from udm.installer.callbacks import log
from udm.platform import command_exists, is_linux, is_mac, is_termux, run_command

_package_index_updated = False


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
    """Run `sudo apt-get update` once per session on Linux."""
    global _package_index_updated

    if _package_index_updated or not is_linux():
        return

    cmd = "pkg update -y" if is_termux() else "sudo apt-get update -y"
    log("  Updating package index…")
    rc, _, err = run_command(cmd, timeout=120)
    if rc != 0:
        log(f"  ⚠ Package index update failed: {err[:200]}")
        return
    _package_index_updated = True
