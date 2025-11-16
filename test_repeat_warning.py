"""Test the 'I told you so' feature."""

from src.interceptor import check_command
from src.display import show_warning

# Test the same dangerous command multiple times
dangerous_cmd = "rm -rf /"

print("Testing repeat warning feature:\n")
print("=" * 70)

for i in range(1, 6):
    print(f"\n\nAttempt #{i}: {dangerous_cmd}")
    print("-" * 70)

    is_dangerous, pattern_name = check_command(dangerous_cmd)
    if is_dangerous:
        show_warning(pattern_name, dangerous_cmd)

print("\n" + "=" * 70)
print("Test complete!")
