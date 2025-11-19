"""
Caution-level warning display for MairuCLI.

Displays lighter warnings for risky but not immediately catastrophic commands.
"""

from src.display.ascii_renderer import AsciiRenderer
from src.interceptor import CAUTION_PATTERNS


class CautionWarning:
    """Display caution-level warnings with user confirmation."""

    def __init__(self, renderer: AsciiRenderer):
        """
        Initialize caution warning display.

        Args:
            renderer: AsciiRenderer instance for colorization
        """
        self.renderer = renderer

    def display(self, pattern_name: str, command: str) -> bool:
        """
        Display caution warning and get user confirmation.

        Args:
            pattern_name: Name of matched caution pattern
            command: The command being executed

        Returns:
            True if user wants to proceed, False to cancel
        """
        pattern = CAUTION_PATTERNS[pattern_name]

        print()
        print("=" * 60)
        title = self.renderer.colorize(
            "⚠️  Heads Up! Think Carefully.",
            "orange"
        )
        print(title)
        print("=" * 60)
        print()

        # Show command and risk
        cmd_display = self.renderer.colorize(command, "purple")
        print(f"Command: {cmd_display}")
        print(f"Risk: {pattern['risk']}")
        print(f"Impact: {pattern['impact']}")
        print()

        # Show considerations
        considerations_title = self.renderer.colorize(
            "💡 What to consider:",
            "chocolate"
        )
        print(considerations_title)
        for consideration in pattern['considerations']:
            print(f"  • {consideration}")
        print()

        # Get user confirmation
        prompt = self.renderer.colorize(
            "Continue anyway? (y/n): ",
            "orange"
        )
        try:
            response = input(prompt).strip().lower()
            return response in ['y', 'yes']
        except (EOFError, KeyboardInterrupt):
            print()
            return False
