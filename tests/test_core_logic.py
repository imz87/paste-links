"""Unit tests for core shortcut logic.

Tests clipboard payload parsing, link naming, collision handling,
and local-only shortcut creation behavior without requiring a live
Nautilus session, GTK dialogs, or desktop clipboard access.
"""

import os
import tempfile

import pytest

# core_logic imports Gio at module level, which requires GObject.
# On Fedora with python3-gobject installed, this works fine.
from core_logic import (
    PasteShortcutError,
    available_link_name,
    create_shortcut,
    join_lines,
    link_variant,
    normalize_clipboard_text,
    parse_payload,
    paste_shortcuts,
)


# ---------------------------------------------------------------------------
# parse_payload
# ---------------------------------------------------------------------------


class TestParsePayload:
    def test_copy_with_one_uri(self):
        payload = "copy\nfile:///tmp/test.txt"
        operation, uris = parse_payload(payload)
        assert operation == "copy"
        assert uris == ["file:///tmp/test.txt"]

    def test_copy_with_two_uris(self):
        payload = "copy\nfile:///tmp/a.txt\nfile:///tmp/b.txt"
        operation, uris = parse_payload(payload)
        assert operation == "copy"
        assert uris == ["file:///tmp/a.txt", "file:///tmp/b.txt"]

    def test_cut_operation(self):
        payload = "cut\nfile:///tmp/test.txt"
        operation, uris = parse_payload(payload)
        assert operation == "cut"
        assert uris == ["file:///tmp/test.txt"]

    def test_blank_lines_are_stripped(self):
        payload = "\n\ncopy\nfile:///tmp/test.txt\n\n"
        operation, uris = parse_payload(payload)
        assert operation == "copy"
        assert uris == ["file:///tmp/test.txt"]

    def test_empty_payload_raises_error(self):
        with pytest.raises(PasteShortcutError, match="Clipboard is empty"):
            parse_payload("")

    def test_whitespace_only_payload_raises_error(self):
        with pytest.raises(PasteShortcutError, match="Clipboard is empty"):
            parse_payload("   \n  \n  ")

    def test_no_uris_just_operation(self):
        payload = "copy"
        operation, uris = parse_payload(payload)
        assert operation == "copy"
        assert uris == []


# ---------------------------------------------------------------------------
# link_variant
# ---------------------------------------------------------------------------


class TestLinkVariant:
    def test_first_collision(self):
        assert link_variant("test.txt", 1) == "test-link.txt"

    def test_second_collision(self):
        assert link_variant("test.txt", 2) == "test-link-2.txt"

    def test_third_collision(self):
        assert link_variant("test.txt", 3) == "test-link-3.txt"

    def test_no_extension(self):
        assert link_variant("Makefile", 1) == "Makefile-link"

    def test_hidden_file(self):
        assert link_variant(".bashrc", 1) == ".bashrc-link"

    def test_hidden_file_with_collision(self):
        assert link_variant(".bashrc", 2) == ".bashrc-link-2"

    def test_multiple_dots(self):
        assert link_variant("archive.tar.gz", 1) == "archive.tar-link.gz"

    def test_extensionless_with_trailing_dot(self):
        # os.path.splitext("file.") returns ("file", "."), so suffix goes before dot
        assert link_variant("file.", 1) == "file-link."

    def test_folder_name(self):
        assert link_variant("my_folder", 1) == "my_folder-link"


# ---------------------------------------------------------------------------
# available_link_name
# ---------------------------------------------------------------------------


class TestAvailableLinkName:
    def test_no_collision(self, tmp_path):
        result = available_link_name("test.txt", str(tmp_path))
        assert result == "test.txt"

    def test_first_collision(self, tmp_path):
        (tmp_path / "test.txt").touch()
        result = available_link_name("test.txt", str(tmp_path))
        assert result == "test-link.txt"

    def test_second_collision(self, tmp_path):
        (tmp_path / "test.txt").touch()
        (tmp_path / "test-link.txt").touch()
        result = available_link_name("test.txt", str(tmp_path))
        assert result == "test-link-2.txt"

    def test_third_collision(self, tmp_path):
        (tmp_path / "test.txt").touch()
        (tmp_path / "test-link.txt").touch()
        (tmp_path / "test-link-2.txt").touch()
        result = available_link_name("test.txt", str(tmp_path))
        assert result == "test-link-3.txt"

    def test_hidden_file_no_collision(self, tmp_path):
        result = available_link_name(".bashrc", str(tmp_path))
        assert result == ".bashrc"

    def test_hidden_file_collision(self, tmp_path):
        (tmp_path / ".bashrc").touch()
        result = available_link_name(".bashrc", str(tmp_path))
        assert result == ".bashrc-link"

    def test_extensionless_file(self, tmp_path):
        result = available_link_name("Makefile", str(tmp_path))
        assert result == "Makefile"

    def test_extensionless_file_collision(self, tmp_path):
        (tmp_path / "Makefile").touch()
        result = available_link_name("Makefile", str(tmp_path))
        assert result == "Makefile-link"


# ---------------------------------------------------------------------------
# create_shortcut
# ---------------------------------------------------------------------------


class TestCreateShortcut:
    def test_creates_working_symlink(self, tmp_path):
        source = tmp_path / "source.txt"
        source.touch()
        dest = tmp_path / "links"
        dest.mkdir()

        create_shortcut(str(source), str(dest))

        link_path = dest / "source.txt"
        assert link_path.is_symlink()
        assert os.readlink(str(link_path)) == str(source)

    def test_collision_safe_naming(self, tmp_path):
        source = tmp_path / "test.txt"
        source.touch()
        dest = tmp_path / "links"
        dest.mkdir()
        (dest / "test.txt").touch()  # existing file

        create_shortcut(str(source), str(dest))

        link_path = dest / "test-link.txt"
        assert link_path.is_symlink()

    def test_folder_symlink(self, tmp_path):
        source = tmp_path / "my_folder"
        source.mkdir()
        dest = tmp_path / "links"
        dest.mkdir()

        create_shortcut(str(source), str(dest))

        link_path = dest / "my_folder"
        assert link_path.is_symlink()
        assert os.readlink(str(link_path)) == str(source)


# ---------------------------------------------------------------------------
# paste_shortcuts
# ---------------------------------------------------------------------------


class TestPasteShortcuts:
    def test_two_local_files(self, tmp_path):
        src1 = tmp_path / "a.txt"
        src2 = tmp_path / "b.txt"
        src1.touch()
        src2.touch()
        dest = tmp_path / "dest"
        dest.mkdir()

        payload = f"copy\nfile://{src1}\nfile://{src2}"
        message = paste_shortcuts(payload, f"file://{dest}")

        assert message is None
        assert (dest / "a.txt").is_symlink()
        assert (dest / "b.txt").is_symlink()

    def test_cut_operation_rejected(self, tmp_path):
        src = tmp_path / "a.txt"
        src.touch()
        dest = tmp_path / "dest"
        dest.mkdir()

        payload = f"cut\nfile://{src}"
        with pytest.raises(PasteShortcutError, match="cut"):
            paste_shortcuts(payload, f"file://{dest}")

    def test_no_local_sources_raises_error(self, tmp_path):
        dest = tmp_path / "dest"
        dest.mkdir()

        payload = "copy\nsftp://remote/file.txt"
        with pytest.raises(PasteShortcutError, match="supported local"):
            paste_shortcuts(payload, f"file://{dest}")

    def test_unsupported_uri_skipped(self, tmp_path):
        src = tmp_path / "local.txt"
        src.touch()
        dest = tmp_path / "dest"
        dest.mkdir()

        payload = f"copy\nfile://{src}\nsftp://remote/file.txt"
        message = paste_shortcuts(payload, f"file://{dest}")

        assert message is not None
        assert "Skipped" in message or "skipped" in message
        assert (dest / "local.txt").is_symlink()

    def test_empty_payload_raises_error(self, tmp_path):
        dest = tmp_path / "dest"
        dest.mkdir()

        with pytest.raises(PasteShortcutError, match="empty"):
            paste_shortcuts("", f"file://{dest}")

    def test_destination_must_be_local_folder(self, tmp_path):
        src = tmp_path / "a.txt"
        src.touch()

        payload = f"copy\nfile://{src}"
        with pytest.raises(PasteShortcutError, match="local folder"):
            paste_shortcuts(payload, "sftp://remote/dest")

    def test_name_collision_resolved(self, tmp_path):
        src = tmp_path / "test.txt"
        src.touch()
        dest = tmp_path / "dest"
        dest.mkdir()
        (dest / "test.txt").touch()

        payload = f"copy\nfile://{src}"
        paste_shortcuts(payload, f"file://{dest}")

        assert (dest / "test-link.txt").is_symlink()


# ---------------------------------------------------------------------------
# normalize_clipboard_text
# ---------------------------------------------------------------------------


class TestNormalizeClipboardText:
    def test_copy_payload_unchanged(self):
        payload = "copy\nfile:///tmp/test.txt"
        assert normalize_clipboard_text(payload) == payload

    def test_cut_payload_unchanged(self):
        payload = "cut\nfile:///tmp/test.txt"
        assert normalize_clipboard_text(payload) == payload

    def test_copy_with_multiple_uris_unchanged(self):
        payload = "copy\nfile:///tmp/a.txt\nfile:///tmp/b.txt"
        assert normalize_clipboard_text(payload) == payload

    def test_single_plain_path(self, tmp_path):
        src = tmp_path / "file.txt"
        src.touch()
        payload = str(src)
        result = normalize_clipboard_text(payload)
        assert result.startswith("copy\n")
        assert f"file://{src}" in result

    def test_multiple_plain_paths(self, tmp_path):
        a = tmp_path / "a.txt"
        b = tmp_path / "b.txt"
        a.touch()
        b.touch()
        payload = f"{a}\n{b}"
        result = normalize_clipboard_text(payload)
        assert result.startswith("copy\n")
        assert f"file://{a}" in result
        assert f"file://{b}" in result

    def test_file_uri_line_unchanged(self):
        payload = "file:///tmp/test.txt"
        result = normalize_clipboard_text(payload)
        assert result.startswith("copy\n")
        assert "file:///tmp/test.txt" in result

    def test_empty_payload(self):
        assert normalize_clipboard_text("") == ""

    def test_whitespace_only(self):
        assert normalize_clipboard_text("   \n  \n  ") == "   \n  \n  "

    def test_non_file_text_fallback(self):
        payload = "some random clipboard text"
        result = normalize_clipboard_text(payload)
        assert result == payload

    def test_nonexistent_path_fallback(self):
        payload = "/home/user/documents/file.txt"
        result = normalize_clipboard_text(payload)
        assert result == payload


# ---------------------------------------------------------------------------
# join_lines
# ---------------------------------------------------------------------------


class TestJoinLines:
    def test_normal_lines(self):
        assert join_lines(["a", "b", "c"]) == "a\nb\nc"

    def test_filters_empty_strings(self):
        assert join_lines(["a", "", "b"]) == "a\nb"

    def test_empty_list(self):
        assert join_lines([]) == ""

    def test_single_line(self):
        assert join_lines(["hello"]) == "hello"
