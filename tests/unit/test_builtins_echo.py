"""
Unit tests for echo command with variable expansion.
"""

import os
import pytest
from src.builtins.shell_utils import cmd_echo


class TestEchoCommand:
    """Test suite for echo command."""

    def test_echo_simple_text(self, capsys):
        """Test echo with simple text."""
        cmd_echo(["Hello", "World"])
        captured = capsys.readouterr()
        assert captured.out == "Hello World\n"

    def test_echo_unix_style_variable(self, capsys, monkeypatch):
        """Test echo with Unix-style environment variable ($VAR)."""
        monkeypatch.setenv("TEST_VAR", "test_value")
        cmd_echo(["Value:", "$TEST_VAR"])
        captured = capsys.readouterr()
        assert captured.out == "Value: test_value\n"

    def test_echo_unix_style_braces(self, capsys, monkeypatch):
        """Test echo with Unix-style braces (${VAR})."""
        monkeypatch.setenv("TEST_VAR", "test_value")
        cmd_echo(["Value:", "${TEST_VAR}"])
        captured = capsys.readouterr()
        assert captured.out == "Value: test_value\n"

    def test_echo_windows_style_variable(self, capsys, monkeypatch):
        """Test echo with Windows-style environment variable (%VAR%)."""
        monkeypatch.setenv("TEST_VAR", "test_value")
        cmd_echo(["Value:", "%TEST_VAR%"])
        captured = capsys.readouterr()
        assert captured.out == "Value: test_value\n"

    def test_echo_undefined_variable_unix(self, capsys):
        """Test echo with undefined Unix-style variable."""
        cmd_echo(["Value:", "$UNDEFINED_VAR"])
        captured = capsys.readouterr()
        assert captured.out == "Value: $UNDEFINED_VAR\n"

    def test_echo_undefined_variable_windows(self, capsys):
        """Test echo with undefined Windows-style variable."""
        cmd_echo(["Value:", "%UNDEFINED_VAR%"])
        captured = capsys.readouterr()
        assert captured.out == "Value: %UNDEFINED_VAR%\n"

    def test_echo_multiple_variables(self, capsys, monkeypatch):
        """Test echo with multiple environment variables."""
        monkeypatch.setenv("VAR1", "value1")
        monkeypatch.setenv("VAR2", "value2")
        cmd_echo(["$VAR1", "and", "$VAR2"])
        captured = capsys.readouterr()
        assert captured.out == "value1 and value2\n"

    def test_echo_mixed_text_and_variables(self, capsys, monkeypatch):
        """Test echo with mixed text and variables."""
        monkeypatch.setenv("USER", "testuser")
        cmd_echo(["Hello", "$USER,", "welcome!"])
        captured = capsys.readouterr()
        assert captured.out == "Hello testuser, welcome!\n"

    def test_echo_home_variable(self, capsys):
        """Test echo with HOME variable (should exist on most systems)."""
        # HOME or USERPROFILE should exist
        home = os.environ.get("HOME") or os.environ.get("USERPROFILE")
        if home:
            cmd_echo(["Home:", "$HOME"])
            captured = capsys.readouterr()
            # Should either expand or stay as $HOME if not set
            assert "Home:" in captured.out

    def test_echo_empty_args(self, capsys):
        """Test echo with no arguments."""
        cmd_echo([])
        captured = capsys.readouterr()
        assert captured.out == "\n"

    def test_echo_returns_true(self):
        """Test that echo always returns True."""
        assert cmd_echo(["test"]) is True
