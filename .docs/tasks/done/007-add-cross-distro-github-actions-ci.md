# Task

Add GitHub Actions CI with a cross-distro matrix and make the project as generic and portable as practical for current Nautilus Python extension constraints.

# Background

The project has been manually debugged on Fedora GNOME/Nautilus 48.7. Current installation and runtime behavior depend on distro-provided Nautilus, GTK 4, PyGObject, and the Nautilus Python extension loader. Task 006 covers local install checks, README troubleshooting, and moving pure clipboard normalization into testable code. This task adds CI coverage so future changes are checked across several common desktop Linux distributions where possible.

GitHub-hosted runners do not provide full graphical desktop sessions for every distribution. Cross-distro CI should therefore focus on what can be reliably automated in containers:

- dependency installation or dependency availability checks
- Python syntax checks
- pure unit tests
- `install.sh` shell syntax checks
- packaging/spec static checks where practical
- documentation that clarifies what CI does and does not prove

Manual Nautilus context-menu and clipboard behavior still require real desktop verification.

# Files Expected To Change

- `.github/workflows/ci.yml`
  - Add the main CI workflow with a matrix for common desktop-oriented Linux distributions.

- `install.sh`
  - May need small portability improvements if CI reveals Fedora-specific assumptions.
  - Coordinate with task 006 if both tasks touch loader/dependency checks.

- `README.md`
  - Add a GitHub Actions CI badge once the workflow exists.
  - Document supported/tested distro expectations and manual desktop verification boundaries.

- `.docs/project/verification.md`
  - Update with the new CI commands and the distinction between automated container checks and manual desktop checks.

- `.docs/project/packaging.md`
  - Update only if distro/package-manager notes or portability expectations change.

- `tests/`
  - May need small test portability fixes if tests assume Fedora-specific paths or packages.

# Architecture Notes

- Nautilus integration surface
  - CI must not pretend to verify live Nautilus menu-provider behavior unless a real desktop session is explicitly added and proven reliable.
  - Matrix jobs should verify that the Python modules can be compiled and pure logic tests can run with distro-appropriate dependencies.

- Clipboard or filesystem behavior
  - CI should cover pure clipboard normalization and symlink logic through tests, not live desktop clipboard APIs.
  - Real clipboard behavior remains desktop-session-specific and should stay in manual verification guidance.

- Packaging or install implications
  - The workflow should use distro package managers inside containers where practical.
  - Candidate matrix should prefer official or widely maintained base images. Suggested starting matrix:
    - Fedora latest/stable
    - Ubuntu latest LTS
    - Debian stable
    - Arch Linux latest
    - openSUSE Tumbleweed
  - Use Arch Linux as the rolling-release proxy instead of adding Manjaro to the initial matrix.
  - Manjaro compatibility may be documented as Arch-like/conditional but should not be claimed as tested unless a reliable Manjaro CI image is explicitly added later.

- User-visible behavior boundaries
  - The project can become more generic by avoiding Fedora-only assumptions in scripts and documentation.
  - CI success means the project passes automated static/unit checks for those distro containers; it does not guarantee the Nautilus context menu appears on every desktop.

# Implementation Steps

1. Inspect current tests and scripts to identify commands that can run headlessly in containers.
2. Add `.github/workflows/ci.yml` with triggers for `push` and `pull_request`.
3. Define a distro matrix using reliable container images. Prefer the five candidate distros listed in Architecture Notes unless a specific image is unavailable or unstable.
4. For each matrix entry, install the distro equivalents of required packages where available:
   - Python 3
   - PyGObject / GObject introspection runtime
   - GTK 4 introspection packages if available
   - Nautilus extension/typelib packages if available
   - pytest or Python tooling required by tests
5. Keep package installation commands distro-specific inside the workflow matrix, but keep project scripts generic.
6. Run focused checks in CI:
   - `python3 -m py_compile src/nautilus_paste_shortcut.py`
   - `bash -n install.sh`
   - relevant pytest command, such as `python3 -m pytest tests/ -v`
7. If a distro image cannot install required Nautilus Python/GTK dependencies reliably, fail the matrix job rather than silently downgrading it to weaker checks. Document any intentional substitution or blocker in the task/review notes.
8. Update `.docs/project/verification.md` with the CI command set and the manual desktop verification boundary.
9. Update README with a concise CI/support statement and a GitHub Actions status badge.
10. Ensure changes do not conflict with task 006. If task 006 has already extracted clipboard normalization, use those tests in CI; otherwise keep this task ready to run after task 006.

# Acceptance Criteria

- [ ] A GitHub Actions workflow exists under `.github/workflows/`.
- [ ] CI runs on `push` and `pull_request`.
- [ ] CI includes a documented five-distro matrix or a documented reason for any substitution.
- [ ] Candidate matrix includes Fedora, Ubuntu LTS, Debian stable, Arch Linux, and openSUSE Tumbleweed unless an implementation-time blocker is documented.
- [ ] Arch Linux is used as the rolling-release proxy; Manjaro is not part of the initial required matrix.
- [ ] CI runs `python3 -m py_compile src/nautilus_paste_shortcut.py`.
- [ ] CI runs `bash -n install.sh`.
- [ ] CI runs the pure/unit test suite where dependencies are available.
- [ ] Distro-specific dependency installation failures fail the relevant matrix job rather than being ignored or downgraded silently.
- [ ] Workflow package-install steps are explicit per distro and do not require interactive prompts.
- [ ] README includes a GitHub Actions CI badge once the workflow exists.
- [ ] README and/or `.docs/project/verification.md` explains that container CI does not replace manual Nautilus desktop verification.
- [ ] The project avoids new Fedora-only assumptions unless they are confined to Fedora packaging or Fedora-specific documentation.

# Out Of Scope

- Full GUI automation of Nautilus context menus in GitHub Actions.
- Guaranteeing runtime support for every Linux distribution.
- Building native `.so` Nautilus extensions.
- Adding COPR, PPA, AUR, Flatpak, Snap, or OBS publishing workflows.
- Replacing Fedora RPM packaging with a universal packaging system.

# Risks

- Some distro containers may not package Nautilus Python loader support in a way that works headlessly.
- Arch package names and availability can drift quickly; Manjaro may differ from Arch and remains unverified unless separately tested.
- Container CI cannot verify Wayland clipboard behavior or Nautilus menu integration.
- Installing full Nautilus/GTK stacks in containers may be slow or brittle; keep jobs focused and document limitations.
- A broad matrix may slow CI; use minimal packages and avoid unnecessary desktop components.

# Questions

- Resolved: use Arch Linux as the rolling-release proxy instead of adding Manjaro to the initial matrix.
- Resolved: distro-specific dependency installation failures should fail the relevant matrix job/workflow rather than being ignored or silently downgraded.
- Resolved: add a README GitHub Actions CI badge once the workflow exists.

# Commit Message

Add cross-distro GitHub Actions CI
