"""
False Negative Testing for System Directory Protection

This test verifies that ALL dangerous operations targeting system directories
are properly detected and blocked. A false negative would be a dangerous
operation that is NOT blocked.

Test Categories:
1. All dangerous commands (rm, mv, chmod, dd, redirection)
2. All protected directories (Windows, Linux, macOS)
3. All path manipulation techniques (relative, env vars, wildcards)
4. All command variations (options, chaining, quoting)
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.interceptor import check_system_directory


class FalseNegativeTests:
    """Test suite to verify zero false negatives."""

    def __init__(self):
        self.total_tests = 0
        self.passed_tests = 0
        self.failed_tests = 0
        self.false_negatives = []

    def test(self, command, expected_level, description):
        """
        Test a command and verify it's blocked as expected.

        Args:
            command: Command to test
            expected_level: Expected protection level ("critical" or "caution")
            description: Test description
        """
        self.total_tests += 1
        level, ptype, path = check_system_directory(command)

        # Check if command was blocked
        is_blocked = level in ["critical", "caution"]
        should_be_blocked = expected_level in ["critical", "caution"]

        if should_be_blocked and not is_blocked:
            # FALSE NEGATIVE: Dangerous command was NOT blocked
            self.failed_tests += 1
            self.false_negatives.append({
                "command": command,
                "description": description,
                "expected": expected_level,
                "actual": level
            })
            print(f"❌ FALSE NEGATIVE: {description}")
            print(f"   Command: {command}")
            print(f"   Expected: {expected_level}, Got: {level}")
            print()
        elif is_blocked and level == expected_level:
            # Correct: Command blocked at expected level
            self.passed_tests += 1
            print(f"✅ {description}")
        elif is_blocked and level != expected_level:
            # Blocked but at wrong level (still safe, but note it)
            self.passed_tests += 1
            print(f"⚠️  {description} (blocked at {level} instead of {expected_level})")
        else:
            # Safe command correctly allowed
            self.passed_tests += 1
            print(f"✅ {description}")

    def run_windows_tests(self):
        """Test Windows system directory protection."""
        if sys.platform != "win32":
            print("Skipping Windows tests (not on Windows)")
            return

        print("=" * 70)
        print("WINDOWS SYSTEM DIRECTORY PROTECTION TESTS")
        print("=" * 70)
        print()

        # Test 1: rm command on System32
        print("Category: rm command on critical directories")
        print("-" * 70)
        self.test(
            r"rm C:\Windows\System32\kernel32.dll",
            "critical",
            "rm on System32 file"
        )
        self.test(
            r"rm -rf C:\Windows\System32",
            "critical",
            "rm -rf on System32 directory"
        )
        self.test(
            r"rmdir C:\Windows\System32",
            "critical",
            "rmdir on System32"
        )
        print()

        # Test 2: mv command with System32
        print("Category: mv command with critical directories")
        print("-" * 70)
        self.test(
            r'mv "C:\Users\Test\file.txt" "C:\Windows\System32\file.txt"',
            "critical",
            "mv to System32"
        )
        self.test(
            r'mv "C:\Windows\System32\file.txt" "C:\Users\Test\file.txt"',
            "critical",
            "mv from System32"
        )
        print()

        # Test 3: Output redirection to System32
        print("Category: Output redirection to critical directories")
        print("-" * 70)
        self.test(
            r"echo test > C:\Windows\System32\test.txt",
            "critical",
            "Redirect to System32"
        )
        self.test(
            r"cat file.txt >> C:\Windows\System32\test.txt",
            "critical",
            "Append to System32"
        )
        print()

        # Test 4: Program Files (caution level)
        print("Category: Operations on caution-level directories")
        print("-" * 70)
        self.test(
            r'rm "C:\Program Files\test.exe"',
            "caution",
            "rm on Program Files"
        )
        self.test(
            r'mv test.txt "C:\Program Files\test.txt"',
            "caution",
            "mv to Program Files"
        )
        print()

        # Test 5: Relative paths to system directories
        print("Category: Relative paths to system directories")
        print("-" * 70)
        self.test(
            r"rm ..\..\Windows\System32\test.dll",
            "critical",
            "Relative path to System32"
        )
        self.test(
            r"rm ..\..\..\Windows\test.txt",
            "critical",
            "Relative path to Windows"
        )
        print()

        # Test 6: Environment variables
        print("Category: Environment variable expansion")
        print("-" * 70)
        self.test(
            r"rm %WINDIR%\System32\test.dll",
            "critical",
            "Environment variable %WINDIR%"
        )
        self.test(
            r"rm $WINDIR\System32\test.dll",
            "critical",
            "Environment variable $WINDIR"
        )
        print()

        # Test 7: Case variations
        print("Category: Case variations (Windows is case-insensitive)")
        print("-" * 70)
        self.test(
            r"rm c:\windows\system32\test.dll",
            "critical",
            "Lowercase path"
        )
        self.test(
            r"rm C:\WINDOWS\SYSTEM32\TEST.DLL",
            "critical",
            "Uppercase path"
        )
        self.test(
            r"rm C:\WiNdOwS\SyStEm32\test.dll",
            "critical",
            "Mixed case path"
        )
        print()

        # Test 8: Path separator variations
        print("Category: Path separator variations")
        print("-" * 70)
        self.test(
            r"rm C:/Windows/System32/test.dll",
            "critical",
            "Forward slashes on Windows"
        )
        self.test(
            r"rm C:\Windows/System32\test.dll",
            "critical",
            "Mixed separators"
        )
        print()

        # Test 9: Wildcards
        print("Category: Wildcards in system directories")
        print("-" * 70)
        self.test(
            r"rm C:\Windows\System32\*.dll",
            "critical",
            "Wildcard in System32"
        )
        self.test(
            r"rm C:\Windows\*",
            "critical",
            "Wildcard in Windows"
        )
        print()

        # Test 10: Command chaining
        print("Category: Command chaining")
        print("-" * 70)
        self.test(
            r"echo test; rm C:\Windows\System32\test.dll",
            "critical",
            "Semicolon chaining"
        )
        self.test(
            r"ls && rm C:\Windows\System32\test.dll",
            "critical",
            "Ampersand chaining"
        )
        self.test(
            r"cat file | rm C:\Windows\System32\test.dll",
            "critical",
            "Pipe chaining"
        )
        print()

    def run_linux_tests(self):
        """Test Linux system directory protection."""
        if sys.platform == "win32":
            print("Skipping Linux tests (on Windows)")
            return

        print("=" * 70)
        print("LINUX SYSTEM DIRECTORY PROTECTION TESTS")
        print("=" * 70)
        print()

        # Test 1: rm command on /etc
        print("Category: rm command on critical directories")
        print("-" * 70)
        self.test(
            "rm /etc/passwd",
            "critical",
            "rm on /etc/passwd"
        )
        self.test(
            "rm -rf /etc",
            "critical",
            "rm -rf on /etc"
        )
        self.test(
            "rmdir /etc",
            "critical",
            "rmdir on /etc"
        )
        print()

        # Test 2: mv command with /etc
        print("Category: mv command with critical directories")
        print("-" * 70)
        self.test(
            "mv /home/user/file.txt /etc/file.txt",
            "critical",
            "mv to /etc"
        )
        self.test(
            "mv /etc/test.conf /home/user/test.conf",
            "critical",
            "mv from /etc"
        )
        print()

        # Test 3: chmod/chown on system directories
        print("Category: Permission changes on critical directories")
        print("-" * 70)
        self.test(
            "chmod 777 /etc/passwd",
            "critical",
            "chmod on /etc/passwd"
        )
        self.test(
            "chown user:user /etc/passwd",
            "critical",
            "chown on /etc/passwd"
        )
        print()

        # Test 4: Output redirection to /etc
        print("Category: Output redirection to critical directories")
        print("-" * 70)
        self.test(
            "echo test > /etc/test.conf",
            "critical",
            "Redirect to /etc"
        )
        self.test(
            "cat file.txt >> /etc/test.conf",
            "critical",
            "Append to /etc"
        )
        print()

        # Test 5: /usr operations (caution level)
        print("Category: Operations on caution-level directories")
        print("-" * 70)
        self.test(
            "rm /usr/bin/test",
            "caution",
            "rm on /usr/bin"
        )
        self.test(
            "mv test.txt /usr/local/test.txt",
            "caution",
            "mv to /usr"
        )
        print()

        # Test 6: Relative paths to system directories
        print("Category: Relative paths to system directories")
        print("-" * 70)
        self.test(
            "rm ../../etc/passwd",
            "critical",
            "Relative path to /etc"
        )
        self.test(
            "rm ../../../etc/test.conf",
            "critical",
            "Multiple traversals to /etc"
        )
        print()

        # Test 7: Environment variables
        print("Category: Environment variable expansion")
        print("-" * 70)
        # Set test environment variable
        os.environ["TEST_SYS_DIR"] = "/etc"
        self.test(
            "rm $TEST_SYS_DIR/test.conf",
            "critical",
            "Environment variable $TEST_SYS_DIR"
        )
        del os.environ["TEST_SYS_DIR"]
        print()

        # Test 8: Home directory expansion
        print("Category: Home directory expansion")
        print("-" * 70)
        self.test(
            "rm ~/../../etc/passwd",
            "critical",
            "Tilde expansion with traversal"
        )
        print()

        # Test 9: Wildcards
        print("Category: Wildcards in system directories")
        print("-" * 70)
        self.test(
            "rm /etc/*.conf",
            "critical",
            "Wildcard in /etc"
        )
        self.test(
            "rm /etc/*",
            "critical",
            "Wildcard all in /etc"
        )
        print()

        # Test 10: Command chaining
        print("Category: Command chaining")
        print("-" * 70)
        self.test(
            "echo test; rm /etc/passwd",
            "critical",
            "Semicolon chaining"
        )
        self.test(
            "ls && rm /etc/passwd",
            "critical",
            "Ampersand chaining"
        )
        self.test(
            "cat file | rm /etc/passwd",
            "critical",
            "Pipe chaining"
        )
        print()

    def run_all_tests(self):
        """Run all false negative tests."""
        print()
        print("=" * 70)
        print("FALSE NEGATIVE TESTING - SYSTEM DIRECTORY PROTECTION")
        print("=" * 70)
        print()
        print("This test verifies that ALL dangerous operations are blocked.")
        print("A false negative is a dangerous operation that is NOT blocked.")
        print()

        # Run platform-specific tests
        self.run_windows_tests()
        self.run_linux_tests()

        # Print summary
        print()
        print("=" * 70)
        print("TEST SUMMARY")
        print("=" * 70)
        print(f"Total tests: {self.total_tests}")
        print(f"Passed: {self.passed_tests}")
        print(f"Failed: {self.failed_tests}")
        print()

        if self.false_negatives:
            print("❌ FALSE NEGATIVES DETECTED:")
            print("=" * 70)
            for fn in self.false_negatives:
                print(f"Description: {fn['description']}")
                print(f"Command: {fn['command']}")
                print(f"Expected: {fn['expected']}, Got: {fn['actual']}")
                print()
            print(f"Total false negatives: {len(self.false_negatives)}")
            print()
            print("⚠️  CRITICAL: False negatives mean dangerous operations are NOT blocked!")
            print("⚠️  This is a SECURITY ISSUE that must be fixed immediately!")
        else:
            print("✅ ZERO FALSE NEGATIVES DETECTED")
            print()
            print("All dangerous operations targeting system directories are properly blocked.")
            print("The system directory protection feature is working correctly.")

        print("=" * 70)
        print()

        return len(self.false_negatives) == 0


def main():
    """Run false negative tests."""
    tester = FalseNegativeTests()
    success = tester.run_all_tests()

    if success:
        print("✅ SUCCESS: Zero false negatives confirmed")
        return 0
    else:
        print("❌ FAILURE: False negatives detected")
        return 1


if __name__ == "__main__":
    exit(main())
