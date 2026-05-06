"""Application entry point."""

import os
import site
import sys
from pathlib import Path

from udm.cli import create_parser, run_cli
from udm.logger import logger
from udm.platform import (
    has_graphical_display,
    is_admin,
    is_termux,
    is_windows,
    request_admin,
)


def _add_termux_site_packages() -> bool:
    """Expose Termux's system site-packages inside uv's virtualenv."""
    if not is_termux():
        return False

    prefix = os.environ.get("PREFIX")
    if not prefix:
        return False

    version = f"python{sys.version_info.major}.{sys.version_info.minor}"
    system_site_packages = Path(prefix) / "lib" / version / "site-packages"
    if not system_site_packages.is_dir():
        return False

    site.addsitedir(str(system_site_packages))
    return True


def main(argv: list[str] | None = None) -> int:
    parser = create_parser()
    args = parser.parse_args(argv)

    logger.info("═══ DevInstaller started ═══")

    if is_windows() and not is_admin():
        if args.elevate:
            logger.info("Requesting UAC elevation…")
            try:
                request_admin()
            except Exception:
                logger.warning("UAC elevation failed — continuing without admin.")
        else:
            logger.warning(
                "Running without admin privileges. "
                "Some installations may need admin. "
                "Relaunch with --elevate for full access."
            )

    if args.cli or not has_graphical_display():
        if not args.cli and is_termux():
            print("Termux uses CLI mode — launching without the Qt GUI.")
        return run_cli(args)

    _add_termux_site_packages()

    try:
        from PySide6.QtWidgets import QApplication
    except ModuleNotFoundError as exc:
        if exc.name not in {"PySide6", "shiboken6"}:
            raise
        logger.warning("PySide6 is not installed; falling back to CLI mode.")
        if is_termux():
            print("Install the Termux 'pyside6' package to enable GUI mode in Termux-X11.")
        return run_cli(args)

    from udm.gui import MainWindow

    app = QApplication([sys.argv[0], *(argv or sys.argv[1:])])
    window = MainWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
