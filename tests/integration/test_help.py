"""Integration test for help command."""

import sys
import os

# Add project root to path
sys.path.insert(
    0,
    os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
)

from src.builtins import BuiltinCommands


class TestHelpCommand:
    """Integration tests for help command."""

    def test_help_command_executes(self):
        """Test that help command executes without errors."""
        result = BuiltinCommands.execute_builtin('help', [])
        assert result is True

    def test_help_command_shows_all_categories(self, capsys):
        """Test that help command shows all command categories."""
        BuiltinCommands.execute_builtin('help', [])
        captured = capsys.readouterr()

        # Check for all major sections
        assert "Navigation & File Management:" in captured.out
        assert "Search & Find:" in captured.out
        assert "System Info:" in captured.out
        assert "Utilities:" in captured.out
        assert "MairuCLI Specific:" in captured.out
        assert "Dangerous Commands" in captured.out

    def test_help_command_lists_new_commands(self, capsys):
        """Test that help command includes newly added commands."""
        BuiltinCommands.execute_builtin('help', [])
        captured = capsys.readouterr()

        # Check for new commands
        assert "touch" in captured.out
        assert "mkdir" in captured.out
        assert "find" in captured.out
        assert "grep" in captured.out
        assert "which" in captured.out
        assert "tree" in captured.out
        assert "whoami" in captured.out
        assert "hostname" in captured.out
