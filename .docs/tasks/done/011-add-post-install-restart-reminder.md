# Task

Add a clear post-install reminder to restart Nautilus / Files after installation on all supported distribution paths, without auto-restarting the file manager.

# Background

The extension is installed through multiple paths:

- local installation with `install.sh`
- Fedora/RPM installation with `dnf install` or a built RPM
- Debian/Ubuntu `.deb` installation with `apt install`
- Arch Linux package installation with `pacman -U`
- openSUSE RPM installation with `zypper install`

Manual verification showed that the extension may not appear in GNOME Files until Nautilus is restarted. The current documentation mentions this in some places, but the install experience is inconsistent across distros. This task standardizes the reminder so users are told what to do immediately after install, while preserving the current behavior of not restarting Nautilus automatically.

# Files Expected To Change

- `install.sh`
  - Keep or improve the post-install success message so it clearly tells the user to restart Nautilus / reopen Files.

- `packaging/nautilus-paste-shortcut.spec`
  - Add an RPM `%post` or equivalent install-time message so Fedora/RPM installs print the restart reminder.

- `packaging/debian/`
  - Add or update Debian maintainer script(s) so `.deb` installs print the restart reminder after installation.

- `packaging/arch/PKGBUILD` and/or Arch install script metadata
  - Add the restart reminder to the Arch install path using the conventional Arch packaging mechanism.

- `packaging/opensuse/nautilus-paste-shortcut.spec`
  - Add an RPM `%post` or equivalent install-time message for openSUSE package installs.

- `README.md`
  - Make the restart requirement obvious in the install sections for all supported distro families.

- `.docs/project/packaging.md`
  - Document the restart reminder behavior and where it is emitted for packaged installs.

- `.docs/project/verification.md`
  - Add or adjust focused verification notes for package install messaging if needed.

# Architecture Notes

- Nautilus integration surface
  - Do not change the extension runtime, menu provider logic, clipboard handling, or symlink creation.
  - The change is limited to installation UX and package metadata.

- Clipboard or filesystem behavior
  - No clipboard, filesystem, or symlink behavior should change.
  - Do not add any runtime hook that watches Files or attempts to restart Nautilus automatically.

- Packaging or install implications
  - Each distro should print a visible reminder during or immediately after installation.
  - Prefer the standard packaging mechanism for each ecosystem (`%post`, maintainer script, `.install`, or equivalent) instead of custom wrapper scripts.
  - Do not introduce a restart flag or auto-restart behavior.

- User-visible behavior boundaries
  - The reminder should tell users to restart Nautilus / reopen Files after installation.
  - The project must not close existing Files windows automatically.
  - The reminder should be consistent across local install and the four supported package families.

# Implementation Steps

1. Inspect the current install messages in `install.sh` and packaging metadata for Fedora/RPM, Debian, Arch, and openSUSE.
2. Choose the smallest packaging-native mechanism for each distro family to emit a restart reminder after install.
3. Update `install.sh` so the local installer clearly tells the user to restart Nautilus / reopen Files.
4. Add package-install messages for RPM-based installs in the Fedora and openSUSE specs.
5. Add the equivalent post-install message for Debian packaging.
6. Add the equivalent post-install message for Arch packaging.
7. Update `README.md` install sections so the restart requirement is visible before users test the extension.
8. Update `.docs/project/packaging.md` and, if needed, `.docs/project/verification.md` to reflect the new install messaging.
9. Verify the package metadata still builds and that the install messages appear in the expected places.

# Acceptance Criteria

- [ ] Local installation via `install.sh` prints a clear restart reminder after a successful install.
- [ ] Fedora/RPM installs print a restart reminder during or immediately after package installation.
- [ ] Debian/Ubuntu `.deb` installs print a restart reminder during or immediately after package installation.
- [ ] Arch package installs print a restart reminder during or immediately after package installation.
- [ ] openSUSE RPM installs print a restart reminder during or immediately after package installation.
- [ ] The project does not auto-restart Nautilus or close existing Files windows.
- [ ] README installation instructions make the restart step obvious for all supported distro families.
- [ ] Packaging docs explain where the reminder is emitted.

# Out Of Scope

- Auto-restarting Nautilus after install.
- Adding a restart flag or other opt-in restart automation.
- Changing extension runtime behavior, clipboard behavior, or filesystem behavior.
- Changing menu visibility, symlink naming, or clipboard parsing.
- Expanding support to additional distros beyond the current four package families.

# Risks

- Package-manager scriptlet behavior differs across RPM, DEB, and Arch ecosystems, so the reminder may need slightly different implementation styles.
- Some package managers may suppress or reorder post-install output, reducing visibility.
- Arch packaging may require a dedicated `.install` file or equivalent helper if `PKGBUILD` alone is not enough.
- The reminder must stay informational only; anything that closes Files windows would be user-hostile.

# Questions

- Resolved: the reminder should be printed for all four supported distro families.
- Resolved: do not auto-restart Nautilus.
- Resolved: do not add a restart flag.

# Commit Message

docs(packaging): add post-install Nautilus restart reminder
