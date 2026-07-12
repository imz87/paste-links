# Packaging Notes

## Current Distribution

- Local install through `install.sh`
- Source distribution through GitHub
- Fedora RPM packaging assets in `packaging/`

## RPM Packaging

The repository contains a `.spec` file for building RPM packages:

```text
packaging/nautilus-paste-shortcut.spec
```

### Build a Local RPM

1. Install build dependencies:
   ```bash
   sudo dnf install rpm-build rpmdevtools
   ```

2. Set up the RPM build tree:
   ```bash
   rpmdev-setuptree
   ```

3. Create a source tarball:
   ```bash
   git archive --format=tar.gz --prefix=nautilus-paste-shortcut-0.1.0/ \
       HEAD -o ~/rpmbuild/SOURCES/nautilus-paste-shortcut-0.1.0.tar.gz
   ```

4. Build the RPM:
   ```bash
   rpmbuild -ba packaging/nautilus-paste-shortcut.spec
   ```

5. Install the built RPM:
   ```bash
   sudo dnf install ~/rpmbuild/RPMS/noarch/nautilus-paste-shortcut-0.1.0-1.*.rpm
   ```

6. Restart Nautilus:
   ```bash
   nautilus -q
   ```

### Uninstall

Remove the installed package and restart Nautilus so the extension is no longer loaded:

```bash
sudo dnf remove nautilus-paste-shortcut
nautilus -q
```

### Install Paths

- Extension file: `/usr/share/nautilus-python/extensions/nautilus_paste_shortcut.py`
- License: `/usr/share/licenses/nautilus-paste-shortcut/LICENSE`
- Documentation: `/usr/share/doc/nautilus-paste-shortcut/README.md`

### Package Dependencies

- `python3-nautilus` - Nautilus Python bindings
- `nautilus-python` - Nautilus Python extension loader (provides `libnautilus-python.so`)
- `python3-gobject` - Python GObject introspection bindings
- `gtk4` - GTK4 toolkit

**Important:** `nautilus-python` is the extension loader, not just Python bindings. Without it, Nautilus silently ignores `.py` files in the extensions directory. The `install.sh` script checks for this before copying files.

### COPR Distribution

COPR packages can be built from the same spec file. To publish to COPR:

1. Create a COPR account at `copr.fedorainfracloud.org`
2. Create a new project at `https://copr.fedorainfracloud.org/coprs/<username>/new-visit/`
3. Get your API token at `https://copr.fedorainfracloud.org/api/`
4. Add the full COPR config block as a GitHub repository secret named `COPR_API_TOKEN`
5. Run the `publish-copr.yml` workflow via GitHub Actions

**Required GitHub Actions Secrets:**

| Secret Name | Description |
|---|---|
| `COPR_API_TOKEN` | Full config block from `https://copr.fedorainfracloud.org/api/`, starting with `[copr-cli]` |
| `OPENSUSE_OBS_USERNAME` | OBS username for openSUSE publishing |
| `OPENSUSE_OBS_PASSWORD` | OBS password for openSUSE publishing |
| `ARCH_AUR_SSH_KEY` | SSH private key for AUR (currently unused while AUR publishing is disabled) |

**Manual COPR build:**

```bash
# Install tools
sudo dnf install rpm-build rpmdevtools copr-cli

# Add package to COPR (one-time setup)
copr-cli add-package-scm imz87/nautilus-paste-shortcut \
    --name nautilus-paste-shortcut \
    --type git \
    --clone-url https://github.com/imz87/nautilus-paste-shortcut.git \
    --commit main \
    --spec packaging/nautilus-paste-shortcut.spec \
    --method make_srpm

# Build source RPM
VERSION=$(cat VERSION)
rpmdev-setuptree
git archive --format=tar.gz --prefix="nautilus-paste-shortcut-${VERSION}/" \
    HEAD -o ~/rpmbuild/SOURCES/nautilus-paste-shortcut-${VERSION}.tar.gz
sed -i "s/^Version:.*/Version:        ${VERSION}/" packaging/nautilus-paste-shortcut.spec
cp packaging/nautilus-paste-shortcut.spec ~/rpmbuild/SPECS/
rpmbuild -bs ~/rpmbuild/SPECS/nautilus-paste-shortcut.spec

# Submit build to COPR
copr-cli build --chroot fedora-rawhide-x86_64 --chroot fedora-44-x86_64 --chroot fedora-43-x86_64 imz87/nautilus-paste-shortcut \
    ~/rpmbuild/SRPMS/nautilus-paste-shortcut-*.src.rpm
```

**Users can then install from COPR:**

```bash
sudo dnf copr enable imz87/nautilus-paste-shortcut
sudo dnf install nautilus-paste-shortcut
```

## Cross-Distro Support

The local installer (`install.sh`) works on any Linux distribution with a compatible Nautilus 4 desktop. The installer checks for the Nautilus Python extension loader before copying files.

Package names vary by distribution. The `nautilus-python` package (or equivalent) must provide `libnautilus-python.so`. See `README.md` for distro-specific install commands.

## Release Artifact Packaging

GitHub Actions can build package artifacts and attach them to GitHub Releases. This provides downloadable installable packages for multiple distributions.

### Version File

The repository uses a `VERSION` file as the single source of truth for package versions. The release workflow reads this file and validates it against Git tags when triggered by version tags.

```bash
cat VERSION
# Output: 0.1.0
```

### Build Artifacts

The release workflow builds these package formats:

| Distribution | Format | Build Container |
|---|---|---|
| Fedora/RHEL | `.rpm` | `fedora:latest` |
| Ubuntu/Debian | `.deb` | `ubuntu:24.04` |
| Arch Linux | `.pkg.tar.zst` | `archlinux:latest` |
| openSUSE | `.rpm` | `opensuse/tumbleweed:latest` |

### Packaging Files

- **Fedora**: `packaging/nautilus-paste-shortcut.spec`
- **Ubuntu/Debian**: `packaging/debian/`
- **Arch Linux**: `packaging/arch/PKGBUILD`
- **openSUSE**: `packaging/opensuse/nautilus-paste-shortcut.spec`

### Installation from Release Artifacts

Fedora/RHEL:
```bash
sudo dnf install ./nautilus-paste-shortcut-*.rpm
nautilus -q
```

Ubuntu/Debian:
```bash
sudo apt install ./nautilus-paste-shortcut_*.deb
nautilus -q
```

Arch Linux:
```bash
sudo pacman -U nautilus-paste-shortcut-*.pkg.tar.zst
nautilus -q
```

openSUSE:
```bash
sudo zypper install ./nautilus-paste-shortcut-*.rpm
nautilus -q
```

### Important Distinctions

**GitHub Release artifacts are NOT the same as native package repositories.** They do not provide automatic updates. Users must download and install new versions manually from GitHub Releases.

**Release artifacts are signed.** Each package file includes a corresponding `.asc` signature file created with GPG.

### Package Signing Strategy

Release artifacts are signed in GitHub Actions using GPG. The signing process:

1. **Signing identity:** `Nautilus Paste Shortcut Release Signing <zolfaghari19@gmail.com>`
2. **Key management:** The GPG private key is stored as a GitHub Actions secret (`GPG_PRIVATE_KEY`) with an optional passphrase (`GPG_PASSPHRASE`).
3. **Signing scope:** All release artifacts (RPM, DEB, Arch, source tarball) are signed with detached `.asc` signatures.
4. **When signing occurs:** Only on tag-triggered releases (`v*` tags), not on pull requests or manual workflow dispatches.

**Required GitHub Actions Secrets:**

| Secret Name | Description |
|---|---|
| `GPG_PRIVATE_KEY` | ASCII-armored GPG private key for signing |
| `GPG_PASSPHRASE` | Passphrase for the GPG key (can be empty) |

**Signing artifacts in GitHub Actions:**

```bash
# Import the GPG key
echo "$GPG_PRIVATE_KEY" | gpg --batch --import

# Sign a file with detached signature
gpg --batch --yes --detach-sign package.rpm

# This creates package.rpm.asc
```

**Signature verification:**

Users can verify signatures using the public key:

```bash
# Import the public key (one-time setup)
gpg --import nautilus-paste-shortcut-signing-key.asc

# Verify a signature
gpg --verify package.rpm.asc package.rpm
```

**Key rotation and revocation:**

- Keys should be rotated annually or when a maintainer leaves.
- Revoked keys should be added to public key servers.
- New keys must be updated in the `GPG_PRIVATE_KEY` secret.

**Security considerations:**

- Private keys are never committed to the repository.
- Signing occurs only in GitHub Actions, not locally.
- The `GPG_PRIVATE_KEY` secret should be protected with branch protection rules.
- Workflow logs should not print key material.

### Future Repository Publishing

Native package repository publishing is separate work:

- **Fedora/RHEL family**: COPR repository (implemented)
- **Debian/Ubuntu family**: PPA or apt repository (implemented)
- **openSUSE family**: OBS publishing (implemented)
- **Arch family**: AUR package recipe (temporarily disabled until the AUR account/package is ready)

Repository publishing requires package signing, credentials, and different automation than release artifact builds. The signing infrastructure established in this task enables future repository publishing.

## PPA/apt Repository Publishing

The first native repository target is PPA for Debian/Ubuntu-family distribution. This provides automatic updates through `apt` rather than manual downloads from GitHub Releases.

### PPA Publishing Strategy

**Repository:** `ppa:imz87/nautilus-paste-shortcut`

**Target distributions:**
- Ubuntu Noble (24.04 LTS) - primary target
- Ubuntu Jammy (22.04 LTS) - LTS support
- Debian Bookworm - stable support

**Publishing workflow:** `.github/workflows/publish-ppa.yml`

**Required GitHub Actions Secrets:**

| Secret Name | Description |
|---|---|
| `PPA_LAUNCHPAD_USERNAME` | Launchpad username for PPA access |
| `GPG_PRIVATE_KEY` | GPG private key for package signing |
| `GPG_PASSPHRASE` | Passphrase for the GPG key (can be empty) |

### PPA Setup Requirements

1. **Launchpad account:** Create an account at `launchpad.net`
2. **PPA creation:** Create a PPA in Launchpad settings
3. **GPG key:** Generate a GPG key for package signing
4. **GitHub secrets:** Configure the required secrets

### PPA Publishing Workflow

The workflow runs on:
- **Tag pushes** (`v*` tags) - automatic publication
- **Manual dispatch** - with dry-run option

**Workflow steps:**
1. Validate version and signing prerequisites
2. Build source package using `dpkg-buildpackage -S`
3. Import GPG key from secrets
4. Upload to PPA using `dput`

**Safety features:**
- Dry-run mode for testing
- Tag validation against VERSION file
- GPG signing for package authenticity
- Secret validation before upload

### PPA Installation

Users can install from the PPA:

```bash
sudo add-apt-repository ppa:imz87/nautilus-paste-shortcut
sudo apt update
sudo apt install nautilus-paste-shortcut
```

### PPA Maintenance

- **Version updates:** Update `VERSION` file and create a new tag
- **Signing key rotation:** Update `PPA_GPG_PRIVATE_KEY` secret
- **Series updates:** Modify workflow `target_series` input
- **Monitoring:** Check Launchpad build logs for issues

### PPA vs Release Artifacts

| Feature | PPA Repository | GitHub Releases |
|---|---|---|
| Installation method | `apt install` | Manual download + `apt install ./package.deb` |
| Automatic updates | Yes | No |
| Update mechanism | `apt update && apt upgrade` | Download new version manually |
| Trust model | Launchpad infrastructure | GitHub Release signatures |
| Supported distros | Ubuntu/Debian | Multiple distros |

### Future Repository Targets

No remaining targets — all major distros are implemented.

Each ecosystem has different credentials, review expectations, metadata rules, and automation constraints. The PPA publishing infrastructure serves as a template for future repository targets.

## Non-Goals

- This project is not a GNOME Shell extension.
- It should not be submitted to `extensions.gnome.org`.
