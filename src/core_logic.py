"""Core shortcut logic for Nautilus Paste Shortcut.

This module contains pure logic that can be imported and tested
without GTK, GDK, or Nautilus bindings.
"""

import os

from gi.repository import Gio


class PasteShortcutError(RuntimeError):
    """Raised when the paste shortcut operation fails."""


def parse_payload(payload):
    """Parse clipboard payload into (operation, source_uris).

    Args:
        payload: Raw clipboard text from x-special/gnome-copied-files.

    Returns:
        Tuple of (operation, list_of_source_uris).

    Raises:
        PasteShortcutError: If the payload is empty.
    """
    lines = [line.strip() for line in payload.splitlines() if line.strip()]
    if not lines:
        raise PasteShortcutError("Clipboard is empty.")
    return lines[0], lines[1:]


def local_path_from_uri(uri):
    """Convert a file URI to a local filesystem path.

    Args:
        uri: A file:// URI string.

    Returns:
        Local path string, or None if the URI is not a local file.
    """
    file_obj = Gio.File.new_for_uri(uri)
    return file_obj.get_path()


def link_variant(base_name, index):
    """Generate a link name variant with a -link suffix.

    Args:
        base_name: Original file or folder name.
        index: Collision index (1 for -link, 2+ for -link-N).

    Returns:
        Modified name with suffix applied.
    """
    root, extension = os.path.splitext(base_name)
    suffix = "-link" if index == 1 else f"-link-{index}"
    if not root:
        return f"{base_name}{suffix}"
    return f"{root}{suffix}{extension}"


def available_link_name(base_name, destination_dir):
    """Find an available link name, avoiding collisions with existing files.

    Args:
        base_name: Desired link name.
        destination_dir: Directory where the link will be created.

    Returns:
        An available name that does not collide with existing entries.
    """
    candidate = base_name
    index = 0
    while os.path.lexists(os.path.join(destination_dir, candidate)):
        index += 1
        candidate = link_variant(base_name, index)
    return candidate


def create_shortcut(source_path, destination_dir):
    """Create a symbolic link for source_path in destination_dir.

    Args:
        source_path: Absolute path to the source file or folder.
        destination_dir: Absolute path to the destination directory.

    Raises:
        OSError: If symlink creation fails.
    """
    link_name = available_link_name(os.path.basename(source_path), destination_dir)
    link_path = os.path.join(destination_dir, link_name)
    os.symlink(source_path, link_path)


def paste_shortcuts(payload, destination_uri):
    """Execute the paste shortcut workflow.

    Parses the clipboard payload, validates sources, resolves paths,
    and creates symbolic links for each valid source.

    Args:
        payload: Raw clipboard text from x-special/gnome-copied-files.
        destination_uri: URI of the folder where links will be created.

    Returns:
        A message string if there were warnings, or None on success.

    Raises:
        PasteShortcutError: On invalid clipboard content or destination.
    """
    operation, source_uris = parse_payload(payload)
    if operation != "copy":
        raise PasteShortcutError(
            "Clipboard contains cut items. Copy files with Ctrl+C first."
        )

    destination_path = local_path_from_uri(destination_uri)
    if not destination_path or not os.path.isdir(destination_path):
        raise PasteShortcutError("Shortcuts can only be pasted into a local folder.")

    local_sources = []
    skipped = []

    for uri in source_uris:
        local_path = local_path_from_uri(uri)
        if local_path is None:
            skipped.append(f"Unsupported source: {uri}")
            continue
        local_sources.append(local_path)

    if not local_sources:
        raise PasteShortcutError(
            "Clipboard does not contain any supported local files or folders."
        )

    failures = []
    for source_path in local_sources:
        try:
            create_shortcut(source_path, destination_path)
        except OSError as error:
            failures.append(f"{os.path.basename(source_path)}: {error}")

    if failures and skipped:
        return join_lines(["Some shortcuts were not created.", *failures, *skipped])
    if failures:
        return join_lines(["Some shortcuts were not created.", *failures])
    if skipped:
        return join_lines(["Some items were skipped.", *skipped])
    return None


def join_lines(lines):
    """Join non-empty lines with newlines.

    Args:
        lines: List of strings.

    Returns:
        Single string with lines separated by newlines.
    """
    return "\n".join(line for line in lines if line)


def normalize_clipboard_text(payload):
    """Normalize clipboard text into the copy payload format.

    On some Nautilus/Wayland setups, Gdk.Clipboard.read_text_async()
    returns plain local paths instead of the old x-special/gnome-copied-files
    payload. This function converts plain paths into the expected format:
    ``copy\\nfile:///path/to/file``.

    If the payload already starts with an operation marker (``copy`` or
    ``cut``), it is returned unchanged.

    Args:
        payload: Raw clipboard text from read_text_async().

    Returns:
        Normalized payload string.
    """
    lines = [line.strip() for line in payload.splitlines() if line.strip()]
    if not lines:
        return payload

    # Older Nautilus clipboard data starts with an operation marker:
    # "copy" or "cut" followed by file:// URIs. Keep that shape intact.
    if lines[0] in {"copy", "cut"}:
        return "\n".join(lines)

    # Convert plain local paths to the copy payload format.
    uris = []
    for line in lines:
        if line.startswith("file://"):
            if local_path_from_uri(line):
                uris.append(line)
        elif os.path.lexists(line):
            uris.append(Gio.File.new_for_path(line).get_uri())

    if not uris:
        return payload

    return "\n".join(["copy", *uris])
