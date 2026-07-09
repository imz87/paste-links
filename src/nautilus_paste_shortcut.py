#!/usr/bin/env python3

import os

import gi

gi.require_version("Gdk", "4.0")
gi.require_version("Gtk", "4.0")
gi.require_version("Nautilus", "4.0")

from gi.repository import Gdk, Gio, GLib, GObject, Gtk, Nautilus


TARGET_MIME_TYPE = "x-special/gnome-copied-files"
MENU_LABEL = "Paste Shortcut Here"
DIALOG_TITLE = "Paste Shortcut Here"


class PasteShortcutExtension(GObject.GObject, Nautilus.MenuProvider):
    def get_background_items(self, current_folder):
        if not self._clipboard_has_copied_files():
            return []

        folder_uri = current_folder.get_uri()
        if not self._local_path_from_uri(folder_uri):
            return []

        item = Nautilus.MenuItem(
            name="PasteShortcutExtension::PasteShortcutHere",
            label=MENU_LABEL,
            tip="Create symbolic links from copied files",
        )
        item.connect("activate", self._on_activate, folder_uri)
        return [item]

    def _clipboard_has_copied_files(self):
        display = Gdk.Display.get_default()
        if display is None:
            return False

        clipboard = display.get_clipboard()
        formats = clipboard.get_formats()
        return formats.contain_mime_type(TARGET_MIME_TYPE)

    def _on_activate(self, _menu_item, destination_uri):
        display = Gdk.Display.get_default()
        if display is None:
            self._show_error("Could not access the current display.")
            return

        clipboard = display.get_clipboard()
        formats = clipboard.get_formats()
        if not formats.contain_mime_type(TARGET_MIME_TYPE):
            self._show_error("Clipboard does not contain copied files from GNOME Files.")
            return

        clipboard.read_async(
            [TARGET_MIME_TYPE],
            GLib.PRIORITY_DEFAULT,
            None,
            self._on_clipboard_read,
            destination_uri,
        )

    def _on_clipboard_read(self, clipboard, result, destination_uri):
        try:
            stream, _mime_type = clipboard.read_finish(result)
            payload = self._read_stream(stream)
        except GLib.Error as error:
            self._show_error("Failed to read the clipboard.", str(error))
            return

        try:
            message = self._paste_shortcuts(payload, destination_uri)
        except PasteShortcutError as error:
            self._show_error(str(error))
            return

        if message:
            self._show_error(message)

    def _paste_shortcuts(self, payload, destination_uri):
        operation, source_uris = self._parse_payload(payload)
        if operation != "copy":
            raise PasteShortcutError("Clipboard contains cut items. Copy files with Ctrl+C first.")

        destination_path = self._local_path_from_uri(destination_uri)
        if not destination_path or not os.path.isdir(destination_path):
            raise PasteShortcutError("Shortcuts can only be pasted into a local folder.")

        local_sources = []
        skipped = []

        for uri in source_uris:
            local_path = self._local_path_from_uri(uri)
            if local_path is None:
                skipped.append(f"Unsupported source: {uri}")
                continue
            local_sources.append(local_path)

        if not local_sources:
            raise PasteShortcutError("Clipboard does not contain any supported local files or folders.")

        failures = []
        for source_path in local_sources:
            try:
                self._create_shortcut(source_path, destination_path)
            except OSError as error:
                failures.append(f"{os.path.basename(source_path)}: {error}")

        if failures and skipped:
            return self._join_lines(["Some shortcuts were not created.", *failures, *skipped])
        if failures:
            return self._join_lines(["Some shortcuts were not created.", *failures])
        if skipped:
            return self._join_lines(["Some items were skipped.", *skipped])
        return None

    def _create_shortcut(self, source_path, destination_dir):
        link_name = self._available_link_name(os.path.basename(source_path), destination_dir)
        link_path = os.path.join(destination_dir, link_name)
        os.symlink(source_path, link_path)

    def _available_link_name(self, base_name, destination_dir):
        candidate = base_name
        index = 0
        while os.path.lexists(os.path.join(destination_dir, candidate)):
            index += 1
            candidate = self._link_variant(base_name, index)
        return candidate

    def _link_variant(self, base_name, index):
        root, extension = os.path.splitext(base_name)
        suffix = "-link" if index == 1 else f"-link-{index}"
        if not root:
            return f"{base_name}{suffix}"
        return f"{root}{suffix}{extension}"

    def _parse_payload(self, payload):
        lines = [line.strip() for line in payload.splitlines() if line.strip()]
        if not lines:
            raise PasteShortcutError("Clipboard is empty.")
        return lines[0], lines[1:]

    def _local_path_from_uri(self, uri):
        file_obj = Gio.File.new_for_uri(uri)
        return file_obj.get_path()

    def _read_stream(self, stream):
        try:
            chunks = []
            while True:
                chunk = stream.read_bytes(64 * 1024, None)
                if chunk.get_size() == 0:
                    break
                chunks.append(chunk.get_data())
            return b"".join(chunks).decode("utf-8", errors="replace")
        finally:
            stream.close(None)

    def _show_error(self, message, detail=None):
        if hasattr(Gtk, "AlertDialog"):
            dialog = Gtk.AlertDialog(message=message, detail=detail, modal=True)
            dialog.show(None)
            return

        dialog = Gtk.MessageDialog(
            transient_for=None,
            modal=True,
            message_type=Gtk.MessageType.ERROR,
            buttons=Gtk.ButtonsType.CLOSE,
            text=message,
            secondary_text=detail,
        )
        dialog.set_title(DIALOG_TITLE)
        dialog.connect("response", lambda current_dialog, _response_id: current_dialog.destroy())
        dialog.present()

    def _join_lines(self, lines):
        return "\n".join(line for line in lines if line)


class PasteShortcutError(RuntimeError):
    pass
