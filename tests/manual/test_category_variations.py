"""
Manual test script for category-based variations system.

Run this to verify the new variation system works correctly.
"""

from src.display.content_loader import ContentLoader


def test_pattern_specific():
    """Test patterns with specific variations."""
    loader = ContentLoader()

    print("=" * 60)
    print("PATTERN-SPECIFIC VARIATIONS TEST")
    print("=" * 60)

    patterns = [
        ("rm_root", "deletion", "Should have 14 unique variations"),
        ("chmod_777", "permission", "Should have 9 unique variations"),
        ("chmod_000", "permission", "Should have 9 ghost/lock themed variations"),
        ("data_destroyer", "deletion", "Should have 9 unique variations"),
        ("fork_bomb", "system", "Should have 8 party/multiplication variations"),
        ("kernel_panic", "system", "Should have 8 overexcited kernel variations"),
    ]

    for pattern, category, description in patterns:
        variations = loader.get_variations(pattern, category)
        print(f"\n{pattern} ({category}): {len(variations)} variations")
        print(f"  Expected: {description}")
        print(f"  Sample: {variations[0][0]} - {variations[0][1]}")
        assert len(variations) > 0, f"No variations for {pattern}"


def test_category_fallback():
    """Test patterns that use category variations."""
    loader = ContentLoader()

    print("\n" + "=" * 60)
    print("CATEGORY VARIATIONS TEST")
    print("=" * 60)

    # drop_database should use database category
    variations = loader.get_variations("drop_database", "database")
    print(f"\ndrop_database (database): {len(variations)} variations")
    print(f"  Sample: {variations[0][0]} - {variations[0][1]}")
    assert len(variations) > 0

    # disk_destroyer should use disk category
    variations = loader.get_variations("disk_destroyer", "disk")
    print(f"\ndisk_destroyer (disk): {len(variations)} variations")
    print(f"  Sample: {variations[0][0]} - {variations[0][1]}")
    assert len(variations) > 0


def test_all_patterns():
    """Test all 11 danger patterns."""
    loader = ContentLoader()

    print("\n" + "=" * 60)
    print("ALL PATTERNS TEST")
    print("=" * 60)

    patterns = [
        ("rm_dangerous", "rm_root", "deletion"),
        ("chmod_777", "chmod_777", "permission"),
        ("chmod_000", "chmod_000", "permission"),
        ("dd_zero", "zero_wipe", "disk"),
        ("drop_database", "drop_database", "database"),
        ("fork_bomb", "fork_bomb", "system"),
        ("redirect_to_disk", "disk_destroyer", "disk"),
        ("mkfs_disk", "disk_destroyer", "disk"),
        ("mv_to_null", "data_void", "deletion"),
        ("overwrite_file", "file_eraser", "deletion"),
        ("dd_random", "disk_destroyer", "disk"),
        ("kernel_panic", "kernel_panic", "system"),
    ]

    print(f"\nTesting {len(patterns)} patterns...")

    for pattern_name, variation_set, category in patterns:
        variations = loader.get_variations(variation_set, category)
        status = "✓" if len(variations) > 0 else "✗"
        print(f"{status} {pattern_name:20} -> {variation_set:20} ({category:10}): {len(variations)} vars")
        assert len(variations) > 0, f"No variations for {pattern_name}"


def test_variation_quality():
    """Test that all variations have proper format."""
    loader = ContentLoader()

    print("\n" + "=" * 60)
    print("VARIATION QUALITY TEST")
    print("=" * 60)

    patterns = [
        ("rm_root", "deletion"),
        ("chmod_777", "permission"),
        ("drop_database", "database"),
        ("fork_bomb", "system"),
        ("disk_destroyer", "disk"),
    ]

    for variation_set, category in patterns:
        variations = loader.get_variations(variation_set, category)

        for i, (title, subtitle) in enumerate(variations):
            # Check format
            assert isinstance(title, str), f"Title not string: {title}"
            assert isinstance(subtitle, str), f"Subtitle not string: {subtitle}"
            assert len(title) > 0, f"Empty title"
            assert len(subtitle) > 0, f"Empty subtitle"

            # Check subtitle has parentheses
            assert subtitle.startswith("(") and subtitle.endswith(")"), \
                f"Subtitle should have parentheses: {subtitle}"

        print(f"✓ {variation_set}: All {len(variations)} variations valid")


if __name__ == "__main__":
    try:
        test_pattern_specific()
        test_category_fallback()
        test_all_patterns()
        test_variation_quality()

        print("\n" + "=" * 60)
        print("✓ ALL TESTS PASSED!")
        print("=" * 60)
        print("\nCategory-based variation system is working correctly!")

    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}")
        exit(1)
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
