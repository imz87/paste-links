# Software Development Practices

## Core Practices

- Prefer correctness over cleverness.
- Keep changes minimal and localized.
- Preserve existing naming and structure when expanding the project.
- Do not refactor unrelated code.
- Prefer modifying the current implementation over introducing a new system.
- Ask instead of guessing when requirements or compatibility needs are unclear.

## Dependencies

- Prefer the platform libraries already needed by Nautilus and PyGObject.
- Do not add extra Python packages unless they solve a concrete problem.
- Keep installation simple for Fedora GNOME users.

## Boundaries

- Keep the extension focused on Nautilus menu behavior and symlink creation.
- Do not add background daemons, clipboard watchers, or unrelated desktop hooks.
- Restrict behavior changes to GNOME Files integration only.

## Python / Nautilus Focus Areas

When working on the extension code, pay attention to:

- **Nautilus menu-provider behavior**: understand when and how the context menu item appears.
- **Clipboard parsing and validation**: validate clipboard content before acting on it.
- **Local filesystem safety and deterministic naming**: avoid race conditions, handle existing names.
- **GNOME Files integration**: keep the extension focused on Nautilus; do not broaden scope.

## Documentation

- Update README and `.docs/` when behavior or installation changes.
- Keep task specs small, explicit, and easy to review.
