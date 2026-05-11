#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(dirname "$SCRIPT_DIR")"
DIST="$ROOT/dist"
BUILD="$ROOT/build/termux-deb"
PKG_ROOT="$BUILD/pkg-root"
CONTROL_DIR="$PKG_ROOT/DEBIAN"
TERMUX_PREFIX="${PREFIX:-/data/data/com.termux/files/usr}"
PREFIX_REL="${TERMUX_PREFIX#/}"
APP_DIR_REL="$PREFIX_REL/lib/devinstaller"
BIN_DIR_REL="$PREFIX_REL/bin"

echo "=== Building Termux .deb ==="

python3 "$ROOT/scripts/sync_version.py"

VERSION="$(
    ROOT="$ROOT" python3 - <<'PY'
import os
import re
from pathlib import Path

root = Path(os.environ["ROOT"])
content = (root / "meson.build").read_text(encoding="utf-8")
match = re.search(r"version:\s*'([0-9A-Za-z.\-]+)'", content)
if not match:
    raise SystemExit("Could not parse version from meson.build")
print(match.group(1))
PY
)"
ARCH="$(dpkg --print-architecture)"
PACKAGE="devinstaller"
OUTPUT="$DIST/${PACKAGE}_${VERSION}_${ARCH}.deb"

rm -rf "$BUILD"
mkdir -p "$CONTROL_DIR" "$PKG_ROOT/$APP_DIR_REL" "$PKG_ROOT/$BIN_DIR_REL" "$DIST"
chmod 755 "$PKG_ROOT" "$CONTROL_DIR"

cp "$ROOT/main.py" "$PKG_ROOT/$APP_DIR_REL/"
cp "$ROOT/tools.json" "$PKG_ROOT/$APP_DIR_REL/"
cp "$ROOT/LICENSE" "$PKG_ROOT/$APP_DIR_REL/"
cp -R "$ROOT/src" "$PKG_ROOT/$APP_DIR_REL/"
find "$PKG_ROOT/$APP_DIR_REL" -type d -name "__pycache__" -prune -exec rm -rf {} +
find "$PKG_ROOT/$APP_DIR_REL" -type f \( -name "*.pyc" -o -name "*.pyo" \) -delete
find "$PKG_ROOT/$PREFIX_REL" -type d -exec chmod 755 {} +
find "$PKG_ROOT/$PREFIX_REL" -type f -exec chmod 644 {} +

cat >"$PKG_ROOT/$BIN_DIR_REL/devinstaller" <<'EOF'
#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

TERMUX_PREFIX="${PREFIX:-/data/data/com.termux/files/usr}"
APP_DIR="$TERMUX_PREFIX/lib/devinstaller"

export PYTHONPATH="$APP_DIR/src${PYTHONPATH:+:$PYTHONPATH}"

exec "$TERMUX_PREFIX/bin/python3" "$APP_DIR/main.py" "$@"
EOF
chmod 755 "$PKG_ROOT/$BIN_DIR_REL/devinstaller"

INSTALLED_SIZE="$(du -sk "$PKG_ROOT/$PREFIX_REL" | cut -f1)"

cat >"$CONTROL_DIR/control" <<EOF
Package: $PACKAGE
Version: $VERSION
Architecture: $ARCH
Maintainer: DevInstaller contributors
Depends: bash, python, pyside6, termux-x11-nightly
Installed-Size: $INSTALLED_SIZE
Homepage: https://github.com/GeneralKaos666/DevInstaller-for-termux
Description: Cross-platform developer tool installer for Termux:X11
 A Qt-based GUI for browsing and installing developer tools from a
 Termux:X11 session.
 .
 Start termux-x11 before launching the app with the devinstaller command.
EOF

(
    cd "$PKG_ROOT"
    find "$PREFIX_REL" -type f -print0 | xargs -0 md5sum >"$CONTROL_DIR/md5sums"
)

if dpkg-deb --help | grep -q -- "--root-owner-group"; then
    dpkg-deb --root-owner-group --build "$PKG_ROOT" "$OUTPUT"
else
    dpkg-deb --build "$PKG_ROOT" "$OUTPUT"
fi

echo "=== Termux package created at $OUTPUT ==="
