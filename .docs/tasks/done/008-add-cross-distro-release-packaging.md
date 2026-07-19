# Task

Add cross-distro packaging assets and a GitHub Actions release workflow that can build downloadable release artifacts for common Linux package managers.

# Background

The project currently supports local installation through `install.sh`, source distribution through GitHub, and Fedora RPM packaging through `packaging/nautilus-paste-shortcut.spec`. Task 003 added the initial Fedora RPM assets. Task 007 covers cross-distro CI for syntax, tests, and dependency availability, but explicitly excludes package publishing workflows.

This task covers packaging for additional distro families and release artifact generation. The intent is to let GitHub Releases provide installable artifacts such as RPM, DEB, Arch, and openSUSE-compatible packages or recipes, while keeping repository publishing systems such as COPR, PPA, AUR, and OBS as separate future work.

Decisions for this task:

- Include all initial packaging targets: RPM, DEB, Arch, and openSUSE.
- Package signing is out of scope and should be planned separately.
- Package versions should come from a version file in the repository, not only from Git tags.
- GitHub Releases are the only distribution mechanism for this task; external repositories are a follow-up task.

# Files Expected To Change

- `.github/workflows/release.yml`
  - Add a release-oriented workflow that builds packages when a version tag or manual workflow dispatch is used.

- `packaging/nautilus-paste-shortcut.spec`
  - Reuse or adjust the existing RPM spec only if required for reliable release builds.

- `packaging/debian/` or equivalent Debian packaging files
  - Add the minimal Debian packaging metadata needed to build a `.deb` package for Ubuntu/Debian users.

- `packaging/arch/PKGBUILD` or equivalent Arch packaging files
  - Add an Arch-style package recipe and build validation for Arch-family users.

- `packaging/opensuse/` or equivalent openSUSE packaging files
  - Add openSUSE-specific RPM packaging metadata if the existing Fedora RPM spec cannot be reused safely across both RPM distro families.

- `VERSION` or another clearly documented repository version file
  - Add a simple version source used by package metadata and release workflow logic.

- `README.md`
  - Document which package artifacts are produced, how users can install them, and the support boundaries for each distro family.

- `.docs/project/packaging.md`
  - Update packaging documentation with the new release artifact strategy, build commands, install paths, and publishing boundaries.

- `.docs/project/verification.md`
  - Add focused verification commands for package metadata/build checks where practical.

# Architecture Notes

- Nautilus integration surface
  - Packaging must continue to install the Python Nautilus extension files into the distro-appropriate Nautilus Python extension directory.
  - Packaging must not change the Nautilus `MenuProvider` behavior or runtime integration surface.

- Clipboard or filesystem behavior
  - This task is packaging-only. It must not change clipboard parsing, symlink creation, collision handling, or supported URI behavior.

- Packaging or install implications
  - GitHub Actions can build package artifacts and attach them to GitHub Releases. This is appropriate for downloadable release packages.
  - GitHub Actions can also prepare artifacts for later repository publishing, but native repository distribution remains different per ecosystem:
    - Fedora/RHEL family: RPM artifacts, with COPR as a likely repository path.
    - Debian/Ubuntu family: DEB artifacts, with PPA or an apt repository as future repository paths.
    - Arch family: PKGBUILD/AUR is usually recipe-based rather than uploading a binary package to a generic release.
    - openSUSE family: RPM can often be reused or adapted, with OBS as the usual repository path.
  - Initial release automation should build downloadable packages for GitHub Releases only. External repository publishing is covered by a separate follow-up task.
  - Keep package metadata dependencies aligned with README dependency guidance: Nautilus 4, GTK 4, PyGObject, and the Nautilus Python extension loader.
  - Package versioning should be driven by a version file in the repository. The release workflow may still validate that release tags match the version file, but tags must not be the only source of package version information.
  - Package signing is intentionally deferred to a separate task so this task can establish unsigned artifact builds first.

- User-visible behavior boundaries
  - Users should be told that GitHub Release artifacts are not the same as adding an apt/dnf/pacman repository.
  - Documentation should be clear about tested versus best-effort distro support.
  - Restarting Nautilus after install or uninstall must remain documented for package installs.

# Implementation Steps

1. Inspect the existing RPM spec and README packaging sections to identify the current package name, version, dependencies, install paths, and release assumptions.
2. Add or choose a repository version file, such as `VERSION`, and document it as the source for package versions.
3. Configure package metadata and release workflow logic to read the version from the repository version file.
4. Validate release tags against the version file when tag-triggered releases run, failing clearly if they do not match.
5. Implement the initial package artifact set:
   - source tarball
   - Fedora-compatible RPM
   - Debian/Ubuntu `.deb`
   - Arch package or PKGBUILD-based artifact
   - openSUSE-compatible RPM/package artifact or clearly separated openSUSE RPM metadata
6. Add minimal Debian packaging metadata under `packaging/debian/` or another conventional location.
7. Add Arch packaging metadata under `packaging/arch/`.
8. Add openSUSE packaging metadata under `packaging/opensuse/` if the Fedora RPM spec cannot safely cover openSUSE dependency names and macros.
9. Add `.github/workflows/release.yml` that runs on version tags such as `v*` and supports `workflow_dispatch` for test builds.
10. In the release workflow, build packages in distro-appropriate containers or runners using non-interactive package-manager commands.
11. Configure the workflow to upload package files as workflow artifacts for manual runs.
12. Configure the workflow to attach package files to GitHub Releases for tag-triggered release runs.
13. Keep package artifacts unsigned and document that signing is deferred to a separate task.
14. Update README with installation examples for release artifacts, including `dnf install ./package.rpm`, `apt install ./package.deb`, Arch install guidance, and openSUSE install guidance.
15. Update `.docs/project/packaging.md` with the release packaging strategy and a clear distinction between GitHub Release artifacts and package repository publishing.
16. Update `.docs/project/verification.md` with package metadata checks and any local build commands that reviewers can run without publishing a release.
17. Run focused verification for package metadata and workflow syntax where available.

# Acceptance Criteria

- [ ] The repository contains a GitHub Actions release workflow for package artifact builds.
- [ ] The release workflow can be run manually with `workflow_dispatch` and uploads package artifacts without publishing an external package repository.
- [ ] The release workflow attaches built artifacts to GitHub Releases when triggered by a valid version tag.
- [ ] The repository has a clear version file used as the package version source.
- [ ] Tag-triggered release builds validate that the Git tag matches the repository version file, or fail with a clear error.
- [ ] RPM release artifact generation reuses the existing RPM packaging assets where practical.
- [ ] Debian/Ubuntu `.deb` packaging metadata exists and declares the required Nautilus/PyGObject/GTK dependencies using appropriate package names.
- [ ] Arch packaging metadata exists, including a clear `PKGBUILD` or equivalent recipe/build artifact path.
- [ ] openSUSE packaging support exists either through compatible RPM metadata or a documented openSUSE-specific packaging path.
- [ ] Package artifacts produced by this task are unsigned, and README or packaging docs state that signing is deferred to a separate task.
- [ ] README documents how to install the generated release artifacts and restart Nautilus afterward.
- [ ] `.docs/project/packaging.md` explains that GitHub Release artifacts are not the same as an apt/dnf/pacman/zypper repository.
- [ ] `.docs/project/packaging.md` lists future repository-publishing paths such as COPR, PPA/apt repo, AUR, and OBS as separate follow-up work.
- [ ] Package install paths remain appropriate for Nautilus Python extensions.
- [ ] Runtime source behavior is unchanged.
- [ ] Focused verification commands for package metadata/builds are documented and pass where the required tooling is available.

# Out Of Scope

- Publishing to COPR, Fedora official repositories, PPA, a hosted apt repository, AUR, OBS, Snapcraft, Flathub, or distro official repositories.
- Adding signing keys, package signing, secrets, repository credentials, or automated external publishing.
- Changing Nautilus runtime behavior, clipboard behavior, symlink behavior, or menu visibility behavior.
- Adding GUI automation for Nautilus package verification.
- Guaranteeing support for every distro or every release version.

# Risks

- Package dependency names differ across Debian, Ubuntu, Arch, Fedora, and openSUSE, especially for Nautilus Python loader support.
- Some distributions may not provide a compatible Nautilus Python extension loader package for current Nautilus versions.
- Binary package artifacts in GitHub Releases do not provide automatic updates like a native package repository.
- Release workflow version handling can become brittle if package metadata, the repository version file, and Git tags drift.
- Building packages across multiple distro containers can make release workflows slow or fragile.
- openSUSE and Fedora both use RPM, but dependency names and macros may differ enough to need separate packaging adjustments.

# Questions

- Resolved: include all initial packaging targets: RPM, DEB, Arch, and openSUSE.
- Resolved: package signing should be planned as a separate task and is out of scope here.
- Resolved: package versions should come from a version file in the repository.
- Resolved: GitHub Releases are the only distribution mechanism for this task; COPR/PPA/AUR/OBS are separate follow-up work.
