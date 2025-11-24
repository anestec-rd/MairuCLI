"""
Configuration management for MairuCLI.

This module handles user preferences and system settings.

Timing Constants (Day 8 - Adjusted for dramatic effect):
- TIMING_ASCII_CHAR_DELAY: Delay between ASCII art lines (0.08s)
- TIMING_PAUSE_SHORT: Short pause after art/achievements (0.5s)
- TIMING_PAUSE_MEDIUM: Medium pause before explanations (1.0s)

Display Constants:
- DISPLAY_SEPARATOR_WIDTH: Width of separator lines (60 chars)
- DISPLAY_MIN_QUOTE_LENGTH: Minimum length for quoted strings (2 chars)

Configuration:
- MairuConfig: Dataclass for user preferences (colors, behavior, etc.)
- Currently uses default values (file loading not implemented in MVP)
"""

from dataclasses import dataclass


# Timing constants (in seconds)
# Day 8: Adjusted for more dramatic effect (demo-friendly)
TIMING_ASCII_CHAR_DELAY = 0.08  # Delay between ASCII art characters (was 0.05)
TIMING_PAUSE_SHORT = 0.5        # Short pause (after art, after achievement) (was 0.3)
TIMING_PAUSE_MEDIUM = 1.0       # Medium pause (before explanation) (was 0.5)

# Display formatting constants
DISPLAY_SEPARATOR_WIDTH = 60    # Width of separator lines (=====)
DISPLAY_MIN_QUOTE_LENGTH = 2    # Minimum length for quoted strings in command parser


@dataclass
class MairuConfig:
    """Configuration for MairuCLI."""

    # Color settings
    colors_enabled: bool = True
    color_scheme: str = "halloween"  # Future: support other themes

    # Display settings
    show_ascii_art: bool = True
    show_educational_messages: bool = True

    # Behavior settings
    intercept_dangerous: bool = True
    intercept_typos: bool = True

    # Performance settings
    pattern_match_timeout_ms: int = 50


# Global config instance
config = MairuConfig()


def load_config() -> MairuConfig:
    """
    Load configuration from file or use defaults.
    MVP: Returns default config (no file loading).

    Returns:
        MairuConfig instance
    """
    return MairuConfig()


def save_config(cfg: MairuConfig) -> None:
    """
    Save configuration to file.
    MVP: Not implemented (future feature).

    Args:
        cfg: Configuration to save
    """
    pass
