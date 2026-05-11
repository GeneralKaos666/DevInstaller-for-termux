"""Application entry point."""

import os
import sys
from pathlib import Path

from udm.logger import logger
from udm.platform import is_admin, is_termux, is_windows, request_admin, termux_prefix


def _configure_termux_runtime():
    """Set sensible Qt defaults for Termux:X11 sessions."""
    if not is_termux():
        return

    prefix = Path(termux_prefix())
    os.environ.setdefault("PREFIX", str(prefix))
    os.environ.setdefault("DISPLAY", ":0")
    os.environ.setdefault("QT_QPA_PLATFORM", "xcb")
    os.environ.setdefault("QT_PLUGIN_PATH", str(prefix / "lib" / "qt6" / "plugins"))
    os.environ.setdefault("QML2_IMPORT_PATH", str(prefix / "lib" / "qt6" / "qml"))

    runtime_value = os.environ.get("XDG_RUNTIME_DIR")
    runtime_dir = (
        Path(runtime_value)
        if runtime_value
        else Path(os.environ.get("TMPDIR", str(prefix / "tmp"))) / "devinstaller-runtime"
    )
    runtime_dir.mkdir(parents=True, exist_ok=True)
    try:
        runtime_dir.chmod(0o700)
    except OSError as exc:
        logger.warning(f"Could not set permissions on {runtime_dir}: {exc}")
    os.environ.setdefault("XDG_RUNTIME_DIR", str(runtime_dir))


def main():
    logger.info("═══ DevInstaller started ═══")
    _configure_termux_runtime()

    if is_windows() and not is_admin():
        if "--elevate" in sys.argv:
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

    from PySide6.QtWidgets import QApplication

    from udm.gui import MainWindow

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
