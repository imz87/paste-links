# Task

Place the `Paste Symlink` action immediately after the native `Paste` item in the GNOME Files / Nautilus right-click context menu, if the Nautilus extension API supports it.

# Background

The extension adds a custom Nautilus context-menu action for creating symlinks from copied files. The desired UX is for this action to appear near the built-in paste action, specifically after `Paste`, because it is conceptually a paste variant.

Nautilus extension APIs may not provide exact ordering control relative to built-in menu items. The implementation should verify what ordering hooks are available and use the smallest supported approach. Documentation updates are not required for this task.

# Files Expected To Change

- `src/paste_links.py`
  - Investigate and update menu item construction or provider behavior if Nautilus supports menu placement/order hints.

# Architecture Notes

- Nautilus integration surface
  - Keep the change limited to context-menu ordering/placement.
  - Do not change when the item appears.
  - Do not change activation behavior.

- Clipboard or filesystem behavior
  - No clipboard parsing, symlink creation, destination validation, or collision behavior should change.

- Packaging or install implications
  - No packaging, installer, release, signing, or publishing changes are required.

- User-visible behavior boundaries
  - Preferred result: `Paste Symlink` appears immediately after native `Paste`.
  - If Nautilus does not support exact placement, preserve current functionality and document the implementation limitation in code comments or task notes only if useful.

# Implementation Steps

1. Inspect Nautilus Python menu-provider API support for ordering, priority, grouping, insertion points, or submenu placement.
2. Determine whether a custom extension item can be placed relative to the native `Paste` item.
3. If supported, update `src/paste_links.py` so `Paste Symlink` appears immediately after `Paste`.
4. If exact placement is not supported, keep behavior unchanged and avoid brittle hacks.
5. Verify the menu item still appears only in the same valid clipboard/folder conditions as before.
6. Verify activation still creates symlinks exactly as before.

# Acceptance Criteria

- [ ] If Nautilus supports relative placement, `Paste Symlink` appears immediately after the native `Paste` item in the right-click context menu.
- [ ] If Nautilus does not support relative placement, no brittle or unsupported workaround is introduced.
- [ ] Menu visibility behavior is unchanged.
- [ ] Clipboard handling behavior is unchanged.
- [ ] Symlink creation behavior is unchanged.
- [ ] No documentation updates are required.

# Out Of Scope

- Renaming the menu label.
- Updating README or project documentation.
- Changing packaging, install scripts, release workflows, signing, or publishing.
- Changing clipboard parsing, menu visibility rules, or symlink creation behavior.
- Adding custom UI outside the Nautilus context menu.

# Risks

- Nautilus may not expose an API for ordering extension-provided items relative to built-in menu items.
- Ordering behavior may vary by Nautilus version, distro patch, or GNOME UI changes.
- Attempting unsupported ordering through private APIs could make the extension brittle; avoid that approach.

# Questions

- Resolved: this should be a separate task from the `Paste Symlink` label rename.
- Resolved: documentation updates are not required.

# Commit Message

refactor(ui): place paste symlink after paste menu item
