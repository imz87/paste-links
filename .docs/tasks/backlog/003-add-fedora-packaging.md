# Task

Add Fedora-friendly packaging assets for local RPM or COPR distribution.

# Background

The project can already be installed locally with `install.sh`, but publishing for Fedora users will be easier with packaging metadata and documented install/uninstall behavior.

# Files Expected To Change

- `packaging/*`
- `README.md`
- `.docs/project/packaging.md`

# Implementation Steps

1. Add basic RPM packaging assets.
2. Document package dependencies and install paths.
3. Document how to restart Nautilus after package install or removal.

# Acceptance Criteria

- [ ] The repository contains basic Fedora packaging assets.
- [ ] README documents the packaged installation path and dependencies.
- [ ] Packaging docs explain local RPM or COPR distribution intent.

# Out Of Scope

- Do not publish to Fedora or COPR from this task.
- Do not change runtime behavior.

# Risks

- Packaging paths may vary slightly by Fedora release.

# Questions

- None currently.

# Commit Message

Add Fedora packaging assets
