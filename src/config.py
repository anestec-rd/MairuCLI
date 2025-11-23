"""
Configuration management for MairuCLI.

This module handles user preferences and system settings.
"""

from dataclasses import dataclass


# Timing constants (in seconds)
TIMING_ASCII_CHAR_DELAY = 0.05  # Delay between ASCII art characters
TIMING_PAUSE_SHORT = 0.3        # Short pause (after art, after achievement)
TIMING_PAUSE_MEDIUM = 0.5       # Medium pause (before explanation, before achievement)

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
