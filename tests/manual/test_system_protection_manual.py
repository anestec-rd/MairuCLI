"""
Manual testing script for system directory protection.

This script runs automated tests that can be executed safely on real systems.
It tests the detection logic without actually executing dangerous commands.

Usage:
    python tests/manual/test_system_protection_manual.py
"""

import sys
import os
import time
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.interceptor import check_system_directory
from src.path_resolver import PathResolver
from src.command_parser import CommandParser


def print_header(text):
    """Print a formatted header."""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70)


def print_test(test_name, passed, details=""):
    """Print test result."""
    status = "✅ PASS" if passed else "❌ FAIL"
    print(f"{status} - {test_name}")
    if details:
        print(f"     {details}")


def test_platform_detection():
    """Test that platform is correctly detected."""
    print_header("Platform Detection")

    platform = sys.platform
    print(f"Detected platform: {platform}")

    if platform == "win32":
        print("✅ Running on Windows")
        return True
    elif platform.startswith("linux"):
        print("✅ Running on Linux")
        return True
    elif platform == "darwin":
        print("✅ Running on macOS")
        return True
    else:
        print(f"⚠️  Unknown platform: {platform}")
        return False


def test_windows_protection():
    """Test Windows system directory protection."""
    if sys.platform != "win32":
        print("⏭️  Skipping Windows tests (not on Windows)")
        return True

    print_header("Windows System Directory Protection")

    tests = [
        ("rm C:\\Windows\\System32\\test.dll", "critical", "Windows System32"),
        ("rm C:\\Windows\\test.txt", "critical", "Windows directory"),
        ("mv test.txt C:\\Program Files\\test.txt", "caution", "Program Files"),
        ("chmod 777 C:\\ProgramData\\test", "caution", "ProgramData"),
        ("rm C:\\Users\\Test\\test.txt", "safe", "User directory (safe)"),
    ]

    all_passed = True
    for command, expected_level, description in tests:
        level, ptype, path = check_system_directory(command)
        passed = level == expected_level
        all_passed = all_passed and passed

        details = f"Expected: {expected_level}, Got: {level}"
        if path:
            details += f" (Path: {path})"

        print_test(description, passed, details)

    return all_passed


def test_linux_protection():
    """Test Linux system directory protection."""
    if not sys.platform.startswith("linux"):
        print("⏭️  Skipping Linux tests (not on Linux)")
        return True

    print_header("Linux System Directory Protection")

    tests = [
        ("rm /etc/test.conf", "critical", "/etc protection"),
        ("rm /bin/test", "critical", "/bin protection"),
        ("chmod 777 /usr/bin/test", "caution", "/usr protection"),
        ("mv test /var/log/test", "caution", "/var/log protection"),
        ("rm /home/user/test.txt", "safe", "User home (safe)"),
    ]

    all_passed = True
    for command, expected_level, description in tests:
        level, ptype, path = check_system_directory(command)
        passed = level == expected_level
        all_passed = all_passed and passed

        details = f"Expected: {expected_level}, Got: {level}"
        if path:
            details += f" (Path: {path})"

        print_test(description, passed, details)

    return all_passed


def test_edge_cases():
    """Test edge cases."""
    print_header("Edge Case Testing")

    all_passed = True

    # Test relative paths (Windows)
    if sys.platform == "win32":
        level, _, _ = check_system_directory("rm ..\\..\\Windows\\test.txt")
        passed = level in ["critical", "caution"]  # Should detect system dir
        print_test("Relative path detection (Windows)", passed, f"Level: {level}")
        all_passed = all_passed and passed

    # Test relative paths (Linux)
    if sys.platform.startswith("linux"):
        level, _, _ = check_system_directory("rm ../../../etc/test.conf")
        passed = level in ["critical", "caution"]  # Should detect system dir
        print_test("Relative path detection (Linux)", passed, f"Level: {level}")
        all_passed = all_passed and passed

    # Test wildcards
    if sys.platform == "win32":
        level, _, _ = check_system_directory("rm C:\\Windows\\*.dll")
        passed = level == "critical"
        print_test("Wildcard detection (Windows)", passed, f"Level: {level}")
        all_passed = all_passed and passed

    if sys.platform.startswith("linux"):
        level, _, _ = check_system_directory("rm /etc/*.conf")
        passed = level == "critical"
        print_test("Wildcard detection (Linux)", passed, f"Level: {level}")
        all_passed = all_passed and passed

    # Test empty command
    level, _, _ = check_system_directory("")
    passed = level == "safe"
    print_test("Empty command handling", passed, f"Level: {level}")
    all_passed = all_passed and passed

    # Test safe command
    level, _, _ = check_system_directory("echo hello")
    passed = level == "safe"
    print_test("Safe command (echo)", passed, f"Level: {level}")
    all_passed = all_passed and passed

    return all_passed


def test_performance():
    """Test performance of system directory checks."""
    print_header("Performance Testing")

    commands = [
        "rm C:\\Windows\\test.txt" if sys.platform == "win32" else "rm /etc/test",
        "mv test.txt dest.txt",
        "chmod 777 test.txt",
        "echo hello",
    ]

    times = []
    for command in commands:
        start = time.perf_counter()
        check_system_directory(command)
        end = time.perf_counter()
        elapsed_ms = (end - start) * 1000
        times.append(elapsed_ms)

    avg_time = sum(times) / len(times)
    max_time = max(times)

    print(f"Average time: {avg_time:.2f}ms")
    print(f"Maximum time: {max_time:.2f}ms")

    passed = avg_time < 50  # Target: < 50ms
    print_test("Performance target (< 50ms avg)", passed, f"Avg: {avg_time:.2f}ms")

    return passed


def test_path_resolver():
    """Test PathResolver functionality."""
    print_header("PathResolver Testing")

    resolver = PathResolver()
    all_passed = True

    # Test home directory expansion
    try:
        resolved = resolver.resolve_path("~")
        passed = os.path.exists(resolved)
        print_test("Home directory expansion (~)", passed, f"Resolved to: {resolved}")
        all_passed = all_passed and passed
    except Exception as e:
        print_test("Home directory expansion (~)", False, f"Error: {e}")
        all_passed = False

    # Test current directory
    try:
        resolved = resolver.resolve_path(".")
        passed = os.path.exists(resolved)
        print_test("Current directory (.)", passed, f"Resolved to: {resolved}")
        all_passed = all_passed and passed
    except Exception as e:
        print_test("Current directory (.)", False, f"Error: {e}")
        all_passed = False

    return all_passed


def test_command_parser():
    """Test CommandParser functionality."""
    print_header("CommandParser Testing")

    parser = CommandParser()
    all_passed = True

    tests = [
        ("rm test.txt", ["test.txt"], "Simple rm"),
        ("rm -rf /tmp/test", ["/tmp/test"], "rm with flags"),
        ("mv source.txt dest.txt", ["source.txt", "dest.txt"], "mv command"),
        ("chmod 777 test.txt", ["test.txt"], "chmod command"),
        ("echo hello > output.txt", ["output.txt"], "Output redirection"),
    ]

    for command, expected_paths, description in tests:
        result = parser.parse(command)
        paths = result.get("paths", [])

        # Check if at least one expected path is found
        passed = any(exp in paths for exp in expected_paths) if expected_paths else len(paths) == 0

        details = f"Expected: {expected_paths}, Got: {paths}"
        print_test(description, passed, details)
        all_passed = all_passed and passed

    return all_passed


def main():
    """Run all manual tests."""
    print("\n" + "=" * 70)
    print("  SYSTEM DIRECTORY PROTECTION - MANUAL TEST SUITE")
    print("=" * 70)
    print(f"\nPlatform: {sys.platform}")
    print(f"Python: {sys.version}")
    print()

    results = {}

    # Run all test suites
    results["Platform Detection"] = test_platform_detection()
    results["PathResolver"] = test_path_resolver()
    results["CommandParser"] = test_command_parser()
    results["Windows Protection"] = test_windows_protection()
    results["Linux Protection"] = test_linux_protection()
    results["Edge Cases"] = test_edge_cases()
    results["Performance"] = test_performance()

    # Summary
    print_header("TEST SUMMARY")

    total = len(results)
    passed = sum(1 for v in results.values() if v)

    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")

    print()
    print(f"Total: {passed}/{total} test suites passed")

    if passed == total:
        print("\n🎉 All tests passed! System directory protection is working correctly.")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test suite(s) failed. Please review the results above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
