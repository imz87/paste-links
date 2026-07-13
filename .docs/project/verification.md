# Verification

## Focused Checks

Use these checks for normal changes:

```bash
python3 -m py_compile src/nautilus_paste_shortcut.py
bash -n install.sh
python3 -m pytest tests/ -v
```

## CI Checks

GitHub Actions CI runs these checks automatically on push and pull request across five distributions:

- **Fedora** (`fedora:latest`)
- **Ubuntu** (`ubuntu:24.04`)
- **Debian** (`debian:bookworm`)
- **Arch Linux** (`archlinux:latest`)
- **openSUSE Tumbleweed** (`opensuse/tumbleweed:latest`)

Each matrix job runs:

1. `bash -n install.sh` -- shell syntax validation
2. `python3 -m py_compile src/nautilus_paste_shortcut.py` -- Python syntax check (only when the Nautilus typelib is available)
3. `python3 -m pytest tests/ -v` -- pure unit tests

CI success means the project passes automated static and unit checks in distro containers. It does **not** guarantee the Nautilus context menu appears on every desktop. Container CI cannot verify Wayland clipboard behavior or Nautilus menu integration.

## Package Verification

Use these commands to verify package metadata and build artifacts locally:

### Version File

```bash
cat VERSION
# Should output: 0.1.0
```

### RPM (Fedora)

```bash
# Install build tools
sudo dnf install rpm-build rpmdevtools

# Set up build tree
rpmdev-setuptree

# Create source tarball
VERSION=$(cat VERSION)
git archive --format=tar.gz --prefix="nautilus-paste-shortcut-${VERSION}/" \
    HEAD -o ~/rpmbuild/SOURCES/nautilus-paste-shortcut-${VERSION}.tar.gz

# Build RPM
rpmbuild -ba packaging/nautilus-paste-shortcut.spec

# Verify RPM contents
rpm -qlp ~/rpmbuild/RPMS/noarch/nautilus-paste-shortcut-*.rpm
```

### DEB (Ubuntu/Debian)

```bash
# Install build tools
sudo apt install debhelper python3-all dh-python

# Build DEB
dpkg-buildpackage -us -uc -b

# Verify DEB contents
dpkg-deb -c ../nautilus-paste-shortcut_*.deb
```

### Arch Linux

```bash
# Install build tools
sudo pacman -S base-dependencies

# Build package
cd packaging/arch
makepkg -s

# Verify package contents
tar -tf nautilus-paste-shortcut-*.pkg.tar.zst
```

### openSUSE

```bash
# Install build tools
sudo zypper install rpm-build rpmdevtools python3-devel

# Set up build tree
rpmdev-setuptree

# Create source tarball
VERSION=$(cat VERSION)
git archive --format=tar.gz --prefix="nautilus-paste-shortcut-${VERSION}/" \
    HEAD -o ~/rpmbuild/SOURCES/nautilus-paste-shortcut-${VERSION}.tar.gz

# Build RPM
rpmbuild -ba packaging/opensuse/nautilus-paste-shortcut.spec

# Verify RPM contents
rpm -qlp ~/rpmbuild/RPMS/noarch/nautilus-paste-shortcut-*.rpm
```

### GitHub Actions Workflow

```bash
# Validate workflow syntax (requires act or similar tool)
act -l

# Or check YAML syntax
python3 -c "import yaml; yaml.safe_load(open('.github/workflows/release.yml'))"
```

### Package Signature Verification

Verify that release artifacts are signed correctly:

```bash
# Download a package and its .asc signature from GitHub Releases

# Import the signing public key (one-time setup)
gpg --import nautilus-paste-shortcut-signing-key.asc

# Verify GPG signature
gpg --verify package.rpm.asc package.rpm
# or
gpg --verify package.deb.asc package.deb
# or
gpg --verify package.pkg.tar.zst.asc package.pkg.tar.zst

# Verify RPM signature (Fedora/openSUSE)
rpm --checksig package.rpm

# List signature details
rpm -qip package.rpm | grep -i signature
```

**Expected output:**
- `gpg: Good signature from "Nautilus Paste Shortcut Release Signing <zolfaghari19@gmail.com>"`
- RPM: `package.rpm: digests SIGNATURE OK`

**Troubleshooting:**

```bash
# If gpg reports "public key not found"
gpg --keyserver keyserver.ubuntu.com --recv-keys <KEY_ID>

# If RPM reports "NOT OK"
rpm --import nautilus-paste-shortcut-signing-key.asc
rpm --checksig package.rpm
```

### Post-Install Restart Reminder

Verify that all installation paths print a clear restart reminder after install:

**Local install (`install.sh`):**
```bash
# Run install.sh and check output mentions "nautilus -q"
./install.sh 2>&1 | grep -q "nautilus -q"
```

**RPM (Fedora/openSUSE):**
```bash
# After building, inspect the spec for %post scriptlet
grep -A5 '%post' packaging/nautilus-paste-shortcut.spec
grep -A5 '%post' packaging/opensuse/nautilus-paste-shortcut.spec
# After installing the RPM, the package manager should print the reminder
```

**Debian/Ubuntu:**
```bash
# After building, inspect the postinst script
cat packaging/debian/postinst
# After installing the .deb, the package manager should print the reminder
```

**Arch Linux:**
```bash
# After building, inspect the PKGBUILD for post_install()
grep -A10 'post_install' packaging/arch/PKGBUILD
# After installing with pacman, the package manager should print the reminder
```

The reminder must:
- Tell the user to run `nautilus -q`
- Tell the user to reopen Files
- Not auto-restart Nautilus or close existing Files windows

### PPA/apt Repository Verification

Verify PPA publication and installation:

```bash
# Check if PPA is configured
apt-cache policy nautilus-paste-shortcut

# Verify package version from PPA
apt-cache show nautilus-paste-shortcut | grep Version

# Test PPA publication (dry run)
# This is done in the workflow - verify locally:
dpkg-buildpackage -us -uc -S
dput --dry-run ppa nautilus-paste-shortcut_*.changes

# Verify package installation from PPA
sudo add-apt-repository ppa:imz87/nautilus-paste-shortcut
sudo apt update
apt-cache policy nautilus-paste-shortcut

# Check package signatures from PPA
apt-key list | grep -A5 "nautilus-paste-shortcut"
```

**Expected output:**
- Package version should match VERSION file
- PPA should be listed in `apt-cache policy`
- Package should be installable via `apt install`

**Troubleshooting:**

```bash
# If PPA is not found
sudo add-apt-repository --remove ppa:imz87/nautilus-paste-shortcut
sudo add-apt-repository ppa:imz87/nautilus-paste-shortcut

# If package signature verification fails
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys <KEY_ID>

# If version mismatch
cat VERSION  # Should match PPA version
```

## Manual Checks

1. Copy one file in GNOME Files and run `Paste Shortcut` in another folder.
2. Copy one folder in GNOME Files and run `Paste Shortcut` in another folder.
3. Copy multiple items and verify one symlink is created per item.
4. Repeat with an existing destination name and verify suffix handling.
5. Press `Ctrl+X` and verify the menu item is hidden.
6. Copy non-file clipboard text and verify the menu item is hidden.

## Notes

- Review is a separate manual phase after development.
- For clipboard or Nautilus API changes, prefer a real desktop test over assumptions.
- Container CI covers dependency installation, Python compilation, shell syntax, and pure logic tests. Desktop integration (context menu, clipboard, error dialogs) still requires manual verification.
