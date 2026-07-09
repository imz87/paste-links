#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
target_dir="${HOME}/.local/share/nautilus-python/extensions"
target_file="${target_dir}/nautilus_paste_shortcut.py"

mkdir -p "${target_dir}"
install -m 0644 "${script_dir}/src/nautilus_paste_shortcut.py" "${target_file}"

printf 'Installed Nautilus extension to %s\n' "${target_file}"
printf 'Restart GNOME Files with: nautilus -q\n'
