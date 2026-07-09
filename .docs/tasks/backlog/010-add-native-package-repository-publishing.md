# Task

Add native PPA/apt repository publishing workflows after GitHub Release artifacts and package signing are working.

# Background

Task 008 adds cross-distro packaging assets and GitHub Actions release artifacts for RPM, DEB, Arch, and openSUSE targets. Task 009 adds package signing support. GitHub Release artifacts are useful downloadable packages, but they are not the same as native package repositories that users can add once and update through `apt`.

This task plans the next distribution step: publishing to a native Debian/Ubuntu repository, with PPA/apt as the first target. It should start only after package metadata, release artifact generation, and package signing are stable.

Decisions for this task:

- Implement PPA/apt publishing first.
- Package signing must be completed before native repository publishing goes live.
- Publishing workflows must require GitHub Environment approval before pushing to external repositories.

# Files Expected To Change

- `.github/workflows/` release or publish workflows
  - Add or extend workflows for PPA/apt publishing after signing and credentials are ready.

- `packaging/debian/` or related Debian package files
  - Adjust package metadata only where required by PPA/apt publishing.

- `README.md`
  - Document PPA/apt repository installation commands once publishing is implemented.

- `.docs/project/packaging.md`
  - Document publishing targets, credential requirements, manual approval boundaries, and maintenance expectations.

- `.docs/project/verification.md`
  - Add safe dry-run or validation commands for publishing workflows where available.

# Architecture Notes

- Nautilus integration surface
  - Repository publishing must not change Nautilus extension runtime behavior.
  - Packages published through repositories must install the same Nautilus Python extension files as the GitHub Release artifacts.

- Clipboard or filesystem behavior
  - This task is distribution-only. It must not change clipboard behavior, symlink behavior, or filesystem runtime behavior.

- Packaging or install implications
  - The first repository target is PPA/apt for Debian/Ubuntu-family distribution.
  - Other repository targets remain future work:
    - Fedora/RHEL family: COPR, then Fedora official repositories only if the project later wants full distro review.
    - Arch family: AUR package recipe publishing.
    - openSUSE family: OBS publishing.
  - Each ecosystem has different credentials, review expectations, metadata rules, and automation constraints.
  - Publishing should use least-privilege secrets and must require GitHub Environment approval for release publication.
  - Package signing must be implemented before this publishing workflow is allowed to publish live packages.

- User-visible behavior boundaries
  - README should distinguish between downloadable GitHub Release artifacts and the PPA/apt repository with update support.
  - Do not claim official Debian/Ubuntu repository support unless the package has actually been accepted into official distro repositories.

# Implementation Steps

1. Confirm that task 008 is complete and package artifacts build successfully for all selected distro families.
2. Confirm package signing support from task 009 exists and is documented. If it is not complete, block this task until task 009 is done.
3. Implement PPA/apt publishing as the first native repository target.
4. Document required accounts, credentials, tokens, signing keys, and manual setup steps for the PPA/apt target.
5. Add publishing workflow steps with manual triggers and appropriate release/tag constraints.
6. Configure the publishing workflow to require GitHub Environment approval before pushing to the external repository.
7. Configure GitHub Actions secrets only by documented names; do not hard-code secrets or credentials.
8. Add dry-run, validation, or staging publishing where the ecosystem supports it.
9. Update README with user-facing PPA/apt repository setup and install commands only after publishing is implemented.
10. Update `.docs/project/packaging.md` with maintenance notes and the distinction between the implemented PPA/apt target and future COPR/AUR/OBS targets.
11. Update `.docs/project/verification.md` with safe validation steps that do not accidentally publish packages.

# Acceptance Criteria

- [ ] Native PPA/apt repository publishing is implemented as the first external repository target.
- [ ] Package signing from task 009 is completed and integrated before any live PPA/apt publication is enabled.
- [ ] Publishing workflows use documented GitHub Actions secrets or protected environments and do not hard-code credentials.
- [ ] Publishing workflows require GitHub Environment approval before pushing to external repositories.
- [ ] Real publication requires an explicit tag/manual trigger and is not run on ordinary pull requests.
- [ ] README documents PPA/apt repository setup and install commands only after the publishing path is implemented.
- [ ] `.docs/project/packaging.md` documents PPA/apt publishing and leaves COPR, AUR, and OBS clearly marked as future work.
- [ ] `.docs/project/verification.md` documents safe validation or dry-run commands.
- [ ] No runtime source behavior changes are introduced.
- [ ] No behavior changes except those explicitly requested in this task.

# Out Of Scope

- Changing Nautilus extension behavior.
- Changing clipboard parsing, symlink creation, or menu visibility.
- Claiming official distro repository support before acceptance into official distro channels.
- Publishing COPR, AUR, OBS, or official distro repository packages.
- Hard-coding signing keys, tokens, passwords, or repository credentials.

# Risks

- External repository publishing requires credentials and manual account setup that cannot be fully validated in ordinary CI.
- Ecosystem-specific policies may reject package metadata that works for GitHub Release artifacts.
- Publishing mistakes can make broken packages available to users, so approval gates and dry-runs are important.
- Package signing must be implemented before publication; signing key handling creates additional operational risk.
- Maintaining multiple repository targets can create version drift if package metadata is not updated consistently.

# Questions

- Resolved: implement PPA/apt repository publishing first.
- Resolved: package signing must be completed before any native repository publishing goes live.
- Resolved: publishing workflows must require GitHub Environment approval before pushing to external repositories.
