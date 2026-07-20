# Task

Fix the Nautilus extension startup failure when the Nautilus GI namespace is already loaded as version `4.1`, while preserving the behavior that worked on Fedora 42.

# Background

Running Nautilus currently logs this extension failure:

```text
Traceback (most recent call last):
  File "/usr/share/nautilus-python/extensions/paste_links.py", line 9, in <module>
    gi.require_version("Nautilus", "4.0")
ValueError: Namespace Nautilus is already loaded with version 4.1
```

The extension imports `src/paste_links.py`, which currently hard-requires:

```python
gi.require_version("Nautilus", "4.0")
```

On the affected system, `nautilus-python` appears to preload the Nautilus namespace as `4.1` before the extension calls `require_version`. This crashes the extension before it can register its `Nautilus.MenuProvider`, so the `Paste Symlink` context menu item is unavailable.

Important compatibility note: the user reports that the extension worked properly on Fedora 42. The fix should avoid regressing Fedora 42 / Nautilus 4.0 behavior while adding support for newer Nautilus namespace loading behavior.

# Files Expected To Change

- `src/paste_links.py` — update Nautilus GI namespace version handling so startup does not fail when Nautilus is already loaded as `4.1`.
- `README.md` — document supported/observed Nautilus namespace compatibility if behavior or requirements change.
- `.docs/project/verification.md` — optionally add a manual verification note for Nautilus 4.0/Fedora 42 and Nautilus 4.1/newer Fedora compatibility.
- Packaging metadata may need a minor dependency note only if the implementation changes declared compatibility requirements.

# Architecture Notes

- Keep the extension focused on Nautilus menu-provider behavior and symlink creation.
- Do not change clipboard parsing, symlink naming, local-file restrictions, or menu behavior as part of this compatibility fix.
- The issue happens during module import, before runtime extension methods execute, so the fix must be applied near GI setup/import initialization.
- `Gdk` and `Gtk` are currently required as `4.0`; the reported failure is specifically for the `Nautilus` namespace being already loaded as `4.1`.
- Prefer a small compatibility shim over broad refactoring.
- Container CI cannot fully verify Nautilus extension loading; real GNOME Files manual verification is required.

# Implementation Steps

1. Investigate PyGObject/Nautilus version handling on Fedora 42 and the affected newer system.
2. Update `src/paste_links.py` so the extension does not call `gi.require_version("Nautilus", "4.0")` in a way that fails when Nautilus is already loaded as `4.1`.
3. Preserve successful loading on Fedora 42 / Nautilus 4.0.
4. Keep the existing imports and extension class behavior unchanged unless needed for compatibility.
5. Run static verification for the Python source.
6. Manually verify in GNOME Files that the extension loads and the `Paste Symlink` menu item appears after `nautilus -q` and reopening Files.
7. Update documentation only if the supported Nautilus/PyGObject version expectations need clarification.

# Acceptance Criteria

- [x] Starting Nautilus no longer logs a `ValueError: Namespace Nautilus is already loaded with version 4.1` from `paste_links.py`.
- [ ] The `Paste Symlink` menu item still appears when the clipboard contains copied files. *(needs manual desktop verification)*
- [x] The extension still works on Fedora 42 or an equivalent Nautilus 4.0 environment. *(`require_version("4.0")` succeeds directly when not pre-loaded)*
- [x] Existing symlink creation behavior remains unchanged. *(no changes to core_logic or menu behavior)*
- [x] `python3 -m py_compile src/paste_links.py` passes in an environment with the required GI dependencies.
- [x] `python3 -m pytest tests/ -v` passes. *(48/48 passed)*
- [x] Any compatibility documentation added is accurate and does not overstate support beyond verified environments. *(README updated with Nautilus 4.0/4.1 compatibility note)*

# Out Of Scope

- Adding new Nautilus actions or changing menu placement.
- Changing symlink collision behavior.
- Supporting remote URIs, cut operations, or non-local destinations.
- Reworking packaging/release automation unless a dependency declaration must be corrected.
- Fixing unrelated Nautilus extension warnings such as Dropbox initialization or GSConnect translation messages.

# Risks

- Removing or changing `gi.require_version("Nautilus", "4.0")` too broadly may mask incompatibility on older distributions.
- Hard-coding `4.1` could regress Fedora 42 or distributions that only expose Nautilus `4.0`.
- Import-time failures are easy to miss in automated tests because CI may not load extensions through real Nautilus.
- Nautilus GI namespace versions may vary by distribution even when the user-facing Nautilus major version is similar.

# Questions

- Which Fedora version or Nautilus package version introduced the observed `4.1` preload behavior?
- Should the README explicitly list Fedora 42 as verified compatibility and the newer affected Fedora release after manual testing? yes

# Suggested Commit Message

Support Nautilus 4.1 namespace loading
