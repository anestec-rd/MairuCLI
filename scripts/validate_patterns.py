#!/usr/bin/env python3
"""
Pattern validation tool for MairuCLI.

This script validates all JSON pattern files against their schemas
and reports any validation errors.

Usage:
    python scripts/validate_patterns.py
"""

import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.interceptor import PatternLoader, JSONSCHEMA_AVAILABLE


def main():
    """Validate all pattern files."""
    print("=" * 60)
    print("MairuCLI Pattern Validation Tool")
    print("=" * 60)
    print()

    if not JSONSCHEMA_AVAILABLE:
        print("❌ Error: jsonschema library not installed")
        print("Install with: pip install jsonschema")
        return 1

    # Create loader with validation enabled
    loader = PatternLoader(validate_schema=True)

    print("Loading and validating patterns...")
    print()

    # Load all patterns (validation happens during load)
    dangerous, caution, typo = loader.load_all_patterns()

    # Report results
    print("=" * 60)
    print("Validation Results")
    print("=" * 60)
    print()

    success = True

    # Check dangerous patterns
    if dangerous:
        print(f"✅ warning_catalog.json: {len(dangerous)} patterns loaded")
    else:
        print("❌ warning_catalog.json: No patterns loaded (check errors above)")
        success = False

    # Check caution patterns
    if caution:
        print(f"✅ caution_catalog.json: {len(caution)} patterns loaded")
    else:
        print("⚠️  caution_catalog.json: No patterns loaded (optional)")

    # Check typo patterns
    if typo:
        print(f"✅ typo_messages.json: {len(typo)} patterns loaded")
    else:
        print("⚠️  typo_messages.json: No patterns loaded (optional)")

    print()

    if success:
        print("✅ All required pattern files validated successfully!")
        return 0
    else:
        print("❌ Validation failed. Check errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
