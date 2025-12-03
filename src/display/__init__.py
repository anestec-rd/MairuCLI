"""
Display system for MairuCLI.

This module provides the public API for the display system.
Internal implementation uses modular components from display/ subdirectory.
"""

from typing import Dict
from src.display.ascii_renderer import AsciiRenderer
from src.display.content_loader import ContentLoader
from src.display.message_formatter import MessageFormatter
from src.display.statistics import Statistics
from src.display.achievements import AchievementTracker
from src.display.warning_components import (
    DangerWarning,
    TypoWarning,
    RepeatWarning,
    EMOJI
)
from src.display.caution_warning import CautionWarning
from src.display.system_protection_warning import SystemProtectionWarning
from src.display.educational_breakdown import EducationalBreakdown

# Initialize components
_renderer = AsciiRenderer()
_content_loader = ContentLoader()
_formatter = MessageFormatter()
_statistics = Statistics()
_achievement_tracker = AchievementTracker(_statistics)

# Initialize warning components
_danger_warning = DangerWarning(_renderer, _formatter, _content_loader)
_typo_warning = TypoWarning(_renderer, _formatter, _content_loader)
_repeat_warning = RepeatWarning(_renderer, _formatter, _content_loader)
_caution_warning = CautionWarning(_renderer)
_system_protection_warning = SystemProtectionWarning(_renderer)
_educational_breakdown = EducationalBreakdown()


def colorize(text: str, color_name: str) -> str:
    """
    Apply ANSI color to text.

    Args:
        text: Text to colorize
        color_name: Name of color from COLORS dict

    Returns:
        Colorized text with reset code
    """
    return _renderer.colorize(text, color_name)


def display_welcome_banner() -> None:
    """
    Display Halloween-themed welcome banner on startup.
    """
    # Load ASCII art banner
    from pathlib import Path
    project_root = Path(__file__).parent.parent.parent
    banner_path = project_root / "data" / "ascii_art" / "welcome_mairu_banner.txt"

    try:
        with open(banner_path, 'r', encoding='utf-8') as f:
            ascii_banner = f.read()
    except FileNotFoundError:
        # Fallback to simple banner if file not found
        ascii_banner = "\n🎃 MairuCLI 🎃\n"

    # Colorize the banner
    colored_banner = colorize(ascii_banner, "orange")

    # Instructions
    instruction1 = colorize(
        "Type commands as usual. I'll keep you safe from scary mistakes!",
        "green"
    )
    instruction2 = colorize(
        "Type 'help' for a list of commands (including dangerous ones!)",
        "purple"
    )
    instruction3 = colorize("Type 'exit' to leave (if you dare...)", "purple")
    warning = colorize(
        "⚠️  Educational tool only - not a security solution",
        "chocolate"
    )

    banner = f"""{colored_banner}
{instruction1}
{instruction2}
{instruction3}

{warning}
"""
    print(banner)


def display_goodbye_message() -> None:
    """
    Display goodbye message when user exits.
    """
    ghost = EMOJI['ghost']
    thanks = colorize("Thanks for using MairuCLI!", "purple")
    reminder = colorize("Stay safe out there, and remember:", "orange")
    tip = colorize("Always double-check before pressing Enter!", "green")

    message = f"""
{ghost} {thanks} {ghost}
{reminder}
{tip}
"""
    print(message)


def show_warning(pattern_name: str, command: str) -> None:
    """
    Display warning for dangerous command or typo.

    Args:
        pattern_name: Name of matched pattern
        command: The dangerous command entered
    """
    # Update statistics
    if pattern_name.startswith("typo_"):
        _statistics.increment_typos_caught()
    else:
        _statistics.increment_dangerous_blocked()

    # Check if this command was already warned about
    repeat_count = _statistics.track_repeat_command(command)

    if repeat_count > 1:
        # Show repeat warning
        _repeat_warning.display(command, repeat_count)
    else:
        # Show normal warning
        if pattern_name.startswith("typo_"):
            _typo_warning.display(pattern_name, command)
        else:
            _danger_warning.display(pattern_name, command)

    # Check for achievements
    _achievement_tracker.check_achievements()

    # Offer educational breakdown for dangerous commands (not typos)
    if not pattern_name.startswith("typo_"):
        _offer_educational_breakdown(pattern_name)


def get_stats() -> Dict[str, int]:
    """
    Get current statistics.

    Returns:
        Dictionary with statistics
    """
    return _statistics.get_stats()


def track_safe_command(command: str) -> None:
    """
    Track safe command usage for achievements.

    Args:
        command: The safe command being used
    """
    _statistics.track_safe_command(command)
    _achievement_tracker.check_achievements()


def show_caution_warning(pattern_name: str, command: str) -> bool:
    """
    Display caution-level warning and get user confirmation.

    Args:
        pattern_name: Name of matched caution pattern
        command: The command being executed

    Returns:
        True if user wants to proceed, False to cancel
    """
    # Update statistics
    _statistics.increment_caution_shown()

    # Show warning and get confirmation
    proceed = _caution_warning.display(pattern_name, command)

    # Track user decision
    if proceed:
        _statistics.increment_caution_proceeded()
    else:
        _statistics.increment_caution_cancelled()

    # Check for achievements
    _achievement_tracker.check_achievements()

    return proceed


def get_unlocked_achievements() -> list:
    """
    Get list of unlocked achievement display names.

    Returns:
        List of achievement display names
    """
    return _achievement_tracker.get_unlocked_achievement_names()


def get_achievements_by_category(category: str) -> list:
    """
    Get unlocked achievements filtered by category.

    Args:
        category: Category to filter by
                 ("danger", "safe", "exploration", "system_protection")

    Returns:
        List of achievement display names in the specified category
    """
    return _achievement_tracker.get_achievements_by_category(category)


def show_system_protection_warning(
    level: str,
    target_path: str,
    command: str
) -> bool:
    """
    Display system directory protection warning.

    Args:
        level: "critical" or "caution"
        target_path: The protected path being targeted
        command: The blocked command

    Returns:
        True if user confirms (caution level), False otherwise
    """
    # Update statistics for blocked command
    if level == "critical":
        _statistics.increment_dangerous_blocked()

    # Track system protection block
    _statistics.track_system_protection_block(target_path)

    # Display warning
    result = _system_protection_warning.display(level, target_path, command)

    # Check for achievements
    _achievement_tracker.check_achievements()

    return result


def _offer_educational_breakdown(pattern_name: str) -> None:
    """
    Offer educational breakdown for a dangerous pattern.

    Args:
        pattern_name: Name of the pattern that was matched
    """
    # Skip in test mode to avoid input() blocking pytest
    import os
    if os.environ.get('MAIRU_TEST_MODE') == '1':
        return

    # Check if breakdown is available
    if not _educational_breakdown.has_breakdown(pattern_name):
        return

    print()
    print(colorize("📚 Want to learn more about this command?", "orange"))
    print("Type 'b' (or 'breakdown') for detailed explanation, or press Enter to continue.")

    try:
        response = input("> ").strip().lower()
        if response in ['breakdown', 'b', 'yes', 'y']:
            print()
            _educational_breakdown.show_full_breakdown(pattern_name)
    except (KeyboardInterrupt, EOFError):
        print()  # Clean exit on Ctrl+C or Ctrl+D
