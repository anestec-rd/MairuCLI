"""
Unit tests for HelpGenerator class.
"""

import json
import pytest
import tempfile
from pathlib import Path
from src.builtins.mairu_commands import HelpGenerator


class TestHelpGenerator:
    """Test suite for HelpGenerator class."""

    @pytest.fixture
    def temp_data_dir(self):
        """Create temporary directory with test data files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            data_dir = Path(tmpdir) / "warnings"
            data_dir.mkdir()
            builtins_dir = Path(tmpdir) / "builtins"
            builtins_dir.mkdir()
            yield tmpdir

    @pytest.fixture
    def sample_warning_catalog(self, temp_data_dir):
        """Create sample warning catalog JSON."""
        catalog = {
            "version": "1.0",
            "warnings": {
                "rm_dangerous": {
                    "category": "deletion",
                    "severity": "critical",
                    "emoji": "fire",
                    "help_example": "rm -rf /",
                    "help_description": "Delete everything"
                },
                "chmod_777": {
                    "category": "permission",
                    "severity": "high",
                    "emoji": "unlock",
                    "help_example": "chmod 777 file",
                    "help_description": "Give everyone access"
                },
                "dd_zero": {
                    "category": "disk",
                    "severity": "critical",
                    "emoji": "bomb",
                    "help_example": "dd if=/dev/zero",
                    "help_description": "Write zeros to disk"
                }
            }
        }
        catalog_path = Path(temp_data_dir) / "warnings" / "warning_catalog.json"
        with open(catalog_path, 'w', encoding='utf-8') as f:
            json.dump(catalog, f)
        return catalog_path

    @pytest.fixture
    def sample_caution_catalog(self, temp_data_dir):
        """Create sample caution catalog JSON."""
        catalog = {
            "version": "1.0",
            "cautions": {
                "sudo_shell": {
                    "category": "privilege_escalation",
                    "severity": "medium",
                    "help_example": "sudo bash",
                    "help_description": "Enter root shell"
                },
                "chmod_permissive": {
                    "category": "permissions",
                    "severity": "medium",
                    "help_example": "chmod 666 file",
                    "help_description": "Make file world-writable"
                }
            }
        }
        catalog_path = Path(temp_data_dir) / "warnings" / "caution_catalog.json"
        with open(catalog_path, 'w', encoding='utf-8') as f:
            json.dump(catalog, f)
        return catalog_path

    def test_load_dangerous_patterns(self, temp_data_dir, sample_warning_catalog):
        """Test loading dangerous patterns from JSON."""
        help_gen = HelpGenerator(
            data_dir=str(Path(temp_data_dir) / "warnings")
        )
        lines = help_gen.generate_dangerous_commands_help()

        # Should have 3 patterns
        assert len(lines) == 3
        # Check that all patterns appear
        assert any("rm -rf /" in line for line in lines)
        assert any("chmod 777 file" in line for line in lines)
        assert any("dd if=/dev/zero" in line for line in lines)

    def test_load_caution_patterns(self, temp_data_dir, sample_caution_catalog):
        """Test loading caution patterns from JSON."""
        help_gen = HelpGenerator(
            data_dir=str(Path(temp_data_dir) / "warnings")
        )
        lines = help_gen.generate_caution_commands_help()

        # Should have 2 patterns
        assert len(lines) == 2
        # Check that all patterns appear
        assert any("sudo bash" in line for line in lines)
        assert any("chmod 666 file" in line for line in lines)

    def test_missing_warning_catalog(self, temp_data_dir):
        """Test handling missing warning catalog file."""
        help_gen = HelpGenerator(
            data_dir=str(Path(temp_data_dir) / "warnings")
        )
        lines = help_gen.generate_dangerous_commands_help()

        # Should return fallback message
        assert len(lines) == 1
        assert "No dangerous patterns loaded" in lines[0]

    def test_missing_caution_catalog(self, temp_data_dir):
        """Test handling missing caution catalog file."""
        help_gen = HelpGenerator(
            data_dir=str(Path(temp_data_dir) / "warnings")
        )
        lines = help_gen.generate_caution_commands_help()

        # Should return fallback message
        assert len(lines) == 1
        assert "No caution patterns loaded" in lines[0]

    def test_missing_help_example_field(self, temp_data_dir):
        """Test handling patterns without help_example field."""
        catalog = {
            "version": "1.0",
            "warnings": {
                "test_pattern": {
                    "category": "deletion",
                    "severity": "critical",
                    "emoji": "fire",
                    # Missing help_example
                    "help_description": "Test description"
                }
            }
        }
        catalog_path = Path(temp_data_dir) / "warnings" / "warning_catalog.json"
        with open(catalog_path, 'w', encoding='utf-8') as f:
            json.dump(catalog, f)

        help_gen = HelpGenerator(
            data_dir=str(Path(temp_data_dir) / "warnings")
        )
        lines = help_gen.generate_dangerous_commands_help()

        # Should use pattern name as fallback
        assert len(lines) == 1
        assert "test_pattern" in lines[0]

    def test_missing_help_description_field(self, temp_data_dir):
        """Test handling patterns without help_description field."""
        catalog = {
            "version": "1.0",
            "warnings": {
                "test_pattern": {
                    "category": "deletion",
                    "severity": "critical",
                    "emoji": "fire",
                    "help_example": "test command",
                    # Missing help_description
                }
            }
        }
        catalog_path = Path(temp_data_dir) / "warnings" / "warning_catalog.json"
        with open(catalog_path, 'w', encoding='utf-8') as f:
            json.dump(catalog, f)

        help_gen = HelpGenerator(
            data_dir=str(Path(temp_data_dir) / "warnings")
        )
        lines = help_gen.generate_dangerous_commands_help()

        # Should use fallback description
        assert len(lines) == 1
        assert "Dangerous command" in lines[0]

    def test_missing_emoji_field(self, temp_data_dir):
        """Test handling patterns without emoji field."""
        catalog = {
            "version": "1.0",
            "warnings": {
                "test_pattern": {
                    "category": "deletion",
                    "severity": "critical",
                    # Missing emoji
                    "help_example": "test command",
                    "help_description": "Test description"
                }
            }
        }
        catalog_path = Path(temp_data_dir) / "warnings" / "warning_catalog.json"
        with open(catalog_path, 'w', encoding='utf-8') as f:
            json.dump(catalog, f)

        help_gen = HelpGenerator(
            data_dir=str(Path(temp_data_dir) / "warnings")
        )
        lines = help_gen.generate_dangerous_commands_help()

        # Should use default fire emoji
        assert len(lines) == 1
        assert "🔥" in lines[0]

    def test_invalid_json_syntax(self, temp_data_dir):
        """Test handling invalid JSON syntax."""
        catalog_path = Path(temp_data_dir) / "warnings" / "warning_catalog.json"
        with open(catalog_path, 'w', encoding='utf-8') as f:
            f.write("{ invalid json }")

        help_gen = HelpGenerator(
            data_dir=str(Path(temp_data_dir) / "warnings")
        )
        lines = help_gen.generate_dangerous_commands_help()

        # Should return fallback message
        assert len(lines) == 1
        assert "No dangerous patterns loaded" in lines[0]

    def test_group_by_category(self, temp_data_dir, sample_warning_catalog):
        """Test grouping patterns by category."""
        help_gen = HelpGenerator(
            data_dir=str(Path(temp_data_dir) / "warnings")
        )
        patterns = help_gen._load_patterns('warning_catalog.json', 'warnings')
        grouped = help_gen._group_by_category(patterns)

        # Should have 3 categories
        assert "deletion" in grouped
        assert "permission" in grouped
        assert "disk" in grouped

        # Check counts
        assert len(grouped["deletion"]) == 1
        assert len(grouped["permission"]) == 1
        assert len(grouped["disk"]) == 1

    def test_real_warning_catalog(self):
        """Test with actual warning_catalog.json file."""
        help_gen = HelpGenerator()
        lines = help_gen.generate_dangerous_commands_help()

        # Should have multiple patterns
        assert len(lines) > 0
        # Should not be fallback message
        assert "No dangerous patterns loaded" not in lines[0]

    def test_real_caution_catalog(self):
        """Test with actual caution_catalog.json file."""
        help_gen = HelpGenerator()
        lines = help_gen.generate_caution_commands_help()

        # Should have multiple patterns
        assert len(lines) > 0
        # Should not be fallback message
        assert "No caution patterns loaded" not in lines[0]

    def test_all_dangerous_patterns_appear_in_help(self):
        """Test that all dangerous patterns from JSON appear in help."""
        help_gen = HelpGenerator()

        # Load patterns directly
        patterns = help_gen._load_patterns('warning_catalog.json', 'warnings')

        # Generate help
        lines = help_gen.generate_dangerous_commands_help()
        help_text = "\n".join(lines)

        # Check each pattern appears
        for pattern_name, pattern_data in patterns.items():
            example = pattern_data.get('help_example', pattern_name)
            assert example in help_text, \
                f"Pattern '{pattern_name}' not found in help"

    def test_all_caution_patterns_appear_in_help(self):
        """Test that all caution patterns from JSON appear in help."""
        help_gen = HelpGenerator()

        # Load patterns directly
        patterns = help_gen._load_patterns('caution_catalog.json', 'cautions')

        # Generate help
        lines = help_gen.generate_caution_commands_help()
        help_text = "\n".join(lines)

        # Check each pattern appears
        for pattern_name, pattern_data in patterns.items():
            example = pattern_data.get('help_example', pattern_name)
            assert example in help_text, \
                f"Pattern '{pattern_name}' not found in help"

    def test_help_formatting_alignment(self, temp_data_dir, sample_warning_catalog):
        """Test that help output has proper alignment."""
        help_gen = HelpGenerator(
            data_dir=str(Path(temp_data_dir) / "warnings")
        )
        lines = help_gen.generate_dangerous_commands_help()

        # All lines should have consistent formatting
        for line in lines:
            # Should have emoji, example, dash, description
            assert " - " in line

    def test_empty_warnings_key(self, temp_data_dir):
        """Test handling empty warnings key in JSON."""
        catalog = {
            "version": "1.0",
            "warnings": {}
        }
        catalog_path = Path(temp_data_dir) / "warnings" / "warning_catalog.json"
        with open(catalog_path, 'w', encoding='utf-8') as f:
            json.dump(catalog, f)

        help_gen = HelpGenerator(
            data_dir=str(Path(temp_data_dir) / "warnings")
        )
        lines = help_gen.generate_dangerous_commands_help()

        # Should return fallback message
        assert len(lines) == 1
        assert "No dangerous patterns loaded" in lines[0]

    def test_category_grouping_preserves_all_patterns(
        self, temp_data_dir, sample_warning_catalog
    ):
        """Test that category grouping doesn't lose any patterns."""
        help_gen = HelpGenerator(
            data_dir=str(Path(temp_data_dir) / "warnings")
        )
        patterns = help_gen._load_patterns('warning_catalog.json', 'warnings')
        grouped = help_gen._group_by_category(patterns)

        # Count total patterns in grouped result
        total_grouped = sum(len(items) for items in grouped.values())

        # Should match original count
        assert total_grouped == len(patterns)
