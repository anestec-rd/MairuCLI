"""
Content loader for MairuCLI display system.

Loads warning messages, variations, and metadata from JSON files.
"""

import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional

from src.project_paths import get_warnings_dir


class ContentLoader:
    """Loads and manages warning content from data files."""

    def __init__(self, data_dir: Optional[Path] = None):
        """
        Initialize content loader.

        Args:
            data_dir: Path to data directory (defaults to project data/)
        """
        if data_dir is None:
            # Use absolute path from project_paths utility
            self.data_dir = get_warnings_dir().parent
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
        fallback = self._get_fallback_warning(pattern_name)
        return warnings.get(pattern_name, fallback)

    def get_variations(
        self,
        variation_set: str,
        pattern_category: Optional[str] = None
    ) -> List[Tuple[str, str]]:
        """
        Get variations for a pattern using merge strategy.

        Strategy:
        1. Get category variations (8 variations)
        2. Get pattern-specific variations (0-4 variations)
        3. Merge both lists (8-12 total)
        4. Fallback to legacy if needed

        Args:
            variation_set: Variation set name (e.g., 'rm_root')
            pattern_category: Category name (e.g., 'deletion', 'permission')

        Returns:
            List of (title, subtitle) tuples (merged from category + pattern)
        """
        # Check cache first
        cache_key = f"{variation_set}:{pattern_category}"
        if cache_key in self._variations:
            return self._variations[cache_key]

        merged_variations = []

        # Step 1: Get category variations (8 variations)
        if pattern_category:
            category_vars_path = (
                self.warnings_dir / "category_variations.json"
            )
            try:
                with open(category_vars_path, "r", encoding="utf-8") as f:
                    category_variations = json.load(f)

                categories = category_variations.get("categories", {})
                if pattern_category in categories:
                    cat_data = categories[pattern_category]
                    variations_list = cat_data["variations"]
                    category_vars = [
                        (v["title"], v["subtitle"])
                        for v in variations_list
                    ]
                    merged_variations.extend(category_vars)
            except (FileNotFoundError, json.JSONDecodeError, KeyError):
                pass  # Continue without category variations

        # Step 2: Get pattern-specific variations (0-4 variations)
        pattern_vars_path = (
            self.warnings_dir / "pattern_variations.json"
        )
        try:
            with open(pattern_vars_path, "r", encoding="utf-8") as f:
                pattern_variations = json.load(f)

            patterns = pattern_variations.get("patterns", {})
            if variation_set in patterns:
                pattern_data = patterns[variation_set]
                variations_list = pattern_data["variations"]
                pattern_vars = [
                    (v["title"], v["subtitle"])
                    for v in variations_list
                ]
                merged_variations.extend(pattern_vars)
        except (FileNotFoundError, json.JSONDecodeError, KeyError):
            pass  # Continue without pattern-specific variations

        # Step 3: If we got variations, cache and return
        if merged_variations:
            self._variations[cache_key] = merged_variations
            return merged_variations

        # Step 4: Fallback to legacy danger_variations.json
        legacy_path = self.warnings_dir / "danger_variations.json"
        try:
            with open(legacy_path, "r", encoding="utf-8") as f:
                legacy_variations = json.load(f)

            if variation_set in legacy_variations:
                variations_list = legacy_variations[variation_set]
                result = [
                    (v["title"], v["subtitle"])
                    for v in variations_list
                ]
                self._variations[cache_key] = result
                return result
        except (FileNotFoundError, json.JSONDecodeError, KeyError):
            pass  # Continue to fallback

        # Step 5: Ultimate fallback
        return self._get_fallback_variations(variation_set)

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
        default = [("DANGER!", "(This command is risky)")]
        return fallbacks.get(category, default)
