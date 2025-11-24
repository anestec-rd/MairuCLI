"""
Unit tests for src/display/ascii_renderer.py
"""

import pytest
from src.display.ascii_renderer import AsciiRenderer


class TestAsciiRenderer:
    """Test suite for AsciiRenderer."""

    def test_colorize_with_valid_color(self):
        """Test colorizing text with valid color name."""
        renderer = AsciiRenderer()

        colored = renderer.colorize("Hello", "orange")

        # Should contain ANSI codes
        assert "\033[" in colored
        assert "Hello" in colored
        assert "\033[0m" in colored  # Reset code

    def test_colorize_with_invalid_color(self):
        """Test colorizing with invalid color falls back to default."""
        renderer = AsciiRenderer()

        # Should not raise error, just use default
        colored = renderer.colorize("Hello", "invalid_color")
        assert "Hello" in colored

    def test_colorize_empty_string(self):
        """Test colorizing empty string."""
        renderer = AsciiRenderer()

        colored = renderer.colorize("", "orange")
        assert colored == "\033[38;5;208m\033[0m"

    def test_display_art_slowly_basic(self):
        """Test display_art_slowly with basic art."""
        renderer = AsciiRenderer()

        art = "Line 1\nLine 2\nLine 3"

        # Should not raise error
        # (We can't easily test the output without mocking print)
        try:
            renderer.display_art_slowly(art, "orange", delay=0)
            success = True
        except Exception:
            success = False

        assert success

    def test_display_art_slowly_empty(self):
        """Test display_art_slowly with empty art."""
        renderer = AsciiRenderer()

        # Should not raise error
        try:
            renderer.display_art_slowly("", "orange", delay=0)
            success = True
        except Exception:
            success = False

        assert success

    def test_display_art_slowly_single_line(self):
        """Test display_art_slowly with single line."""
        renderer = AsciiRenderer()

        art = "Single line"

        # Should not raise error
        try:
            renderer.display_art_slowly(art, "orange", delay=0)
            success = True
        except Exception:
            success = False

        assert success

    def test_colorize_preserves_text_content(self):
        """Test colorize doesn't modify text content."""
        renderer = AsciiRenderer()

        original = "Test 123 !@#"
        colored = renderer.colorize(original, "orange")

        # Remove ANSI codes to check content
        # Simple check: original text should be in colored string
        assert original in colored

    def test_multiple_colorize_calls(self):
        """Test multiple colorize calls work correctly."""
        renderer = AsciiRenderer()

        text1 = renderer.colorize("Red", "red")
        text2 = renderer.colorize("Green", "green")
        text3 = renderer.colorize("Orange", "orange")

        # All should contain their text
        assert "Red" in text1
        assert "Green" in text2
        assert "Orange" in text3

        # All should have reset codes
        assert "\033[0m" in text1
        assert "\033[0m" in text2
        assert "\033[0m" in text3
