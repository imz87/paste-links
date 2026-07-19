# Task

Make GitHub Releases publish installable package artifacts for Fedora, openSUSE, Debian/Ubuntu, and Arch Linux.

# Background

The project already has multi-distro packaging intent documented in `README.md` and `.docs/project/packaging.md`. Packaging metadata exists for the target formats:

- Fedora RPM: `packaging/nautilus-paste-shortcut.spec`
- openSUSE RPM: `packaging/opensuse/nautilus-paste-shortcut.spec`
- Debian/Ubuntu DEB: `packaging/debian/`
- Arch Linux package: `packaging/arch/PKGBUILD`

Current CI tests Fedora, Ubuntu, Debian, Arch Linux, and openSUSE containers. However, the release workflow in `.github/workflows/ci.yml` currently appears to build and attach only a source tarball and Fedora RPM to GitHub Releases, while the Debian path is oriented toward source-package/PPA publishing. The workflow should match the documented GitHub Release artifact promise by producing downloadable installable packages for all requested distributions.

# Files Expected To Change

- `.github/workflows/ci.yml`
  - Add or adjust release jobs to build Fedora RPM, openSUSE RPM, Debian/Ubuntu `.deb`, Arch `.pkg.tar.zst`, and source tarball artifacts.
  - Ensure the GitHub Release upload includes all built package artifacts and their signatures where applicable.
- `packaging/nautilus-paste-shortcut.spec`
  - May need small metadata/version/source consistency fixes for Fedora RPM builds from the release tarball.
- `packaging/opensuse/nautilus-paste-shortcut.spec`
  - May need small metadata/version/source consistency fixes for openSUSE RPM builds from the release tarball.
- `packaging/debian/*`
  - May need small build metadata adjustments so `dpkg-buildpackage -b` produces an installable `.deb` in the release workflow.
- `packaging/arch/PKGBUILD`
  - May need small source/version/path adjustments so `makepkg` can build from the workflow-provided source tarball.
- `README.md`
  - Update only if release artifact instructions or package availability wording changes.
- `.docs/project/packaging.md`
  - Update only if the actual release artifact workflow differs from the current documented design.
- `.docs/project/verification.md`
  - Update only if verification commands or expected artifact outputs change.

# Architecture Notes

- Nautilus integration surface
  - Do not change the Nautilus extension API, context menu behavior, clipboard parsing, or symlink creation behavior. This is packaging/release automation work only.
- Clipboard or filesystem behavior
  - No clipboard-format, symlink, collision-handling, or local-filesystem runtime behavior should change.
- Packaging or install implications
  - GitHub Release artifacts should be installable manually by users with native package tools:
    - Fedora: `dnf install ./nautilus-paste-shortcut-*.rpm`
    - openSUSE: `zypper install ./nautilus-paste-shortcut-*.rpm`
    - Debian/Ubuntu: `apt install ./nautilus-paste-shortcut_*.deb`
    - Arch Linux: `pacman -U nautilus-paste-shortcut-*.pkg.tar.zst`
  - Native package repository publishing is out of scope. Do not add COPR, OBS, AUR upload, apt repository, or new PPA publishing behavior as part of this task.
  - Preserve the existing CI test matrix for Fedora, Ubuntu, Debian, Arch Linux, and openSUSE.
- Release artifact signing should be consistent across built package artifacts. If the existing signing approach requires secrets, keep secret material out of the repository and make unsigned dry-run behavior explicit if needed.
  - Release artifact signing should be consistent across built package artifacts. Required GPG signing secrets must be present; missing signing secrets should fail the whole release artifact process.
- User-visible behavior boundaries
  - Users should see more downloadable package files attached to GitHub Releases.
  - Application behavior inside Nautilus should remain unchanged.
  - GitHub Release artifacts do not provide automatic updates; users still manually download and install newer release artifacts.

# Implementation Steps

1. Inspect the current release jobs in `.github/workflows/ci.yml` and identify the existing source tarball, Fedora RPM, source-package/PPA, signing, tag, and release-upload flow.
2. Decide whether to keep all release artifact jobs in `.github/workflows/ci.yml` or split release packaging into a dedicated workflow. Prefer the smallest safe change unless the existing workflow becomes too hard to maintain.
3. Ensure the source tarball is created once from the checked-out release revision and is usable by all package builders with the expected `nautilus-paste-shortcut-${VERSION}/` prefix.
4. Add or update the Fedora RPM build job to build `packaging/nautilus-paste-shortcut.spec` using the workflow `VERSION` value and upload the resulting `.rpm` artifact.
5. Add an openSUSE RPM build job using an openSUSE container, `packaging/opensuse/nautilus-paste-shortcut.spec`, the same source tarball, and upload the resulting `.rpm` artifact.
6. Add a Debian/Ubuntu binary package build job using an Ubuntu or Debian container. Copy `packaging/debian` to `debian`, update the changelog version from `VERSION`, run a binary package build such as `dpkg-buildpackage -us -uc -b`, and upload the resulting `.deb` artifact.
7. Add an Arch Linux package build job using an Arch container. Use `packaging/arch/PKGBUILD`, ensure it consumes the release source tarball correctly, run `makepkg`, and upload the resulting `.pkg.tar.zst` artifact.
8. Update the signing job so each release package artifact receives a detached `.asc` signature using the existing GPG secret strategy, without committing keys or printing secret material.
9. Update the GitHub Release creation step so it attaches the source tarball, Fedora RPM, openSUSE RPM, Debian/Ubuntu `.deb`, Arch `.pkg.tar.zst`, and corresponding `.asc` signature files.
10. Keep PPA publishing behavior unchanged unless a small adjustment is necessary to avoid breaking the new release artifact flow. Do not expand PPA scope.
11. Update README and project packaging/verification docs only where needed so they match the actual release artifact workflow.
12. Run targeted workflow syntax and packaging metadata checks where practical.

# Acceptance Criteria

- [ ] A release workflow run builds a source tarball artifact.
- [ ] A release workflow run builds a Fedora `.rpm` artifact.
- [ ] A release workflow run builds an openSUSE `.rpm` artifact.
- [ ] A release workflow run builds a Debian/Ubuntu `.deb` artifact.
- [ ] A release workflow run builds an Arch Linux `.pkg.tar.zst` artifact.
- [ ] GitHub Release upload includes all package artifacts listed above.
- [ ] GitHub Release upload includes detached `.asc` signatures for all published package artifacts when signing is enabled.
- [ ] Missing required GPG signing secrets fail the release artifact process rather than producing unsigned release artifacts.
- [ ] Artifact filenames include the project name and release version in distro-appropriate formats.
- [ ] Existing multi-distro CI test jobs remain in place.
- [ ] Docs do not claim native repository support as part of this task.
- [ ] No behavior changes except those explicitly requested in this task.
- [ ] No new background services or desktop hooks unless explicitly requested.
- [ ] No packaging-system expansion beyond GitHub Release artifacts unless explicitly requested.
- [ ] No clipboard-format changes unless explicitly requested.
- [ ] No environment or secret-handling changes beyond release artifact signing unless explicitly requested.

# Out Of Scope

- Publishing to COPR.
- Publishing to openSUSE OBS.
- Publishing to AUR.
- Publishing to Debian/Ubuntu package archives or adding a new apt repository.
- Expanding PPA support beyond preserving existing behavior.
- Changing Nautilus menu behavior, clipboard handling, symlink creation, or error dialogs.
- Adding automatic update mechanisms for GitHub Release artifact users.

# Risks

- Package dependency names differ by distribution, especially for Nautilus Python loader packages.
- Arch `PKGBUILD` may require workflow-specific source handling because release tarballs are generated during CI rather than downloaded from a stable URL.
- openSUSE RPM dependency names may not match Fedora names exactly.
- Signing release artifacts can fail if GPG secrets are missing, incorrectly configured, or unavailable on non-tag workflow runs.
- Current release and PPA logic share the same workflow; adding binary package artifacts must not accidentally publish to PPA or require protected-environment approval for normal artifact builds.
- Container package builds validate package creation but do not prove the Nautilus extension loads in a real desktop session.

# Questions

- Resolved: Build one Debian-compatible `.deb` artifact; separate Debian and Ubuntu artifacts are not required.
- Resolved: Keep the current release triggering strategy, including the existing manual workflow dispatch path for testing without unintended publication.
- Resolved: Missing required GPG signing secrets should fail the whole release artifact process; do not produce unsigned release artifacts when signing is expected.
