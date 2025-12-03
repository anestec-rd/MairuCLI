"""
Educational content loader for MairuCLI.

Loads command breakdowns, simulations, and incident stories from JSON files.
"""

import json
import os
from pathlib import Path
from typing import Dict, Optional, List


class EducationalLoader:
    """Load educational content from JSON files."""

    def __init__(self, base_path: str = "data/educational"):
        """
        Initialize educational content loader.

        Args:
            base_path: Base directory for educational content
        """
        # Convert to absolute path to handle cd command changes
        if not Path(base_path).is_absolute():
            # Get the project root (where src/ is located)
            project_root = Path(__file__).parent.parent.parent
            self.base_path = project_root / base_path
        else:
            self.base_path = Path(base_path)
        self.breakdowns_cache: Dict[str, Dict] = {}
        self.simulations_cache: Dict[str, Dict] = {}
        self.incidents_cache: Dict[str, Dict] = {}

    def load_breakdown(self, pattern_name: str) -> Optional[Dict]:
        """
        Load command breakdown for a pattern.

        Args:
            pattern_name: Name of the pattern (e.g., "rm_dangerous")

        Returns:
            Dictionary with breakdown data, or None if not found
        """
        # Check cache first
        if pattern_name in self.breakdowns_cache:
            return self.breakdowns_cache[pattern_name]

        # Load from file
        breakdown_path = self.base_path / "command_breakdowns" / f"{pattern_name}.json"

        try:
            with open(breakdown_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.breakdowns_cache[pattern_name] = data
                return data
        except FileNotFoundError:
            return None
        except json.JSONDecodeError as e:
            print(f"Warning: Invalid JSON in {breakdown_path}: {e}")
            return None

    def load_simulation(self, pattern_name: str) -> Optional[Dict]:
        """
        Load timeline simulation for a pattern.

        Args:
            pattern_name: Name of the pattern (e.g., "rm_dangerous")

        Returns:
            Dictionary with simulation data, or None if not found
        """
        # Check cache first
        if pattern_name in self.simulations_cache:
            return self.simulations_cache[pattern_name]

        # Load from file
        simulation_path = self.base_path / "simulations" / f"{pattern_name}.json"

        try:
            with open(simulation_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.simulations_cache[pattern_name] = data
                return data
        except FileNotFoundError:
            return None
        except json.JSONDecodeError as e:
            print(f"Warning: Invalid JSON in {simulation_path}: {e}")
            return None

    def load_incident(self, incident_name: str) -> Optional[Dict]:
        """
        Load incident story.

        Args:
            incident_name: Name of the incident (e.g., "gitlab_2017")

        Returns:
            Dictionary with incident data, or None if not found
        """
        # Check cache first
        if incident_name in self.incidents_cache:
            return self.incidents_cache[incident_name]

        # Load from file
        incident_path = self.base_path / "incidents" / f"{incident_name}.json"

        try:
            with open(incident_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.incidents_cache[incident_name] = data
                return data
        except FileNotFoundError:
            return None
        except json.JSONDecodeError as e:
            print(f"Warning: Invalid JSON in {incident_path}: {e}")
            return None

    def get_related_incidents(self, pattern_name: str) -> List[str]:
        """
        Get list of related incident names for a pattern.

        Args:
            pattern_name: Name of the pattern

        Returns:
            List of incident names
        """
        breakdown = self.load_breakdown(pattern_name)
        if breakdown and 'related_incidents' in breakdown:
            return breakdown['related_incidents']
        return []
