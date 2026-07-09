# Verification

## Focused Checks

Use these checks for normal changes:

```bash
python3 -m py_compile src/nautilus_paste_shortcut.py
bash -n install.sh
```

## Manual Checks

1. Copy one file in GNOME Files and run `Paste Shortcut Here` in another folder.
2. Copy one folder in GNOME Files and run `Paste Shortcut Here` in another folder.
3. Copy multiple items and verify one symlink is created per item.
4. Repeat with an existing destination name and verify suffix handling.
5. Press `Ctrl+X` and verify the extension shows an error dialog.
6. Copy non-file clipboard text and verify the extension shows an error dialog.

## Notes

- Review is a separate manual phase after development.
- For clipboard or Nautilus API changes, prefer a real desktop test over assumptions.
