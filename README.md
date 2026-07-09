# Nautilus Paste Shortcut

Add a `Paste Shortcut Here` action to GNOME Files on Fedora and other Nautilus-based desktops.

The extension reads Nautilus's copied-files clipboard payload after a normal `Ctrl+C` and creates symbolic links in the folder you right-clicked.

## Features

- Supports multiple copied files and folders.
- Uses the normal GNOME Files copy flow.
- Creates symbolic links instead of duplicating file contents.
- Shows a small error dialog for invalid clipboard cases.
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

From this repository:

```bash
./install.sh
```

The script installs the extension into:

```text
~/.local/share/nautilus-python/extensions/
```

Then restart Nautilus:

```bash
nautilus -q
```

Open GNOME Files again after that.

## Usage

1. In GNOME Files, select one or more files or folders.
2. Press `Ctrl+C`.
3. Navigate to another local folder.
4. Right-click empty space.
5. Choose `Paste Shortcut Here`.

If the clipboard does not contain copied local files, the extension shows a small error dialog.

## Uninstall

Remove the installed extension file and restart Nautilus:

```bash
rm ~/.local/share/nautilus-python/extensions/nautilus_paste_shortcut.py
nautilus -q
```

## Development

- Source file: `src/nautilus_paste_shortcut.py`
- Installer: `install.sh`
- Project docs: `.docs/`

## Manual Verification

1. Copy one local file and paste a shortcut into another folder.
2. Copy one local folder and paste a shortcut into another folder.
3. Copy multiple local items and verify one symlink is created per item.
4. Repeat with a conflicting destination name and verify `-link` suffixes are used.
5. Press `Ctrl+X` instead of `Ctrl+C` and verify an error dialog appears.
6. Copy plain text from another app and verify an error dialog appears.

## License

MIT
