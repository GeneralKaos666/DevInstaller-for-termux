"""Configuration loader for tools.json."""

import json
import sys
from pathlib import Path
from typing import Any

from udm.logger import logger


def _get_base_dir() -> Path:
    """Return the base directory — sys._MEIPASS when frozen by PyInstaller."""
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS)
    return Path(__file__).resolve().parent.parent.parent


TOOLS_JSON_PATH = _get_base_dir() / "tools.json"
_STRING_FIELDS = (
    "key",
    "name",
    "description",
    "category",
    "detect_cmd",
    "detect_cmd_alt",
    "install_command_windows",
    "install_command_linux",
    "install_command_mac",
    "install_command_termux",
)
_PATH_FIELDS = (
    "path_dirs_windows",
    "path_dirs_linux",
    "path_dirs_mac",
    "path_dirs_termux",
)


def _is_str_list(value: Any) -> bool:
    return isinstance(value, list) and all(isinstance(item, str) for item in value)


def _validate_tool(entry: Any, index: int) -> dict[str, Any] | None:
    """Validate a single tools.json entry."""
    if not isinstance(entry, dict):
        logger.error(f"tools.json entry {index} is not an object; skipping it.")
        return None
    if not isinstance(entry.get("name"), str) or not entry["name"].strip():
        logger.error(f"tools.json entry {index} is missing a valid 'name'; skipping it.")
        return None
    for field in _STRING_FIELDS:
        value = entry.get(field)
        if value is not None and not isinstance(value, str):
            logger.error(
                f"tools.json entry {index} has non-string field '{field}'; skipping it."
            )
            return None
    for field in _PATH_FIELDS:
        value = entry.get(field)
        if value is not None and not _is_str_list(value):
            logger.error(
                f"tools.json entry {index} has invalid '{field}'; expected a list of strings."
            )
            return None
    path_required = entry.get("path_required")
    if path_required is not None and not isinstance(path_required, bool):
        logger.error(
            f"tools.json entry {index} has invalid 'path_required'; expected true/false."
        )
        return None
    return entry


def load_tools() -> list[dict]:
    """Load and return the tools list from tools.json."""
    try:
        with open(TOOLS_JSON_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, list):
            raise ValueError("tools.json must contain a top-level array")
        validated: list[dict] = []
        for index, entry in enumerate(data, start=1):
            tool = _validate_tool(entry, index)
            if tool is not None:
                validated.append(tool)
        logger.info(f"Loaded {len(validated)} tools from tools.json")
        return validated
    except Exception as e:
        logger.error(f"Failed to load tools.json: {e}")
        return []


def get_categories(tools: list[dict]) -> list[str]:
    """Return a sorted list of unique category names."""
    return sorted({t.get("category", "Other") for t in tools})
