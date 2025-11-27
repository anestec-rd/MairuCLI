"""
Script to add pattern fields to warning_catalog.json from interceptor.py

This migrates regex patterns from code to JSON for data-driven architecture.
"""

import json
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.interceptor import DANGEROUS_PATTERNS

def add_patterns_to_catalog():
    """Add pattern fields to warning_catalog.json."""

    # Load current catalog
    catalog_path = "data/warnings/warning_catalog.json"
    with open(catalog_path, 'r', encoding='utf-8') as f:
        catalog = json.load(f)

    # Add patterns to each warning
    updated_count = 0
    for pattern_name, pattern_data in DANGEROUS_PATTERNS.items():
        if pattern_name in catalog['warnings']:
            # Add pattern field (escape backslashes for JSON)
            catalog['warnings'][pattern_name]['pattern'] = pattern_data['pattern']
            updated_count += 1
            print(f"✅ Added pattern to: {pattern_name}")
        else:
            print(f"⚠️  Warning not found in catalog: {pattern_name}")

    # Save updated catalog
    with open(catalog_path, 'w', encoding='utf-8') as f:
        json.dump(catalog, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Updated {updated_count} patterns in {catalog_path}")
    print("✅ Patterns are now data-driven!")

if __name__ == "__main__":
    add_patterns_to_catalog()
