# Task

> **Status:** In Progress

Create a Nautilus Python extension that adds `Paste Shortcut Here` to the folder background context menu and creates symlinks from files or folders currently copied in GNOME Files.

# Background

GNOME Files stores copied file selections in the clipboard using `x-special/gnome-copied-files`. The desired behavior is a Windows-like shortcut paste action that uses the normal `Ctrl+C` flow and creates symbolic links in the destination folder instead of copying file contents.

This project uses a Nautilus Python extension rather than a GNOME Shell extension or plain Nautilus script because:

- the feature belongs to GNOME Files
- clipboard access is more reliable from Nautilus than from standalone shell tools on Wayland
- the action needs to appear on the folder background context menu

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
7. Show a small error dialog for invalid clipboard data and partial failures.
8. Add local install and verification documentation.

# Acceptance Criteria

- [x] The repository contains a Nautilus extension implementation for `Paste Shortcut Here`.
- [x] The implementation reads `x-special/gnome-copied-files` with GTK4/GDK APIs.
- [x] The implementation rejects `cut` clipboard entries with an error dialog.
- [x] The implementation handles multiple local copied items.
- [x] Name collisions are resolved with deterministic suffixes such as `-link` and `-link-2`.
- [x] The project documents installation, usage, restart steps, and current limitations.
- [ ] Right-clicking folder background in GNOME Files shows `Paste Shortcut Here` during live desktop testing.
- [ ] Copying a local file with `Ctrl+C` then running `Paste Shortcut Here` creates a symlink in the destination folder during live desktop testing.
- [ ] Copying multiple local items creates one symlink per item during live desktop testing.
- [ ] Non-file clipboard contents are rejected with a small error dialog during live desktop testing.

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

# Commit Message

Add Nautilus Paste Shortcut extension
