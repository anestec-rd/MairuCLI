"""
Manual test to verify generic typo detection covers removed patterns.
"""

from src.interceptor import check_generic_typo, COMMON_COMMANDS

def test_removed_patterns():
    """Test that removed individual patterns are covered by generic detection."""

    print("Testing Generic Typo Detection Coverage")
    print("=" * 60)
    print()

    # Patterns we removed from TYPO_PATTERNS (now covered by generic)
    removed_patterns = [
        ("mkdi", "mkdir", "missing last char"),
        ("gre", "grep", "missing last char"),
    ]

    print("Removed patterns (should be detected by generic system):")
    print("-" * 60)

    all_passed = True
    for typo, expected_correct, reason in removed_patterns:
        is_typo, correct_cmd, message = check_generic_typo(typo)

        if is_typo and correct_cmd == expected_correct:
            print(f"✅ {typo:10} -> {correct_cmd:10} ({reason})")
            print(f"   Message: {message}")
        else:
            print(f"❌ {typo:10} -> FAILED (expected {expected_correct})")
            all_passed = False
        print()

    print()
    print("Patterns kept in TYPO_PATTERNS (special handling):")
    print("-" * 60)

    special_patterns = [
        ("sl", "ls", "Special 'Choo choo' message"),
        ("gti", "git", "Character transposition + car joke"),
        ("tou", "touch", "Missing 2 chars (special case)"),
        ("cd..", "cd ..", "Space missing pattern"),
        ("ls-la", "ls -[options]", "Space missing pattern"),
        ("git-status", "git [command]", "Space missing pattern"),
    ]

    for typo, expected, reason in special_patterns:
        print(f"⭐ {typo:15} -> {expected:20} ({reason})")

    print()
    print("=" * 60)
    print(f"Common commands covered: {len(COMMON_COMMANDS)}")
    print(f"Commands: {', '.join(COMMON_COMMANDS[:10])}...")
    print()

    if all_passed:
        print("✅ All removed patterns are covered by generic detection!")
    else:
        print("❌ Some patterns are not covered!")

    return all_passed


if __name__ == "__main__":
    test_removed_patterns()
