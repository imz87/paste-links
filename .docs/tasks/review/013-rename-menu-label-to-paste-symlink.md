# Task

Rename the Nautilus context-menu label and related user-facing text to `Paste Symlink`.

# Background

The project/package identity has already moved toward `paste-links`, and the current remaining naming cleanup is the action label. Current runtime and documentation still use `Paste Symlink Here` in several places. The desired final action wording is `Paste Symlink`, without `Here`.

This is a wording-only task. It should not change menu visibility, clipboard parsing, symlink creation, packaging mechanics, or release behavior.

# Files Expected To Change

- `src/paste_links.py`
  - Update `MENU_LABEL`, `DIALOG_TITLE`, menu item name if appropriate, and directly related user-facing strings to `Paste Symlink`.

- `install.sh`
  - Update the post-install reminder text so it names the `Paste Symlink` menu item.

- `README.md`
  - Update usage, install, troubleshooting, and manual verification wording that refers to the menu action.

- `packaging/paste-links.spec`
  - Update summary, description, changelog text, and post-install messaging that names the action.

- `packaging/opensuse/paste-links.spec`
  - Update summary, description, changelog text, and post-install messaging that names the action.

- `packaging/debian/`
  - Update package description, changelog, and post-install messaging that names the action.

- `packaging/arch/PKGBUILD`
  - Update package description and post-install messaging that names the action.

- `.docs/project/verification.md`
  - Update manual verification notes and any command examples that mention the old label.

- `.docs/project/packaging.md`
  - Update packaging notes only if they mention the old action label.

# Architecture Notes

- Nautilus integration surface
  - Limit runtime changes to displayed label/title/name text only.
  - Do not change when the menu item appears, how activation works, or how Nautilus APIs are called.

- Clipboard or filesystem behavior
  - No clipboard normalization, source validation, destination validation, symlink naming, or symlink creation behavior should change.

- Packaging or install implications
  - Package metadata and install-time reminders should use the same visible action name as the runtime menu item.
  - Do not change package names, package build logic, repository publishing, signing, or install locations.

- User-visible behavior boundaries
  - The visible menu item should be `Paste Symlink`.
  - Dialog titles and directly related documentation should use `Paste Symlink`.
  - Remove current user-facing `Paste Symlink Here` wording unless it appears only in historical completed task records.

# Implementation Steps

1. Update the runtime menu label and dialog title in `src/paste_links.py` from `Paste Symlink Here` to `Paste Symlink`.
2. Update install-time reminder text in `install.sh` and packaging metadata/scripts to refer to `Paste Symlink`.
3. Update README usage, install, troubleshooting, and verification wording to use `Paste Symlink`.
4. Update `.docs/project/verification.md` and `.docs/project/packaging.md` where they describe current behavior.
5. Search current source, README, packaging, workflow, and project docs for `Paste Symlink Here` and update current-behavior references.
6. Leave historical task records under `.docs/tasks/done/` unchanged unless they describe current active work.
7. Run focused verification for Python syntax, shell syntax, tests, and a final text search for remaining current references.

# Acceptance Criteria

- [ ] The Nautilus context-menu item is labeled `Paste Symlink`.
- [ ] Dialog titles use `Paste Symlink`.
- [ ] README refers to the menu action as `Paste Symlink`.
- [ ] Install-time reminders refer to the `Paste Symlink` menu item.
- [ ] RPM, DEB, Arch, and openSUSE package metadata/user-facing text use `Paste Symlink`.
- [ ] Current project docs use `Paste Symlink` for the action label.
- [ ] No current user-facing `Paste Symlink Here` references remain outside historical completed task records.
- [ ] No clipboard, filesystem, symlink, menu-visibility, packaging mechanics, signing, or publishing behavior changes are introduced.

# Out Of Scope

- Renaming the project/package identity.
- Changing package publishing workflows, signing, release artifacts, or GitHub Actions approval behavior.
- Changing clipboard handling, symlink creation, collision handling, or menu visibility rules.
- Adding localization/internationalization support.
- Updating historical completed task records solely for wording consistency.

# Risks

- Some old wording may remain in package descriptions, install scripts, or documentation if search-based updates miss a file.
- Changing internal menu item names is safe only if it does not affect Nautilus behavior; prefer changing only user-visible text unless the internal name is also user-facing or misleading.
- Historical task docs may intentionally mention older labels, so searches need to distinguish current docs from completed history.

# Questions

- Resolved: the final desired action label is `Paste Symlink`.
- Resolved: `Here` should be removed from current user-facing action wording.
- Resolved: PPA environment approval cleanup is not important for this task.

# Commit Message

refactor(ui): rename action label to paste symlink
