"""
Manual test script for timing adjustments.

Run this to test different timing values and choose the best dramatic effect.
"""

import os
import sys
import time

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))


def test_timing_scenario(name: str, short: float, medium: float, description: str):
    """Test a timing scenario."""
    print("\n" + "=" * 80)
    print(f"SCENARIO: {name}")
    print(f"Description: {description}")
    print(f"TIMING_PAUSE_SHORT = {short}s")
    print(f"TIMING_PAUSE_MEDIUM = {medium}s")
    print("=" * 80)
    print()

    # Simulate warning display flow
    print("🔥 DANGER DETECTED! 🔥")
    print("(Displaying ASCII art...)")
    time.sleep(short)  # After art
    print()

    print("💀 CRITICAL WARNING 💀")
    print("(This is the title)")
    time.sleep(medium)  # Before explanation
    print()

    print("📖 Explanation:")
    print("This command would delete everything on your system.")
    print()

    print("💡 Safe alternative:")
    print("  - Use 'rm -i' for confirmation")
    time.sleep(short)  # Before achievement
    print()

    print("🏆 ACHIEVEMENT UNLOCKED!")
    print("First Blood - Blocked your first dangerous command!")
    print()

    print("=" * 80)
    print("How did this timing feel?")
    print("  - Too fast? (not dramatic enough)")
    print("  - Just right? (good dramatic effect)")
    print("  - Too slow? (annoying/boring)")
    print("=" * 80)


def main():
    """Test different timing scenarios."""
    print("\n🎃 MairuCLI Timing Adjustment Test 🎃\n")
    print("Testing different timing values for dramatic effect...")
    print("Watch the pauses between sections carefully.")

    # Current values (Day 7)
    input("\nPress Enter to test CURRENT timing (Day 7)...")
    test_timing_scenario(
        "Current (Day 7)",
        short=0.3,
        medium=0.5,
        description="Current production values"
    )

    # Option 1: Slightly slower (more dramatic)
    input("\nPress Enter to test OPTION 1 (Slightly Slower)...")
    test_timing_scenario(
        "Option 1: Slightly Slower",
        short=0.4,
        medium=0.7,
        description="Increase pauses by ~40% for more drama"
    )

    # Option 2: Much slower (very dramatic)
    input("\nPress Enter to test OPTION 2 (Much Slower)...")
    test_timing_scenario(
        "Option 2: Much Slower",
        short=0.5,
        medium=1.0,
        description="Double the drama - might be too slow"
    )

    # Option 3: Faster (snappier)
    input("\nPress Enter to test OPTION 3 (Faster)...")
    test_timing_scenario(
        "Option 3: Faster",
        short=0.2,
        medium=0.3,
        description="Reduce pauses for snappier feel"
    )

    print("\n" + "=" * 80)
    print("RECOMMENDATION:")
    print()
    print("Based on testing, which timing felt best?")
    print()
    print("Current (0.3s / 0.5s) - Good balance")
    print("Option 1 (0.4s / 0.7s) - More dramatic, still comfortable")
    print("Option 2 (0.5s / 1.0s) - Very dramatic, might be too slow")
    print("Option 3 (0.2s / 0.3s) - Snappy, less dramatic")
    print()
    print("Consider:")
    print("- Demo presentation: Slightly slower helps audience follow")
    print("- Daily use: Current or faster is better")
    print("- Educational tool: Medium pace helps learning")
    print("=" * 80)


if __name__ == "__main__":
    main()
