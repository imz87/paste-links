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
2. Add a new project
3. Upload the spec file and source tarball
4. Enable builds for desired Fedora releases

## Cross-Distro Support

The local installer (`install.sh`) works on any Linux distribution with a compatible Nautilus 4 desktop. The installer checks for the Nautilus Python extension loader before copying files.

Package names vary by distribution. The `nautilus-python` package (or equivalent) must provide `libnautilus-python.so`. See `README.md` for distro-specific install commands.

## Non-Goals

- This project is not a GNOME Shell extension.
- It should not be submitted to `extensions.gnome.org`.
