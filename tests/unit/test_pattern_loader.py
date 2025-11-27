"""
Unit tests for PatternLoader class in src/interceptor.py
"""

import json
import os
import tempfile
import pytest
from pathlib import Path

# Add project root to path
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))

from src.interceptor import PatternLoader


class TestPatternLoader:
    """Test suite for PatternLoader class."""

    def test_load_valid_dangerous_patterns(self):
        """Test loading valid dangerous patterns from warning_catalog.json."""
        loader = PatternLoader()
        dangerous, _, _ = loader.load_all_patterns()

        # Verify patterns were loaded
        assert len(dangerous) > 0, "Should load dangerous patterns"

        # Verify pattern structure
        for name, data in dangerous.items():
            assert 'pattern' in data, f"Pattern {name} should have 'pattern'"
            assert 'category' in data, f"Pattern {name} should have 'category'"
            assert 'severity' in data, f"Pattern {name} should have 'severity'"
            assert 'art_file' in data, f"Pattern {name} should have 'art_file'"

    def test_load_valid_caution_patterns(self):
        """Test loading valid caution patterns from caution_catalog.json."""
        loader = PatternLoader()
        _, caution, _ = loader.load_all_patterns()

        # Verify patterns were loaded (may be empty if file doesn't exist)
        assert isinstance(caution, dict), "Should return dict"

        # If patterns exist, verify structure
        for name, data in caution.items():
            assert 'pattern' in data, f"Pattern {name} should have 'pattern'"

    def test_load_valid_typo_patterns(self):
        """Test loading valid typo patterns from typo_messages.json."""
        loader = PatternLoader()
        _, _, typo = loader.load_all_patterns()

        # Verify patterns were loaded (may be empty if file doesn't exist)
        assert isinstance(typo, dict), "Should return dict"

        # If patterns exist, verify structure
        for name, data in typo.items():
            assert 'pattern' in data, f"Pattern {name} should have 'pattern'"

    def test_missing_warning_catalog_file(self):
        """Test handling of missing warning_catalog.json file."""
        # Create loader with non-existent directory
        loader = PatternLoader(data_dir="nonexistent_directory")

        # Should not raise exception
        dangerous, _, _ = loader.load_all_patterns()

        # Should return empty dict
        assert dangerous == {}, "Should return empty dict for missing file"

    def test_missing_caution_catalog_file(self):
        """Test handling of missing caution_catalog.json file."""
        # Create temp directory with only warning_catalog.json
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create minimal warning_catalog.json
            warning_catalog = {
                "version": "1.0",
                "warnings": {
                    "test_pattern": {
                        "pattern": "test",
                        "category": "test",
                        "severity": "high"
                    }
                }
            }
            with open(os.path.join(tmpdir, "warning_catalog.json"),
                      'w') as f:
                json.dump(warning_catalog, f)

            loader = PatternLoader(data_dir=tmpdir)
            _, caution, _ = loader.load_all_patterns()

            # Should return empty dict for missing caution file
            assert caution == {}, "Should return empty dict for missing file"

    def test_missing_typo_messages_file(self):
        """Test handling of missing typo_messages.json file."""
        # Create temp directory with only warning_catalog.json
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create minimal warning_catalog.json
            warning_catalog = {
                "version": "1.0",
                "warnings": {
                    "test_pattern": {
                        "pattern": "test",
                        "category": "test",
                        "severity": "high"
                    }
                }
            }
            with open(os.path.join(tmpdir, "warning_catalog.json"),
                      'w') as f:
                json.dump(warning_catalog, f)

            loader = PatternLoader(data_dir=tmpdir)
            _, _, typo = loader.load_all_patterns()

            # Should return empty dict for missing typo file
            assert typo == {}, "Should return empty dict for missing file"

    def test_invalid_json_syntax_warning_catalog(self):
        """Test handling of invalid JSON syntax in warning_catalog.json."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create file with invalid JSON
            invalid_json_path = os.path.join(tmpdir, "warning_catalog.json")
            with open(invalid_json_path, 'w') as f:
                f.write("{ invalid json syntax }")

            loader = PatternLoader(data_dir=tmpdir)
            dangerous, _, _ = loader.load_all_patterns()

            # Should return empty dict for invalid JSON
            assert dangerous == {}, "Should return empty dict for invalid JSON"

    def test_invalid_json_syntax_caution_catalog(self):
        """Test handling of invalid JSON syntax in caution_catalog.json."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create valid warning_catalog.json
            warning_catalog = {
                "version": "1.0",
                "warnings": {
                    "test_pattern": {
                        "pattern": "test",
                        "category": "test",
                        "severity": "high"
                    }
                }
            }
            with open(os.path.join(tmpdir, "warning_catalog.json"),
                      'w') as f:
                json.dump(warning_catalog, f)

            # Create invalid caution_catalog.json
            invalid_json_path = os.path.join(tmpdir, "caution_catalog.json")
            with open(invalid_json_path, 'w') as f:
                f.write("{ invalid json }")

            loader = PatternLoader(data_dir=tmpdir)
            _, caution, _ = loader.load_all_patterns()

            # Should return empty dict for invalid JSON
            assert caution == {}, "Should return empty dict for invalid JSON"

    def test_invalid_json_syntax_typo_messages(self):
        """Test handling of invalid JSON syntax in typo_messages.json."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create valid warning_catalog.json
            warning_catalog = {
                "version": "1.0",
                "warnings": {
                    "test_pattern": {
                        "pattern": "test",
                        "category": "test",
                        "severity": "high"
                    }
                }
            }
            with open(os.path.join(tmpdir, "warning_catalog.json"),
                      'w') as f:
                json.dump(warning_catalog, f)

            # Create invalid typo_messages.json
            invalid_json_path = os.path.join(tmpdir, "typo_messages.json")
            with open(invalid_json_path, 'w') as f:
                f.write("{ invalid json }")

            loader = PatternLoader(data_dir=tmpdir)
            _, _, typo = loader.load_all_patterns()

            # Should return empty dict for invalid JSON
            assert typo == {}, "Should return empty dict for invalid JSON"

    def test_missing_pattern_field_in_warning(self):
        """Test handling of missing 'pattern' field in warning entry."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create warning_catalog.json with missing pattern field
            warning_catalog = {
                "version": "1.0",
                "warnings": {
                    "valid_pattern": {
                        "pattern": "test.*pattern",
                        "category": "test",
                        "severity": "high"
                    },
                    "missing_pattern": {
                        # No pattern field
                        "category": "test",
                        "severity": "high"
                    }
                }
            }
            with open(os.path.join(tmpdir, "warning_catalog.json"),
                      'w') as f:
                json.dump(warning_catalog, f)

            loader = PatternLoader(data_dir=tmpdir)
            dangerous, _, _ = loader.load_all_patterns()

            # Should load valid pattern but skip invalid one
            assert "valid_pattern" in dangerous, "Should load valid pattern"
            assert "missing_pattern" not in dangerous, \
                "Should skip pattern without 'pattern' field"

    def test_missing_pattern_field_in_caution(self):
        """Test handling of missing 'pattern' field in caution entry."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create valid warning_catalog.json
            warning_catalog = {
                "version": "1.0",
                "warnings": {
                    "test": {
                        "pattern": "test",
                        "category": "test",
                        "severity": "high"
                    }
                }
            }
            with open(os.path.join(tmpdir, "warning_catalog.json"),
                      'w') as f:
                json.dump(warning_catalog, f)

            # Create caution_catalog.json with missing pattern field
            caution_catalog = {
                "version": "1.0",
                "cautions": {
                    "valid_caution": {
                        "pattern": "sudo.*su",
                        "risk": "test"
                    },
                    "missing_pattern": {
                        # No pattern field
                        "risk": "test"
                    }
                }
            }
            with open(os.path.join(tmpdir, "caution_catalog.json"),
                      'w') as f:
                json.dump(caution_catalog, f)

            loader = PatternLoader(data_dir=tmpdir)
            _, caution, _ = loader.load_all_patterns()

            # Should load valid pattern but skip invalid one
            assert "valid_caution" in caution, "Should load valid pattern"
            assert "missing_pattern" not in caution, \
                "Should skip pattern without 'pattern' field"

    def test_missing_pattern_field_in_typo(self):
        """Test handling of missing 'pattern' field in typo entry."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create valid warning_catalog.json
            warning_catalog = {
                "version": "1.0",
                "warnings": {
                    "test": {
                        "pattern": "test",
                        "category": "test",
                        "severity": "high"
                    }
                }
            }
            with open(os.path.join(tmpdir, "warning_catalog.json"),
                      'w') as f:
                json.dump(warning_catalog, f)

            # Create typo_messages.json with missing pattern field
            typo_messages = {
                "version": "1.0",
                "typos": {
                    "valid_typo": {
                        "pattern": "^sl$",
                        "correct": "ls",
                        "message": "test"
                    },
                    "missing_pattern": {
                        # No pattern field
                        "correct": "cd",
                        "message": "test"
                    }
                }
            }
            with open(os.path.join(tmpdir, "typo_messages.json"),
                      'w') as f:
                json.dump(typo_messages, f)

            loader = PatternLoader(data_dir=tmpdir)
            _, _, typo = loader.load_all_patterns()

            # Should load valid pattern but skip invalid one
            assert "valid_typo" in typo, "Should load valid pattern"
            assert "missing_pattern" not in typo, \
                "Should skip pattern without 'pattern' field"

    def test_pattern_specificity_sorting(self):
        """Test that patterns are sorted by specificity."""
        loader = PatternLoader()
        dangerous, _, _ = loader.load_all_patterns()

        # Get pattern names as list
        pattern_names = list(dangerous.keys())

        # Verify system_modify comes before overwrite_file
        if "system_modify" in pattern_names and \
           "overwrite_file" in pattern_names:
            system_idx = pattern_names.index("system_modify")
            overwrite_idx = pattern_names.index("overwrite_file")
            assert system_idx < overwrite_idx, \
                "system_modify should be checked before overwrite_file"

    def test_default_values_for_missing_fields(self):
        """Test that default values are used for missing optional fields."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create pattern with minimal fields
            warning_catalog = {
                "version": "1.0",
                "warnings": {
                    "minimal_pattern": {
                        "pattern": "test.*pattern"
                        # Missing category, severity, ascii_art
                    }
                }
            }
            with open(os.path.join(tmpdir, "warning_catalog.json"),
                      'w') as f:
                json.dump(warning_catalog, f)

            loader = PatternLoader(data_dir=tmpdir)
            dangerous, _, _ = loader.load_all_patterns()

            # Should load with default values
            assert "minimal_pattern" in dangerous
            pattern = dangerous["minimal_pattern"]
            assert pattern["category"] == "unknown", \
                "Should use default category"
            assert pattern["severity"] == "medium", \
                "Should use default severity"
            assert pattern["art_file"] == "default.txt", \
                "Should use default art_file"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
