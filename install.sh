#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
target_dir="${HOME}/.local/share/nautilus-python/extensions"

mkdir -p "${target_dir}"
install -m 0644 "${script_dir}/src/nautilus_paste_shortcut.py" "${target_dir}/nautilus_paste_shortcut.py"
install -m 0644 "${script_dir}/src/core_logic.py" "${target_dir}/core_logic.py"

printf 'Installed Nautilus extension to %s\n' "${target_dir}"
printf 'Restart GNOME Files with: nautilus -q\n'
