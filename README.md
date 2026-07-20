# Paste Links

[![CI](https://github.com/imz87/paste-links/actions/workflows/ci.yml/badge.svg)](https://github.com/imz87/paste-links/actions/workflows/ci.yml)

Add a `Paste Symlink` action to GNOME Files on Fedora and other Nautilus-based desktops.

The extension reads Nautilus's copied-files clipboard payload after a normal `Ctrl+C` and creates symbolic links in the folder you right-clicked.

### Quick Links

- [Latest Release](https://github.com/imz87/paste-links/releases/latest)
- [Installation Guide](#install)
- [COPR Repository (Fedora)](#copr-install-fedora)
- [PPA Repository (Ubuntu/Debian)](#ppaapt-repository-ubuntudebian)
- [Report a Bug](https://github.com/imz87/paste-links/issues)
- [Sponsor / Donate](https://github.com/sponsors/imz87)

## Features

- Supports multiple copied files and folders.
- Uses the normal GNOME Files copy flow.
- Creates symbolic links instead of duplicating file contents.
- Hides the menu item when the clipboard does not contain copied files.
- Shows a small error dialog for invalid clipboard cases as a fallback.
- Handles name collisions with `-link`, `-link-2`, and so on.

## Current Scope

- Supported source items: local `file://` URIs only
- Supported destination: local folders only
- Supported clipboard mode: `copy` only
- Unsupported in v1:
  - `Ctrl+X` / cut clipboard entries
  - remote URIs such as `sftp://`, `smb://`, and `trash://`
  - GNOME Shell integration

## CI and Tested Distributions

GitHub Actions CI runs automated checks across five distributions:

| Distribution | Container Image |
|---|---|
| Fedora (latest) | `fedora:latest` |
| Ubuntu (latest LTS) | `ubuntu:24.04` |
| Debian (stable) | `debian:bookworm` |
| Arch Linux (latest) | `archlinux:latest` |
| openSUSE Tumbleweed | `opensuse/tumbleweed:latest` |

CI verifies Python syntax, shell script syntax, and pure unit tests in each container. Container CI does **not** replace manual Nautilus desktop verification. The Nautilus context menu, clipboard integration, and Wayland behavior still require a real desktop session.

## Dependencies

This extension requires a Nautilus 4 desktop with GTK 4, PyGObject, and the **Nautilus Python extension loader** (`nautilus-python`). The loader is the package that tells Nautilus how to load `.py` files from the extensions directory. Without it, installed extension files are silently ignored.

The extension supports Nautilus GI namespace versions 4.0 and 4.1. On systems where the nautilus-python loader pre-loads a newer namespace version (e.g. 4.1 on Fedora 43+), the extension handles this automatically. Verified on Fedora 42 (Nautilus 4.0) and Fedora 43+ (Nautilus 4.1).

### Fedora

```bash
sudo dnf install nautilus-python python3-gobject gtk4
```

### Ubuntu / Debian

```bash
sudo apt install python3-nautilus gir1.2-nautilus-4.0 python3-gi gir1.2-gtk-4.0
```

Package names may vary by Ubuntu/Debian release. Check that `libnautilus-python.so` is available on your system.

### Arch Linux / Manjaro

```bash
sudo pacman -S nautilus python-gobject gtk4
```

### openSUSE

```bash
sudo zypper install nautilus-python python3-gobject gtk4
```

Support on non-Fedora distributions is conditional and depends on having compatible Nautilus 4, GTK 4, PyGObject, and a working Nautilus Python extension loader. Package names and availability may differ.

## Install

> **Important:** After installing by any method, restart Nautilus / GNOME Files for the extension to take effect. Run `nautilus -q` and reopen Files.

### Local Install

From this repository:

```bash
./install.sh
```

The script installs the extension files into:

```text
~/.local/share/nautilus-python/extensions/
```

**Restart Nautilus / GNOME Files for the extension to take effect:**

```bash
nautilus -q
```

Then reopen Files. The "Paste Symlink" menu will appear in the context menu.

### RPM Install

Build and install a Fedora RPM:

```bash
# Install build tools
sudo dnf install rpm-build rpmdevtools
rpmdev-setuptree

# Create source tarball
git archive --format=tar.gz --prefix=paste-links-0.1.0/ \
    HEAD -o ~/rpmbuild/SOURCES/paste-links-0.1.0.tar.gz

# Build the RPM
rpmbuild -ba packaging/paste-links.spec

# Install the RPM
sudo dnf install ~/rpmbuild/RPMS/noarch/paste-links-0.1.0-1.*.rpm
```

The RPM installs the extension files to the system-wide path:

```text
/usr/share/nautilus-python/extensions/
```

**Restart Nautilus / GNOME Files for the extension to take effect:**

```bash
nautilus -q
```

Then reopen Files. The "Paste Symlink" menu will appear in the context menu.

### COPR Install (Fedora)

For Fedora users, the easiest way to install is through the COPR repository:

```bash
sudo dnf copr enable imz87/paste-links
sudo dnf install paste-links
```

This provides automatic updates through `dnf`. **Restart Nautilus / GNOME Files for the extension to take effect:**

```bash
nautilus -q
```

Then reopen Files. The "Paste Symlink" menu will appear in the context menu.

**Uninstalling from COPR:**

```bash
sudo dnf remove paste-links
sudo dnf copr disable imz87/paste-links
nautilus -q
```

### RPM Uninstall

Remove the RPM package:

```bash
sudo dnf remove paste-links
```

After removal, **restart Nautilus / GNOME Files so the extension is no longer loaded:**

```bash
nautilus -q
```

See `.docs/project/packaging.md` for more details on RPM and COPR distribution.

### Release Artifacts

GitHub Releases provide pre-built packages for multiple distributions. These are downloadable installable artifacts, not native package repositories.

**Available formats:**
- **Fedora/RHEL**: `.rpm` package
- **Ubuntu/Debian**: `.deb` package
- **Arch Linux**: `.pkg.tar.zst` package
- **openSUSE**: `.rpm` package

**Installation from release artifacts:**

Fedora/RHEL:
```bash
sudo dnf install ./paste-links-*.rpm
```

Ubuntu/Debian:
```bash
sudo apt install ./paste-links_*.deb
```

Arch Linux:
```bash
sudo pacman -U paste-links-*.pkg.tar.zst
```

openSUSE:
```bash
sudo zypper install ./paste-links-*.rpm
```

After installation, **restart Nautilus / GNOME Files for the extension to take effect:**
```bash
nautilus -q
```
Then reopen Files. The "Paste Symlink" menu will appear in the context menu.

**Important:** Release artifacts are not the same as adding an apt/dnf/pacman/zypper repository. They do not provide automatic updates. You must download and install new versions manually from GitHub Releases.

### Package Signing

Release artifacts are signed with GPG. Each package file includes a corresponding `.asc` signature file.

**Verifying signatures:**

Download both the package and its `.asc` signature file, then verify:

Fedora/RHEL:
```bash
rpm --import paste-links-signing-key.asc
rpm --checksig paste-links-*.rpm
```

Ubuntu/Debian:
```bash
gpg --verify paste-links_*.deb.asc paste-links_*.deb
```

Arch Linux:
```bash
gpg --verify paste-links-*.pkg.tar.zst.asc paste-links-*.pkg.tar.zst
```

openSUSE:
```bash
rpm --import paste-links-signing-key.asc
rpm --checksig paste-links-*.rpm
```

**Signing key identity:** `Paste Links Release Signing <zolfaghari19@gmail.com>`

See `.docs/project/packaging.md` for details on the signing strategy and key management.

### PPA/apt Repository (Ubuntu/Debian)

For Ubuntu and Debian users, the extension is available through a PPA repository with automatic updates.

**Installation from PPA:**

```bash
sudo add-apt-repository ppa:imz87/paste-links
sudo apt update
sudo apt install paste-links
```

After installation, **restart Nautilus / GNOME Files for the extension to take effect:**
```bash
nautilus -q
```
Then reopen Files. The "Paste Symlink" menu will appear in the context menu.

**Uninstalling from PPA:**

```bash
sudo apt remove paste-links
sudo add-apt-repository --remove ppa:imz87/paste-links
nautilus -q
```

**Note:** The PPA provides automatic updates through `apt`. This is different from manually downloading release artifacts from GitHub Releases.

See `.docs/project/packaging.md` for details on PPA publishing and maintenance.

## Usage

1. In GNOME Files, select one or more files or folders.
2. Press `Ctrl+C`.
3. Navigate to another local folder.
4. Right-click empty space.
5. Choose `Paste Symlink` (only visible when the clipboard contains copied files).

If the clipboard does not contain copied local files, the menu item is hidden. An error dialog may still appear as a fallback if clipboard inspection fails.

## Uninstall

Remove the installed extension files and restart Nautilus / GNOME Files:

```bash
rm ~/.local/share/nautilus-python/extensions/paste_links.py \
   ~/.local/share/nautilus-python/extensions/core_logic.py
nautilus -q
```

## Development

- Source files:
  - `src/paste_links.py` - Nautilus/GTK integration entrypoint
  - `src/core_logic.py` - Pure symlink logic (testable without GTK/GDK/Nautilus)
- Installer: `install.sh`
- RPM packaging: `packaging/paste-links.spec`
- Project docs: `.docs/`

## Testing

Run the automated unit tests for the core shortcut logic:

```bash
python3 -m pytest tests/ -v
```

These tests cover:
- clipboard payload parsing
- link-name generation and collision handling
- symlink creation in temporary directories
- mixed supported/unsupported source URI handling

The tests do **not** require a live GNOME session, Nautilus, or clipboard access. Desktop integration (context menu, clipboard, dialogs) still requires manual verification.

## Manual Verification

1. Copy one local file and paste a symlink into another folder.
2. Copy one local folder and paste a symlink into another folder.
3. Copy multiple local items and verify one symlink is created per item.
4. Repeat with a conflicting destination name and verify `-link` suffixes are used.
5. Press `Ctrl+X` instead of `Ctrl+C` and verify the menu item is hidden.
6. Copy plain text from another app and verify the menu item is hidden.

## Troubleshooting

### Menu item does not appear

If the extension files are installed but `Paste Symlink` does not appear in the context menu:

1. **Check the loader is installed.** The `nautilus-python` package provides the shared library that lets Nautilus load Python extensions. Run:
   ```bash
   find /usr/lib* /usr/share -name "libnautilus-python.so" 2>/dev/null
   ```
   If nothing is found, install the loader package for your distro (see [Dependencies](#dependencies)).

2. **Restart Nautilus.** After installing the extension or its dependencies:
   ```bash
   nautilus -q
   ```
   Then open GNOME Files again.

3. **Check you are right-clicking empty space.** The menu item only appears when you right-click the folder background, not when you right-click a file.

4. **Check the clipboard.** The menu item is hidden when the clipboard does not contain copied files. Select a file in Nautilus, press `Ctrl+C`, then try again.

### Nautilus crashes on paste

On some Nautilus/Wayland setups, the native clipboard transfer API can crash. This extension uses a text-based clipboard read path to avoid that issue. If you still see crashes, check the terminal output for error messages and open an issue.

## Support & Donations

If you find this project useful, consider supporting its development:

- [GitHub Sponsors](https://github.com/sponsors/imz87)
- [Open an Issue](https://github.com/imz87/paste-links/issues) for bugs or feature requests
- [Contribute](https://github.com/imz87/paste-links/pulls) with a pull request

Your support helps with:
- Maintaining and improving the extension
- Packaging for more distributions
- Writing better documentation

## License

MIT
