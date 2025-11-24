"""
Manual test script for ASCII art display timing.

Run this to test different ASCII art display speeds.
"""

import os
import sys
import time

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))


def display_art_with_delay(art: str, delay: float, color_code: str = "\033[38;5;208m"):
    """Display ASCII art line by line with specified delay."""
    reset = "\033[0m"
    lines = art.split('\n')
    for line in lines:
        print(f"{color_code}{line}{reset}")
        time.sleep(delay)


def test_ascii_timing(name: str, delay: float, description: str):
    """Test ASCII art timing."""
    print("\n" + "=" * 80)
    print(f"TIMING: {name}")
    print(f"Description: {description}")
    print(f"Delay per line: {delay}s ({int(delay * 1000)}ms)")
    print("=" * 80)
    print()

    # Sample ASCII art (fired.txt style)
    art = """
    .-""""""-.
  .'          '.
 /   O      O   \\
:                :
|                |
:    .-----.    :
 \\  '       '  /
  '.          .'
    '-......-'
"""

    print("Displaying ASCII art...")
    display_art_with_delay(art, delay)
    print()
    print("=" * 80)


def main():
    """Test different ASCII art display speeds."""
    print("\n🎃 ASCII Art Display Speed Test 🎃\n")
    print("Watch how the ASCII art appears line by line.")

    # Current speed
    input("\nPress Enter to test CURRENT speed (0.05s per line)...")
    test_ascii_timing(
        "Current (0.05s)",
        delay=0.05,
        description="Current production speed - 10 lines in 0.5s"
    )

    # Slightly slower
    input("\nPress Enter to test SLIGHTLY SLOWER (0.08s per line)...")
    test_ascii_timing(
        "Slightly Slower (0.08s)",
        delay=0.08,
        description="More dramatic - 10 lines in 0.8s"
    )

    # Much slower
    input("\nPress Enter to test MUCH SLOWER (0.1s per line)...")
    test_ascii_timing(
        "Much Slower (0.1s)",
        delay=0.1,
        description="Very dramatic - 10 lines in 1.0s"
    )

    # Faster
    input("\nPress Enter to test FASTER (0.03s per line)...")
    test_ascii_timing(
        "Faster (0.03s)",
        delay=0.03,
        description="Snappy - 10 lines in 0.3s"
    )

    # Instant (for comparison)
    input("\nPress Enter to test INSTANT (0s - no delay)...")
    test_ascii_timing(
        "Instant (0s)",
        delay=0,
        description="All at once - no dramatic effect"
    )

    print("\n" + "=" * 80)
    print("RECOMMENDATION:")
    print()
    print("Current (0.05s) - Good balance, not too slow")
    print("Slightly Slower (0.08s) - More dramatic, still comfortable")
    print("Much Slower (0.1s) - Very dramatic, might be too slow")
    print("Faster (0.03s) - Quick, less dramatic")
    print("Instant (0s) - No effect, just shows the art")
    print()
    print("Consider:")
    print("- ASCII art is the first thing users see")
    print("- Too slow = annoying, too fast = no impact")
    print("- 0.05-0.08s is the sweet spot for most users")
    print("=" * 80)


if __name__ == "__main__":
    main()
