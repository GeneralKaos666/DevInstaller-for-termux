# DevInstaller

DevInstaller is a cross-platform desktop application that lets developers search, select, and install programming languages, compilers, SDKs, and developer tools from a comprehensive catalog — all from a single, premium Qt-based GUI.

## About

DevInstaller simplifies the setup process for developers by providing a unified interface to install tools across different operating systems. It uses native package managers (`winget`, `apt`, `brew`) and automatically handles PATH configurations, ensuring your environment is ready to use without manual tweaking.

## Features

- **Cross-Platform:** Works on Windows, Linux, and macOS using native package managers.
- **Smart Install:** Automatically skips installed tools to save time.
- **Configurable:** Easily customize the available tools by editing `tools.json`.

## Installation & Usage

### Requirements
- **Python 3.10+**
- **[uv](https://docs.astral.sh/uv/)**

*Note: On Windows, it is recommended to run elevated: `uv run python -m udm --elevate`*

### Running on Termux + Termux:X11

Install the runtime packages, start a Termux:X11 session, then launch the app:

```bash
pkg install -y python pyside6 termux-x11-nightly
termux-x11 :0 &
bash scripts/run_termux_x11.sh
```

The launcher sets the Python import path for the checkout, and the app now defaults to the Qt6 plugin directories and `DISPLAY=:0` layout used by Termux:X11.

## Building Distributables

### Using Meson

```bash
meson setup builddir
meson compile -C builddir build-exe       # Windows .exe
meson compile -C builddir build-appimage  # Linux AppImage
meson compile -C builddir build-dmg       # macOS .dmg
meson compile -C builddir build-termux-deb  # Termux .deb
```

### Building a Termux package directly

```bash
bash scripts/build_termux_deb.sh
```

This creates a local `.deb` in `dist/` that installs a `devinstaller` launcher plus the bundled application tree under the Termux prefix.

## License

DevInstaller is licensed under the MIT License. See the [`LICENSE`](LICENSE) file for more information.
