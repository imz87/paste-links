Name:           paste-links
Version:        0.1.3
Release:        1%{?dist}
Summary:        Add Paste Symlink action to GNOME Files
License:        MIT
URL:            https://github.com/imz87/paste-links
Source0:        %{name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python3-devel
Requires:       nautilus-python
Requires:       python3-gobject
Requires:       gtk4

%description
A Nautilus Python extension that adds a "Paste Symlink" action to the
folder background context menu in GNOME Files. It creates symbolic links from
files or folders currently copied in GNOME Files using the normal Ctrl+C flow.

Supports multiple copied items, handles name collisions, and shows error
dialogs for invalid clipboard cases.

%prep
%autosetup -n %{name}-%{version}

%build
# Nothing to build; this is a pure Python extension

%install
mkdir -p %{buildroot}%{_datadir}/nautilus-python/extensions
install -m 0644 src/paste_links.py \
    %{buildroot}%{_datadir}/nautilus-python/extensions/paste_links.py
install -m 0644 src/core_logic.py \
    %{buildroot}%{_datadir}/nautilus-python/extensions/core_logic.py

%files
%license LICENSE
%doc README.md
%{_datadir}/nautilus-python/extensions/paste_links.py
%{_datadir}/nautilus-python/extensions/core_logic.py

%post
echo ""
echo "Restart Nautilus / GNOME Files for the extension to take effect:"
echo ""
echo "  nautilus -q"
echo ""
echo "Then reopen Files. The \"Paste Symlink\" menu will appear in the context menu."
echo ""

%changelog
* Thu Jul 09 2026 Iman <iman@example.com> 0.1.0-1
- Initial RPM release
- Add Paste Symlink context menu action for GNOME Files
- Create symlinks from copied local files and folders
- Handle name collisions with -link suffixes
