"""
Unit tests for CommandParser module.

Tests command parsing and path extraction.
"""

import pytest
from src.command_parser import CommandParser


class TestCommandParser:
    """Test suite for CommandParser class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.parser = CommandParser()

    def test_parse_rm_command(self):
        """Test parsing rm command."""
        result = self.parser.parse("rm /etc/passwd")

        assert result["command"] == "rm"
        assert "/etc/passwd" in result["paths"]
        assert result["operation"] == "delete"
        assert result["has_redirect"] is False

    def test_parse_rm_with_options(self):
        """Test parsing rm command with options."""
        result = self.parser.parse("rm -rf /tmp/test")

        assert result["command"] == "rm"
        assert "/tmp/test" in result["paths"]
        assert result["operation"] == "delete"

    def test_parse_mv_command(self):
        """Test parsing mv command (source and destination)."""
        result = self.parser.parse("mv /tmp/source /tmp/dest")

        assert result["command"] == "mv"
        assert "/tmp/source" in result["paths"]
        assert "/tmp/dest" in result["paths"]
        assert len(result["paths"]) == 2
        assert result["operation"] == "move"

    def test_parse_chmod_command(self):
        """Test parsing chmod command."""
        result = self.parser.parse("chmod 755 /etc/config")

        assert result["command"] == "chmod"
        assert "/etc/config" in result["paths"]
        assert result["operation"] == "permission"

    def test_parse_chown_command(self):
        """Test parsing chown command."""
        result = self.parser.parse("chown root:root /etc/passwd")

        assert result["command"] == "chown"
        assert "/etc/passwd" in result["paths"]
        assert result["operation"] == "ownership"

    def test_parse_dd_command(self):
        """Test parsing dd command with if= and of=."""
        result = self.parser.parse("dd if=/dev/zero of=/dev/sda")

        assert result["command"] == "dd"
        assert "/dev/zero" in result["paths"]
        assert "/dev/sda" in result["paths"]
        assert len(result["paths"]) == 2
        assert result["operation"] == "disk_operation"

    def test_parse_dd_command_partial(self):
        """Test parsing dd command with only if=."""
        result = self.parser.parse("dd if=/dev/zero bs=1M")

        assert result["command"] == "dd"
        assert "/dev/zero" in result["paths"]
        assert len(result["paths"]) == 1

    def test_parse_output_redirection(self):
        """Test detection of output redirection."""
        result = self.parser.parse("echo test > /etc/config")

        assert result["has_redirect"] is True
        assert result["redirect_target"] == "/etc/config"
        assert "/etc/config" in result["paths"]

    def test_parse_append_redirection(self):
        """Test detection of append redirection (>>)."""
        result = self.parser.parse("echo test >> /var/log/app.log")

        assert result["has_redirect"] is True
        assert result["redirect_target"] == "/var/log/app.log"

    def test_parse_quoted_path(self):
        """Test parsing command with quoted path containing spaces."""
        result = self.parser.parse('rm "/tmp/my file.txt"')

        assert result["command"] == "rm"
        assert "/tmp/my file.txt" in result["paths"]

    def test_parse_single_quoted_path(self):
        """Test parsing command with single-quoted path."""
        result = self.parser.parse("rm '/tmp/my file.txt'")

        assert result["command"] == "rm"
        assert "/tmp/my file.txt" in result["paths"]

    def test_parse_empty_command(self):
        """Test parsing empty command."""
        result = self.parser.parse("")

        assert result["command"] == ""
        assert result["paths"] == []
        assert result["operation"] == ""

    def test_parse_whitespace_only(self):
        """Test parsing whitespace-only command."""
        result = self.parser.parse("   ")

        assert result["command"] == ""
        assert result["paths"] == []

    def test_parse_unknown_command(self):
        """Test parsing unknown command."""
        result = self.parser.parse("unknowncmd /tmp/file")

        assert result["command"] == "unknowncmd"
        assert result["paths"] == []  # No paths extracted for unknown commands
        assert result["operation"] == "unknown"

    def test_extract_all_paths_convenience(self):
        """Test extract_all_paths convenience method."""
        paths = self.parser.extract_all_paths("mv /tmp/a /tmp/b")

        assert len(paths) == 2
        assert "/tmp/a" in paths
        assert "/tmp/b" in paths

    def test_parse_cat_command(self):
        """Test parsing cat command."""
        result = self.parser.parse("cat /etc/passwd")

        assert result["command"] == "cat"
        assert "/etc/passwd" in result["paths"]
        assert result["operation"] == "read"

    def test_parse_mkdir_command(self):
        """Test parsing mkdir command."""
        result = self.parser.parse("mkdir /tmp/newdir")

        assert result["command"] == "mkdir"
        assert "/tmp/newdir" in result["paths"]
        assert result["operation"] == "create"

    def test_parse_ln_command(self):
        """Test parsing ln command (source and destination)."""
        result = self.parser.parse("ln -s /tmp/source /tmp/link")

        assert result["command"] == "ln"
        assert "/tmp/source" in result["paths"]
        assert "/tmp/link" in result["paths"]
        assert result["operation"] == "link"

    def test_parse_multiple_options(self):
        """Test parsing command with multiple options."""
        result = self.parser.parse("rm -r -f -v /tmp/test")

        assert result["command"] == "rm"
        assert "/tmp/test" in result["paths"]
        # Options should be filtered out
        assert "-r" not in result["paths"]
        assert "-f" not in result["paths"]

    def test_parse_combined_options(self):
        """Test parsing command with combined options."""
        result = self.parser.parse("rm -rfv /tmp/test")

        assert result["command"] == "rm"
        assert "/tmp/test" in result["paths"]
        assert "-rfv" not in result["paths"]

    def test_parse_windows_path(self):
        """Test parsing Windows-style path."""
        result = self.parser.parse(r"rm C:\Windows\System32\test.dll")

        assert result["command"] == "rm"
        assert r"C:\Windows\System32\test.dll" in result["paths"]

    def test_parse_redirect_with_quotes(self):
        """Test parsing redirection with quoted filename."""
        result = self.parser.parse('echo test > "/tmp/my file.txt"')

        assert result["has_redirect"] is True
        assert "/tmp/my file.txt" in result["redirect_target"]

    def test_parse_complex_command(self):
        """Test parsing complex command with multiple elements."""
        result = self.parser.parse("mv -v /tmp/source /tmp/dest > /var/log/mv.log")

        assert result["command"] == "mv"
        assert "/tmp/source" in result["paths"]
        assert "/tmp/dest" in result["paths"]
        assert "/var/log/mv.log" in result["paths"]
        assert result["has_redirect"] is True
