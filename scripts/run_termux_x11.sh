#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(dirname "$SCRIPT_DIR")"
TERMUX_PREFIX="${PREFIX:-/data/data/com.termux/files/usr}"

export PYTHONPATH="$ROOT/src${PYTHONPATH:+:$PYTHONPATH}"

exec "$TERMUX_PREFIX/bin/python3" "$ROOT/main.py" "$@"
