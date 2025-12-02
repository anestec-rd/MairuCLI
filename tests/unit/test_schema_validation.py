"""
Unit tests for JSON schema validation in PatternLoader.
"""

import json
import os
import tempfile
import pytest
from src.interceptor import PatternLoader, JSONSCHEMA_AVAILABLE


class TestSchemaValidation:
    """Test suite for JSON schema validation."""

    def test_valid_warning_catalog_passes_validation(self):
        """Test that valid warning_catalog.json passes schema validation."""
        loader = PatternLoader(validate_schema=True)
        dangerous, _, _ = loader.load_all_patterns()

        # Should load patterns successfully
        assert len(dangerous) > 0
        assert 'rm_dangerous' in dangerous

    def test_valid_caution_catalog_passes_validation(self):
        """Test that valid caution_catalog.json passes schema validation."""
        loader = PatternLoader(validate_schema=True)
        _, caution, _ = loader.load_all_patterns()

        # Should load patterns successfully
        assert len(caution) > 0
        assert 'sudo_shell' in caution

    def test_valid_typo_messages_passes_validation(self):
        """Test that valid typo_messages.json passes schema validation."""
        loader = PatternLoader(validate_schema=True)
        _, _, typo = loader.load_all_patterns()

        # Should load patterns successfully
        assert len(typo) > 0
        assert 'sl' in typo

    def test_validation_can_be_disabled(self):
        """Test that schema validation can be disabled."""
        loader = PatternLoader(validate_schema=False)
        assert loader.validate_schema is False

        # Should still load patterns
        dangerous, caution, typo = loader.load_all_patterns()
        assert len(dangerous) > 0

    @pytest.mark.skipif(not JSONSCHEMA_AVAILABLE, reason="jsonschema not installed")
    def test_invalid_warning_catalog_reports_error(self, tmp_path, capsys):
        """Test that invalid warning_catalog.json reports validation error."""
        # Create invalid catalog (missing required 'pattern' field)
        invalid_catalog = {
            "version": "1.0",
            "warnings": {
                "test_pattern": {
                    "category": "deletion",
                    "severity": "critical"
                    # Missing 'pattern' field
                }
            }
        }

        # Write to temp file
        catalog_path = tmp_path / "warning_catalog.json"
        with open(catalog_path, 'w') as f:
            json.dump(invalid_catalog, f)

        # Create loader with temp directory
        loader = PatternLoader(data_dir=str(tmp_path), validate_schema=True)
        dangerous, _, _ = loader.load_all_patterns()

        # Should report validation error
        captured = capsys.readouterr()
        assert "Validation error" in captured.out or "Warning" in captured.out

    @pytest.mark.skipif(not JSONSCHEMA_AVAILABLE, reason="jsonschema not installed")
    def test_invalid_caution_catalog_reports_error(self, tmp_path, capsys):
        """Test that invalid caution_catalog.json reports validation error."""
        # Create invalid catalog (missing required 'considerations' field)
        invalid_catalog = {
            "version": "1.0",
            "cautions": {
                "test_caution": {
                    "pattern": "test",
                    "category": "security",
                    "severity": "medium",
                    "risk": "Test risk",
                    "impact": "Test impact"
                    # Missing 'considerations' field
                }
            }
        }

        # Write to temp file
        catalog_path = tmp_path / "caution_catalog.json"
        with open(catalog_path, 'w') as f:
            json.dump(invalid_catalog, f)

        # Create loader with temp directory
        loader = PatternLoader(data_dir=str(tmp_path), validate_schema=True)
        _, caution, _ = loader.load_all_patterns()

        # Should report validation error
        captured = capsys.readouterr()
        assert "Validation error" in captured.out or "Warning" in captured.out

    @pytest.mark.skipif(not JSONSCHEMA_AVAILABLE, reason="jsonschema not installed")
    def test_invalid_typo_messages_reports_error(self, tmp_path, capsys):
        """Test that invalid typo_messages.json reports validation error."""
        # Create invalid typo messages (missing required 'message' field)
        invalid_typos = {
            "version": "1.0",
            "typos": {
                "test_typo": {
                    "pattern": "^test$",
                    "correct": "test_correct"
                    # Missing 'message' field
                }
            }
        }

        # Write to temp file
        typo_path = tmp_path / "typo_messages.json"
        with open(typo_path, 'w') as f:
            json.dump(invalid_typos, f)

        # Create loader with temp directory
        loader = PatternLoader(data_dir=str(tmp_path), validate_schema=True)
        _, _, typo = loader.load_all_patterns()

        # Should report validation error
        captured = capsys.readouterr()
        assert "Validation error" in captured.out or "Warning" in captured.out

    def test_missing_schema_file_skips_validation(self, tmp_path, capsys):
        """Test that missing schema file skips validation gracefully."""
        # Create valid catalog
        valid_catalog = {
            "version": "1.0",
            "warnings": {
                "test_pattern": {
                    "pattern": "test",
                    "category": "deletion",
                    "severity": "critical"
                }
            }
        }

        # Write to temp file (no schema directory)
        catalog_path = tmp_path / "warning_catalog.json"
        with open(catalog_path, 'w') as f:
            json.dump(valid_catalog, f)

        # Create loader with temp directory (no schemas)
        loader = PatternLoader(data_dir=str(tmp_path), validate_schema=True)
        dangerous, _, _ = loader.load_all_patterns()

        # Should load patterns despite missing schema
        assert len(dangerous) > 0

        # Should warn about missing schema
        captured = capsys.readouterr()
        assert "Schema file" in captured.out or "not found" in captured.out

    def test_schema_validation_with_extra_fields(self, tmp_path):
        """Test that extra fields in JSON are handled correctly."""
        # Create catalog with extra field
        catalog_with_extra = {
            "version": "1.0",
            "warnings": {
                "test_pattern": {
                    "pattern": "test",
                    "category": "deletion",
                    "severity": "critical",
                    "extra_field": "should be ignored"  # Extra field
                }
            }
        }

        # Write to temp file
        catalog_path = tmp_path / "warning_catalog.json"
        with open(catalog_path, 'w') as f:
            json.dump(catalog_with_extra, f)

        # Copy schema to temp directory
        schema_dir = tmp_path / "schemas"
        schema_dir.mkdir()

        import shutil
        shutil.copy(
            "data/warnings/schemas/warning_catalog_schema.json",
            schema_dir / "warning_catalog_schema.json"
        )

        # Create loader with temp directory
        loader = PatternLoader(data_dir=str(tmp_path), validate_schema=True)
        dangerous, _, _ = loader.load_all_patterns()

        # Should load patterns (extra fields allowed in pattern objects)
        assert len(dangerous) > 0

    def test_schema_validation_with_invalid_enum_value(self, tmp_path, capsys):
        """Test that invalid enum values are caught by validation."""
        # Create catalog with invalid severity
        invalid_catalog = {
            "version": "1.0",
            "warnings": {
                "test_pattern": {
                    "pattern": "test",
                    "category": "deletion",
                    "severity": "super_critical"  # Invalid enum value
                }
            }
        }

        # Write to temp file
        catalog_path = tmp_path / "warning_catalog.json"
        with open(catalog_path, 'w') as f:
            json.dump(invalid_catalog, f)

        # Copy schema to temp directory
        schema_dir = tmp_path / "schemas"
        schema_dir.mkdir()

        import shutil
        shutil.copy(
            "data/warnings/schemas/warning_catalog_schema.json",
            schema_dir / "warning_catalog_schema.json"
        )

        # Create loader with temp directory
        loader = PatternLoader(data_dir=str(tmp_path), validate_schema=True)
        dangerous, _, _ = loader.load_all_patterns()

        # Should report validation error
        captured = capsys.readouterr()
        if JSONSCHEMA_AVAILABLE:
            assert "Validation error" in captured.out or "Warning" in captured.out
