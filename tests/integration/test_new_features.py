"""Test random variations and achievements."""

import sys
import os

# Add project root to path
sys.path.insert(
    0,
    os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
)

from src.interceptor import check_command
from src.display import show_warning

print("=" * 70)
print("Testing Random Variations and Achievements")
print("=" * 70)

# Test random variations - run same command multiple times
print("\n\n1. Testing Random Warning Variations")
print("-" * 70)
for i in range(3):
    print(f"\n\nAttempt {i+1}: rm -rf /")
    print("-" * 40)
    is_dangerous, pattern_name = check_command("rm -rf /")
    if is_dangerous:
        show_warning(pattern_name, "rm -rf /")

# Test different dangerous commands to trigger achievements
print("\n\n2. Testing Achievement System")
print("-" * 70)

test_commands = [
    "chmod 777 file.txt",
    "DROP DATABASE test",
    "dd if=/dev/zero of=/dev/sda",
    "sl",  # Typo
    "cd..",  # Typo
    "rm -rf /",  # Again
]

for cmd in test_commands:
    print(f"\n\nCommand: {cmd}")
    print("-" * 40)
    is_dangerous, pattern_name = check_command(cmd)
    if is_dangerous:
        show_warning(pattern_name, cmd)

print("\n\n" + "=" * 70)
print("Test Complete!")
print("=" * 70)
