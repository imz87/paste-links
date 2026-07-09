# Nautilus Paste Shortcut

Add a `Paste Shortcut Here` action to GNOME Files on Fedora and other Nautilus-based desktops.

The extension reads Nautilus's copied-files clipboard payload after a normal `Ctrl+C` and creates symbolic links in the folder you right-clicked.

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

## Dependencies

Fedora packages:

```bash
sudo dnf install python3-nautilus nautilus-python python3-gobject gtk4
```

Package names may vary slightly by Fedora release. `python3-nautilus` is the important one.

## Install

### Local Install

From this repository:

```bash
./install.sh
```

The script installs the extension files into:

```text
~/.local/share/nautilus-python/extensions/
```

Then restart Nautilus:

```bash
nautilus -q
```

Open GNOME Files again after that.

### RPM Install

Build and install a Fedora RPM:

```bash
# Install build tools
sudo dnf install rpm-build rpmdevtools
rpmdev-setuptree

# Create source tarball
git archive --format=tar.gz --prefix=nautilus-paste-shortcut-0.1.0/ \
    HEAD -o ~/rpmbuild/SOURCES/nautilus-paste-shortcut-0.1.0.tar.gz

# Build the RPM
rpmbuild -ba packaging/nautilus-paste-shortcut.spec

# Install the RPM
sudo dnf install ~/rpmbuild/RPMS/noarch/nautilus-paste-shortcut-0.1.0-1.*.rpm
```

The RPM installs the extension files to the system-wide path:

```text
/usr/share/nautilus-python/extensions/
```

After installation, restart Nautilus:

```bash
nautilus -q
```

### RPM Uninstall

Remove the RPM package:

```bash
sudo dnf remove nautilus-paste-shortcut
```

After removal, restart Nautilus so the extension is no longer loaded:

```bash
nautilus -q
```

See `.docs/project/packaging.md` for more details on RPM and COPR distribution.

## Usage

1. In GNOME Files, select one or more files or folders.
2. Press `Ctrl+C`.
3. Navigate to another local folder.
4. Right-click empty space.
5. Choose `Paste Shortcut Here` (only visible when the clipboard contains copied files).

If the clipboard does not contain copied local files, the menu item is hidden. An error dialog may still appear as a fallback if clipboard inspection fails.

## Uninstall

Remove the installed extension files and restart Nautilus:

```bash
rm ~/.local/share/nautilus-python/extensions/nautilus_paste_shortcut.py \
   ~/.local/share/nautilus-python/extensions/core_logic.py
nautilus -q
```

## Development

- Source files:
  - `src/nautilus_paste_shortcut.py` - Nautilus/GTK integration entrypoint
  - `src/core_logic.py` - Pure shortcut logic (testable without GTK/GDK/Nautilus)
- Installer: `install.sh`
- RPM packaging: `packaging/nautilus-paste-shortcut.spec`
- Project docs: `.docs/`

## Manual Verification

1. Copy one local file and paste a shortcut into another folder.
2. Copy one local folder and paste a shortcut into another folder.
3. Copy multiple local items and verify one symlink is created per item.
4. Repeat with a conflicting destination name and verify `-link` suffixes are used.
5. Press `Ctrl+X` instead of `Ctrl+C` and verify the menu item is hidden.
6. Copy plain text from another app and verify the menu item is hidden.

## License

MIT
