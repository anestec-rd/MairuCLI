"""
Integration tests for educational breakdown system.

Tests the complete flow from loading content to displaying breakdowns.
"""

import pytest
from src.display.educational_breakdown import EducationalBreakdown


class TestEducationalBreakdownFlow:
    """Test suite for educational breakdown integration."""

    def test_init(self):
        """Test EducationalBreakdown initialization."""
        breakdown = EducationalBreakdown()

        assert breakdown.loader is not None
        assert breakdown.formatter is not None

    def test_show_quick_explanation_existing_pattern(self, capsys):
        """Test showing quick explanation for existing pattern."""
        breakdown = EducationalBreakdown()

        breakdown.show_quick_explanation("rm_dangerous")

        captured = capsys.readouterr()
        assert len(captured.out) > 0
        # Should contain quick summary
        assert "Quick Summary" in captured.out or "rm" in captured.out.lower()

    def test_show_quick_explanation_missing_pattern(self, capsys):
        """Test showing quick explanation for non-existent pattern."""
        breakdown = EducationalBreakdown()

        breakdown.show_quick_explanation("nonexistent_pattern")

        captured = capsys.readouterr()
        # Should show fallback message
        assert "dangerous" in captured.out.lower()

    def test_show_full_breakdown_existing_pattern(self, capsys):
        """Test showing full breakdown for existing pattern."""
        breakdown = EducationalBreakdown()

        breakdown.show_full_breakdown("rm_dangerous")

        captured = capsys.readouterr()
        assert len(captured.out) > 0
        # Should contain breakdown content
        assert "Command Breakdown" in captured.out
        assert "rm" in captured.out.lower()

    def test_show_full_breakdown_missing_pattern(self, capsys):
        """Test showing full breakdown for non-existent pattern."""
        breakdown = EducationalBreakdown()

        result = breakdown.show_full_breakdown("nonexistent_pattern")

        captured = capsys.readouterr()
        # Should return False for non-existent pattern
        assert result is False
        # Should show fallback message
        assert "not yet available" in captured.out

    def test_show_full_breakdown_with_simulation(self, capsys):
        """Test that full breakdown includes simulation if available."""
        breakdown = EducationalBreakdown()

        breakdown.show_full_breakdown("rm_dangerous")

        captured = capsys.readouterr()
        # Should contain simulation content
        assert "Timeline Simulation" in captured.out or "T+" in captured.out

    def test_show_full_breakdown_with_incidents(self, capsys):
        """Test that full breakdown includes incidents if available."""
        breakdown = EducationalBreakdown()

        breakdown.show_full_breakdown("rm_dangerous")

        captured = capsys.readouterr()
        # Should contain incident content if related incidents exist
        # GitLab incident should be shown for rm_dangerous
        assert "Horror Story" in captured.out or "GitLab" in captured.out

    def test_graceful_degradation_missing_simulation(self, capsys):
        """Test graceful handling when simulation is missing."""
        breakdown = EducationalBreakdown()

        # Pattern with breakdown but possibly no simulation
        breakdown.show_full_breakdown("chmod_777")

        captured = capsys.readouterr()
        # Should still show breakdown even if simulation is missing
        assert "Command Breakdown" in captured.out
        assert len(captured.out) > 0

    def test_graceful_degradation_missing_incidents(self, capsys):
        """Test graceful handling when incidents are missing."""
        breakdown = EducationalBreakdown()

        # Pattern with breakdown but no related incidents
        breakdown.show_full_breakdown("chmod_000")

        captured = capsys.readouterr()
        # Should still show breakdown even if incidents are missing
        assert "Command Breakdown" in captured.out
        assert len(captured.out) > 0

    def test_multiple_patterns_sequential(self, capsys):
        """Test showing breakdowns for multiple patterns sequentially."""
        breakdown = EducationalBreakdown()

        patterns = ["rm_dangerous", "chmod_777", "dd_zero"]

        for pattern in patterns:
            breakdown.show_quick_explanation(pattern)

        captured = capsys.readouterr()
        assert len(captured.out) > 0

    def test_loader_formatter_integration(self):
        """Test that loader and formatter work together correctly."""
        breakdown = EducationalBreakdown()

        # Loader should load data
        breakdown_data = breakdown.loader.load_breakdown("rm_dangerous")
        assert breakdown_data is not None

        # Formatter should format it
        result = breakdown.formatter.format_command_breakdown(breakdown_data)
        assert isinstance(result, str)
        assert len(result) > 0

    def test_caching_across_calls(self, capsys):
        """Test that content is cached across multiple calls."""
        breakdown = EducationalBreakdown()

        # First call
        breakdown.show_quick_explanation("rm_dangerous")

        # Check cache
        assert "rm_dangerous" in breakdown.loader.breakdowns_cache

        # Second call should use cache
        breakdown.show_quick_explanation("rm_dangerous")

        captured = capsys.readouterr()
        assert len(captured.out) > 0

    def test_fallback_breakdown_display(self, capsys):
        """Test fallback message when content is not available."""
        breakdown = EducationalBreakdown()

        breakdown._show_fallback_breakdown("test_pattern")

        captured = capsys.readouterr()
        assert "not yet available" in captured.out
        assert "dangerous" in captured.out.lower()

    def test_loader_returns_none_for_missing_content(self):
        """Test that loader returns None for missing content."""
        breakdown = EducationalBreakdown()

        result = breakdown.loader.load_breakdown("nonexistent")
        assert result is None

        result = breakdown.loader.load_simulation("nonexistent")
        assert result is None

        result = breakdown.loader.load_incident("nonexistent")
        assert result is None

    def test_get_related_incidents_returns_list(self):
        """Test that get_related_incidents returns a list."""
        breakdown = EducationalBreakdown()

        result = breakdown.loader.get_related_incidents("rm_dangerous")
        assert isinstance(result, list)
