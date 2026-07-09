# Task

Add a small automated test suite for the extension's pure logic and local filesystem behavior without testing live Nautilus, GTK, or clipboard UI integration.

# Background

The repository currently relies on focused manual verification for Nautilus and clipboard behavior, but it does not have automated tests. The current implementation keeps both Nautilus integration and pure logic in `src/nautilus_paste_shortcut.py`, which makes low-level behavior harder to test in isolation.

This project depends mainly on system packages such as PyGObject and Nautilus Python bindings. A normal runtime `requirements.txt` is not a good fit for those dependencies. For this task, keep runtime installation unchanged and add only the minimum developer-oriented test setup needed to run unit tests.

# Files Expected To Change

- `src/nautilus_paste_shortcut.py`
  - Likely needs a small restructuring so clipboard payload parsing, link naming, and symlink-creation workflow can be tested without requiring a live Nautilus session.
- Optional new helper module under `src/`
  - If needed, extract pure logic into a small helper module that does not import GTK, GDK, or Nautilus at import time.
- `tests/test_core_logic.py`
  - Add pytest coverage for payload parsing, link naming, collision handling, and local-only shortcut creation behavior.
- `README.md`
  - Document the test scope, how to run the automated tests, and that manual desktop checks are still required for Nautilus integration.
- Optional developer dependency file such as `requirements-dev.txt`
  - Only add this if the coding agent determines it is needed for pytest tooling. Do not add a runtime `requirements.txt`.
- Optional `.gitignore`
  - Add `.venv/` only if the updated docs recommend a local virtual environment for contributors.

# Architecture Notes

- Nautilus integration surface:
  - Keep `PasteShortcutExtension` as the Nautilus-facing entry point.
  - Do not try to unit test `get_background_items`, clipboard display access, async clipboard callbacks, or GTK dialogs in this task.
- Clipboard or filesystem behavior:
  - Automated tests should cover parsing the copied-files payload, rejecting unsupported operations, deterministic `-link` suffix generation, mixed supported/unsupported URIs, and symlink creation in temporary local directories.
- Packaging or install implications:
  - Do not change runtime packaging or local install behavior.
  - Do not introduce a runtime `requirements.txt` for Nautilus/PyGObject dependencies.
  - A contributor-only `.venv` may be documented as optional, not required.
- User-visible behavior boundaries:
  - The live Nautilus menu behavior, clipboard interaction, and dialogs must behave the same after this task.
  - Manual desktop verification remains required for integration behavior.

# Implementation Steps

1. Identify the smallest set of pure functions or helper methods that can be tested without importing live GTK/Nautilus objects.
2. Restructure only as much as needed so those logic paths can be imported and tested in a normal pytest run.
3. Add pytest tests for clipboard payload parsing, including blank-line handling, empty payload rejection, and `copy` vs `cut` operation parsing.
4. Add pytest tests for link-name generation, including plain filenames, no-extension names, hidden-file edge cases, and multi-dot filenames.
5. Add pytest tests for collision handling in a temporary directory so `-link`, `-link-2`, and later suffixes are deterministic.
6. Add pytest tests for shortcut creation behavior in temporary directories, including one file, one folder, multiple sources, name collisions, unsupported URIs, and partial-skip reporting.
7. Update `README.md` with a small testing section that explains automated test scope, optional contributor `.venv` usage, and that manual Nautilus checks are still required.
8. Add a developer dependency file only if necessary for repository clarity; if it is added, keep it test-tool-only.

# Acceptance Criteria

- [ ] The repository contains an automated test file for the extension's pure logic and local filesystem behavior.
- [ ] The automated tests do not depend on launching Nautilus, opening GTK dialogs, or accessing a live desktop clipboard.
- [ ] Clipboard payload parsing is covered for valid copy payloads, blank lines, empty payloads, and cut payloads.
- [ ] Link-name generation is covered for conflict-free names and deterministic `-link` suffix collisions.
- [ ] Shortcut creation behavior is covered for local file and folder sources in temporary directories.
- [ ] Mixed supported and unsupported source URIs are covered, including the returned warning message behavior.
- [ ] `README.md` explains how to run the tests and clearly states that desktop integration still requires manual verification.
- [ ] No runtime `requirements.txt` is introduced for Nautilus or PyGObject dependencies unless the user explicitly asks for packaging changes.
- [ ] No behavior changes except those explicitly requested in this task.
- [ ] No new background services or desktop hooks unless explicitly requested.
- [ ] No packaging-system expansion unless explicitly requested.
- [ ] No clipboard-format changes unless explicitly requested.
- [ ] No environment or secret-handling changes unless explicitly requested.

# Out Of Scope

- Testing live Nautilus context menu visibility.
- Testing GTK dialog rendering.
- Testing async clipboard reads against a real desktop session.
- Reworking installation or packaging for Fedora/COPR.
- Broad refactoring unrelated to testability.

# Risks

- Top-level `gi` / Nautilus imports may make test execution awkward unless the pure logic is isolated carefully.
- Hidden-file naming behavior such as `.bashrc` may expose edge cases that the current implementation already has; tests should capture current intended behavior before changing it.
- Over-refactoring for testability could accidentally change user-visible Nautilus behavior if the integration boundary is not preserved.

# Questions

- Should contributor setup documentation prefer Fedora system package installation for `pytest`, or mention `python -m venv .venv` as an optional convenience?
- If the coding agent discovers a hidden-file naming bug while writing tests, should that be fixed in this task or split into a follow-up behavior-change task?

# Commit Message

Add unit tests for core shortcut logic
