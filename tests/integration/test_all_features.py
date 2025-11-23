"""Test all new features together."""

import sys
import os

# Add project root to path
sys.path.insert(
    0,
    os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
)

from src.builtins import BuiltinCommands
from src.interceptor import check_command
from src.display import show_warning

print("=" * 70)
print("MairuCLI Feature Demo")
print("=" * 70)

# Test various dangerous commands
test_commands = [
    "rm -rf /",
    "chmod 777 secret.txt",
    "sl",
    "rm -rf /",  # Repeat!
    "cd..",
    "DROP DATABASE production",
    "rm -rf /",  # Repeat again!
]

for cmd in test_commands:
    print(f"\n\nmairu> {cmd}")
    print("-" * 70)

    is_dangerous, pattern_name = check_command(cmd)
    if is_dangerous:
        show_warning(pattern_name, cmd)

# Show statistics
print("\n\nmairu> stats")
print("-" * 70)
BuiltinCommands.execute_builtin('stats', [])

print("\n" + "=" * 70)
print("Demo Complete!")
print("=" * 70)
