#!/usr/bin/env python3

import gi

gi.require_version("Gdk", "4.0")
gi.require_version("Gtk", "4.0")
gi.require_version("Nautilus", "4.0")

from gi.repository import Gdk, GLib, GObject, Gtk, Nautilus

from core_logic import (
    PasteShortcutError,
    local_path_from_uri,
    paste_shortcuts,
)


TARGET_MIME_TYPE = "x-special/gnome-copied-files"
MENU_LABEL = "Paste Shortcut Here"
DIALOG_TITLE = "Paste Shortcut Here"


class PasteShortcutExtension(GObject.GObject, Nautilus.MenuProvider):
    def get_background_items(self, current_folder):
        if not self._clipboard_has_copied_files():
            return []

        folder_uri = current_folder.get_uri()
        if not local_path_from_uri(folder_uri):
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
            message = paste_shortcuts(payload, destination_uri)
        except PasteShortcutError as error:
            self._show_error(str(error))
            return

        if message:
            self._show_error(message)

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
