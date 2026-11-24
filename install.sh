#!/usr/bin/env bash
set -euo pipefail

usage() {
    printf 'Usage: %s [--install | --uninstall]\n\n' "$(basename "$0")"
    printf 'Install or uninstall the Paste Links extension.\n\n'
    printf '  --install      Install the extension (default)\n'
    printf '  --uninstall    Remove the extension and restart Nautilus\n'
}

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
target_dir="${HOME}/.local/share/nautilus-python/extensions"
extension_files=("paste_links.py" "core_logic.py")

# --- Parse arguments ---
action="install"
if [[ $# -gt 0 ]]; then
    case "$1" in
        --install)   action="install" ;;
        --uninstall) action="uninstall" ;;
        --help|-h)   usage; exit 0 ;;
        *)           printf 'Unknown option: %s\n\n' "$1" >&2; usage >&2; exit 1 ;;
    esac
fi

# --- Uninstall mode ---
if [[ "${action}" == "uninstall" ]]; then
    removed=0
    for file in "${extension_files[@]}"; do
        if [[ -f "${target_dir}/${file}" ]]; then
            rm "${target_dir}/${file}"
            printf 'Removed %s\n' "${target_dir}/${file}"
            removed=1
        fi
    done

    if [[ "${removed}" -eq 0 ]]; then
        printf 'Nothing to remove. Extension is not installed.\n'
        exit 0
    fi

    printf '\nRestart Nautilus / GNOME Files for the change to take effect:\n\n'
    printf '  nautilus -q\n\n'
    printf 'Then reopen Files. The "Paste Symlink" menu will no longer appear.\n'
    exit 0
fi

# --- Preflight: check for the Nautilus Python extension loader ---
# The nautilus-python package provides a shared library that tells
# Nautilus how to load .py files from the extensions directory.
# Without it, installed extension files are silently ignored.

loader_found=0
loader_dirs=(
    "/usr/lib64/nautilus/extensions-4"
    "/usr/lib/nautilus/extensions-4"
    # Ubuntu and Debian use architecture-specific library directories.
    /usr/lib/*-linux-gnu*/nautilus/extensions-4
    "/usr/lib64/nautilus/extensions-3"
    "/usr/lib/nautilus/extensions-3"
)

for dir in "${loader_dirs[@]}"; do
    if [ -f "${dir}/libnautilus-python.so" ]; then
        loader_found=1
        break
    fi
done

if [ "${loader_found}" -eq 0 ]; then
    printf 'Error: Nautilus Python extension loader not found.\n\n' >&2
    printf 'This extension requires the nautilus-python package, which provides the\n' >&2
    printf 'shared library that lets Nautilus load Python extensions.\n\n' >&2

    # Detect distro and print the relevant install command.
    install_cmd=""
    if [ -f /etc/os-release ]; then
        # shellcheck source=/dev/null
        . /etc/os-release
        case "${ID:-}" in
            fedora)   install_cmd="sudo dnf install nautilus-python" ;;
            arch|manjaro) install_cmd="sudo pacman -S nautilus-python" ;;
            debian|ubuntu|linuxmint|pop)
                      install_cmd="sudo apt install python3-nautilus" ;;
            opensuse*|suse|sles)
                      install_cmd="sudo zypper install nautilus-python" ;;
        esac
    fi

    if [ -n "${install_cmd}" ]; then
        printf 'Install it with:\n\n' >&2
        printf '  %s\n' "${install_cmd}" >&2
    else
        printf 'Install the nautilus-python package for your distribution.\n' >&2
    fi

    printf '\nAfter installing, run this script again.\n' >&2
    exit 1
fi

mkdir -p "${target_dir}"
install -m 0644 "${script_dir}/src/paste_links.py" "${target_dir}/paste_links.py"
install -m 0644 "${script_dir}/src/core_logic.py" "${target_dir}/core_logic.py"

printf 'Installed Nautilus extension to %s\n\n' "${target_dir}"
printf 'Restart Nautilus / GNOME Files for the extension to take effect:\n\n'
printf '  nautilus -q\n\n'
printf 'Then reopen Files. The "Paste Symlink" menu will appear in the context menu.\n'
