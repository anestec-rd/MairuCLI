"""
Unit tests for src/display/educational_loader.py
"""

import pytest
import json
from pathlib import Path
from src.display.educational_loader import EducationalLoader


class TestEducationalLoader:
    """Test suite for EducationalLoader."""

    def test_init(self):
        """Test EducationalLoader initialization."""
        loader = EducationalLoader()
        assert loader.base_path == Path("data/educational")
        assert loader.breakdowns_cache == {}
        assert loader.simulations_cache == {}
        assert loader.incidents_cache == {}

    def test_load_breakdown_success(self):
        """Test loading a valid breakdown file."""
        loader = EducationalLoader()
        breakdown = loader.load_breakdown("rm_dangerous")

        assert breakdown is not None
        assert "command" in breakdown
        assert "parts" in breakdown
        assert isinstance(breakdown["parts"], list)

    def test_load_breakdown_caching(self):
        """Test that breakdowns are cached after first load."""
        loader = EducationalLoader()

        # First load
        breakdown1 = loader.load_breakdown("rm_dangerous")
        assert "rm_dangerous" in loader.breakdowns_cache

        # Second load should use cache
        breakdown2 = loader.load_breakdown("rm_dangerous")
        assert breakdown1 is breakdown2  # Same object reference

    def test_load_breakdown_missing_file(self):
        """Test loading a non-existent breakdown file."""
        loader = EducationalLoader()
        breakdown = loader.load_breakdown("nonexistent_pattern")

        assert breakdown is None

    def test_load_simulation_success(self):
        """Test loading a valid simulation file."""
        loader = EducationalLoader()
        simulation = loader.load_simulation("rm_dangerous")

        assert simulation is not None
        assert "timeline" in simulation
        assert isinstance(simulation["timeline"], list)

    def test_load_simulation_caching(self):
        """Test that simulations are cached after first load."""
        loader = EducationalLoader()

        # First load
        simulation1 = loader.load_simulation("rm_dangerous")
        assert "rm_dangerous" in loader.simulations_cache

        # Second load should use cache
        simulation2 = loader.load_simulation("rm_dangerous")
        assert simulation1 is simulation2  # Same object reference

    def test_load_simulation_missing_file(self):
        """Test loading a non-existent simulation file."""
        loader = EducationalLoader()
        simulation = loader.load_simulation("nonexistent_pattern")

        assert simulation is None

    def test_load_incident_success(self):
        """Test loading a valid incident file."""
        loader = EducationalLoader()
        incident = loader.load_incident("gitlab_2017")

        assert incident is not None
        assert "title" in incident
        assert "company" in incident
        assert "date" in incident
        assert "what_happened" in incident

    def test_load_incident_caching(self):
        """Test that incidents are cached after first load."""
        loader = EducationalLoader()

        # First load
        incident1 = loader.load_incident("gitlab_2017")
        assert "gitlab_2017" in loader.incidents_cache

        # Second load should use cache
        incident2 = loader.load_incident("gitlab_2017")
        assert incident1 is incident2  # Same object reference

    def test_load_incident_missing_file(self):
        """Test loading a non-existent incident file."""
        loader = EducationalLoader()
        incident = loader.load_incident("nonexistent_incident")

        assert incident is None

    def test_get_related_incidents(self):
        """Test getting related incidents for a pattern."""
        loader = EducationalLoader()

        # Load breakdown that has related incidents
        breakdown = loader.load_breakdown("rm_dangerous")
        if breakdown and "related_incidents" in breakdown:
            related = loader.get_related_incidents("rm_dangerous")
            assert isinstance(related, list)
        else:
            # If no related incidents field, should return empty list
            related = loader.get_related_incidents("rm_dangerous")
            assert related == []

    def test_get_related_incidents_missing_breakdown(self):
        """Test getting related incidents for non-existent pattern."""
        loader = EducationalLoader()
        related = loader.get_related_incidents("nonexistent_pattern")

        assert related == []

    def test_malformed_json_handling(self, tmp_path):
        """Test handling of malformed JSON files."""
        # Create a temporary malformed JSON file
        test_file = tmp_path / "command_breakdowns" / "bad.json"
        test_file.parent.mkdir(parents=True, exist_ok=True)
        test_file.write_text("{ invalid json }")

        # Create loader with temporary path
        loader = EducationalLoader()
        loader.base_path = tmp_path

        # Should return None for malformed JSON
        breakdown = loader.load_breakdown("bad")
        assert breakdown is None
