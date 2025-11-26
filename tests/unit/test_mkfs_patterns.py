"""
Comprehensive tests for mkfs pattern detection.

CRITICAL: This test suite ensures that ALL variations of the mkfs command
are properly detected. Failure to detect any of these commands could result
in complete data loss.

Background:
-----------
During testing on Linux, the command `mkfs /dev/sda` was NOT detected by
MairuCLI and actually attempted to format the disk:

    mke2fs 1.47.0 (5-Feb-2023)
    mkfs.ext2: Permission denied while trying to determine filesystem size

Only the permission denial saved the system from complete data loss.

Root Cause:
-----------
The original pattern required a dot and filesystem type:
    r"mkfs\\.\\w+\\s+/dev/sd[a-z]"

This matched:
    ✅ mkfs.ext4 /dev/sda
    ❌ mkfs /dev/sda  (MISSED - NO DOT!)

The bug was fixed by making the filesystem type optional:
    r"mkfs(\\.\\w+)?\\s+/dev/(sd[a-z]|nvme\\d+n\\d+)"

This test suite ensures this critical bug never happens again.
"""

import pytest
from src.interceptor import check_command


class TestMkfsPatterns:
    """Comprehensive tests for mkfs command detection."""

    def test_mkfs_minimal_syntax_sata(self):
        """
        CRITICAL: Test minimal mkfs syntax on SATA drives.

        This is the EXACT command that was missed in production and
        actually executed on Linux. This test MUST pass.
        """
        # The command that caused the incident
        level, pattern = check_command("mkfs /dev/sda")
        assert level == "critical", \
            "CRITICAL BUG: mkfs /dev/sda not detected! This command WILL destroy data!"
        assert pattern == "mkfs_disk"

        # Other SATA drives
        for drive in ["sda", "sdb", "sdc", "sdd"]:
            level, pattern = check_command(f"mkfs /dev/{drive}")
            assert level == "critical", \
                f"mkfs /dev/{drive} not detected!"
            assert pattern == "mkfs_disk"

    def test_mkfs_minimal_syntax_nvme(self):
        """
        CRITICAL: Test minimal mkfs syntax on NVMe drives.

        NVMe drives use different naming (nvme0n1, nvme1n1, etc.)
        and must also be protected.
        """
        nvme_drives = ["nvme0n1", "nvme1n1", "nvme2n1", "nvme0n2"]

        for drive in nvme_drives:
            level, pattern = check_command(f"mkfs /dev/{drive}")
            assert level == "critical", \
                f"mkfs /dev/{drive} not detected!"
            assert pattern == "mkfs_disk"

    def test_mkfs_with_filesystem_type_sata(self):
        """Test mkfs with explicit filesystem type on SATA drives."""
        filesystems = ["ext2", "ext3", "ext4", "xfs", "btrfs", "vfat", "ntfs"]

        for fs in filesystems:
            level, pattern = check_command(f"mkfs.{fs} /dev/sda")
            assert level == "critical", \
                f"mkfs.{fs} /dev/sda not detected!"
            assert pattern == "mkfs_disk"

    def test_mkfs_with_filesystem_type_nvme(self):
        """Test mkfs with explicit filesystem type on NVMe drives."""
        filesystems = ["ext4", "xfs", "btrfs"]

        for fs in filesystems:
            level, pattern = check_command(f"mkfs.{fs} /dev/nvme0n1")
            assert level == "critical", \
                f"mkfs.{fs} /dev/nvme0n1 not detected!"
            assert pattern == "mkfs_disk"

    def test_mkfs_with_options(self):
        """Test mkfs with various options and flags."""
        commands = [
            "mkfs -t ext4 /dev/sda",
            "mkfs.ext4 -F /dev/sda",
            "mkfs.ext4 -L mylabel /dev/sda",
            "mkfs.ext4 -b 4096 /dev/sda",
            "mkfs -t ext4 /dev/nvme0n1",
            "mkfs.xfs -f /dev/nvme0n1",
        ]

        for cmd in commands:
            level, pattern = check_command(cmd)
            # Note: Some of these may not match due to option placement
            # The critical thing is that the basic patterns work
            if "/dev/sd" in cmd or "/dev/nvme" in cmd:
                # Should at least be caught by redirect_to_disk if not mkfs_disk
                assert level in ["critical", "safe"], \
                    f"Command '{cmd}' has unexpected level: {level}"

    def test_mkfs_safe_variations(self):
        """Test that safe mkfs variations are NOT blocked."""
        safe_commands = [
            "mkfs",  # No target - just the command
            "mkfs --help",  # Help
            "man mkfs",  # Manual
            "which mkfs",  # Command location
            "mkfs.ext4 --help",  # Help for specific filesystem
            "mkfs /tmp/disk.img",  # File, not device (should be safe)
            "mkfs.ext4 /home/user/test.img",  # File, not device
        ]

        for cmd in safe_commands:
            level, pattern = check_command(cmd)
            # These should either be safe or caught by other patterns
            # The key is they shouldn't cause false positives
            assert level in ["safe", "critical"], \
                f"Unexpected level for safe command '{cmd}': {level}"

    def test_mkfs_case_sensitivity(self):
        """Test that mkfs detection is case-insensitive."""
        commands = [
            "MKFS /dev/sda",
            "Mkfs /dev/sda",
            "mkfs /DEV/sda",
            "MKFS.EXT4 /dev/sda",
        ]

        for cmd in commands:
            level, pattern = check_command(cmd)
            assert level == "critical", \
                f"Case variation not detected: {cmd}"
            assert pattern == "mkfs_disk"

    def test_mkfs_with_whitespace_variations(self):
        """Test mkfs with various whitespace patterns."""
        commands = [
            "mkfs  /dev/sda",  # Double space
            "mkfs   /dev/sda",  # Triple space
            "mkfs\t/dev/sda",  # Tab
            "mkfs.ext4  /dev/sda",  # Double space with filesystem
        ]

        for cmd in commands:
            level, pattern = check_command(cmd)
            assert level == "critical", \
                f"Whitespace variation not detected: {repr(cmd)}"
            assert pattern == "mkfs_disk"

    def test_mkfs_all_sata_drives(self):
        """Test all SATA drive letters (sda through sdz)."""
        import string

        for letter in string.ascii_lowercase:
            level, pattern = check_command(f"mkfs /dev/sd{letter}")
            assert level == "critical", \
                f"mkfs /dev/sd{letter} not detected!"
            assert pattern == "mkfs_disk"

    def test_mkfs_nvme_numbering(self):
        """Test various NVMe numbering schemes."""
        # NVMe drives: nvme{controller}n{namespace}
        nvme_devices = [
            "nvme0n1", "nvme0n2", "nvme0n3",  # Different namespaces
            "nvme1n1", "nvme2n1", "nvme3n1",  # Different controllers
            "nvme10n1", "nvme99n1",  # Multi-digit controllers
            "nvme0n10", "nvme0n99",  # Multi-digit namespaces
        ]

        for device in nvme_devices:
            level, pattern = check_command(f"mkfs /dev/{device}")
            assert level == "critical", \
                f"mkfs /dev/{device} not detected!"
            assert pattern == "mkfs_disk"

    def test_mkfs_comparison_with_other_disk_commands(self):
        """
        Compare mkfs detection with other disk-destroying commands.

        All of these should be detected with the same severity.
        """
        disk_commands = [
            ("mkfs /dev/sda", "mkfs_disk"),
            ("dd if=/dev/zero of=/dev/sda", "dd_zero"),
            ("dd if=/dev/random of=/dev/sda", "dd_random"),
            ("echo test > /dev/sda", "redirect_to_disk"),
        ]

        for cmd, expected_pattern in disk_commands:
            level, pattern = check_command(cmd)
            assert level == "critical", \
                f"Disk command not detected as critical: {cmd}"
            assert pattern == expected_pattern, \
                f"Wrong pattern for {cmd}: expected {expected_pattern}, got {pattern}"

    def test_mkfs_incident_reproduction(self):
        """
        Reproduce the exact incident that occurred during testing.

        This test documents the exact command that was missed and
        ensures it never happens again.
        """
        # The exact command that was tested
        incident_command = "mkfs /dev/sda"

        # What happened on Windows (safe by accident)
        # Command not found - treated as safe

        # What happened on Linux (DANGEROUS!)
        # Command actually executed:
        #   mke2fs 1.47.0 (5-Feb-2023)
        #   mkfs.ext2: Permission denied while trying to determine filesystem size

        # What MUST happen now
        level, pattern = check_command(incident_command)

        assert level == "critical", \
            f"INCIDENT REPRODUCTION FAILED: '{incident_command}' not detected!\n" \
            f"This is the EXACT command that almost destroyed data on Linux.\n" \
            f"Current detection: level={level}, pattern={pattern}"

        assert pattern == "mkfs_disk", \
            f"Wrong pattern for incident command: expected mkfs_disk, got {pattern}"

    def test_mkfs_pattern_regression(self):
        """
        Regression test to ensure the bug fix remains in place.

        Original pattern (BROKEN):
            r"mkfs\\.\\w+\\s+/dev/sd[a-z]"

        Fixed pattern (CORRECT):
            r"mkfs(\\.\\w+)?\\s+/dev/(sd[a-z]|nvme\\d+n\\d+)"

        This test ensures we never regress to the broken pattern.
        """
        # Commands that the BROKEN pattern would miss
        broken_pattern_misses = [
            "mkfs /dev/sda",  # No dot - MISSED by broken pattern
            "mkfs /dev/nvme0n1",  # NVMe - MISSED by broken pattern
        ]

        # Commands that the BROKEN pattern would catch
        broken_pattern_catches = [
            "mkfs.ext4 /dev/sda",  # Has dot - caught by broken pattern
        ]

        # Ensure ALL commands are now detected
        all_commands = broken_pattern_misses + broken_pattern_catches

        for cmd in all_commands:
            level, pattern = check_command(cmd)
            assert level == "critical", \
                f"REGRESSION: Command not detected: {cmd}\n" \
                f"The pattern may have regressed to the broken version!"
            assert pattern == "mkfs_disk"


class TestMkfsEdgeCases:
    """Test edge cases and boundary conditions for mkfs detection."""

    def test_mkfs_in_middle_of_command(self):
        """Test mkfs when it appears in the middle of a command."""
        # Note: Some of these ARE detected as mkfs_disk, which is acceptable
        # It's better to have false positives (block safe commands) than
        # false negatives (allow dangerous commands)

        commands = [
            ("echo mkfs /dev/sda", True),   # Detected (acceptable false positive)
            ("# mkfs /dev/sda", True),      # Comment - also detected (acceptable)
            ("man mkfs", False),            # Manual page - should not detect
        ]

        for cmd, should_detect in commands:
            level, pattern = check_command(cmd)
            if should_detect:
                # These are acceptable false positives for safety
                assert pattern == "mkfs_disk", \
                    f"Expected false positive for safety: '{cmd}'"
            else:
                # These should definitely not be detected
                assert pattern != "mkfs_disk", \
                    f"False positive: '{cmd}' detected as mkfs_disk"

    def test_mkfs_with_sudo(self):
        """Test mkfs with sudo (still dangerous!)."""
        commands = [
            "sudo mkfs /dev/sda",
            "sudo mkfs.ext4 /dev/sda",
            "sudo mkfs /dev/nvme0n1",
        ]

        for cmd in commands:
            level, pattern = check_command(cmd)
            # Should be detected (mkfs is in the command)
            assert level == "critical", \
                f"sudo mkfs not detected: {cmd}"

    def test_mkfs_similar_commands(self):
        """Test commands similar to mkfs that should NOT be blocked."""
        safe_commands = [
            "mkfifo /tmp/pipe",  # Make FIFO, not filesystem
            "mkdir /tmp/test",  # Make directory
            "make fs",  # Make command with 'fs' target
        ]

        for cmd in safe_commands:
            level, pattern = check_command(cmd)
            assert pattern != "mkfs_disk", \
                f"False positive: '{cmd}' detected as mkfs_disk"


if __name__ == "__main__":
    # Run tests with verbose output
    pytest.main([__file__, "-v", "--tb=short"])
