"""
Unit tests for ContentLoader variation selection logic.

Tests the merge strategy:
1. Category variations (8 variations)
2. Pattern-specific variations (0-4 variations)
3. Merge both lists (8-12 total)
4. Fallback to legacy if needed
"""

import pytest
import json
import tempfile
from pathlib import Path
from src.display.content_loader import ContentLoader


class TestVariationPriority:
    """Test variation selection priority system."""

    def test_pattern_specific_variations_highest_priority(self, tmp_path):
        """Pattern-specific and category variations should be merged."""
        # Create pattern_variations.json
        pattern_vars = {
            "version": "1.0",
            "patterns": {
                "rm_root": {
                    "variations": [
                        {"title": "PATTERN!", "subtitle": "(From pattern)"}
                    ]
                }
            }
        }

        warnings_dir = tmp_path / "warnings"
        warnings_dir.mkdir()

        with open(warnings_dir / "pattern_variations.json", "w") as f:
            json.dump(pattern_vars, f)

        # Create category_variations.json (should be merged)
        category_vars = {
            "version": "1.0",
            "categories": {
                "deletion": {
                    "variations": [
                        {"title": "CATEGORY!", "subtitle": "(From category)"}
                    ]
                }
            }
        }

        with open(warnings_dir / "category_variations.json", "w") as f:
            json.dump(category_vars, f)

        loader = ContentLoader(tmp_path)
        variations = loader.get_variations("rm_root", "deletion")

        # Should merge: category (1) + pattern (1) = 2 total
        assert len(variations) == 2
        titles = [v[0] for v in variations]
        assert "PATTERN!" in titles
        assert "CATEGORY!" in titles

    def test_category_variations_second_priority(self, tmp_path):
        """Category variations should be used when no pattern-specific exists."""
        # Create only category_variations.json
        category_vars = {
            "version": "1.0",
            "categories": {
                "deletion": {
                    "variations": [
                        {"title": "CATEGORY VAR!", "subtitle": "(From category)"}
                    ]
                }
            }
        }

        warnings_dir = tmp_path / "warnings"
        warnings_dir.mkdir()

        with open(warnings_dir / "category_variations.json", "w") as f:
            json.dump(category_vars, f)

        loader = ContentLoader(tmp_path)
        variations = loader.get_variations("some_pattern", "deletion")

        assert len(variations) == 1
        assert variations[0][0] == "CATEGORY VAR!"
        assert variations[0][1] == "(From category)"

    def test_legacy_variations_third_priority(self, tmp_path):
        """Legacy danger_variations.json should work for backward compatibility."""
        # Create only danger_variations.json
        legacy_vars = {
            "rm_root": [
                {"title": "LEGACY!", "subtitle": "(From old file)"}
            ]
        }

        warnings_dir = tmp_path / "warnings"
        warnings_dir.mkdir()

        with open(warnings_dir / "danger_variations.json", "w") as f:
            json.dump(legacy_vars, f)

        loader = ContentLoader(tmp_path)
        variations = loader.get_variations("rm_root", None)

        assert len(variations) == 1
        assert variations[0][0] == "LEGACY!"
        assert variations[0][1] == "(From old file)"

    def test_fallback_when_no_files(self, tmp_path):
        """Fallback should be used when no variation files exist."""
        warnings_dir = tmp_path / "warnings"
        warnings_dir.mkdir()

        loader = ContentLoader(tmp_path)
        variations = loader.get_variations("unknown_pattern", "unknown_category")

        # Should return fallback variations
        assert len(variations) > 0
        assert isinstance(variations[0], tuple)
        assert len(variations[0]) == 2

    def test_caching_works(self, tmp_path):
        """Variations should be cached after first load."""
        pattern_vars = {
            "version": "1.0",
            "patterns": {
                "test_pattern": {
                    "variations": [
                        {"title": "CACHED!", "subtitle": "(Should be cached)"}
                    ]
                }
            }
        }

        warnings_dir = tmp_path / "warnings"
        warnings_dir.mkdir()

        pattern_file = warnings_dir / "pattern_variations.json"
        with open(pattern_file, "w") as f:
            json.dump(pattern_vars, f)

        loader = ContentLoader(tmp_path)

        # First call - loads from file
        variations1 = loader.get_variations("test_pattern", "deletion")

        # Delete file
        pattern_file.unlink()

        # Second call - should use cache
        variations2 = loader.get_variations("test_pattern", "deletion")

        assert variations1 == variations2
        assert variations2[0][0] == "CACHED!"


class TestRealFiles:
    """Test with actual project files."""

    def test_rm_root_uses_pattern_specific(self):
        """rm_root should use pattern-specific variations."""
        loader = ContentLoader()
        variations = loader.get_variations("rm_root", "deletion")

        # Should have variations from pattern_variations.json
        assert len(variations) > 0

        # Check for known rm_root variations
        titles = [v[0] for v in variations]
        assert "YOU'RE FIRED!" in titles or "NOPE. JUST NOPE." in titles

    def test_drop_database_uses_category(self):
        """drop_database should use category variations (database)."""
        loader = ContentLoader()
        variations = loader.get_variations("drop_database", "database")

        # Should have variations
        assert len(variations) > 0

        # Check for database category variations
        titles = [v[0] for v in variations]
        assert any("DATABASE" in title or "SQL" in title for title in titles)

    def test_chmod_000_uses_pattern_specific(self):
        """chmod_000 should use its unique ghost/lock theme variations."""
        loader = ContentLoader()
        variations = loader.get_variations("chmod_000", "permission")

        # Should have variations
        assert len(variations) > 0

        # Check for ghost theme
        titles = [v[0] for v in variations]
        assert any("GHOST" in title or "PHANTOM" in title for title in titles)

    def test_all_variations_have_correct_format(self):
        """All variations should be (title, subtitle) tuples."""
        loader = ContentLoader()

        test_cases = [
            ("rm_root", "deletion"),
            ("chmod_777", "permission"),
            ("chmod_000", "permission"),
            ("drop_database", "database"),
            ("fork_bomb", "system"),
            ("kernel_panic", "system"),
        ]

        for variation_set, category in test_cases:
            variations = loader.get_variations(variation_set, category)

            assert len(variations) > 0, f"No variations for {variation_set}"

            for title, subtitle in variations:
                assert isinstance(title, str), f"Title not string: {title}"
                assert isinstance(subtitle, str), f"Subtitle not string: {subtitle}"
                assert len(title) > 0, f"Empty title for {variation_set}"
                assert len(subtitle) > 0, f"Empty subtitle for {variation_set}"
