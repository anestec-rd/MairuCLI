"""
Quick test script to verify MairuCLI functionality.
Tests core features and generates a report.
"""

import sys
import os

# Add project root to path (tests/unit -> tests -> root)
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.interceptor import check_command, DANGEROUS_PATTERNS, CAUTION_PATTERNS, TYPO_PATTERNS
from datetime import datetime


def test_pattern_detection():
    """Test pattern detection logic."""
    print("=" * 70)
    print("MairuCLI Pattern Detection Test - Day 5")
    print("=" * 70)
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Version: 1.1")
    print("=" * 70)
    print()

    results = []

    # Test 1: Bug Fix - dd command
    print("Test 1: Bug Fix Verification (Issue #2)")
    print("-" * 70)

    test_cases = [
        ("dd if=/dev/zero", "critical", "dd_zero", "PASS - Now detected!"),
        ("dd if=/dev/zero of=/dev/sda", "critical", "dd_zero", "PASS - Still detected"),
        ("dd if=file of=file2", "safe", "", "PASS - Safe command allowed"),
    ]

    for cmd, expected_level, expected_pattern, note in test_cases:
        level, pattern = check_command(cmd)
        status = "PASS" if level == expected_level else "FAIL"
        print(f"  Command: {cmd}")
        print(f"  Expected: {expected_level} / {expected_pattern}")
        print(f"  Got: {level} / {pattern}")
        print(f"  Status: {status}")
        print(f"  Note: {note}")
        print()
        results.append((cmd, status))

    # Test 2: All Dangerous Patterns
    print("Test 2: Dangerous Pattern Detection (11 patterns)")
    print("-" * 70)

    dangerous_commands = [
        ("rm -rf /", "rm_dangerous"),
        ("rm -rf ~", "rm_dangerous"),
        ("rm -rf *", "rm_dangerous"),
        ("chmod 777 file.txt", "chmod_777"),
        ("chmod -R 777 /var", "chmod_777"),
        ("dd if=/dev/zero of=/dev/sda", "dd_zero"),
        ("DROP DATABASE production", "drop_database"),
        (":(){ :|:& };:", "fork_bomb"),
        ("echo test > /dev/sda", "redirect_to_disk"),
        ("mkfs.ext4 /dev/sda", "mkfs_disk"),
        ("mv important.txt /dev/null", "mv_to_null"),
        ("> /etc/passwd", "overwrite_file"),
        ("dd if=/dev/random of=/dev/sda", "dd_random"),
        ("echo c > /proc/sysrq-trigger", "kernel_panic"),
    ]

    for cmd, expected_pattern in dangerous_commands:
        level, pattern = check_command(cmd)
        status = "PASS" if level == "critical" and pattern == expected_pattern else "FAIL"
        print(f"  {expected_pattern}: {cmd}")
        print(f"    Level: {level}, Pattern: {pattern}")
        print(f"    Status: {status}")
        results.append((cmd, status))
    print()

    # Test 3: Caution Patterns
    print("Test 3: Caution Pattern Detection (4 patterns)")
    print("-" * 70)

    caution_commands = [
        ("sudo su", "sudo_shell"),
        ("sudo bash", "sudo_shell"),
        ("chmod 666 file.txt", "chmod_permissive"),
        ("chmod 755 /var", "chmod_permissive"),
        ("ufw disable", "firewall_disable"),
        ("iptables -F", "firewall_disable"),
        ("setenforce 0", "selinux_disable"),
    ]

    for cmd, expected_pattern in caution_commands:
        level, pattern = check_command(cmd)
        status = "PASS" if level == "caution" and pattern == expected_pattern else "FAIL"
        print(f"  {expected_pattern}: {cmd}")
        print(f"    Level: {level}, Pattern: {pattern}")
        print(f"    Status: {status}")
        results.append((cmd, status))
    print()

    # Test 4: Typo Patterns
    print("Test 4: Typo Detection (2 patterns)")
    print("-" * 70)

    typo_commands = [
        ("sl", "typo_sl"),
        ("cd..", "typo_cd_stuck"),
    ]

    for cmd, expected_pattern in typo_commands:
        level, pattern = check_command(cmd)
        status = "PASS" if level == "critical" and pattern == expected_pattern else "FAIL"
        print(f"  {expected_pattern}: {cmd}")
        print(f"    Level: {level}, Pattern: {pattern}")
        print(f"    Status: {status}")
        results.append((cmd, status))
    print()

    # Test 5: Safe Commands
    print("Test 5: Safe Command Pass-Through")
    print("-" * 70)

    safe_commands = [
        "ls -la",
        "pwd",
        "echo Hello",
        "cd /tmp",
        "cat file.txt",
        "grep pattern file",
        "chmod 644 file.txt",
        "rm file.txt",
        "dd if=input.txt of=output.txt",
    ]

    for cmd in safe_commands:
        level, pattern = check_command(cmd)
        status = "PASS" if level == "safe" else "FAIL"
        print(f"  {cmd}")
        print(f"    Level: {level}")
        print(f"    Status: {status}")
        results.append((cmd, status))
    print()

    # Summary
    print("=" * 70)
    print("Test Summary")
    print("=" * 70)

    total = len(results)
    passed = sum(1 for _, status in results if "PASS" in status)
    failed = sum(1 for _, status in results if "FAIL" in status)

    print(f"Total Tests: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Success Rate: {(passed/total*100):.1f}%")
    print()

    print("Pattern Statistics:")
    print(f"  Dangerous Patterns: {len(DANGEROUS_PATTERNS)}")
    print(f"  Caution Patterns: {len(CAUTION_PATTERNS)}")
    print(f"  Typo Patterns: {len(TYPO_PATTERNS)}")
    print(f"  Total Patterns: {len(DANGEROUS_PATTERNS) + len(CAUTION_PATTERNS) + len(TYPO_PATTERNS)}")
    print()

    if failed == 0:
        print("All tests passed! MairuCLI is working correctly.")
    else:
        print(f"WARNING: {failed} test(s) failed. Please review.")

    print("=" * 70)

    return passed, failed, total


if __name__ == "__main__":
    passed, failed, total = test_pattern_detection()
    sys.exit(0 if failed == 0 else 1)
