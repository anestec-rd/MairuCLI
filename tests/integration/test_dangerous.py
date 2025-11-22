"""Test script to verify dangerous command detection."""

import sys
import os

# Add project root to path
sys.path.insert(
    0,
    os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
)

from src.interceptor import check_command
from src.display import show_warning

# Test dangerous commands
test_commands = [
    "rm -rf /",
    "chmod 777 test.txt",
    "dd if=/dev/zero of=/dev/sda",
    "DROP DATABASE production",
    "sudo rm -rf $HOME",
    "sl",
    "cd..",
    "ls -la"  # Safe command
]

print("Testing dangerous command detection:\n")
print("=" * 60)

for cmd in test_commands:
    is_dangerous, pattern_name = check_command(cmd)
    print(f"\nCommand: {cmd}")
    print(f"Dangerous: {is_dangerous}")
    print(f"Pattern: {pattern_name}")

    if is_dangerous:
        print("\nWarning display:")
        show_warning(pattern_name, cmd)

    print("-" * 60)
