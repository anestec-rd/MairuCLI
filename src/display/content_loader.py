"""
Content loader for MairuCLI display system.

Loads warning messages, variations, and metadata from JSON files.
"""

import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional


class ContentLoader:
    """Loads and manages warning content from data files."""

    def __init__(self, data_dir: Optional[Path] = None):
        """
        Initialize content loader.

        Args:
            data_dir: Path to data directory (defaults to project data/)
        """
        if data_dir is None:
            # Default to data/ directory relative to project root
            self.data_dir = Path(__file__).parent.parent.parent / "data"
        else:
            self.data_dir = Path(data_dir)

        self.warnings_dir = self.data_dir / "warnings"
        self._catalog: Optional[Dict] = None
        self._variations: Dict[str, List[Tuple[str, str]]] = {}

    def load_catalog(self) -> Dict:
        """
        Load the master warning catalog.

        Returns:
            Dictionary with warning catalog data

        Raises:
            FileNotFoundError: If catalog file doesn't exist
            json.JSONDecodeError: If catalog file is invalid JSON
        """
        catalog_path = self.warnings_dir / "warning_catalog.json"

        try:
            with open(catalog_path, "r", encoding="utf-8") as f:
                self._catalog = json.load(f)
            return self._catalog
        except FileNotFoundError:
            # Return fallback catalog if file doesn't exist
            print(f"Warning: {catalog_path} not found, using fallback catalog")
            return self._get_fallback_catalog()
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON in {catalog_path}: {e}")
            return self._get_fallback_catalog()

    def get_warning_content(self, pattern_name: str) -> Dict:
        """
        Get warning content for a specific pattern.

        Args:
            pattern_name: Name of the pattern (e.g., 'rm_root')

        Returns:
            Dictionary with warning content
        """
        if self._catalog is None:
            self._catalog = self.load_catalog()

        warnings = self._catalog.get("warnings", {})
        return warnings.get(pattern_name, self._get_fallback_warning(pattern_name))

    def get_variations(self, category: str) -> List[Tuple[str, str]]:
        """
        Get all variations for a warning category.

        Args:
            category: Category name (e.g., 'rm_root', 'chmod_777')

        Returns:
            List of (title, subtitle) tuples
        """
        # Check cache first
        if category in self._variations:
            return self._variations[category]

        # Load from file
        variations_path = self.warnings_dir / "danger_variations.json"

        try:
            with open(variations_path, "r", encoding="utf-8") as f:
                all_variations = json.load(f)

            variations_list = all_variations.get(category, [])
            # Convert to list of tuples
            result = [(v["title"], v["subtitle"]) for v in variations_list]
            self._variations[category] = result
            return result

        except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
            print(f"Warning: Could not load variations for {category}: {e}")
            return self._get_fallback_variations(category)

    def validate_content(self, content: Dict) -> bool:
        """
        Validate content structure.

        Args:
            content: Content dictionary to validate

        Returns:
            True if valid, False otherwise
        """
        required_fields = ["category", "severity", "variation_set"]
        return all(field in content for field in required_fields)

    def _get_fallback_catalog(self) -> Dict:
        """Get fallback catalog when file is missing."""
        return {
            "version": "1.0",
            "warnings": {
                "rm_root": {
                    "category": "deletion",
                    "severity": "critical",
                    "variation_set": "rm_root",
                    "ascii_art": "fired.txt",
                    "color": "red",
                    "emoji": "fire"
                },
                "chmod_777": {
                    "category": "permission",
                    "severity": "high",
                    "variation_set": "chmod_777",
                    "ascii_art": "permission_denied.txt",
                    "color": "purple",
                    "emoji": "skull"
                }
            }
        }

    def _get_fallback_warning(self, pattern_name: str) -> Dict:
        """Get fallback warning content."""
        return {
            "category": "unknown",
            "severity": "high",
            "variation_set": "data_destroyer",
            "ascii_art": "fired.txt",
            "color": "red",
            "emoji": "fire"
        }

    def _get_fallback_variations(self, category: str) -> List[Tuple[str, str]]:
        """Get fallback variations."""
        fallbacks = {
            "rm_root": [
                ("YOU'RE FIRED!", "(And so is your entire filesystem!)"),
                ("GAME OVER!", "(No continues, no save points)")
            ],
            "chmod_777": [
                ("PERMISSION DENIED!", "(By your future self)"),
                ("SECURITY BREACH ALERT!", "(This is how hacks happen)")
            ],
            "data_destroyer": [
                ("DATA DESTROYER DETECTED!", "(This will not end well)"),
                ("DISK ANNIHILATOR!", "(Say goodbye to your data)")
            ]
        }
        return fallbacks.get(category, [("DANGER!", "(This command is risky)")])
