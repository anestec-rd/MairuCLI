"""
Unit tests for src/display/statistics.py
"""

import pytest
from src.display.statistics import Statistics


class TestStatistics:
    """Test suite for Statistics."""

    def test_initial_stats_are_zero(self):
        """Test statistics start at zero."""
        stats = Statistics()

        assert stats.get_total_blocks() == 0
        assert stats.get_total_typos() == 0
        assert stats.get_safe_commands_count() == 0
        assert stats.get_max_repeats() == 0

    def test_increment_dangerous_blocked(self):
        """Test incrementing dangerous blocked counter."""
        stats = Statistics()

        stats.increment_dangerous_blocked()
        assert stats.get_total_blocks() == 1

        stats.increment_dangerous_blocked()
        assert stats.get_total_blocks() == 2

    def test_increment_typos_caught(self):
        """Test incrementing typos caught counter."""
        stats = Statistics()

        stats.increment_typos_caught()
        assert stats.get_total_typos() == 1

        stats.increment_typos_caught()
        assert stats.get_total_typos() == 2

    def test_track_safe_command(self):
        """Test tracking unique safe commands."""
        stats = Statistics()

        stats.track_safe_command("ls")
        assert stats.get_safe_commands_count() == 1

        stats.track_safe_command("pwd")
        assert stats.get_safe_commands_count() == 2

        # Same command again - should not increase count
        stats.track_safe_command("ls")
        assert stats.get_safe_commands_count() == 2

    def test_has_used_command(self):
        """Test checking if specific command was used."""
        stats = Statistics()

        assert not stats.has_used_command("touch")

        stats.track_safe_command("touch")
        assert stats.has_used_command("touch")
        assert not stats.has_used_command("mkdir")

    def test_track_repeat_command(self):
        """Test tracking repeat command attempts."""
        stats = Statistics()

        count1 = stats.track_repeat_command("rm -rf /")
        assert count1 == 1

        count2 = stats.track_repeat_command("rm -rf /")
        assert count2 == 2

        count3 = stats.track_repeat_command("rm -rf /")
        assert count3 == 3

    def test_get_max_repeats(self):
        """Test getting maximum repeat count."""
        stats = Statistics()

        # No repeats initially
        assert stats.get_max_repeats() == 0

        # Track different commands
        stats.track_repeat_command("rm -rf /")
        stats.track_repeat_command("rm -rf /")
        stats.track_repeat_command("chmod 777 file")

        # Max should be 2 (rm -rf / repeated twice)
        assert stats.get_max_repeats() == 2

        # Add more repeats
        stats.track_repeat_command("chmod 777 file")
        stats.track_repeat_command("chmod 777 file")

        # Max should now be 3 (chmod 777 repeated 3 times)
        assert stats.get_max_repeats() == 3

    def test_caution_stats(self):
        """Test caution warning statistics."""
        stats = Statistics()

        stats.increment_caution_shown()
        stats.increment_caution_proceeded()

        stats.increment_caution_shown()
        stats.increment_caution_cancelled()

        caution_stats = stats.get_caution_stats()
        assert caution_stats["shown"] == 2
        assert caution_stats["proceeded"] == 1
        assert caution_stats["cancelled"] == 1

    def test_system_protection_tracking(self):
        """Test system directory protection tracking."""
        stats = Statistics()

        assert stats.get_system_protection_blocks() == 0

        stats.track_system_protection_block("C:\\Windows")
        assert stats.get_system_protection_blocks() == 1

        stats.track_system_protection_block("C:\\Program Files")
        assert stats.get_system_protection_blocks() == 2

        # Same directory again
        stats.track_system_protection_block("C:\\Windows")
        assert stats.get_system_protection_blocks() == 3

        # Unique directories count
        assert stats.get_unique_protected_dirs_count() == 2

    def test_get_stats_returns_copy(self):
        """Test get_stats returns a copy, not reference."""
        stats = Statistics()

        stats.increment_dangerous_blocked()
        stats_dict = stats.get_stats()

        # Modify returned dict
        stats_dict["dangerous_blocked"] = 999

        # Original should be unchanged
        assert stats.get_total_blocks() == 1
