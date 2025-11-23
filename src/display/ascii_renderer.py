"""
ASCII art renderer for MairuCLI display system.

Handles loading and displaying ASCII art with color and timing effects.
"""

import time
from pathlib import Path
from typing import Optional

from src.config import TIMING_ASCII_CHAR_DELAY


# Halloween color palette (ANSI 256-color codes)
COLORS = {
    "orange": "\033[38;5;208m",
    "chocolate": "\033[38;5;130m",
    "purple": "\033[38;5;141m",
    "green": "\033[38;5;46m",
    "red": "\033[38;5;196m",
    "reset": "\033[0m"
}


class AsciiRenderer:
    """Handles ASCII art loading and rendering with effects."""

    def __init__(self, art_dir: Optional[Path] = None):
        """
        Initialize ASCII renderer.

        Args:
            art_dir: Path to ASCII art directory (defaults to project data/ascii_art/)
        """
        if art_dir is None:
            # Default to data/ascii_art/ directory relative to project root
            self.art_dir = Path(__file__).parent.parent.parent / "data" / "ascii_art"
        else:
            self.art_dir = Path(art_dir)

    def load_art(self, filename: str) -> str:
        """
        Load ASCII art from file with error handling.

        Args:
            filename: Name of ASCII art file

        Returns:
            ASCII art as string, or placeholder if file not found
        """
        try:
            art_path = self.art_dir / filename
            with open(art_path, "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            return f"[ASCII art not found: {filename}]"
        except Exception as e:
            return f"[Error loading ASCII art: {e}]"

    def display_art(self, art: str, color: str) -> None:
        """
        Display ASCII art with color (no timing effects).

        Args:
            art: ASCII art string
            color: Color name from COLORS dict
        """
        colored_art = self.colorize(art, color)
        print(colored_art)

    def display_art_slowly(
        self,
        art: str,
        color: str,
        delay: float = TIMING_ASCII_CHAR_DELAY
    ) -> None:
        """
        Display ASCII art line by line with dramatic effect.

        Args:
            art: ASCII art string
            color: Color name for the art
            delay: Delay between lines in seconds
        """
        lines = art.split('\n')
        for line in lines:
            print(self.colorize(line, color))
            time.sleep(delay)

    def colorize(self, text: str, color_name: str) -> str:
        """
        Apply ANSI color to text.

        Args:
            text: Text to colorize
            color_name: Name of color from COLORS dict

        Returns:
            Colorized text with reset code
        """
        color_code = COLORS.get(color_name, COLORS["reset"])
        return f"{color_code}{text}{COLORS['reset']}"
