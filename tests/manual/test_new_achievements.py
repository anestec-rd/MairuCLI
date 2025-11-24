"""
Manual test script for new achievements.

Test the newly added achievements:
- Unstoppable (20 repeats)
- Creator (touch command)
- Architect (mkdir command)
- Detective (grep/find command)
"""

import os
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.display.statistics import Statistics
from src.display.achievements import AchievementTracker


def test_creator_achievement():
    """Test Creator achievement (touch command)."""
    print("\n" + "=" * 80)
    print("TEST: Creator Achievement")
    print("=" * 80)

    stats = Statistics()
    tracker = AchievementTracker(stats)

    print("Simulating 'touch' command usage...")
    stats.track_safe_command("touch")
    tracker.check_achievements()

    print("\nUnlocked achievements:", tracker.get_unlocked_achievement_names())
    print("=" * 80)


def test_architect_achievement():
    """Test Architect achievement (mkdir command)."""
    print("\n" + "=" * 80)
    print("TEST: Architect Achievement")
    print("=" * 80)

    stats = Statistics()
    tracker = AchievementTracker(stats)

    print("Simulating 'mkdir' command usage...")
    stats.track_safe_command("mkdir")
    tracker.check_achievements()

    print("\nUnlocked achievements:", tracker.get_unlocked_achievement_names())
    print("=" * 80)


def test_detective_achievement():
    """Test Detective achievement (grep/find command)."""
    print("\n" + "=" * 80)
    print("TEST: Detective Achievement")
    print("=" * 80)

    stats = Statistics()
    tracker = AchievementTracker(stats)

    print("Simulating 'grep' command usage...")
    stats.track_safe_command("grep")
    tracker.check_achievements()

    print("\nUnlocked achievements:", tracker.get_unlocked_achievement_names())
    print("=" * 80)


def test_unstoppable_achievement():
    """Test Unstoppable achievement (20 repeats)."""
    print("\n" + "=" * 80)
    print("TEST: Unstoppable Achievement")
    print("=" * 80)

    stats = Statistics()
    tracker = AchievementTracker(stats)

    print("Simulating 20 repeats of the same command...")
    for i in range(20):
        stats.increment_dangerous_blocked()
        count = stats.track_repeat_command("rm -rf /")
        if i == 2:  # Stubborn at 3
            print(f"\nRepeat #{count}: Checking for Stubborn...")
            tracker.check_achievements()
        elif i == 19:  # Unstoppable at 20
            print(f"\nRepeat #{count}: Checking for Unstoppable...")
            tracker.check_achievements()

    print("\nUnlocked achievements:", tracker.get_unlocked_achievement_names())
    print("=" * 80)


def main():
    """Run all achievement tests."""
    print("\n🏆 New Achievements Test Suite 🏆\n")

    input("Press Enter to test Creator achievement...")
    test_creator_achievement()

    input("\nPress Enter to test Architect achievement...")
    test_architect_achievement()

    input("\nPress Enter to test Detective achievement...")
    test_detective_achievement()

    input("\nPress Enter to test Unstoppable achievement...")
    test_unstoppable_achievement()

    print("\n" + "=" * 80)
    print("All tests complete!")
    print("\nNew achievements added:")
    print("  🏆 Creator - Use 'touch' command")
    print("  🏆 Architect - Use 'mkdir' command")
    print("  🏆 Detective - Use 'grep' or 'find' command")
    print("  🏆 Unstoppable - Repeat same command 20 times")
    print("=" * 80)


if __name__ == "__main__":
    main()
