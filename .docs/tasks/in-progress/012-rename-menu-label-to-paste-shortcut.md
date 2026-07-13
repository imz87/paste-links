# Task

Rename the Nautilus context-menu label from `Paste Shortcut Here` to `Paste Shortcut`, and update user-facing docs and package metadata to match.

# Background

The current runtime label is defined in `src/nautilus_paste_shortcut.py` as `MENU_LABEL = "Paste Shortcut Here"`, and the same wording appears in README, packaging metadata, and verification notes. The action is shown from a folder background context menu, so “Here” is redundant and the shorter label is easier to scan.

# Files Expected To Change

- `src/nautilus_paste_shortcut.py`
  - Update the menu label string.
  - Update `DIALOG_TITLE` to the same `Paste Shortcut` wording.

- `README.md`
  - Replace user-facing references and manual usage instructions with the shorter label.

- `packaging/nautilus-paste-shortcut.spec`
  - Update summary/description text and any install-time messaging that names the action.

- `packaging/opensuse/nautilus-paste-shortcut.spec`
  - Update summary/description text and any install-time messaging that names the action.

- `packaging/arch/PKGBUILD`
  - Update the package description and any user-facing install reminder text that names the action.

- `.docs/project/verification.md`
  - Update manual verification notes to refer to the new label.

# Architecture Notes

- Nautilus integration surface
  - Limit the change to the displayed menu label and any directly related explanatory text.
  - Do not change menu-provider selection, clipboard checks, or activation flow.

- Clipboard or filesystem behavior
  - Clipboard parsing, symlink creation, and destination validation must remain unchanged.

- Packaging or install implications
  - Keep package metadata and post-install text aligned with the new label where they mention the action name.
  - Do not change packaging mechanics or install flow.

- User-visible behavior boundaries
  - The action label and dialog title should both use `Paste Shortcut`.
  - No change to whether the action appears, only how it is named.

# Implementation Steps

1. Update the runtime menu label in `src/nautilus_paste_shortcut.py`.
2. Update `DIALOG_TITLE` in `src/nautilus_paste_shortcut.py` to `Paste Shortcut`.
3. Update package descriptions and install-time wording in the RPM, openSUSE, and Arch packaging files.
4. Update `README.md` and `.docs/project/verification.md` to use the new label.
5. Search for remaining user-facing `Paste Shortcut Here` references and update them to `Paste Shortcut` everywhere.
6. Verify the updated wording is consistent across docs and packaging metadata.

# Acceptance Criteria

- [ ] The Nautilus context-menu item is labeled `Paste Shortcut`.
- [ ] Dialog titles use `Paste Shortcut` instead of `Paste Shortcut Here`.
- [ ] User-facing README and verification notes refer to the new label.
- [ ] Package metadata and install-time messages are consistent with the new label.
- [ ] No clipboard, filesystem, symlink, or menu-visibility behavior changes are introduced.
- [ ] No user-facing `Paste Shortcut Here` references remain in source, docs, or packaging metadata.

# Out Of Scope

- Changing clipboard handling or symlink creation behavior.
- Changing menu visibility rules.
- Adding localization/internationalization support.
- Changing packaging mechanisms or install scripts beyond label text updates.

# Risks

- Some docs or package descriptions may still mention the old label if search-based updates miss them.
- Users may rely on the old wording in screenshots or notes, so documentation needs to stay consistent.

# Questions

- Resolved: `DIALOG_TITLE` should also change to `Paste Shortcut`.
- Resolved: package summaries, descriptions, docs, and user-facing text should remove `Here` everywhere.

# Commit Message

feat(ui): rename menu label to paste shortcut
