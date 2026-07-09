# Task

Add package signing support for release artifacts before native package repository publishing goes live.

# Background

Task 008 plans unsigned GitHub Release artifacts for RPM, DEB, Arch, and openSUSE packaging. Native PPA/apt repository publishing should not go live until package signing is implemented and documented.

This task establishes signing for package artifacts and documents how signing keys are managed safely in GitHub Actions.

Decisions for this task:

- Signing should be performed in GitHub Actions only.
- Local maintainer signing should not be part of the initial implementation.
- Use this initial signing key identity: `Nautilus Paste Shortcut Release Signing <zolfaghari19@gmail.com>`.

# Files Expected To Change

- `.github/workflows/release.yml` or a dedicated signing workflow
  - Add signing steps for release artifacts after package builds complete.

- `packaging/`
  - Adjust package metadata or build scripts only where required for signing.

- `README.md`
  - Document signed release artifacts and how users can verify them where appropriate.

- `.docs/project/packaging.md`
  - Document signing strategy, key ownership, secret names, and GitHub Actions operational boundaries.

- `.docs/project/verification.md`
  - Document safe signing verification commands that do not expose private keys.

# Architecture Notes

- Nautilus integration surface
  - Signing must not change Nautilus extension runtime behavior or install locations.

- Clipboard or filesystem behavior
  - Signing is distribution-only. It must not change clipboard behavior, symlink behavior, or filesystem runtime behavior.

- Packaging or install implications
  - Signing should cover package artifacts needed for GitHub Releases and future PPA/apt publishing.
  - Signing keys must not be committed to the repository.
  - GitHub Actions should use documented secret names and protected environments for signing operations.
  - Local maintainer signing is out of scope for the initial signing implementation.
  - Signing should be integrated in a way that future repository publishing tasks can reuse.

- User-visible behavior boundaries
  - README should not overpromise official distro trust. It should describe project-provided signatures and verification steps only.

# Implementation Steps

1. Inspect task 008 package artifact outputs and identify which formats need signing for RPM, DEB/PPA, Arch, and openSUSE paths.
2. Use the initial signing key identity `Nautilus Paste Shortcut Release Signing <zolfaghari19@gmail.com>`.
3. Choose a signing strategy for each artifact type and document any format-specific limits.
4. Define required GitHub Actions secret names and protected environment expectations.
5. Add signing steps after successful package builds, ensuring private keys are never printed or committed.
6. Add verification steps that check signatures using public keys or package tooling.
7. Update README with concise user-facing verification guidance.
8. Update `.docs/project/packaging.md` with signing ownership, rotation expectations, and relationship to future repository publishing.
9. Update `.docs/project/verification.md` with safe local and CI verification commands.

# Acceptance Criteria

- [ ] Package signing support exists for the release artifact formats needed before PPA/apt publishing.
- [ ] The initial signing identity is `Nautilus Paste Shortcut Release Signing <zolfaghari19@gmail.com>`.
- [ ] Signing keys are provided only through documented secrets or protected release infrastructure.
- [ ] No private keys, passwords, or signing secrets are committed to the repository.
- [ ] Signing workflows require an explicit release/tag/manual trigger and do not sign packages on ordinary pull requests.
- [ ] Signing is performed in GitHub Actions only for the initial implementation.
- [ ] Signature verification is documented and automated where practical.
- [ ] README explains how users can verify signed artifacts where appropriate.
- [ ] `.docs/project/packaging.md` documents the signing strategy and how it enables future native repository publishing.
- [ ] Runtime source behavior is unchanged.
- [ ] No behavior changes except those explicitly requested in this task.

# Out Of Scope

- Publishing to PPA/apt, COPR, AUR, OBS, or official distro repositories.
- Local maintainer signing workflows or local private-key setup documentation.
- Changing Nautilus runtime behavior.
- Changing clipboard parsing, symlink creation, or menu visibility.
- Committing private signing material to the repository.

# Risks

- Signing setup can expose secrets if workflow logging is not handled carefully.
- Different package formats have different signing conventions and verification commands.
- Key rotation and revocation need operational planning beyond the initial implementation.
- Repository publishing may have additional signing requirements not fully covered by downloadable release artifacts.

# Questions

- Resolved: use initial signing identity `Nautilus Paste Shortcut Release Signing <zolfaghari19@gmail.com>`.
- Resolved: signing should be performed in GitHub Actions only; local maintainer signing is out of scope for the initial implementation.
