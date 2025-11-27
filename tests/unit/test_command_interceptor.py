"""
Unit tests for command interception functionality in src/interceptor.py

Tests pattern detection with JSON-loaded patterns for dangerous commands,
caution commands, and typos.
"""

import os
import sys
import pytest

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))

from src.interceptor import (
    check_command,
    get_pattern_info,
    DANGEROUS_PATTERNS,
    CAUTION_PATTERNS,
    TYPO_PATTERNS
)


class TestCommandInterceptor:
    """Test suite for command interception with JSON-loaded patterns."""

    def test_patterns_loaded_from_json(self):
        """Test that patterns are loaded from JSON files."""
        # Verify dangerous patterns were loaded
        assert len(DANGEROUS_PATTERNS) > 0, \
            "Dangerous patterns should be loaded from JSON"

        # Verify each pattern has required fields
        for name, data in DANGEROUS_PATTERNS.items():
            assert 'pattern' in data, \
                f"Pattern {name} should have 'pattern' field"
            assert 'compiled' in data, \
                f"Pattern {name} should have compiled regex"
            assert 'category' in data, \
                f"Pattern {name} should have 'category' field"

    def test_dangerous_pattern_rm_dangerous(self):
        """Test rm -rf dangerous pattern detection."""
        # Test various rm -rf patterns
        test_cases = [
            ("rm -rf /", "critical", "rm_dangerous"),
            ("rm -rf ~", "critical", "rm_dangerous"),
            ("rm -rf $HOME", "critical", "rm_dangerous"),
            ("rm -rf *", "critical", "rm_dangerous"),
            ("rm -fr /", "critical", "rm_dangerous"),
            ("rm -r -f /", "critical", "rm_dangerous"),
            ("rm -f -r /home", "critical", "rm_dangerous"),
        ]

        for cmd, expected_level, expected_pattern in test_cases:
            level, pattern = check_command(cmd)
            assert level == expected_level, \
                f"Command '{cmd}' should be detected as {expected_level}"
            assert pattern == expected_pattern, \
                f"Command '{cmd}' should match pattern {expected_pattern}"

    def test_dangerous_pattern_chmod_777(self):
        """Test chmod 777 dangerous pattern detection."""
        test_cases = [
            ("chmod 777 file.txt", "critical", "chmod_777"),
            ("chmod -R 777 /var", "critical", "chmod_777"),
            ("chmod 777 .", "critical", "chmod_777"),
        ]

        for cmd, expected_level, expected_pattern in test_cases:
            level, pattern = check_command(cmd)
            assert level == expected_level, \
                f"Command '{cmd}' should be detected as {expected_level}"
            assert pattern == expected_pattern, \
                f"Command '{cmd}' should match pattern {expected_pattern}"

    def test_dangerous_pattern_chmod_000(self):
        """Test chmod 000 dangerous pattern detection."""
        test_cases = [
            ("chmod 000 file.txt", "critical", "chmod_000"),
            ("chmod -R 000 /var", "critical", "chmod_000"),
        ]

        for cmd, expected_level, expected_pattern in test_cases:
            level, pattern = check_command(cmd)
            assert level == expected_level, \
                f"Command '{cmd}' should be detected as {expected_level}"
            assert pattern == expected_pattern, \
                f"Command '{cmd}' should match pattern {expected_pattern}"

    def test_dangerous_pattern_dd_zero(self):
        """Test dd if=/dev/zero dangerous pattern detection."""
        test_cases = [
            ("dd if=/dev/zero of=/dev/sda", "critical", "dd_zero"),
            ("dd if=/dev/zero of=/dev/nvme0n1", "critical", "dd_zero"),
            ("dd if=/dev/zero", "critical", "dd_zero"),
        ]

        for cmd, expected_level, expected_pattern in test_cases:
            level, pattern = check_command(cmd)
            assert level == expected_level, \
                f"Command '{cmd}' should be detected as {expected_level}"
            assert pattern == expected_pattern, \
                f"Command '{cmd}' should match pattern {expected_pattern}"

    def test_dangerous_pattern_dd_random(self):
        """Test dd if=/dev/random dangerous pattern detection."""
        test_cases = [
            ("dd if=/dev/random of=/dev/sda", "critical", "dd_random"),
            ("dd if=/dev/random of=/dev/nvme0n1", "critical", "dd_random"),
        ]

        for cmd, expected_level, expected_pattern in test_cases:
            level, pattern = check_command(cmd)
            assert level == expected_level, \
                f"Command '{cmd}' should be detected as {expected_level}"
            assert pattern == expected_pattern, \
                f"Command '{cmd}' should match pattern {expected_pattern}"

    def test_dangerous_pattern_drop_database(self):
        """Test DROP DATABASE dangerous pattern detection."""
        test_cases = [
            ("DROP DATABASE production", "critical", "drop_database"),
            ("drop database test", "critical", "drop_database"),
            ("DROP DATABASE IF EXISTS mydb", "critical", "drop_database"),
        ]

        for cmd, expected_level, expected_pattern in test_cases:
            level, pattern = check_command(cmd)
            assert level == expected_level, \
                f"Command '{cmd}' should be detected as {expected_level}"
            assert pattern == expected_pattern, \
                f"Command '{cmd}' should match pattern {expected_pattern}"

    def test_dangerous_pattern_fork_bomb(self):
        """Test fork bomb dangerous pattern detection."""
        test_cases = [
            (":(){ :|:& };:", "critical", "fork_bomb"),
            (":() { :|:& };:", "critical", "fork_bomb"),
        ]

        for cmd, expected_level, expected_pattern in test_cases:
            level, pattern = check_command(cmd)
            assert level == expected_level, \
                f"Command '{cmd}' should be detected as {expected_level}"
            assert pattern == expected_pattern, \
                f"Command '{cmd}' should match pattern {expected_pattern}"

    def test_dangerous_pattern_redirect_to_disk(self):
        """Test redirect to disk dangerous pattern detection."""
        test_cases = [
            ("echo test > /dev/sda", "critical", "redirect_to_disk"),
            ("cat file > /dev/nvme0n1", "critical", "redirect_to_disk"),
        ]

        for cmd, expected_level, expected_pattern in test_cases:
            level, pattern = check_command(cmd)
            assert level == expected_level, \
                f"Command '{cmd}' should be detected as {expected_level}"
            assert pattern == expected_pattern, \
                f"Command '{cmd}' should match pattern {expected_pattern}"

    def test_dangerous_pattern_mkfs_disk(self):
        """Test mkfs disk dangerous pattern detection."""
        test_cases = [
            ("mkfs.ext4 /dev/sda", "critical", "mkfs_disk"),
            ("mkfs.ext4 /dev/nvme0n1", "critical", "mkfs_disk"),
            ("mkfs /dev/sda1", "critical", "mkfs_disk"),
        ]

        for cmd, expected_level, expected_pattern in test_cases:
            level, pattern = check_command(cmd)
            assert level == expected_level, \
                f"Command '{cmd}' should be detected as {expected_level}"
            assert pattern == expected_pattern, \
                f"Command '{cmd}' should match pattern {expected_pattern}"

    def test_dangerous_pattern_mv_to_null(self):
        """Test mv to /dev/null dangerous pattern detection."""
        test_cases = [
            ("mv important.txt /dev/null", "critical", "mv_to_null"),
            ("mv file.doc /dev/null", "critical", "mv_to_null"),
        ]

        for cmd, expected_level, expected_pattern in test_cases:
            level, pattern = check_command(cmd)
            assert level == expected_level, \
                f"Command '{cmd}' should be detected as {expected_level}"
            assert pattern == expected_pattern, \
                f"Command '{cmd}' should match pattern {expected_pattern}"

    def test_dangerous_pattern_system_modify(self):
        """Test system file modification dangerous pattern detection."""
        test_cases = [
            ("> /etc/passwd", "critical", "system_modify"),
            ("echo test > /etc/shadow", "critical", "system_modify"),
            ("cat file > /etc/fstab", "critical", "system_modify"),
        ]

        for cmd, expected_level, expected_pattern in test_cases:
            level, pattern = check_command(cmd)
            assert level == expected_level, \
                f"Command '{cmd}' should be detected as {expected_level}"
            assert pattern == expected_pattern, \
                f"Command '{cmd}' should match pattern {expected_pattern}"

    def test_dangerous_pattern_kernel_panic(self):
        """Test kernel panic dangerous pattern detection."""
        test_cases = [
            ("echo c > /proc/sysrq-trigger", "critical", "kernel_panic"),
            # Note: pattern only matches 'c', not other letters
        ]

        for cmd, expected_level, expected_pattern in test_cases:
            level, pattern = check_command(cmd)
            assert level == expected_level, \
                f"Command '{cmd}' should be detected as {expected_level}"
            assert pattern == expected_pattern, \
                f"Command '{cmd}' should match pattern {expected_pattern}"

    def test_dangerous_pattern_shred_secure(self):
        """Test shred secure deletion dangerous pattern detection."""
        # Check if shred_secure pattern exists
        if "shred_secure" in DANGEROUS_PATTERNS:
            test_cases = [
                # Pattern requires /dev/sd*, /dev/nvme, or -n with 2+ digits
                ("shred /dev/sda", "critical", "shred_secure"),
                ("shred -n 10 file.txt", "critical", "shred_secure"),
                ("shred -n 100 file.txt", "critical", "shred_secure"),
            ]

            for cmd, expected_level, expected_pattern in test_cases:
                level, pattern = check_command(cmd)
                assert level == expected_level, \
                    f"Command '{cmd}' should be detected as {expected_level}"
                assert pattern == expected_pattern, \
                    f"Command '{cmd}' should match pattern {expected_pattern}"

    def test_all_dangerous_patterns_detected(self):
        """Test that all dangerous patterns from JSON are detected."""
        # Create test commands for each dangerous pattern
        pattern_tests = {
            "rm_dangerous": "rm -rf /",
            "chmod_777": "chmod 777 file",
            "chmod_000": "chmod 000 file",
            "dd_zero": "dd if=/dev/zero of=/dev/sda",
            "dd_random": "dd if=/dev/random of=/dev/sda",
            "drop_database": "DROP DATABASE test",
            "fork_bomb": ":(){ :|:& };:",
            "redirect_to_disk": "echo > /dev/sda",
            "mkfs_disk": "mkfs.ext4 /dev/sda",
            "mv_to_null": "mv file /dev/null",
            "system_modify": "> /etc/passwd",
            "kernel_panic": "echo c > /proc/sysrq-trigger",
        }

        for pattern_name in DANGEROUS_PATTERNS.keys():
            if pattern_name in pattern_tests:
                cmd = pattern_tests[pattern_name]
                level, detected_pattern = check_command(cmd)
                assert level == "critical", \
                    f"Pattern {pattern_name} should be detected as critical"
                assert detected_pattern == pattern_name, \
                    f"Pattern {pattern_name} should be correctly identified"

    def test_caution_pattern_sudo_shell(self):
        """Test sudo shell caution pattern detection."""
        # Check if caution patterns are loaded
        if len(CAUTION_PATTERNS) > 0 and "sudo_shell" in CAUTION_PATTERNS:
            test_cases = [
                ("sudo su", "caution", "sudo_shell"),
                ("sudo bash", "caution", "sudo_shell"),
                ("sudo sh", "caution", "sudo_shell"),
                ("sudo -i", "caution", "sudo_shell"),
            ]

            for cmd, expected_level, expected_pattern in test_cases:
                level, pattern = check_command(cmd)
                assert level == expected_level, \
                    f"Command '{cmd}' should be detected as {expected_level}"
                assert pattern == expected_pattern, \
                    f"Command '{cmd}' should match pattern {expected_pattern}"

    def test_caution_pattern_chmod_permissive(self):
        """Test chmod permissive caution pattern detection."""
        if len(CAUTION_PATTERNS) > 0 and \
           "chmod_permissive" in CAUTION_PATTERNS:
            test_cases = [
                ("chmod 666 file.txt", "caution", "chmod_permissive"),
                ("chmod 755 /var", "caution", "chmod_permissive"),
                ("chmod -R 775 dir", "caution", "chmod_permissive"),
            ]

            for cmd, expected_level, expected_pattern in test_cases:
                level, pattern = check_command(cmd)
                assert level == expected_level, \
                    f"Command '{cmd}' should be detected as {expected_level}"
                assert pattern == expected_pattern, \
                    f"Command '{cmd}' should match pattern {expected_pattern}"

    def test_caution_pattern_firewall_disable(self):
        """Test firewall disable caution pattern detection."""
        if len(CAUTION_PATTERNS) > 0 and \
           "firewall_disable" in CAUTION_PATTERNS:
            test_cases = [
                ("ufw disable", "caution", "firewall_disable"),
                ("iptables -F", "caution", "firewall_disable"),
            ]

            for cmd, expected_level, expected_pattern in test_cases:
                level, pattern = check_command(cmd)
                assert level == expected_level, \
                    f"Command '{cmd}' should be detected as {expected_level}"
                assert pattern == expected_pattern, \
                    f"Command '{cmd}' should match pattern {expected_pattern}"

    def test_caution_pattern_selinux_disable(self):
        """Test SELinux disable caution pattern detection."""
        if len(CAUTION_PATTERNS) > 0 and \
           "selinux_disable" in CAUTION_PATTERNS:
            test_cases = [
                ("setenforce 0", "caution", "selinux_disable"),
            ]

            for cmd, expected_level, expected_pattern in test_cases:
                level, pattern = check_command(cmd)
                assert level == expected_level, \
                    f"Command '{cmd}' should be detected as {expected_level}"
                assert pattern == expected_pattern, \
                    f"Command '{cmd}' should match pattern {expected_pattern}"

    def test_all_caution_patterns_detected(self):
        """Test that all caution patterns from JSON are detected."""
        if len(CAUTION_PATTERNS) == 0:
            pytest.skip("No caution patterns loaded")

        # Create test commands for each caution pattern
        pattern_tests = {
            "sudo_shell": "sudo su",
            "chmod_permissive": "chmod 666 file",
            "firewall_disable": "ufw disable",
            "selinux_disable": "setenforce 0",
        }

        for pattern_name in CAUTION_PATTERNS.keys():
            if pattern_name in pattern_tests:
                cmd = pattern_tests[pattern_name]
                level, detected_pattern = check_command(cmd)
                assert level == "caution", \
                    f"Pattern {pattern_name} should be detected as caution"
                assert detected_pattern == pattern_name, \
                    f"Pattern {pattern_name} should be correctly identified"

    def test_typo_pattern_sl(self):
        """Test 'sl' typo pattern detection."""
        if len(TYPO_PATTERNS) > 0 and "sl" in TYPO_PATTERNS:
            level, pattern = check_command("sl")
            assert level == "critical", \
                "Typo 'sl' should be detected as critical"
            assert pattern == "typo_sl", \
                "Typo 'sl' should match typo_sl pattern"

    def test_typo_pattern_cd_stuck(self):
        """Test 'cd..' typo pattern detection."""
        if len(TYPO_PATTERNS) > 0 and "cd_stuck" in TYPO_PATTERNS:
            level, pattern = check_command("cd..")
            assert level == "critical", \
                "Typo 'cd..' should be detected as critical"
            assert pattern == "typo_cd_stuck", \
                "Typo 'cd..' should match typo_cd_stuck pattern"

    def test_all_typo_patterns_detected(self):
        """Test that all typo patterns from JSON are detected."""
        if len(TYPO_PATTERNS) == 0:
            pytest.skip("No typo patterns loaded")

        # Create test commands for each typo pattern
        pattern_tests = {
            "sl": "sl",
            "cd_stuck": "cd..",
        }

        for pattern_name in TYPO_PATTERNS.keys():
            if pattern_name in pattern_tests:
                cmd = pattern_tests[pattern_name]
                level, detected_pattern = check_command(cmd)
                assert level == "critical", \
                    f"Typo pattern {pattern_name} should be detected"
                assert detected_pattern == f"typo_{pattern_name}", \
                    f"Typo pattern {pattern_name} should be identified"

    def test_safe_commands_not_detected(self):
        """Test that safe commands are not flagged."""
        safe_commands = [
            "ls -la",
            "pwd",
            "echo Hello World",
            "cd /tmp",
            "cat file.txt",
            "grep pattern file",
            "chmod 644 file.txt",
            "rm file.txt",
            "dd if=input.txt of=output.txt",
            "mkdir newdir",
            "touch newfile",
            "cp source dest",
            "mv oldname newname",
        ]

        for cmd in safe_commands:
            level, pattern = check_command(cmd)
            assert level == "safe", \
                f"Safe command '{cmd}' should not be flagged"
            assert pattern == "", \
                f"Safe command '{cmd}' should have empty pattern"

    def test_get_pattern_info_dangerous(self):
        """Test retrieving pattern info for dangerous patterns."""
        # Test with a known dangerous pattern
        if "rm_dangerous" in DANGEROUS_PATTERNS:
            info = get_pattern_info("rm_dangerous")
            assert isinstance(info, dict), "Should return dict"
            assert 'pattern' in info, "Should have pattern field"
            assert 'category' in info, "Should have category field"

    def test_get_pattern_info_typo(self):
        """Test retrieving pattern info for typo patterns."""
        if "sl" in TYPO_PATTERNS:
            info = get_pattern_info("typo_sl")
            assert isinstance(info, dict), "Should return dict"

    def test_case_insensitive_matching(self):
        """Test that pattern matching is case-insensitive."""
        test_cases = [
            ("RM -RF /", "critical"),
            ("CHMOD 777 file", "critical"),
            ("DROP DATABASE test", "critical"),
        ]

        for cmd, expected_level in test_cases:
            level, _ = check_command(cmd)
            assert level == expected_level, \
                f"Command '{cmd}' should be detected (case-insensitive)"

    def test_pattern_priority_dangerous_over_caution(self):
        """Test that dangerous patterns have priority over caution."""
        # chmod 777 is dangerous, chmod 666 is caution
        level_777, pattern_777 = check_command("chmod 777 file")
        assert level_777 == "critical", \
            "chmod 777 should be critical (dangerous)"

        if "chmod_permissive" in CAUTION_PATTERNS:
            level_666, pattern_666 = check_command("chmod 666 file")
            assert level_666 == "caution", \
                "chmod 666 should be caution"

    def test_pattern_with_multiple_spaces(self):
        """Test patterns with multiple spaces."""
        test_cases = [
            ("rm  -rf  /", "critical"),
            ("chmod   777   file", "critical"),
        ]

        for cmd, expected_level in test_cases:
            level, _ = check_command(cmd)
            assert level == expected_level, \
                f"Command '{cmd}' with multiple spaces should be detected"

    def test_pattern_with_tabs(self):
        """Test patterns with tabs."""
        test_cases = [
            ("rm\t-rf\t/", "critical"),
            ("chmod\t777\tfile", "critical"),
        ]

        for cmd, expected_level in test_cases:
            level, _ = check_command(cmd)
            assert level == expected_level, \
                f"Command '{cmd}' with tabs should be detected"

    def test_empty_command(self):
        """Test handling of empty command."""
        level, pattern = check_command("")
        assert level == "safe", "Empty command should be safe"
        assert pattern == "", "Empty command should have no pattern"

    def test_whitespace_only_command(self):
        """Test handling of whitespace-only command."""
        level, pattern = check_command("   ")
        assert level == "safe", "Whitespace-only command should be safe"
        assert pattern == "", "Whitespace-only command should have no pattern"

    def test_command_with_arguments(self):
        """Test that patterns match commands with various arguments."""
        test_cases = [
            ("rm -rf / --no-preserve-root", "critical", "rm_dangerous"),
            ("chmod 777 file1 file2 file3", "critical", "chmod_777"),
        ]

        for cmd, expected_level, expected_pattern in test_cases:
            level, pattern = check_command(cmd)
            assert level == expected_level, \
                f"Command '{cmd}' with arguments should be detected"
            assert pattern == expected_pattern, \
                f"Command '{cmd}' should match {expected_pattern}"

    def test_performance_check_command(self):
        """Test that check_command completes within performance target."""
        import time

        # Test with a safe command (worst case - checks all patterns)
        start = time.time()
        for _ in range(100):
            check_command("ls -la")
        end = time.time()

        avg_time_ms = ((end - start) / 100) * 1000
        assert avg_time_ms < 50, \
            f"check_command should complete within 50ms, got {avg_time_ms}ms"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
