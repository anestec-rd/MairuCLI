"""Demo script to showcase MairuCLI features."""

import sys
from io import StringIO

# Simulate user input
test_commands = [
    "help",
    "pwd",
    "echo Hello from MairuCLI!",
    "rm -rf /",
    "sl",
    "exit"
]

print("=" * 70)
print("MairuCLI Demo Session")
print("=" * 70)
print()

# Import after setting up
from src.display import display_welcome_banner

display_welcome_banner()

print("\n" + "=" * 70)
print("Simulating commands:")
print("=" * 70)

from src.builtins import BuiltinCommands
from src.interceptor import check_command
from src.display import show_warning

for cmd in test_commands:
    print(f"\nmairu> {cmd}")
    print("-" * 70)

    if cmd == "exit":
        print("Exiting...")
        break

    # Check if builtin
    parts = cmd.split()
    if parts and BuiltinCommands.is_builtin(parts[0]):
        BuiltinCommands.execute_builtin(parts[0], parts[1:])
        continue

    # Check if dangerous
    is_dangerous, pattern_name = check_command(cmd)
    if is_dangerous:
        show_warning(pattern_name, cmd)
        continue

    # Safe command (would execute in real shell)
    print(f"[Would execute in system shell: {cmd}]")

print("\n" + "=" * 70)
print("Demo Complete!")
print("=" * 70)
