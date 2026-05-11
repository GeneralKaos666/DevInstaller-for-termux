"""Core installation engine — detect, install, and configure PATH."""

import platform

from udm.installer.callbacks import log
from udm.installer.prerequisites import ensure_apt_updated, ensure_homebrew
from udm.platform import (
    add_to_path,
    is_linux,
    is_mac,
    is_termux,
    is_windows,
    resolve_env_path,
    run_command,
)

TERMUX_PACKAGE_ALIASES = {
    "python3": "python",
    "python3-pip": "python-pip",
    "python3-venv": "",
    "python3.11": "python",
    "python3.11-venv": "",
    "ninja-build": "ninja",
    "golang-go": "golang",
    "openjdk-17-jdk": "openjdk-17",
    "openjdk-21-jdk": "openjdk-21",
    "php-cli": "",
    "php-mbstring": "",
    "ruby-full": "ruby",
    "p7zip-full": "p7zip",
    "fd-find": "fd",
    "protobuf-compiler": "protobuf",
    "mysql-server": "mariadb",
    "postgresql-client": "",
    "redis-server": "redis",
}

TERMUX_DETECT_OVERRIDES = {
    "python311": "python --version",
}

APT_INSTALL_PREFIXES = (
    "sudo apt-get install -y ",
    "apt-get install -y ",
    "sudo apt install -y ",
    "apt install -y ",
)


def _map_termux_packages(packages: list[str]) -> list[str]:
    """Translate Debian package names to their Termux equivalents."""
    mapped_packages: list[str] = []
    for package in packages:
        mapped = TERMUX_PACKAGE_ALIASES.get(package, package)
        if not mapped or mapped in mapped_packages:
            continue
        mapped_packages.append(mapped)
    return mapped_packages


def _rewrite_termux_install_cmd(cmd: str) -> str:
    """Rewrite Debian-style install commands to their Termux form."""
    for prefix in APT_INSTALL_PREFIXES:
        if cmd.startswith(prefix):
            packages = cmd[len(prefix) :].split()
            mapped_packages = _map_termux_packages(packages)
            if not mapped_packages:
                return ""
            return f"pkg install -y {' '.join(mapped_packages)}"
    return cmd


def _detect_commands(tool: dict) -> list[str]:
    """Return detection commands in preferred order for the active platform."""
    commands: list[str] = []

    if is_termux():
        override = tool.get("detect_cmd_termux", "")
        if override:
            commands.append(override)

        alias = TERMUX_DETECT_OVERRIDES.get(tool.get("key", ""))
        if alias:
            commands.append(alias)

    detect_cmd = tool.get("detect_cmd", "")
    if detect_cmd:
        commands.append(detect_cmd)

    alt = tool.get("detect_cmd_alt", "")
    if alt:
        commands.append(alt)

    return commands


def _get_install_cmd(tool: dict) -> str:
    """Return the install command for the current platform, or '' if none."""
    cmd = ""
    if is_windows():
        cmd = tool.get("install_command_windows", "")
        if cmd.startswith("winget") and "--disable-interactivity" not in cmd:
            cmd += " --disable-interactivity"
    elif is_linux():
        if is_termux():
            cmd = tool.get("install_command_termux", "")
            if cmd:
                return cmd
        cmd = tool.get("install_command_linux", "")
        if is_termux():
            cmd = _rewrite_termux_install_cmd(cmd)
    elif is_mac():
        cmd = tool.get("install_command_mac", "")
    return cmd


def detect_tool(tool: dict) -> bool:
    """Return True if the tool is already present on the system."""
    for command in _detect_commands(tool):
        rc, _, _ = run_command(command, timeout=15)
        if rc == 0:
            return True
    return False


def install_tool(tool: dict) -> bool:
    """Install a single tool using the platform install command."""
    name = tool.get("name", "Unknown")
    cmd = _get_install_cmd(tool)

    if not cmd:
        log(f"  ⚠ No install command for {name} on {platform.system()}")
        return False

    if is_mac():
        ensure_homebrew()
    if is_linux() and (
        cmd.startswith("sudo apt")
        or cmd.startswith("apt ")
        or cmd.startswith("apt-get ")
        or cmd.startswith("pkg ")
    ):
        ensure_apt_updated()

    log(f"  Running: {cmd}")
    rc, out, err = run_command(cmd, timeout=900)

    combined = (out + err).lower()
    if rc == 0:
        return True
    if (
        "already installed" in combined
        or "no upgrade" in combined
        or "is already the newest" in combined
    ):
        log(f"  {name} appears already installed (package manager says so).")
        return True

    out_clean = "\n".join(line.strip() for line in out.splitlines() if line.strip())
    err_clean = "\n".join(line.strip() for line in err.splitlines() if line.strip())
    
    log(f"  stdout: {out_clean[-1000:]}")
    if err_clean:
        log(f"  stderr: {err_clean[-1000:]}")
    return False


def setup_path(tool: dict) -> bool:
    """Add required directories to PATH for the given tool."""
    if not tool.get("path_required", False):
        return True

    if is_windows():
        dirs = tool.get("path_dirs_windows", [])
    elif is_termux():
        dirs = tool.get("path_dirs_termux") or tool.get("path_dirs_linux", [])
    elif is_linux():
        dirs = tool.get("path_dirs_linux", [])
    else:
        dirs = tool.get("path_dirs_mac", [])

    if not dirs:
        return True

    ok = True
    for d in dirs:
        resolved = resolve_env_path(d)
        log(f"  PATH → {resolved}")
        if not add_to_path(resolved):
            log(f"  ⚠ Could not add {resolved} to PATH")
            ok = False
    return ok
