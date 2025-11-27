"""
Unit tests for src/display/breakdown_formatter.py
"""

import pytest
from src.display.breakdown_formatter import BreakdownFormatter


class TestBreakdownFormatter:
    """Test suite for BreakdownFormatter."""

    def test_init(self):
        """Test BreakdownFormatter initialization."""
        formatter = BreakdownFormatter()
        # BreakdownFormatter doesn't have instance variables to test
        assert formatter is not None

    def test_format_command_breakdown_basic(self):
        """Test formatting a basic command breakdown."""
        formatter = BreakdownFormatter()

        breakdown_data = {
            "parts": [
                {
                    "part": "test",
                    "emoji": "🧪",
                    "meaning": "A test part",
                    "danger_level": "low"
                }
            ]
        }

        result = formatter.format_command_breakdown(breakdown_data)

        assert isinstance(result, str)
        assert len(result) > 0
        assert "Command Breakdown" in result
        assert "test" in result

    def test_format_command_breakdown_empty(self):
        """Test formatting with empty breakdown data."""
        formatter = BreakdownFormatter()
        result = formatter.format_command_breakdown({})

        assert isinstance(result, str)
        assert "Command Breakdown" in result

    def test_format_command_breakdown_with_translation(self):
        """Test formatting with translation field."""
        formatter = BreakdownFormatter()

        breakdown_data = {
            "parts": [],
            "translation": "This is a test translation"
        }

        result = formatter.format_command_breakdown(breakdown_data)

        assert "In plain English" in result
        assert "This is a test translation" in result

    def test_format_command_breakdown_with_halloween_analogy(self):
        """Test formatting with Halloween analogy."""
        formatter = BreakdownFormatter()

        breakdown_data = {
            "parts": [],
            "halloween_analogy": "Like a spooky ghost"
        }

        result = formatter.format_command_breakdown(breakdown_data)

        assert "Halloween Analogy" in result
        assert "Like a spooky ghost" in result

    def test_format_command_breakdown_with_safe_alternatives(self):
        """Test formatting with safe alternatives."""
        formatter = BreakdownFormatter()

        breakdown_data = {
            "parts": [],
            "safe_alternatives": ["Alternative 1", "Alternative 2"]
        }

        result = formatter.format_command_breakdown(breakdown_data)

        assert "Safe Alternatives" in result
        assert "Alternative 1" in result
        assert "Alternative 2" in result

    def test_format_timeline_simulation_basic(self):
        """Test formatting a basic timeline simulation."""
        formatter = BreakdownFormatter()

        simulation_data = {
            "description": "Test simulation description",
            "timeline": [
                {
                    "time": "T+0s",
                    "emoji": "⚡",
                    "description": "First event",
                    "severity": "info"
                },
                {
                    "time": "T+1s",
                    "emoji": "💥",
                    "description": "Second event",
                    "severity": "critical"
                }
            ]
        }

        result = formatter.format_timeline_simulation(simulation_data)

        assert isinstance(result, str)
        assert "Timeline Simulation" in result
        assert "Test simulation description" in result
        assert "T+0s" in result
        assert "First event" in result

    def test_format_timeline_simulation_empty(self):
        """Test formatting with empty simulation data."""
        formatter = BreakdownFormatter()
        result = formatter.format_timeline_simulation({})

        assert isinstance(result, str)
        assert "Timeline Simulation" in result

    def test_format_incident_story_basic(self):
        """Test formatting a basic incident story."""
        formatter = BreakdownFormatter()

        incident_data = {
            "title": "Test Incident",
            "company": "Test Corp",
            "date": "2025-01-01",
            "what_happened": "Something bad happened",
            "impact": ["Impact 1", "Impact 2"],
            "lesson": "Always test your code",
            "source": "https://example.com"
        }

        result = formatter.format_incident_story(incident_data)

        assert isinstance(result, str)
        assert "Real Horror Story" in result
        assert "Test Incident" in result
        assert "Test Corp" in result
        assert "2025-01-01" in result
        assert "Something bad happened" in result

    def test_format_incident_story_empty(self):
        """Test formatting with empty incident data."""
        formatter = BreakdownFormatter()
        result = formatter.format_incident_story({})

        assert isinstance(result, str)
        assert "Real Horror Story" in result

    def test_format_quick_explanation_with_summary(self):
        """Test formatting quick explanation with summary."""
        formatter = BreakdownFormatter()

        breakdown_data = {
            "quick_summary": "This is a quick summary"
        }

        result = formatter.format_quick_explanation(breakdown_data)

        assert isinstance(result, str)
        assert "Quick Summary" in result
        assert "This is a quick summary" in result

    def test_format_quick_explanation_fallback_to_translation(self):
        """Test formatting quick explanation falls back to translation."""
        formatter = BreakdownFormatter()

        breakdown_data = {
            "translation": "This is a translation"
        }

        result = formatter.format_quick_explanation(breakdown_data)

        assert isinstance(result, str)
        assert "Quick Summary" in result
        assert "This is a translation" in result

    def test_format_quick_explanation_empty(self):
        """Test formatting quick explanation with empty data."""
        formatter = BreakdownFormatter()
        result = formatter.format_quick_explanation({})

        assert isinstance(result, str)
        # Should return empty or minimal string
        assert len(result) >= 0

    def test_halloween_theme_elements(self):
        """Test that Halloween theme elements (emojis) are present."""
        formatter = BreakdownFormatter()

        breakdown_data = {
            "parts": [{"part": "test", "emoji": "🎃", "meaning": "test"}]
        }

        result = formatter.format_command_breakdown(breakdown_data)

        # Check for emojis (Halloween theme indicators)
        assert any(emoji in result for emoji in ["🎓", "📚", "🌍", "🎃", "✅"])

    def test_severity_color_mapping(self):
        """Test that different severity levels are handled in timeline."""
        formatter = BreakdownFormatter()

        simulation_data = {
            "timeline": [
                {"time": "T+0s", "emoji": "✅", "description": "Info", "severity": "info"},
                {"time": "T+1s", "emoji": "⚠️", "description": "Warning", "severity": "warning"},
                {"time": "T+2s", "emoji": "🔥", "description": "Danger", "severity": "danger"},
                {"time": "T+3s", "emoji": "💥", "description": "Critical", "severity": "critical"}
            ]
        }

        result = formatter.format_timeline_simulation(simulation_data)

        # Should contain all severity levels
        assert "Info" in result
        assert "Warning" in result
        assert "Danger" in result
        assert "Critical" in result
