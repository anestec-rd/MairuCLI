"""Integration test for repeat warning feature ('I told you so')."""

import sys
import os
from unittest.mock import patch
from io import StringIO

# Add project root to path
sys.path.insert(
    0,
    os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
)

from src.interceptor import check_command
from src.display import show_warning
from src.display.statistics import Statistics


class TestRepeatWarning:
    """Integration tests for repeat warning feature."""

    def test_repeat_warning_escalation(self):
        """Test that repeat warnings escalate properly."""
        dangerous_cmd = "rm -rf /"
        stats = Statistics()

        # First attempt
        is_dangerous, pattern_name = check_command(dangerous_cmd)
        assert is_dangerous == "critical"
        assert pattern_name == "rm_dangerous"

        # Track repeat
        count1 = stats.track_repeat_command(dangerous_cmd)
        assert count1 == 1

        # Second attempt
        count2 = stats.track_repeat_command(dangerous_cmd)
        assert count2 == 2

        # Third attempt
        count3 = stats.track_repeat_command(dangerous_cmd)
        assert count3 == 3

    def test_repeat_warning_different_commands(self):
        """Test that different commands are tracked separately."""
        stats = Statistics()

        cmd1 = "rm -rf /"
        cmd2 = "chmod 777 file.txt"

        count1a = stats.track_repeat_command(cmd1)
        count2a = stats.track_repeat_command(cmd2)
        count1b = stats.track_repeat_command(cmd1)

        assert count1a == 1
        assert count2a == 1
        assert count1b == 2

    def test_max_repeats_tracking(self):
        """Test that max repeats are tracked correctly."""
        stats = Statistics()

        stats.track_repeat_command("cmd1")
        stats.track_repeat_command("cmd1")
        stats.track_repeat_command("cmd2")
        stats.track_repeat_command("cmd1")

        max_repeats = stats.get_max_repeats()
        assert max_repeats == 3  # cmd1 was repeated 3 times

    def test_repeat_warning_with_show_warning(self, capsys):
        """Test that show_warning handles repeat commands."""
        dangerous_cmd = "rm -rf /"
        pattern_name = "rm_dangerous"

        # Capture output
        with patch('src.display.warning_components.time.sleep'):
            show_warning(pattern_name, dangerous_cmd)

        captured = capsys.readouterr()
        # Should show some warning output
        assert len(captured.out) > 0
