# Task

Extract the extension's pure shortcut logic from the Nautilus entrypoint so the core behavior can be imported and tested without requiring GTK, GDK, or Nautilus bindings at module import time.

# Background

`src/nautilus_paste_shortcut.py` currently mixes two responsibilities:

- the Nautilus/GTK integration layer
- the pure clipboard-payload, path-validation, naming, and symlink-creation logic

That coupling makes automated testing harder because importing the current module requires `gi` and Nautilus bindings. The test task in `004-add-unit-tests-for-core-logic.md` depends on a small refactor that preserves current behavior while isolating the non-desktop logic behind a normal Python import boundary.

# Files Expected To Change

- `src/nautilus_paste_shortcut.py`
  - Reduce this file to the Nautilus-facing integration code plus calls into extracted helpers.
- New helper module under `src/` such as `src/core_logic.py` or similar
  - Move payload parsing, URI-to-local-path handling, link naming, join-lines behavior, and shortcut creation workflow into a module that does not import GTK, GDK, or Nautilus.
- `README.md`
  - Update development notes if file layout or testing guidance changes.
- Optional `.docs/project/software-development.md`
  - Only if a reusable project rule about keeping pure logic separate from desktop integration is worth documenting.

# Architecture Notes

- Nautilus integration surface:
  - `PasteShortcutExtension` must remain the Nautilus extension entry point.
  - Menu creation, clipboard access, async callbacks, and error-dialog presentation stay in the Nautilus-facing module.
- Clipboard or filesystem behavior:
  - The extracted module should own pure logic for payload parsing, supported-path resolution, suffix generation, and symlink-creation workflow.
  - The extracted module must be importable in a plain Python process that does not have a live GNOME session.
- Packaging or install implications:
  - Do not change the install path, extension filename, or local installation flow.
  - Avoid introducing new third-party runtime dependencies.
- User-visible behavior boundaries:
  - The context menu label, clipboard validation outcomes, name-collision behavior, skipped-item messaging, and error text should stay unchanged unless a follow-up task explicitly changes them.

# Implementation Steps

1. Identify the pure methods in `PasteShortcutExtension` that can move into a helper module without changing Nautilus-facing behavior.
2. Create a small helper module under `src/` that contains the extracted pure logic and the existing `PasteShortcutError` type, or another equivalent minimal design.
3. Ensure the helper module does not import `gi`, GTK, GDK, or Nautilus.
4. Update `src/nautilus_paste_shortcut.py` so the Nautilus class delegates to the helper module instead of owning the pure logic directly.
5. Keep method names, message strings, and symlink behavior stable unless a behavior change is explicitly required by another task.
6. Update README development notes only as needed so future contributors know where the testable core logic now lives.
7. Verify the refactor with focused syntax checks and preserve the existing manual desktop verification expectations.

# Acceptance Criteria

- [ ] The repository contains a helper module for the extension's pure logic that can be imported without GTK, GDK, or Nautilus bindings.
- [ ] `src/nautilus_paste_shortcut.py` remains the Nautilus entrypoint and delegates core logic to the extracted module.
- [ ] The extracted helper covers payload parsing, local-path resolution, deterministic link naming, line-joining, and shortcut creation workflow.
- [ ] The extension filename and install path remain unchanged.
- [ ] Existing user-visible behavior and message text remain unchanged unless explicitly required elsewhere.
- [ ] README development notes are updated if needed to reflect the new module layout.
- [ ] No behavior changes except those explicitly requested in this task.
- [ ] No new background services or desktop hooks unless explicitly requested.
- [ ] No packaging-system expansion unless explicitly requested.
- [ ] No clipboard-format changes unless explicitly requested.
- [ ] No environment or secret-handling changes unless explicitly requested.

# Out Of Scope

- Adding the pytest suite itself.
- Changing Nautilus menu visibility behavior.
- Changing clipboard semantics or adding cut support.
- Packaging or installer changes.
- Any broad module reorganization beyond what is required for testability.

# Risks

- A refactor that moves too much code could accidentally change the desktop integration behavior.
- If the extracted API is too abstract, it may add unnecessary indirection to a small project.
- Message-text drift between the helper module and the Nautilus UI layer could create subtle behavior changes.

# Questions

- Should the extracted helper keep `PasteShortcutError` in the core module, or should that error type stay in the Nautilus entrypoint and be imported by the helper?
- Should URI-to-local-path conversion stay in the helper if it still depends on `Gio`, or should that boundary be adjusted so the helper only accepts already-resolved local paths and raw URIs are handled in the Nautilus layer?

# Commit Message

Extract core shortcut logic from Nautilus entrypoint
