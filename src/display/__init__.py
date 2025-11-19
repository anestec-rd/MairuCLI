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
    pumpkin = EMOJI['pumpkin']
    title = colorize("Welcome to MairuCLI", "red")
    subtitle = colorize(
        "Your friendly CLI safety wrapper with a spooky twist!",
        "chocolate"
    )

    # Simple separator line (no box to avoid emoji alignment issues)
    separator = colorize("=" * 65, "orange")

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

    banner = f"""
{separator}
  {pumpkin} {title} {pumpkin}
  {subtitle}
{separator}

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
