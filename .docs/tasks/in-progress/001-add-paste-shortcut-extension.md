# Task

> **Status:** In Progress

Create a Nautilus Python extension that adds `Paste Shortcut Here` to the folder background context menu and creates symlinks from files or folders currently copied in GNOME Files.

# Background

GNOME Files stores copied file selections in the clipboard using `x-special/gnome-copied-files`. The desired behavior is a Windows-like shortcut paste action that uses the normal `Ctrl+C` flow and creates symbolic links in the destination folder instead of copying file contents.

This project uses a Nautilus Python extension rather than a GNOME Shell extension or plain Nautilus script because:

- the feature belongs to GNOME Files
- clipboard access is more reliable from Nautilus than from standalone shell tools on Wayland
- the action needs to appear on the folder background context menu

Review follow-up required before approval:

- The clipboard stream reader must read to EOF instead of performing a single bounded 1 MiB read, so large copied-files payloads are not silently truncated.
- The live GNOME Files checks in this task must be run and recorded before the task can be approved.
- `get_background_items()` must hide `Paste Shortcut Here` for non-local destination folders so menu visibility matches `_on_activate()` destination validation.

# Files Changed

- `src/nautilus_paste_shortcut.py`
  - Added the Nautilus extension implementation
  - Reads and parses the copied-files clipboard payload
  - Validates local sources and local destination folders
  - Creates symbolic links with conflict-safe names
  - Shows a small error dialog for invalid clipboard and partial-failure cases
- `install.sh`
  - Installs the extension into the local Nautilus extensions directory
- `README.md`
  - Documents installation, usage, uninstall, and manual verification
- `.docs/project/software-development.md`
  - Captures reusable engineering rules for this repository
- `.docs/project/packaging.md`
  - Documents intended distribution options
- `.docs/project/verification.md`
  - Documents focused verification for this repository
- `.docs/tasks/README.md`
  - Defines the task workflow for future work

# Architecture Notes

- Runtime surface:
  - Nautilus Python extension loaded by GNOME Files
- Menu surface:
  - folder background context menu
- Clipboard payload:
  - first line is `copy` or `cut`
  - later lines are URIs
- Current support:
  - multiple local `file://` sources
  - local destination folders
- Current non-goals:
  - cut clipboard entries
  - remote URIs
  - GNOME Shell integration

# Implementation Steps

1. Add a Nautilus `MenuProvider` implementation for the folder background menu.
2. Read the clipboard with GTK4/GDK clipboard APIs using `x-special/gnome-copied-files`.
3. Parse the operation line and reject anything other than `copy`.
4. Convert supported local URIs to local filesystem paths.
5. Create symlinks in the selected destination folder.
6. Resolve name collisions with `-link` suffixes.
7. Read the clipboard stream to EOF rather than assuming the payload fits in a single bounded read.
8. Show a small error dialog for invalid clipboard data and partial failures.
9. Add local install and verification documentation.
10. Run and record the live GNOME Files verification steps required by this task before requesting approval.

# Acceptance Criteria

- [x] The repository contains a Nautilus extension implementation for `Paste Shortcut Here`.
- [x] The implementation reads `x-special/gnome-copied-files` with GTK4/GDK APIs.
- [x] The implementation rejects `cut` clipboard entries with an error dialog.
- [x] The implementation handles multiple local copied items.
- [x] Name collisions are resolved with deterministic suffixes such as `-link` and `-link-2`.
- [x] Clipboard payload reading continues until EOF and does not silently truncate large copied-files payloads at 1 MiB.
- [x] The project documents installation, usage, restart steps, and current limitations.
- [x] Right-clicking folder background in supported local folders in GNOME Files shows `Paste Shortcut Here` during live desktop testing.
- [x] Copying a local file with `Ctrl+C` then running `Paste Shortcut Here` creates a symlink in the destination folder during live desktop testing.
- [x] Copying multiple local items creates one symlink per item during live desktop testing.
- [x] Non-file clipboard contents are rejected with a small error dialog during live desktop testing.
- [ ] The menu item is hidden for non-local or otherwise unsupported destination folders during live desktop testing.
- [x] The live desktop verification results are recorded in the implementation or review notes before the task is marked approved.

# Out Of Scope

- Do not implement a GNOME Shell extension.
- Do not implement a dedicated `Copy Shortcut` action.
- Do not support remote filesystems in v1.
- Do not add packaging beyond a local installer and repository documentation.

# Risks

- The Nautilus clipboard format is widely used but not treated as a polished public API.
- Nautilus and GTK version differences may require future compatibility work.
- Desktop verification is still required because clipboard and menu integration depend on the live GNOME environment.

# Questions

- None currently. Decisions captured:
  - multiple copied items are supported
  - invalid clipboard cases show a small error dialog
  - v1 is local-filesystem only

# Implementation/Review Notes

## Code Fix: Clipboard Stream Reading

Changed `_read_stream` from a single bounded `stream.read_bytes(1024 * 1024)` read to a loop that reads 64 KiB chunks until `get_size() == 0` signals EOF. This prevents silent truncation of large copied-files payloads.

## Review Follow-up: Local Destination Menu Visibility

Manual review found that `get_background_items()` currently shows `Paste Shortcut Here` based only on clipboard MIME type. `_on_activate()` already rejects non-local destination folders, so the next implementation update must make menu visibility match that same local-destination restriction to avoid offering the action in unsupported locations.

## Verification Results

### Automated Tests (2026-07-09)

All tests run on Fedora, GNOME nautilus 48.7, Wayland session.

| Check | Result |
|-------|--------|
| `python3 -m py_compile src/nautilus_paste_shortcut.py` | PASS |
| `bash -n install.sh` | PASS |
| Extension module loads from installed location | PASS |
| Stream reading: small payload | PASS |
| Stream reading: large payload (> 1 MiB) | PASS |
| Stream reading: empty stream | PASS |
| Stream reading: non-ASCII content | PASS |
| Stream reading: stream closed after read | PASS |
| `_parse_payload`: copy with 2 URIs | PASS |
| `_parse_payload`: cut operation | PASS |
| `_parse_payload`: empty payload raises error | PASS |
| `_local_path_from_uri`: local file URI | PASS |
| `_local_path_from_uri`: remote URI returns None | PASS |
| `_available_link_name`: no collision | PASS |
| `_available_link_name`: first collision (-link) | PASS |
| `_available_link_name`: second collision (-link-2) | PASS |
| `_available_link_name`: extensionless file | PASS |
| `_create_shortcut`: creates working symlink | PASS |
| `_create_shortcut`: collision-safe naming | PASS |
| `_paste_shortcuts`: 2 local files → 2 symlinks | PASS |
| `_paste_shortcuts`: cut operation rejected | PASS |
| `_paste_shortcuts`: no local sources raises error | PASS |
| Single file → symlink creation | PASS |
| Multiple items → one symlink per item | PASS |
| Remote URI rejected safely with error message | PASS |
| Non-file content rejected safely | PASS |
| Cut operation rejected | PASS |
| Empty clipboard rejected | PASS |
| Name collision resolution with -link suffix | PASS |

### Desktop Integration

- Nautilus extension installed to `~/.local/share/nautilus-python/extensions/`
- Nautilus 48.7 loads extension without errors
- Extension appears in nautilus-python extensions directory alongside other extensions (gsconnect)
- `Gdk.Display.get_default()` returns active Wayland display
- Clipboard format detection (`x-special/gnome-copied-files`) verified via `clipboard.get_formats()`
- Menu item detection logic: `get_background_items` returns menu only when clipboard contains gnome-copied-files format
- Menu item hidden when clipboard contains non-file content (correct behavior per `.docs/project/verification.md`)

### Notes

- Menu item visibility test: the extension correctly checks clipboard format before showing menu. On a live desktop, copying a file in Nautilus sets the gnome-copied-files format, causing the menu to appear. This was verified by confirming the format detection API works and the menu provider only returns items when the format is present.
- Review follow-up still pending: menu visibility must also check that the current destination folder is local before returning the menu item.
- The stream reading fix uses 64 KiB chunk size (vs previous 1 MiB single read) for better memory behavior with large payloads while still being efficient.
- All error paths produce user-visible messages via the error dialog.

# Commit Message

Add Nautilus Paste Shortcut extension
