"""
Unit tests for src/display/achievements.py
"""

import pytest
from src.display.achievements import AchievementTracker, ACHIEVEMENT_METADATA
from src.display.statistics import Statistics


class TestAchievementTracker:
    """Test suite for AchievementTracker."""

    def test_first_blood_achievement(self):
        """Test First Blood achievement unlocks on first block."""
        stats = Statistics()
        tracker = AchievementTracker(stats)

        # No achievements initially
        assert len(tracker.get_unlocked_achievement_names()) == 0

        # Block first dangerous command
        stats.increment_dangerous_blocked()
        tracker.check_achievements()

        # First Blood should unlock
        unlocked = tracker.get_unlocked_achievement_names()
        assert "First Blood" in unlocked

    def test_creator_achievement(self):
        """Test Creator achievement unlocks when using touch."""
        stats = Statistics()
        tracker = AchievementTracker(stats)

        # Use touch command
        stats.track_safe_command("touch")
        tracker.check_achievements()

        # Creator should unlock
        unlocked = tracker.get_unlocked_achievement_names()
        assert "Creator" in unlocked

    def test_architect_achievement(self):
        """Test Architect achievement unlocks when using mkdir."""
        stats = Statistics()
        tracker = AchievementTracker(stats)

        # Use mkdir command
        stats.track_safe_command("mkdir")
        tracker.check_achievements()

        # Architect should unlock
        unlocked = tracker.get_unlocked_achievement_names()
        assert "Architect" in unlocked

    def test_detective_achievement_with_grep(self):
        """Test Detective achievement unlocks when using grep."""
        stats = Statistics()
        tracker = AchievementTracker(stats)

        # Use grep command
        stats.track_safe_command("grep")
        tracker.check_achievements()

        # Detective should unlock
        unlocked = tracker.get_unlocked_achievement_names()
        assert "Detective" in unlocked

    def test_detective_achievement_with_find(self):
        """Test Detective achievement unlocks when using find."""
        stats = Statistics()
        tracker = AchievementTracker(stats)

        # Use find command
        stats.track_safe_command("find")
        tracker.check_achievements()

        # Detective should unlock
        unlocked = tracker.get_unlocked_achievement_names()
        assert "Detective" in unlocked

    def test_unstoppable_achievement(self):
        """Test Unstoppable achievement unlocks after 20 repeats."""
        stats = Statistics()
        tracker = AchievementTracker(stats)

        # Repeat command 20 times
        for _ in range(20):
            stats.increment_dangerous_blocked()
            stats.track_repeat_command("rm -rf /")

        tracker.check_achievements()

        # Unstoppable should unlock
        unlocked = tracker.get_unlocked_achievement_names()
        assert "Unstoppable" in unlocked

    def test_achievements_dont_unlock_twice(self):
        """Test achievements only unlock once."""
        stats = Statistics()
        tracker = AchievementTracker(stats)

        # Block two dangerous commands
        stats.increment_dangerous_blocked()
        tracker.check_achievements()

        stats.increment_dangerous_blocked()
        tracker.check_achievements()

        # First Blood should only appear once
        unlocked = tracker.get_unlocked_achievement_names()
        assert unlocked.count("First Blood") == 1

    def test_get_achievements_by_category(self):
        """Test filtering achievements by category."""
        stats = Statistics()
        tracker = AchievementTracker(stats)

        # Unlock achievements from different categories
        stats.increment_dangerous_blocked()  # First Blood (danger)
        stats.track_safe_command("touch")    # Creator (safe)
        tracker.check_achievements()

        # Check danger category
        danger_achievements = tracker.get_achievements_by_category("danger")
        assert "First Blood" in danger_achievements
        assert "Creator" not in danger_achievements

        # Check safe category
        safe_achievements = tracker.get_achievements_by_category("safe")
        assert "Creator" in safe_achievements
        assert "First Blood" not in safe_achievements

    def test_achievement_metadata_completeness(self):
        """Test all achievements have metadata."""
        # All achievement keys should have metadata
        expected_achievements = [
            "first_blood", "persistent", "typo_master", "danger_addict",
            "stubborn", "explorer", "command_master", "balanced",
            "curious_explorer", "boundary_tester", "system_adventurer",
            "unstoppable", "creator", "architect", "detective"
        ]

        for achievement in expected_achievements:
            assert achievement in ACHIEVEMENT_METADATA
            assert "name" in ACHIEVEMENT_METADATA[achievement]
            assert "category" in ACHIEVEMENT_METADATA[achievement]
