# Task

Only show `Paste Shortcut Here` when the clipboard currently contains copied local files from GNOME Files.

# Background

The initial implementation always shows the menu item and validates the clipboard when the action is clicked. That keeps the extension simple, but a more polished experience would hide the action when Nautilus's copied-files clipboard format is not present.

# Files Expected To Change

- `src/nautilus_paste_shortcut.py`
- `README.md`
- Optional: `.docs/project/verification.md`

# Implementation Steps

1. Check whether Nautilus allows safe clipboard inspection while building the background menu.
2. Hide the menu item when the clipboard does not contain supported copied local files.
3. Keep the current activation-time validation as a fallback.
4. Update docs if the visibility behavior changes.

# Acceptance Criteria

- [ ] `Paste Shortcut Here` is hidden when the clipboard does not contain copied files from GNOME Files.
- [ ] The action still works for one or more copied local files.
- [ ] Invalid clipboard cases still fail safely.

# Out Of Scope

- Do not add a dedicated `Copy Shortcut` action.
- Do not change symlink naming behavior.

# Risks

- Clipboard inspection during menu creation may be version-sensitive across Nautilus and GTK releases.

# Questions

- None currently.

# Commit Message

Hide Paste Shortcut when clipboard is invalid
