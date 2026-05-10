"""Logging configuration."""

import logging
import sys
from pathlib import Path


def _log_file_path() -> Path:
    if getattr(sys, "frozen", False):
        return Path.home() / ".universal_dev_manager.log"
    return Path(__file__).resolve().parent.parent.parent / "installer.log"


import io

_handlers = [logging.FileHandler(_log_file_path(), encoding="utf-8")]

if sys.stdout is not None:
    _stream = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    _handlers.append(logging.StreamHandler(_stream))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=_handlers,
)

logger = logging.getLogger("UniversalDevManager")
