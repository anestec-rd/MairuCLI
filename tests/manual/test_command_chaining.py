"""
Test command chaining behavior in MairuCLI.

This script verifies that command chaining (;, &&, |) is properly handled.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.interceptor import check_system_directory, check_command
from src.command_parser import CommandParser


def test_command_chaining():
    """Test how command chaining is handled."""
    print("="*70)
    print("COMMAND CHAINING BEHAVIOR TEST")
    print("="*70)

    test_cases = [
        # Semicolon chaining
        ("echo test; rm C:\\Windows\\System32\\test.dll", "Semicolon"),
        ("echo test && rm C:\\Windows\\System32\\test.dll", "Ampersand"),
        ("echo test | rm C:\\Windows\\System32\\test.dll", "Pipe"),

        # Multiple commands
        ("ls; rm C:\\Windows\\System32\\test.dll; echo done", "Multiple semicolons"),

        # Safe command chains
        ("echo hello; echo world", "Safe chain"),
        ("ls && pwd", "Safe ampersand"),
    ]

    for command, description in test_cases:
        print(f"\n{'-'*70}")
        print(f"Test: {description}")
        print(f"Command: {command}")
        print()

        # Check system protection
        sys_level, sys_type, sys_path = check_system_directory(command)
        print(f"System Protection: {sys_level} ({sys_type})")
        if sys_path:
            print(f"  Target: {sys_path}")

        # Check dangerous pattern
        cmd_level, pattern = check_command(command)
        print(f"Pattern Match: {cmd_level} ({pattern})")

        # Parse command
        parser = CommandParser()
        parsed = parser.parse(command)
        print(f"Parsed paths: {parsed['paths']}")

        # Overall result
        blocked = (sys_level in ["critical", "caution"]) or \
                  (cmd_level in ["critical", "caution"])
        print(f"\nResult: {'BLOCKED' if blocked else 'ALLOWED'}")

        # Analysis
        if ";" in command or "&&" in command or "|" in command:
            if not blocked:
                print("⚠️  WARNING: Command chaining detected but not blocked!")
                print("   However, this is expected behavior because:")
                print("   1. MairuCLI processes the ENTIRE command string")
                print("   2. Command chaining operators are part of the string")
                print("   3. The parser extracts paths from the full string")
                print("   4. If dangerous paths are found, command is blocked")
                print()
                print("   The question is: Does the parser extract paths correctly")
                print("   from chained commands?")
            else:
                print("✅ Command chaining with dangerous path correctly blocked")


if __name__ == "__main__":
    test_command_chaining()
