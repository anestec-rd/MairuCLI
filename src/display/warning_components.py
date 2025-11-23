"""
Warning components for MairuCLI display system.

Provides modular warning display components for different warning types.
"""

import random
import time
from abc import ABC, abstractmethod
from src.display.ascii_renderer import AsciiRenderer
from src.display.message_formatter import MessageFormatter
from src.display.content_loader import ContentLoader
from src.config import (
    TIMING_ASCII_CHAR_DELAY,
    TIMING_PAUSE_SHORT,
    TIMING_PAUSE_MEDIUM,
    DISPLAY_SEPARATOR_WIDTH
)


# Emoji constants
EMOJI = {
    "fire": "🔥",
    "pumpkin": "🎃",
    "train": "🚂",
    "spider": "🕷️",
    "skull": "💀",
    "lightbulb": "💡",
    "ghost": "👻",
    "facepalm": "🤦",
    "eyes": "👀"
}


class WarningComponent(ABC):
    """Base class for all warning components."""

    def __init__(
        self,
        ascii_renderer: AsciiRenderer,
        message_formatter: MessageFormatter
    ):
        """
        Initialize with required dependencies.

        Args:
            ascii_renderer: ASCII art renderer instance
            message_formatter: Message formatter instance
        """
        self.renderer = ascii_renderer
        self.formatter = message_formatter

    @abstractmethod
    def display(self, pattern_name: str, command: str) -> None:
        """
        Display the warning.

        Args:
            pattern_name: Name of matched pattern
            command: The command entered
        """
        pass


class DangerWarning(WarningComponent):
    """Displays warnings for dangerous commands."""

    def __init__(
        self,
        ascii_renderer: AsciiRenderer,
        message_formatter: MessageFormatter,
        content_loader: ContentLoader
    ):
        """
        Initialize with dependencies and content loader.

        Args:
            ascii_renderer: ASCII art renderer instance
            message_formatter: Message formatter instance
            content_loader: Content loader instance
        """
        super().__init__(ascii_renderer, message_formatter)
        self.content = content_loader

    def display(self, pattern_name: str, command: str) -> None:
        """
        Display danger warning with ASCII art and message.

        Args:
            pattern_name: Name of matched dangerous pattern
            command: The dangerous command entered
        """
        # Load content for this pattern
        warning_content = self.content.get_warning_content(pattern_name)

        # Get variation set and category, then select random variation
        variation_set = warning_content.get("variation_set", "data_destroyer")
        category = warning_content.get("category", None)
        variations = self.content.get_variations(variation_set, category)
        title, subtitle = random.choice(variations) if variations else ("DANGER!", "(Be careful)")

        # Load and display ASCII art
        art_file = warning_content.get("ascii_art", "fired.txt")
        art = self.renderer.load_art(art_file)
        color = warning_content.get("color", "red")
        timing = warning_content.get("timing", {})

        print("\n" + "=" * DISPLAY_SEPARATOR_WIDTH)

        # Display ASCII art slowly for dramatic effect
        art_delay = timing.get("art_delay", TIMING_ASCII_CHAR_DELAY)
        self.renderer.display_art_slowly(art, color, delay=art_delay)
        time.sleep(timing.get("pause_after_art", TIMING_PAUSE_SHORT))

        # Display title and subtitle
        emoji_name = warning_content.get("emoji", "fire")
        emoji = EMOJI.get(emoji_name, "🔥")
        title_colored = self.renderer.colorize(title, "red")
        print(f"{emoji} {title_colored} {emoji}")
        subtitle_colored = self.renderer.colorize(subtitle, "orange")
        print(subtitle_colored)
        print()
        time.sleep(timing.get("pause_before_explanation", TIMING_PAUSE_MEDIUM))

        # Display explanation and consequence
        explanation = warning_content.get("explanation", "This command is dangerous.")
        consequence = warning_content.get("consequence", "It can cause problems.")
        print(explanation)
        print(consequence)
        print()

        # Display advice
        advice = warning_content.get("advice", ["Be careful with this command"])
        lightbulb = EMOJI["lightbulb"]
        advice_title = self.renderer.colorize("Safe alternative:", "green")
        print(f"{lightbulb} {advice_title}")
        for item in advice:
            print(f"  - {item}")
        time.sleep(timing.get("pause_before_achievement", TIMING_PAUSE_SHORT))

        print()
        command_text = self.renderer.colorize(f"Blocked command: {command}", "chocolate")
        print(command_text)
        print("=" * DISPLAY_SEPARATOR_WIDTH + "\n")


class TypoWarning(WarningComponent):
    """Displays warnings for typos."""

    def __init__(
        self,
        ascii_renderer: AsciiRenderer,
        message_formatter: MessageFormatter,
        content_loader: ContentLoader
    ):
        """
        Initialize with dependencies and content loader.

        Args:
            ascii_renderer: ASCII art renderer instance
            message_formatter: Message formatter instance
            content_loader: Content loader instance
        """
        super().__init__(ascii_renderer, message_formatter)
        self.content = content_loader

    def display(self, pattern_name: str, command: str) -> None:
        """
        Display typo warning with suggestion.

        Args:
            pattern_name: Name of matched typo pattern (with 'typo_' prefix)
            command: The typo command entered
        """
        # Load typo message from content
        from src.interceptor import get_pattern_info
        pattern_info = get_pattern_info(pattern_name)

        print("\n" + "=" * DISPLAY_SEPARATOR_WIDTH)
        print(pattern_info.get("message", "Oops! Typo detected!"))
        print()

        typed_colored = self.renderer.colorize(command, "red")
        correct_colored = self.renderer.colorize(pattern_info["correct"], "green")
        print(f"You typed: {typed_colored}")
        print(f"Did you mean: {correct_colored}?")
        print("=" * DISPLAY_SEPARATOR_WIDTH + "\n")


class RepeatWarning(WarningComponent):
    """Displays escalating warnings for repeated commands."""

    def __init__(
        self,
        ascii_renderer: AsciiRenderer,
        message_formatter: MessageFormatter,
        content_loader: ContentLoader
    ):
        """
        Initialize with dependencies and content loader.

        Args:
            ascii_renderer: ASCII art renderer instance
            message_formatter: Message formatter instance
            content_loader: Content loader instance
        """
        super().__init__(ascii_renderer, message_formatter)
        self.content = content_loader

    def display(self, command: str, count: int) -> None:
        """
        Display repeat warning based on attempt count.

        Args:
            command: The repeated command
            count: Number of times user tried this command
        """
        # Load repeat warnings from content
        import json
        from pathlib import Path

        warnings_path = Path(__file__).parent.parent.parent / "data" / "warnings" / "repeat_warnings.json"

        try:
            with open(warnings_path, "r", encoding="utf-8") as f:
                repeat_warnings = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            # Fallback if file not found
            repeat_warnings = {
                "default": {
                    "emoji": None,
                    "title": "...",
                    "lines": ["", "[Command log: '{command}' - Attempt #{count}]", "[No comment.]"]
                }
            }

        # Get warning for this count
        count_key = str(count) if str(count) in repeat_warnings else "default"
        warning_data = repeat_warnings.get(count_key, repeat_warnings["default"])

        print("\n" + "=" * DISPLAY_SEPARATOR_WIDTH)

        # Display emoji and title
        emoji_name = warning_data.get("emoji")
        title = warning_data.get("title", "...")

        if emoji_name:
            emoji = EMOJI.get(emoji_name, "")
            title_colored = self.renderer.colorize(title, "orange")
            print(f"{emoji} {title_colored}")
        else:
            title_colored = self.renderer.colorize(title, "chocolate")
            print(title_colored)

        # Display lines with placeholder replacement
        lines = warning_data.get("lines", [])
        for line in lines:
            formatted_line = line.replace("{command}", command)
            formatted_line = formatted_line.replace("{count}", str(count))
            print(formatted_line)

        print("=" * DISPLAY_SEPARATOR_WIDTH)
        print()
