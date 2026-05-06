"""Terminal-friendly interface for headless and Termux environments."""

from __future__ import annotations

import argparse
from typing import Iterable

from udm.config import get_categories, load_tools
from udm.installer import install_selected


def create_parser() -> argparse.ArgumentParser:
    """Build the shared argument parser."""
    parser = argparse.ArgumentParser(
        prog="devinstaller",
        description="Install developer tools from the DevInstaller catalog.",
    )
    parser.add_argument(
        "--cli",
        action="store_true",
        help="Run in terminal mode instead of the Qt GUI.",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List available tools after applying any filters.",
    )
    parser.add_argument(
        "--search",
        metavar="TEXT",
        help="Filter tools by key, name, description, or category.",
    )
    parser.add_argument(
        "--category",
        metavar="NAME",
        help="Filter tools by category name.",
    )
    parser.add_argument(
        "--install",
        nargs="+",
        metavar="KEY",
        help="Install one or more tools by key.",
    )
    parser.add_argument(
        "--elevate",
        action="store_true",
        help="Request elevated privileges where supported.",
    )
    return parser


def _filter_tools(
    tools: list[dict], search: str | None = None, category: str | None = None
) -> list[dict]:
    """Filter tools by search text and category."""
    query = (search or "").strip().lower()
    selected_category = (category or "").strip().lower()

    filtered: list[dict] = []
    for tool in tools:
        tool_category = str(tool.get("category", "Other"))
        haystack = " ".join(
            [
                str(tool.get("key", "")),
                str(tool.get("name", "")),
                str(tool.get("description", "")),
                tool_category,
            ]
        ).lower()
        if query and query not in haystack:
            continue
        if selected_category and tool_category.lower() != selected_category:
            continue
        filtered.append(tool)
    return filtered


def _print_tools(tools: Iterable[dict]) -> None:
    """Print a compact tool listing."""
    for tool in tools:
        key = str(tool.get("key", ""))
        name = str(tool.get("name", key))
        category = str(tool.get("category", "Other"))
        print(f"{key:<18} {name} [{category}]")


def _print_categories(tools: list[dict]) -> None:
    """Print known categories."""
    categories = ", ".join(get_categories(tools))
    print(f"Categories: {categories}")


def run_cli(args: argparse.Namespace) -> int:
    """Execute the terminal workflow."""
    tools = load_tools()
    filtered = _filter_tools(tools, args.search, args.category)

    if args.list:
        if not filtered:
            print("No tools matched the current filters.")
            return 0
        _print_tools(filtered)
        return 0

    if args.install:
        selected_by_key = {str(tool.get("key", "")): tool for tool in tools}
        requested: list[dict] = []
        missing: list[str] = []
        for key in args.install:
            tool = selected_by_key.get(key)
            if tool is None:
                missing.append(key)
                continue
            requested.append(tool)
        if missing:
            print(f"Unknown tool key(s): {', '.join(missing)}")
            return 1
        if args.search or args.category:
            allowed_keys = {str(tool.get("key", "")) for tool in filtered}
            requested = [
                tool
                for tool in requested
                if str(tool.get("key", "")) in allowed_keys
            ]
            if not requested:
                print("No requested tools matched the active filters.")
                return 1
        results = install_selected(requested)
        return 0 if all(status != "failed" for status in results.values()) else 1

    print("CLI mode is active.")
    _print_categories(tools)
    print("Use --list to browse tools or --install <key ...> to install them.")
    return 0
