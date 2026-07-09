# Task

Improve installation dependency checks, revise tests after the clipboard-handling changes, and update README documentation where needed.

# Background

Manual desktop debugging showed two important runtime/installation realities:

- The local installer can copy extension files into `~/.local/share/nautilus-python/extensions/` even when the `nautilus-python` package is not installed. In that case Nautilus ignores the Python extension files because the Python extension loader is missing.
- On Fedora/Nautilus/Wayland, reading `x-special/gnome-copied-files` directly can crash inside the native GDK clipboard transfer path. The working runtime path uses `Gdk.Clipboard.read_text_async()` and normalizes plain local-path clipboard text into the existing core payload shape (`copy\nfile://...`).
- Tests currently focus on `core_logic.py`. They should be reviewed and extended as appropriate because the Nautilus entrypoint now contains additional clipboard text normalization behavior.

# Files Expected To Change

- `install.sh`
  - Add a preflight check for the `nautilus-python` extension loader package or installed loader library before reporting a successful install.
  - Fail with a clear error when the Nautilus Python extension loader is missing.
  - Keep the check generic enough for non-Fedora systems while still giving useful Fedora guidance.

- `src/nautilus_paste_shortcut.py`
  - Move pure clipboard text normalization out of this Nautilus entrypoint if it can be tested without GTK/GDK/Nautilus.

- `tests/test_core_logic.py` or a new focused test file under `tests/`
  - Add/update tests for clipboard text normalization after the helper is moved to pure code.
  - Keep tests runnable without a live GNOME session.

- `README.md`
  - Clarify that `nautilus-python` is required because it provides the Nautilus Python extension loader.
  - Add or improve troubleshooting guidance for the case where files are installed but the menu item does not appear.
  - Document known support expectations for non-Fedora distributions without claiming unverified distro support.

- `.docs/project/packaging.md`
  - Update only if dependency or install-check behavior changes need to be reflected in project docs.
  - Clarify distribution support boundaries if README support wording changes.

- `packaging/nautilus-paste-shortcut.spec`
  - Verify existing package dependencies still include `nautilus-python`; update only if missing or incorrect.

# Architecture Notes

- Nautilus integration surface
  - The extension remains a `Nautilus.MenuProvider` Python extension loaded by `nautilus-python`.
  - The installer should detect missing loader support early so users are not misled by files being copied into the extension directory.

- Clipboard or filesystem behavior
  - Preserve the working clipboard path based on `read_text_async()` plus normalization of plain local paths into the existing `copy\nfile://...` payload format.
  - Do not reintroduce direct `x-special/gnome-copied-files` reads in the activation path unless proven safe on the target desktop.
  - Symlink creation behavior should remain in `core_logic.py` and continue to use deterministic collision handling.

- Packaging or install implications
  - Local install should explicitly check for the Nautilus Python extension loader and fail when it is missing.
  - The missing-dependency message should use generic wording first and may include Fedora guidance such as `sudo dnf install nautilus-python` as an example.
  - RPM dependencies should continue to require `nautilus-python` so packaged installs work without extra manual steps.

- User-visible behavior boundaries
  - If `nautilus-python`/loader support is missing, `install.sh` must fail rather than continue with a misleading success message.
  - README troubleshooting should explain the difference between files being present and Nautilus actually loading Python extensions.
  - README should describe Ubuntu/Manjaro/other distro support as conditional on compatible Nautilus 4, GTK 4, PyGObject, and Nautilus Python loader packages being available.

# Implementation Steps

1. Inspect the current `install.sh` behavior and implement the simplest reliable generic dependency check for the Nautilus Python extension loader. Prefer checking for the installed loader library in common Nautilus extension directories, with package-manager checks only as helpful hints.
2. Update `install.sh` so missing loader support produces a clear error, exits non-zero, and does not report a successful/ready install.
3. Review `src/nautilus_paste_shortcut.py` for the clipboard normalization code added during debugging.
4. Extract the pure clipboard text normalization logic into `core_logic.py` or another pure module-level helper that can be unit-tested without GTK, GDK, Nautilus, or a live clipboard.
5. Add or update tests to cover:
   - existing `copy\nfile://...` payload remains unchanged
   - existing `cut\nfile://...` payload remains unchanged/rejected by existing core logic
   - plain local path text becomes a `copy` payload with `file://` URI
   - multiple plain local path lines become one `copy` payload with multiple URIs
   - non-file/non-path text is not silently treated as a valid file copy
6. Review `README.md` install and troubleshooting sections.
7. Update README only where useful to document `nautilus-python`, the restart step, and troubleshooting when the menu is missing.
8. Verify `packaging/nautilus-paste-shortcut.spec` still declares the correct `nautilus-python` dependency; update only if necessary.
9. Add README wording for non-Fedora distributions: support is expected only when equivalent Nautilus 4 / GTK 4 / PyGObject / Nautilus Python loader packages are installed, and distro package names may differ.
10. Run focused verification commands.

# Acceptance Criteria

- [ ] `install.sh` clearly detects missing Nautilus Python loader support and gives actionable generic guidance.
- [ ] `install.sh` exits non-zero when loader support is missing.
- [ ] `install.sh` does not misleadingly report a ready Nautilus extension when the Python extension loader is missing.
- [ ] Pure clipboard text normalization is extracted from the Nautilus entrypoint when practical and covered by unit tests.
- [ ] Existing core shortcut tests still pass.
- [ ] README explains that `nautilus-python` is required to load `.py` extensions, not merely to provide importable Python bindings.
- [ ] README troubleshooting covers the case where files exist in `~/.local/share/nautilus-python/extensions/` but the context menu does not appear.
- [ ] README describes Ubuntu, Manjaro, and other distro support as conditional/untested unless verified, with package names expected to vary.
- [ ] RPM dependency declarations are verified and updated if required.
- [ ] Focused checks pass: `python3 -m py_compile src/nautilus_paste_shortcut.py`, `bash -n install.sh`, and relevant pytest tests.

# Out Of Scope

- Rewriting the extension in C, Vala, Rust, JavaScript, or another language.
- Adding background services, clipboard watchers, or GNOME Shell integration.
- Changing symlink naming/collision behavior.
- Changing supported remote URI behavior.
- Adding broad distro-specific installation systems beyond the current local installer and Fedora RPM packaging.
- Claiming full Ubuntu, Manjaro, Arch, Debian, or other distro support without manual verification on those systems.

# Risks

- Checking only `rpm -q nautilus-python` is too Fedora-specific; use generic loader detection and keep distro package names as guidance rather than hard assumptions.
- Checking only for a loader file path may vary by architecture or distribution.
- Moving normalization code for testing could accidentally change runtime behavior; keep extraction small and preserve current behavior.
- Clipboard behavior may vary between Nautilus/GDK versions; tests should cover pure normalization, while live clipboard behavior still needs manual verification.
- Ubuntu, Manjaro, and other distro compatibility depends on Nautilus version, GTK version, `nautilus-python`/loader availability, and whether their clipboard text behavior matches the Fedora/Nautilus/Wayland behavior observed here.

# Questions

- Resolved: `install.sh` must fail when Nautilus Python loader support is missing.
- Resolved: local install dependency checks and messages should be generic, with Fedora package commands only as examples.
- Resolved: pure clipboard normalization should be moved to pure code, such as `core_logic.py`, so it can be unit-tested.

# Commit Message

Improve install checks, tests, and README guidance
