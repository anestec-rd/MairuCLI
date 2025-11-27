"""
Comprehensive bypass method testing for system directory protection.

This script tests various techniques that attackers might use to bypass
the protection mechanisms. Each test should FAIL (i.e., the protection
should catch the attempt).

Run this script to verify no bypass methods exist.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.interceptor import check_system_directory, check_command
from src.command_parser import CommandParser
from src.path_resolver import PathResolver


class BypassTester:
    """Test various bypass techniques against system protection."""

    def __init__(self):
        self.tests_run = 0
        self.tests_passed = 0
        self.tests_failed = 0
        self.vulnerabilities = []

    def test(self, name: str, command: str, should_block: bool = True):
        """
        Test a potential bypass method.

        Args:
            name: Test name/description
            command: Command to test
            should_block: True if command should be blocked, False if allowed
        """
        self.tests_run += 1
        print(f"\n{'='*70}")
        print(f"Test {self.tests_run}: {name}")
        print(f"Command: {command}")
        print(f"Expected: {'BLOCKED' if should_block else 'ALLOWED'}")

        # Check system directory protection
        level, ptype, path = check_system_directory(command)
        sys_blocked = level in ["critical", "caution"]

        # Check dangerous pattern
        cmd_level, pattern = check_command(command)
        pattern_blocked = cmd_level in ["critical", "caution"]

        # Overall result
        blocked = sys_blocked or pattern_blocked

        print(f"System Protection: {level} ({ptype})")
        print(f"Pattern Match: {cmd_level} ({pattern})")
        print(f"Result: {'BLOCKED' if blocked else 'ALLOWED'}")

        # Verify result matches expectation
        if blocked == should_block:
            print("✅ PASS - Protection working as expected")
            self.tests_passed += 1
        else:
            print("❌ FAIL - VULNERABILITY DETECTED!")
            self.tests_failed += 1
            self.vulnerabilities.append({
                'name': name,
                'command': command,
                'expected': 'BLOCKED' if should_block else 'ALLOWED',
                'actual': 'BLOCKED' if blocked else 'ALLOWED'
            })

    def print_summary(self):
        """Print test summary."""
        print(f"\n{'='*70}")
        print("BYPASS METHOD TEST SUMMARY")
        print(f"{'='*70}")
        print(f"Total Tests: {self.tests_run}")
        print(f"Passed: {self.tests_passed}")
        print(f"Failed: {self.tests_failed}")

        if self.vulnerabilities:
            print(f"\n❌ {len(self.vulnerabilities)} VULNERABILITIES FOUND:")
            for vuln in self.vulnerabilities:
                print(f"\n  - {vuln['name']}")
                print(f"    Command: {vuln['command']}")
                print(f"    Expected: {vuln['expected']}, Got: {vuln['actual']}")
        else:
            print("\n✅ NO VULNERABILITIES FOUND - All bypass attempts blocked!")

        return len(self.vulnerabilities) == 0


def main():
    """Run all bypass tests."""
    tester = BypassTester()

    print("="*70)
    print("SYSTEM DIRECTORY PROTECTION - BYPASS METHOD TESTING")
    print("="*70)
    print("\nTesting various techniques to bypass protection...")
    print("All tests should PASS (i.e., bypass attempts should be blocked)")

    # ========================================================================
    # Category 1: Path Traversal Attacks
    # ========================================================================
    print("\n" + "="*70)
    print("CATEGORY 1: PATH TRAVERSAL ATTACKS")
    print("="*70)

    # Windows path traversal
    if sys.platform == 'win32':
        tester.test(
            "Windows - Relative path traversal",
            "rm ../../Windows/System32/test.dll"
        )
        tester.test(
            "Windows - Parent directory traversal",
            "rm C:\\Users\\..\\Windows\\System32\\test.dll"
        )
        tester.test(
            "Windows - Multiple traversals",
            "rm C:\\Users\\Test\\..\\..\\Windows\\System32\\test.dll"
        )
        tester.test(
            "Windows - Current directory traversal",
            "rm .\\..\\..\\Windows\\System32\\test.dll"
        )

    # Linux path traversal
    else:
        tester.test(
            "Linux - Relative path traversal",
            "rm ../../etc/passwd"
        )
        tester.test(
            "Linux - Parent directory traversal",
            "rm /home/../etc/passwd"
        )
        tester.test(
            "Linux - Multiple traversals",
            "rm /home/user/../../etc/passwd"
        )
        tester.test(
            "Linux - Current directory traversal",
            "rm ./../../etc/passwd"
        )

    # ========================================================================
    # Category 2: Environment Variable Expansion
    # ========================================================================
    print("\n" + "="*70)
    print("CATEGORY 2: ENVIRONMENT VARIABLE EXPANSION")
    print("="*70)

    if sys.platform == 'win32':
        tester.test(
            "Windows - %WINDIR% expansion",
            "rm %WINDIR%\\System32\\test.dll"
        )
        tester.test(
            "Windows - %SYSTEMROOT% expansion",
            "rm %SYSTEMROOT%\\System32\\test.dll"
        )
        tester.test(
            "Windows - $WINDIR expansion (PowerShell style)",
            "rm $WINDIR\\System32\\test.dll"
        )
    else:
        tester.test(
            "Linux - $HOME expansion",
            "rm $HOME/../../../etc/passwd"
        )
        tester.test(
            "Linux - ${HOME} expansion",
            "rm ${HOME}/../../../etc/passwd"
        )

    # ========================================================================
    # Category 3: Case Variations (Windows/macOS)
    # ========================================================================
    print("\n" + "="*70)
    print("CATEGORY 3: CASE VARIATIONS")
    print("="*70)

    if sys.platform == 'win32':
        tester.test(
            "Windows - Lowercase system32",
            "rm c:\\windows\\system32\\test.dll"
        )
        tester.test(
            "Windows - Mixed case SYSTEM32",
            "rm C:\\Windows\\SYSTEM32\\test.dll"
        )
        tester.test(
            "Windows - All uppercase",
            "rm C:\\WINDOWS\\SYSTEM32\\TEST.DLL"
        )

    # ========================================================================
    # Category 4: Path Separator Variations
    # ========================================================================
    print("\n" + "="*70)
    print("CATEGORY 4: PATH SEPARATOR VARIATIONS")
    print("="*70)

    if sys.platform == 'win32':
        tester.test(
            "Windows - Forward slashes",
            "rm C:/Windows/System32/test.dll"
        )
        tester.test(
            "Windows - Mixed separators",
            "rm C:\\Windows/System32\\test.dll"
        )
        tester.test(
            "Windows - Double backslashes",
            "rm C:\\\\Windows\\\\System32\\\\test.dll"
        )

    # ========================================================================
    # Category 5: Wildcard Attacks
    # ========================================================================
    print("\n" + "="*70)
    print("CATEGORY 5: WILDCARD ATTACKS")
    print("="*70)

    if sys.platform == 'win32':
        tester.test(
            "Windows - Wildcard in System32",
            "rm C:\\Windows\\System32\\*.dll"
        )
        tester.test(
            "Windows - Wildcard in Windows",
            "rm C:\\Windows\\*"
        )
    else:
        tester.test(
            "Linux - Wildcard in /etc",
            "rm /etc/*.conf"
        )
        tester.test(
            "Linux - Wildcard in /bin",
            "rm /bin/*"
        )

    # ========================================================================
    # Category 6: Command Variations
    # ========================================================================
    print("\n" + "="*70)
    print("CATEGORY 6: COMMAND VARIATIONS")
    print("="*70)

    if sys.platform == 'win32':
        tester.test(
            "Windows - mv command",
            "mv C:\\Windows\\System32\\test.dll C:\\Temp\\"
        )
        tester.test(
            "Windows - chmod command",
            "chmod 000 C:\\Windows\\System32\\test.dll"
        )
        tester.test(
            "Windows - cp command",
            "cp C:\\Windows\\System32\\test.dll C:\\Temp\\"
        )
    else:
        tester.test(
            "Linux - mv command",
            "mv /etc/passwd /tmp/"
        )
        tester.test(
            "Linux - chmod command",
            "chmod 000 /etc/passwd"
        )
        tester.test(
            "Linux - cp command",
            "cp /etc/passwd /tmp/"
        )

    # ========================================================================
    # Category 7: Output Redirection
    # ========================================================================
    print("\n" + "="*70)
    print("CATEGORY 7: OUTPUT REDIRECTION")
    print("="*70)

    if sys.platform == 'win32':
        tester.test(
            "Windows - Redirect to System32",
            "echo test > C:\\Windows\\System32\\test.txt"
        )
        tester.test(
            "Windows - Append to System32",
            "echo test >> C:\\Windows\\System32\\test.txt"
        )
    else:
        tester.test(
            "Linux - Redirect to /etc",
            "echo test > /etc/test.conf"
        )
        tester.test(
            "Linux - Append to /etc/passwd",
            "echo test >> /etc/passwd"
        )

    # ========================================================================
    # Category 8: Quoted Paths
    # ========================================================================
    print("\n" + "="*70)
    print("CATEGORY 8: QUOTED PATHS")
    print("="*70)

    if sys.platform == 'win32':
        tester.test(
            "Windows - Double quoted path",
            'rm "C:\\Windows\\System32\\test.dll"'
        )
        tester.test(
            "Windows - Single quoted path",
            "rm 'C:\\Windows\\System32\\test.dll'"
        )
    else:
        tester.test(
            "Linux - Double quoted path",
            'rm "/etc/passwd"'
        )
        tester.test(
            "Linux - Single quoted path",
            "rm '/etc/passwd'"
        )

    # ========================================================================
    # Category 9: Home Directory Expansion
    # ========================================================================
    print("\n" + "="*70)
    print("CATEGORY 9: HOME DIRECTORY EXPANSION")
    print("="*70)

    if sys.platform != 'win32':
        tester.test(
            "Linux - Tilde expansion to /etc",
            "rm ~/../../etc/passwd"
        )
        tester.test(
            "Linux - Tilde expansion to /bin",
            "rm ~/../../bin/ls"
        )

    # ========================================================================
    # Category 10: Edge Cases
    # ========================================================================
    print("\n" + "="*70)
    print("CATEGORY 10: EDGE CASES")
    print("="*70)

    if sys.platform == 'win32':
        tester.test(
            "Windows - Trailing slash",
            "rm C:\\Windows\\System32\\"
        )
        tester.test(
            "Windows - No drive letter",
            "rm \\Windows\\System32\\test.dll"
        )
    else:
        tester.test(
            "Linux - Trailing slash",
            "rm /etc/"
        )
        tester.test(
            "Linux - Double slash",
            "rm //etc/passwd"
        )

    # ========================================================================
    # Category 11: Safe Commands (Should NOT be blocked)
    # ========================================================================
    print("\n" + "="*70)
    print("CATEGORY 11: SAFE COMMANDS (Should NOT be blocked)")
    print("="*70)

    if sys.platform == 'win32':
        tester.test(
            "Windows - User directory (safe)",
            "rm C:\\Users\\Test\\file.txt",
            should_block=False
        )
        tester.test(
            "Windows - Temp directory (safe)",
            "rm C:\\Temp\\file.txt",
            should_block=False
        )
    else:
        tester.test(
            "Linux - Home directory (safe)",
            "rm /home/user/file.txt",
            should_block=False
        )
        tester.test(
            "Linux - Tmp directory (safe)",
            "rm /tmp/file.txt",
            should_block=False
        )

    # ========================================================================
    # Category 12: Command Injection Attempts
    # ========================================================================
    print("\n" + "="*70)
    print("CATEGORY 12: COMMAND INJECTION ATTEMPTS")
    print("="*70)

    if sys.platform == 'win32':
        tester.test(
            "Windows - Semicolon injection",
            "echo test; rm C:\\Windows\\System32\\test.dll"
        )
        tester.test(
            "Windows - Ampersand injection",
            "echo test && rm C:\\Windows\\System32\\test.dll"
        )
        tester.test(
            "Windows - Pipe injection",
            "echo test | rm C:\\Windows\\System32\\test.dll"
        )
    else:
        tester.test(
            "Linux - Semicolon injection",
            "echo test; rm /etc/passwd"
        )
        tester.test(
            "Linux - Ampersand injection",
            "echo test && rm /etc/passwd"
        )
        tester.test(
            "Linux - Pipe injection",
            "echo test | rm /etc/passwd"
        )

    # Print summary
    success = tester.print_summary()

    # Return exit code
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
