"""
Manual test for verifying educational message clarity and helpfulness.

This script displays system protection warnings and provides a checklist
for evaluating message quality.
"""

import sys
import os

# Add src to path
sys.path.insert(
    0,
    os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
)

from src.display.ascii_renderer import AsciiRenderer
from src.display.system_protection_warning import SystemProtectionWarning


def print_section(title: str):
    """Print a section header."""
    print()
    print("=" * 70)
    print(f"  {title}")
    print("=" * 70)
    print()


def print_checklist():
    """Print evaluation checklist."""
    print()
    print("📋 EVALUATION CHECKLIST")
    print("-" * 70)
    print()
    print("For each message, verify:")
    print()
    print("✓ CLARITY:")
    print("  [ ] Message is easy to understand")
    print("  [ ] Technical terms are explained")
    print("  [ ] No jargon without context")
    print("  [ ] Appropriate for beginners")
    print()
    print("✓ HELPFULNESS:")
    print("  [ ] Explains WHAT the directory contains")
    print("  [ ] Explains WHY it's protected")
    print("  [ ] Explains CONSEQUENCES of modification")
    print("  [ ] Provides ACTIONABLE alternatives")
    print()
    print("✓ TONE:")
    print("  [ ] Friendly and encouraging (not scary)")
    print("  [ ] Educational (not preachy)")
    print("  [ ] Halloween-themed but appropriate")
    print("  [ ] Respectful to user's learning journey")
    print()
    print("✓ COMPLETENESS:")
    print("  [ ] All necessary information provided")
    print("  [ ] Safe alternatives are specific")
    print("  [ ] User knows what to do next")
    print()
    print("-" * 70)
    print()


def test_critical_warnings():
    """Test critical-level warnings."""
    print_section("CRITICAL WARNINGS (No Confirmation)")

    renderer = AsciiRenderer()
    warning = SystemProtectionWarning(renderer)

    test_cases = [
        (r"C:\Windows\System32", "rm C:\\Windows\\System32\\kernel32.dll"),
        (r"C:\Windows", "rm C:\\Windows\\test.txt"),
        ("/etc", "rm /etc/passwd"),
        ("/bin", "rm /bin/bash"),
        ("/boot", "rm /boot/vmlinuz"),
    ]

    for path, command in test_cases:
        print(f"Test Case: {command}")
        print("-" * 70)
        warning._display_critical_warning(path, command)
        input("Press Enter to continue to next test case...")
        print()


def test_caution_warnings():
    """Test caution-level warnings."""
    print_section("CAUTION WARNINGS (With Confirmation)")

    renderer = AsciiRenderer()
    warning = SystemProtectionWarning(renderer)

    test_cases = [
        (r"C:\Program Files", r'rm "C:\Program Files\test.txt"'),
        ("/usr", "rm /usr/local/test.txt"),
        ("/Library", "rm /Library/test.txt"),
    ]

    for path, command in test_cases:
        print(f"Test Case: {command}")
        print("-" * 70)
        # Display warning (will prompt for input)
        result = warning._display_caution_warning(path, command)
        print(f"User response: {'Confirmed' if result else 'Cancelled'}")
        print()
        input("Press Enter to continue to next test case...")
        print()


def test_fallback_message():
    """Test fallback message for unknown directories."""
    print_section("FALLBACK MESSAGE (Unknown Directory)")

    renderer = AsciiRenderer()
    warning = SystemProtectionWarning(renderer)

    # Test with a path not in the directory info database
    path = "/unknown/protected/path"
    command = "rm /unknown/protected/path/file.txt"

    print(f"Test Case: {command}")
    print("-" * 70)
    warning._display_critical_warning(path, command)
    print()


def test_message_content_review():
    """Review message content for all directories."""
    print_section("MESSAGE CONTENT REVIEW")

    from src.display.system_protection_warning import DIRECTORY_INFO

    print("Reviewing all directory information entries:")
    print()

    for dir_path, info in DIRECTORY_INFO.items():
        print(f"📁 Directory: {dir_path}")
        print("-" * 70)
        print(f"Description: {info['description']}")
        print(f"Risk: {info['risk']}")
        print(f"Consequence: {info['consequence']}")
        print()
        print("Alternatives:")
        for i, alt in enumerate(info['alternatives'], 1):
            print(f"  {i}. {alt}")
        print()
        print("Evaluation:")
        print("  - Is the description clear? (yes/no)")
        print("  - Is the risk well-explained? (yes/no)")
        print("  - Are consequences specific? (yes/no)")
        print("  - Are alternatives actionable? (yes/no)")
        print()
        input("Press Enter to continue to next directory...")
        print()


def test_age_appropriateness():
    """Test age-appropriateness of messages."""
    print_section("AGE-APPROPRIATENESS TEST")

    print("Consider these user personas:")
    print()
    print("👶 Persona 1: 10-year-old learning CLI basics")
    print("   - Can they understand the message?")
    print("   - Is the tone appropriate?")
    print("   - Are alternatives clear enough?")
    print()
    print("🧑 Persona 2: 16-year-old high school student")
    print("   - Is the message educational?")
    print("   - Does it teach system concepts?")
    print("   - Is it engaging?")
    print()
    print("👨 Persona 3: Adult beginner (non-technical)")
    print("   - Is the message respectful?")
    print("   - Does it avoid condescension?")
    print("   - Are technical terms explained?")
    print()
    print("👴 Persona 4: Senior learning technology")
    print("   - Is the message patient?")
    print("   - Are instructions clear?")
    print("   - Is help accessible?")
    print()

    renderer = AsciiRenderer()
    warning = SystemProtectionWarning(renderer)

    # Show a sample message
    print("Sample message for evaluation:")
    print("-" * 70)
    warning._display_critical_warning(
        r"C:\Windows\System32",
        "rm C:\\Windows\\System32\\test.dll"
    )

    print()
    print("For each persona, evaluate:")
    print("  [ ] Message is understandable")
    print("  [ ] Tone is appropriate")
    print("  [ ] User knows what to do next")
    print()


def main():
    """Run all manual tests."""
    print()
    print("=" * 70)
    print("  EDUCATIONAL MESSAGE CLARITY & HELPFULNESS TEST")
    print("=" * 70)
    print()
    print("This manual test verifies that system protection messages are:")
    print("  - Clear and easy to understand")
    print("  - Helpful and educational")
    print("  - Age-appropriate for children and beginners")
    print("  - Actionable with specific alternatives")
    print()
    print("You will see various warning messages and evaluate them using")
    print("the provided checklist.")
    print()
    input("Press Enter to begin...")

    # Print checklist first
    print_checklist()
    input("Press Enter to start testing...")

    # Run tests
    test_critical_warnings()
    test_caution_warnings()
    test_fallback_message()
    test_message_content_review()
    test_age_appropriateness()

    # Final summary
    print_section("TEST COMPLETE")
    print("Review your evaluations and consider:")
    print()
    print("1. Are all messages clear and understandable?")
    print("2. Do messages provide helpful guidance?")
    print("3. Are alternatives specific and actionable?")
    print("4. Is the tone appropriate for all age groups?")
    print("5. Do messages teach system concepts effectively?")
    print()
    print("If any message needs improvement, document it in:")
    print("  docs/issues.md")
    print()
    print("=" * 70)
    print()


if __name__ == "__main__":
    main()
