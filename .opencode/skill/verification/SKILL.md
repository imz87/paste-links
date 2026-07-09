---
name: verification
description: Use when choosing verification commands, syntax checks, manual desktop checks, install-script validation, or packaging-sensitive validation.
---

# Verification

Use this to choose checks for a change.

Default checks:
- Python source change: `python3 -m py_compile src/nautilus_paste_shortcut.py`
- Install script change: `bash -n install.sh`
- Documentation-only change: manual read-through of the updated instructions

Manual checks when needed:
- GNOME Files clipboard behavior: follow `.docs/project/verification.md`
- Packaging or install flow change: re-run the relevant install steps from `README.md`
