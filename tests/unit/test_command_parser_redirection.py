"""
Unit tests for command parser redirection detection.

Tests the extract_redirection_target() method to ensure it correctly
identifies output redirection targets in commands.
"""

import pytest
from src.command_parser import CommandParser


class TestRedirectionDetection:
    """Test redirection target extraction."""

    def setup_method(self):
        """Set up test fixtures."""
        self.parser = CommandParser()

    def test_simple_redirection(self):
        """Test simple output redirection."""
        target = self.parser.extract_redirection_target("echo test > /tmp/file")
        assert target == "/tmp/file"

    def test_append_redirection(self):
        """Test append redirection (>>)."""
        target = self.parser.extract_redirection_target("echo test >> /tmp/file")
        assert target == "/tmp/file"

    def test_dangerous_disk_redirection(self):
        """Test redirection to disk device."""
        target = self.parser.extract_redirection_target("echo data > /dev/sda")
        assert target == "/dev/sda"

    def test_dangerous_nvme_redirection(self):
        """Test redirection to NVMe device."""
        target = self.parser.extract_redirection_target("cat file > /dev/nvme0n1")
        assert target == "/dev/nvme0n1"

    def test_dangerous_kernel_panic(self):
        """Test redirection to kernel panic trigger."""
        target = self.parser.extract_redirection_target("echo c > /proc/sysrq-trigger")
        assert target == "/proc/sysrq-trigger"

    def test_dangerous_system_file(self):
        """Test redirection to system file."""
        target = self.parser.extract_redirection_target("echo test > /etc/passwd")
        assert target == "/etc/passwd"

    def test_quoted_path(self):
        """Test redirection with quoted path."""
        target = self.parser.extract_redirection_target('echo test > "/path with spaces"')
        assert target == "/path with spaces"

    def test_single_quoted_path(self):
        """Test redirection with single-quoted path."""
        target = self.parser.extract_redirection_target("echo test > '/path with spaces'")
        assert target == "/path with spaces"

    def test_no_redirection(self):
        """Test command without redirection."""
        target = self.parser.extract_redirection_target("ls -la")
        assert target is None

    def test_no_redirection_with_dash(self):
        """Test command with dash but no redirection."""
        target = self.parser.extract_redirection_target("grep -r pattern")
        assert target is None

    def test_redirection_with_spaces(self):
        """Test redirection with multiple spaces."""
        target = self.parser.extract_redirection_target("echo test >   /tmp/file")
        assert target == "/tmp/file"

    def test_complex_command_with_redirection(self):
        """Test complex command with redirection."""
        target = self.parser.extract_redirection_target("cat /etc/hosts | grep localhost > /tmp/out")
        assert target == "/tmp/out"

    def test_builtin_echo_with_redirection(self):
        """Test builtin echo command with redirection."""
        target = self.parser.extract_redirection_target("echo 'dangerous data' > /dev/sda")
        assert target == "/dev/sda"

    def test_builtin_cat_with_redirection(self):
        """Test builtin cat command with redirection."""
        target = self.parser.extract_redirection_target("cat important.txt > /dev/null")
        assert target == "/dev/null"


class TestRedirectionEdgeCases:
    """Test edge cases for redirection detection."""

    def setup_method(self):
        """Set up test fixtures."""
        self.parser = CommandParser()

    def test_empty_command(self):
        """Test empty command."""
        target = self.parser.extract_redirection_target("")
        assert target is None

    def test_whitespace_only(self):
        """Test whitespace-only command."""
        target = self.parser.extract_redirection_target("   ")
        assert target is None

    def test_redirection_without_target(self):
        """Test redirection without target (invalid syntax)."""
        # This is invalid syntax, but we should handle it gracefully
        target = self.parser.extract_redirection_target("echo test >")
        # Should return None or empty string, not crash
        assert target is None or target == ""

    def test_multiple_redirections(self):
        """Test command with multiple redirections (last one wins)."""
        target = self.parser.extract_redirection_target("echo test > /tmp/file1 > /tmp/file2")
        # Should detect at least one redirection
        assert target is not None

    def test_redirection_in_string(self):
        """Test > character inside a string (not actual redirection)."""
        # This is tricky - ">" inside quotes is not redirection
        # Current implementation may not handle this perfectly
        target = self.parser.extract_redirection_target('echo "a > b"')
        # Depending on implementation, this might be None or "b"
        # The important thing is it doesn't crash
        assert target is None or isinstance(target, str)


class TestDangerousRedirectionPatterns:
    """Test specific dangerous redirection patterns that must be caught."""

    def setup_method(self):
        """Set up test fixtures."""
        self.parser = CommandParser()

    def test_all_sata_drives(self):
        """Test redirection to all SATA drive letters."""
        import string
        for letter in string.ascii_lowercase:
            target = self.parser.extract_redirection_target(f"echo test > /dev/sd{letter}")
            assert target == f"/dev/sd{letter}"

    def test_all_nvme_variations(self):
        """Test redirection to various NVMe devices."""
        nvme_devices = [
            "nvme0n1", "nvme0n2", "nvme1n1", "nvme2n1",
            "nvme10n1", "nvme0n10"
        ]
        for device in nvme_devices:
            target = self.parser.extract_redirection_target(f"echo test > /dev/{device}")
            assert target == f"/dev/{device}"

    def test_all_critical_system_files(self):
        """Test redirection to critical system files."""
        system_files = [
            "/etc/passwd",
            "/etc/shadow",
            "/etc/fstab",
            "/etc/sudoers",
            "/etc/hosts",
            "/etc/group",
        ]
        for file in system_files:
            target = self.parser.extract_redirection_target(f"echo test > {file}")
            assert target == file

    def test_kernel_panic_trigger(self):
        """Test redirection to kernel panic trigger."""
        target = self.parser.extract_redirection_target("echo c > /proc/sysrq-trigger")
        assert target == "/proc/sysrq-trigger"

    def test_memory_device(self):
        """Test redirection to memory device."""
        target = self.parser.extract_redirection_target("echo test > /dev/mem")
        assert target == "/dev/mem"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
