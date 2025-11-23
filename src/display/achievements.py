"""
Achievement tracking for MairuCLI display system.

Tracks and displays achievement unlocks based on user actions.
"""

import time
from typing import List
from src.display.statistics import Statistics
from src.display.ascii_renderer import AsciiRenderer
from src.config import TIMING_PAUSE_SHORT, TIMING_PAUSE_MEDIUM, DISPLAY_SEPARATOR_WIDTH


# Achievement threshold constants
ACHIEVEMENT_FIRST_BLOOD = 1          # First dangerous command blocked
ACHIEVEMENT_THRESHOLD_LOW = 3        # Typo Master, Stubborn, Boundary Tester
ACHIEVEMENT_THRESHOLD_MEDIUM = 5     # Persistent Troublemaker, Explorer
ACHIEVEMENT_THRESHOLD_HIGH = 8       # Balanced User
ACHIEVEMENT_THRESHOLD_EXPERT = 10    # Danger Addict


# Achievement metadata with categories
ACHIEVEMENT_METADATA = {
    "first_blood": {
        "name": "First Blood",
        "category": "danger"
    },
    "persistent": {
        "name": "Persistent Troublemaker",
        "category": "danger"
    },
    "typo_master": {
        "name": "Typo Master",
        "category": "exploration"
    },
    "danger_addict": {
        "name": "Danger Addict",
        "category": "danger"
    },
    "stubborn": {
        "name": "Stubborn",
        "category": "danger"
    },
    "explorer": {
        "name": "Explorer",
        "category": "safe"
    },
    "command_master": {
        "name": "Command Master",
        "category": "safe"
    },
    "balanced": {
        "name": "Balanced User",
        "category": "safe"
    },
    "curious_explorer": {
        "name": "Curious Explorer",
        "category": "system_protection"
    },
    "boundary_tester": {
        "name": "Boundary Tester",
        "category": "system_protection"
    },
    "system_adventurer": {
        "name": "System Adventurer",
        "category": "system_protection"
    }
}


class AchievementTracker:
    """Tracks and displays achievements."""

    def __init__(self, statistics: Statistics):
        """
        Initialize achievement tracker.

        Args:
            statistics: Statistics instance to check for achievements
        """
        self.statistics = statistics
        self.renderer = AsciiRenderer()
        self._unlocked: List[str] = []

    def check_achievements(self) -> None:
        """
        Check if user has unlocked any achievements.
        Display achievement notification if newly unlocked.
        """
        total_blocks = self.statistics.get_total_blocks()
        total_typos = self.statistics.get_total_typos()
        max_repeats = self.statistics.get_max_repeats()
        safe_commands = self.statistics.get_safe_commands_count()

        # Achievement: First Blood
        if total_blocks == ACHIEVEMENT_FIRST_BLOOD and "first_blood" not in self._unlocked:
            self._unlocked.append("first_blood")
            self.show_achievement(
                "First Blood",
                "Blocked your first dangerous command!"
            )

        # Achievement: Persistent Troublemaker
        if total_blocks >= ACHIEVEMENT_THRESHOLD_MEDIUM and "persistent" not in self._unlocked:
            self._unlocked.append("persistent")
            self.show_achievement(
                "Persistent Troublemaker",
                "Tried 5 dangerous commands. Impressive dedication!"
            )

        # Achievement: Typo Master
        if total_typos >= ACHIEVEMENT_THRESHOLD_LOW and "typo_master" not in self._unlocked:
            self._unlocked.append("typo_master")
            self.show_achievement(
                "Typo Master",
                "Made 3 typos. Your keyboard needs calibration!"
            )

        # Achievement: Danger Addict
        if total_blocks >= ACHIEVEMENT_THRESHOLD_EXPERT and "danger_addict" not in self._unlocked:
            self._unlocked.append("danger_addict")
            self.show_achievement(
                "Danger Addict",
                "10 dangerous commands blocked. Do you have a death wish?"
            )

        # Achievement: Stubborn
        if max_repeats >= ACHIEVEMENT_THRESHOLD_LOW and "stubborn" not in self._unlocked:
            self._unlocked.append("stubborn")
            self.show_achievement(
                "Stubborn",
                "Tried the same command 3 times. I admire your persistence!"
            )

        # Achievement: Explorer
        if safe_commands >= ACHIEVEMENT_THRESHOLD_MEDIUM and "explorer" not in self._unlocked:
            self._unlocked.append("explorer")
            self.show_achievement(
                "Explorer",
                "Used 5 different safe commands. You're learning the ropes!"
            )

        # Achievement: Command Master
        if safe_commands >= ACHIEVEMENT_THRESHOLD_EXPERT and "command_master" not in self._unlocked:
            self._unlocked.append("command_master")
            self.show_achievement(
                "Command Master",
                "Used 10 different safe commands. You're a CLI wizard!"
            )

        # Achievement: Balanced User
        if (safe_commands >= ACHIEVEMENT_THRESHOLD_HIGH and total_blocks >= ACHIEVEMENT_THRESHOLD_LOW and
                "balanced" not in self._unlocked):
            self._unlocked.append("balanced")
            self.show_achievement(
                "Balanced User",
                "Explored both safe and dangerous commands. Perfect balance!"
            )

        # System Protection Achievements
        sys_blocks = self.statistics.get_system_protection_blocks()
        unique_dirs = self.statistics.get_unique_protected_dirs_count()

        # Achievement: Curious Explorer
        if sys_blocks == 1 and "curious_explorer" not in self._unlocked:
            self._unlocked.append("curious_explorer")
            self.show_achievement(
                "Curious Explorer",
                "Found a protected area! Curiosity is great, but be careful!"
            )

        # Achievement: Boundary Tester
        if sys_blocks >= ACHIEVEMENT_THRESHOLD_LOW and "boundary_tester" not in self._unlocked:
            self._unlocked.append("boundary_tester")
            self.show_achievement(
                "Boundary Tester",
                "Tested protected boundaries 3 times. You're thorough!"
            )

        # Achievement: System Adventurer
        if unique_dirs >= ACHIEVEMENT_THRESHOLD_LOW and "system_adventurer" not in self._unlocked:
            self._unlocked.append("system_adventurer")
            self.show_achievement(
                "System Adventurer",
                "Explored 3 different protected areas. What a journey!"
            )

    def show_achievement(self, title: str, description: str) -> None:
        """
        Display achievement unlock notification.

        Args:
            title: Achievement title
            description: Achievement description
        """
        time.sleep(TIMING_PAUSE_MEDIUM)  # Pause before achievement (dramatic timing)
        print()
        print("=" * DISPLAY_SEPARATOR_WIDTH)
        trophy = "🏆"
        title_text = self.renderer.colorize("ACHIEVEMENT UNLOCKED!", "orange")
        print(f"{trophy} {title_text} {trophy}")
        print()
        achievement_title = self.renderer.colorize(title, "purple")
        print(f"  {achievement_title}")
        print(f"  {description}")
        print("=" * DISPLAY_SEPARATOR_WIDTH)
        print()
        time.sleep(TIMING_PAUSE_SHORT)  # Brief pause after achievement

    def get_unlocked_achievements(self) -> List[str]:
        """
        Get list of unlocked achievement IDs.

        Returns:
            List of achievement IDs
        """
        return self._unlocked.copy()

    def get_unlocked_achievement_names(self) -> List[str]:
        """
        Get list of unlocked achievement display names.

        Returns:
            List of achievement display names
        """
        return [ACHIEVEMENT_METADATA[ach_id]["name"]
                for ach_id in self._unlocked
                if ach_id in ACHIEVEMENT_METADATA]

    def get_achievements_by_category(self, category: str) -> List[str]:
        """
        Get unlocked achievements filtered by category.

        Args:
            category: Category to filter by
                     ("danger", "safe", "exploration", "system_protection")

        Returns:
            List of achievement display names in the specified category
        """
        return [ACHIEVEMENT_METADATA[ach_id]["name"]
                for ach_id in self._unlocked
                if ach_id in ACHIEVEMENT_METADATA and
                ACHIEVEMENT_METADATA[ach_id]["category"] == category]

    def get_all_categories(self) -> List[str]:
        """
        Get list of all achievement categories that have unlocked achievements.

        Returns:
            List of category names
        """
        categories = set()
        for ach_id in self._unlocked:
            if ach_id in ACHIEVEMENT_METADATA:
                categories.add(ACHIEVEMENT_METADATA[ach_id]["category"])
        return sorted(list(categories))
