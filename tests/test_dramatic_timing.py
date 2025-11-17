"""Test dramatic timing for warnings."""

from src.interceptor import check_command
from src.display import show_warning

print("=" * 70)
print("Testing Dramatic Timing")
print("=" * 70)
print()
print("Watch the ASCII art appear line by line...")
print("Notice the pauses between sections...")
print()
input("Press Enter to start...")

# Test with rm -rf /
print("\n\nTesting: rm -rf /")
print("-" * 70)
is_dangerous, pattern_name = check_command("rm -rf /")
if is_dangerous:
    show_warning(pattern_name, "rm -rf /")

print("\n" + "=" * 70)
print("Test Complete!")
print()
print("Did you notice:")
print("1. ASCII art appeared line by line?")
print("2. Pause after the art?")
print("3. Pause before explanation?")
print("4. Pause before achievement?")
print()
print("This creates dramatic impact and prevents achievement")
print("from pushing the important warning off screen!")
