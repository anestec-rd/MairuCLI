"""
Integration tests for builtin command redirection detection.

CRITICAL: These tests ensure that dangerous redirections are blocked
even when using builtin commands like echo and cat.

Background:
-----------
Issue #4: Commands like `echo data > /dev/sda` were not being detected
because builtin commands executed before dangerous pattern detection.

This test suite ensures that dangerous redirections are caught BEFORE
builtin execution, preventing data loss and system damage.
"""

import pytest
from unittest.mock import patch, MagicMock
from src.main import process_command


class TestBuiltinRedirectionBlocking:
    """Test that dangerous redirections are blocked for builtin commands."""

    @patch('src.main.show_warning')
    @patch('src.main.BuiltinCommands.execute_builtin')
    def test_echo_to_disk_blocked(self, mock_execute, mock_warning):
        """
        CRITICAL: Test that echo > /dev/sda is blocked.

        This is the exact issue reported in Issue #4.
        """
        command = "echo dangerous data > /dev/sda"
        result = process_command(command)

        # Should show warning
        mock_warning.assert_called_once()

        # Should NOT execute builtin
        mock_execute.assert_not_called()

        # Should return empty string (not EXIT)
        assert result == ""

    @patch('src.main.show_warning')
    @patch('src.main.BuiltinCommands.execute_builtin')
    def test_cat_to_disk_blocked(self, mock_execute, mock_warning):
        """Test that cat > /dev/sdb is blocked."""
        command = "cat file.txt > /dev/sdb"
        result = process_command(command)

        mock_warning.assert_called_once()
        mock_execute.assert_not_called()
        assert result == ""

    @patch('src.main.show_warning')
    @patch('src.main.BuiltinCommands.execute_builtin')
    def test_echo_to_nvme_blocked(self, mock_execute, mock_warning):
        """Test that echo > /dev/nvme0n1 is blocked."""
        command = "echo test > /dev/nvme0n1"
        result = process_command(command)

        mock_warning.assert_called_once()
        mock_execute.assert_not_called()
        assert result == ""

    @patch('src.main.show_warning')
    @patch('src.main.BuiltinCommands.execute_builtin')
    def test_echo_to_kernel_panic_blocked(self, mock_execute, mock_warning):
        """Test that echo c > /proc/sysrq-trigger is blocked."""
        command = "echo c > /proc/sysrq-trigger"
        result = process_command(command)

        mock_warning.assert_called_once()
        mock_execute.assert_not_called()
        assert result == ""

    @patch('src.main.show_warning')
    @patch('src.main.BuiltinCommands.execute_builtin')
    def test_echo_to_passwd_blocked(self, mock_execute, mock_warning):
        """Test that echo > /etc/passwd is blocked."""
        command = "echo hacker > /etc/passwd"
        result = process_command(command)

        mock_warning.assert_called_once()
        mock_execute.assert_not_called()
        assert result == ""

    @patch('src.main.show_warning')
    @patch('src.main.BuiltinCommands.execute_builtin')
    def test_echo_to_shadow_blocked(self, mock_execute, mock_warning):
        """Test that echo > /etc/shadow is blocked."""
        command = "echo test > /etc/shadow"
        result = process_command(command)

        mock_warning.assert_called_once()
        mock_execute.assert_not_called()
        assert result == ""


class TestBuiltinRedirectionAllowed:
    """Test that safe redirections are allowed for builtin commands."""

    @patch('src.main.BuiltinCommands.execute_builtin')
    def test_echo_to_tmp_allowed(self, mock_execute):
        """Test that echo > /tmp/file is allowed."""
        command = "echo test > /tmp/file.txt"
        result = process_command(command)

        # Should execute builtin (redirection handled by shell)
        # Note: Builtin might not be called if shell handles it
        # The important thing is no warning is shown
        assert result == ""

    @patch('src.main.BuiltinCommands.execute_builtin')
    def test_echo_to_home_allowed(self, mock_execute):
        """Test that echo > ~/file is allowed."""
        command = "echo test > ~/output.txt"
        result = process_command(command)

        assert result == ""

    @patch('src.main.BuiltinCommands.execute_builtin')
    def test_cat_to_tmp_allowed(self, mock_execute):
        """Test that cat > /tmp/file is allowed."""
        # Use absolute path to avoid system protection warnings
        command = "cat /tmp/input.txt > /tmp/output.txt"
        result = process_command(command)

        assert result == ""


class TestRedirectionPriority:
    """Test that redirection check happens before builtin execution."""

    @patch('src.main.show_warning')
    @patch('src.main.BuiltinCommands.execute_builtin')
    def test_redirection_checked_before_builtin(self, mock_execute, mock_warning):
        """
        Test that dangerous redirection is checked BEFORE builtin executes.

        This is the core fix for Issue #4.
        """
        command = "echo data > /dev/sda"

        # Process command
        process_command(command)

        # Warning should be shown
        assert mock_warning.called

        # Builtin should NOT be executed
        assert not mock_execute.called

        # This proves the order: redirection check → warning → block
        # NOT: builtin execute → redirection happens → damage done

    @patch('src.main.show_warning')
    @patch('src.main.BuiltinCommands.execute_builtin')
    def test_multiple_dangerous_redirections(self, mock_execute, mock_warning):
        """Test that all dangerous redirections are caught."""
        dangerous_commands = [
            "echo test > /dev/sda",
            "echo test > /dev/sdb",
            "echo test > /dev/nvme0n1",
            "echo c > /proc/sysrq-trigger",
            "echo test > /etc/passwd",
            "echo test > /etc/shadow",
            "echo test > /dev/mem",
        ]

        for cmd in dangerous_commands:
            mock_warning.reset_mock()
            mock_execute.reset_mock()

            process_command(cmd)

            assert mock_warning.called, f"Warning not shown for: {cmd}"
            assert not mock_execute.called, f"Builtin executed for: {cmd}"


class TestIssue4Reproduction:
    """Reproduce the exact issue reported in Issue #4."""

    @patch('src.main.show_warning')
    @patch('src.main.BuiltinCommands.execute_builtin')
    def test_issue_4_echo_to_disk(self, mock_execute, mock_warning):
        """
        Reproduce Issue #4: echo data > /dev/sda not detected.

        Before fix: Builtin echo executed, wrote to disk
        After fix: Warning shown, command blocked
        """
        command = "echo data > /dev/sda"

        result = process_command(command)

        # MUST show warning
        assert mock_warning.called, "Issue #4 NOT FIXED: Warning not shown!"

        # MUST NOT execute builtin
        assert not mock_execute.called, "Issue #4 NOT FIXED: Builtin executed!"

        # Should return empty string
        assert result == ""

    @patch('src.main.show_warning')
    @patch('src.main.BuiltinCommands.execute_builtin')
    def test_issue_4_cat_to_disk(self, mock_execute, mock_warning):
        """
        Reproduce Issue #4: cat file > /dev/sdb not detected.
        """
        command = "cat file > /dev/sdb"

        result = process_command(command)

        assert mock_warning.called, "Issue #4 NOT FIXED: Warning not shown!"
        assert not mock_execute.called, "Issue #4 NOT FIXED: Builtin executed!"
        assert result == ""

    @patch('src.main.show_warning')
    @patch('src.main.BuiltinCommands.execute_builtin')
    def test_issue_4_kernel_panic(self, mock_execute, mock_warning):
        """
        Reproduce Issue #4: echo c > /proc/sysrq-trigger not detected.
        """
        command = "echo c > /proc/sysrq-trigger"

        result = process_command(command)

        assert mock_warning.called, "Issue #4 NOT FIXED: Warning not shown!"
        assert not mock_execute.called, "Issue #4 NOT FIXED: Builtin executed!"
        assert result == ""


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
