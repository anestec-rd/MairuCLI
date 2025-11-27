"""
Educational breakdown mode for MairuCLI.

Provides detailed educational content about dangerous commands.
"""

from typing import Optional
from src.display.educational_loader import EducationalLoader
from src.display.breakdown_formatter import BreakdownFormatter


class EducationalBreakdown:
    """Manage educational breakdown mode."""

    def __init__(self):
        """Initialize educational breakdown with loader and formatter."""
        self.loader = EducationalLoader()
        self.formatter = BreakdownFormatter()

    def show_breakdown_prompt(self, pattern_name: str) -> str:
        """
        Display options and get user choice.

        Args:
            pattern_name: Name of the pattern

        Returns:
            User choice: 'q' (quick), 'f' (full), 's' (skip)
        """
        from src.display import colorize

        print()
        print(colorize("📚 Want to learn more about this command?", "orange"))
        print()
        print("  q - Quick explanation (5 seconds)")
        print("  f - Full breakdown (command parts + timeline + real incidents)")
        print("  s - Skip (just block the command)")
        print()

        while True:
            choice = input(colorize("Your choice (q/f/s): ", "green")).lower().strip()
            if choice in ['q', 'f', 's']:
                return choice
            print(colorize("Please enter 'q', 'f', or 's'", "red"))

    def show_quick_explanation(self, pattern_name: str) -> None:
        """
        Show quick 5-second explanation.

        Args:
            pattern_name: Name of the pattern
        """
        breakdown = self.loader.load_breakdown(pattern_name)

        if breakdown:
            output = self.formatter.format_quick_explanation(breakdown)
            print(output)
        else:
            # Fallback message
            from src.display import colorize
            print()
            print(colorize("⚡ Quick Summary:", "orange"))
            print("  This command is dangerous and could cause data loss.")
            print()

    def show_breakdown(self, pattern_name: str, show_simulation: bool = False,
                      show_incidents: bool = False) -> bool:
        """
        Show educational breakdown for a pattern.

        Args:
            pattern_name: Name of the pattern (e.g., "rm_dangerous")
            show_simulation: Whether to show timeline simulation
            show_incidents: Whether to show related incident stories

        Returns:
            True if breakdown was shown, False if not available
        """
        from src.display import colorize

        # Load and display command breakdown
        breakdown = self.loader.load_breakdown(pattern_name)
        if not breakdown:
            return False

        # Format and display breakdown slowly
        output = self.formatter.format_command_breakdown(breakdown)
        self.formatter.print_slowly(output, delay=0.03)

        # Show simulation if requested
        if show_simulation:
            simulation = self.loader.load_simulation(pattern_name)
            if simulation:
                # Prompt user to continue
                print()
                print(colorize("Press Enter to see the timeline simulation...", "orange"))
                try:
                    input()
                except (KeyboardInterrupt, EOFError):
                    return True

                print("\n" + "=" * 70)
                output = self.formatter.format_timeline_simulation(simulation)
                self.formatter.print_slowly(output, delay=0.05)  # Slower for timeline

        # Show related incidents if requested
        if show_incidents:
            incident_names = self.loader.get_related_incidents(pattern_name)
            for incident_name in incident_names:
                incident = self.loader.load_incident(incident_name)
                if incident:
                    # Prompt user to continue
                    print()
                    print(colorize("Press Enter to see the real horror story...", "orange"))
                    try:
                        input()
                    except (KeyboardInterrupt, EOFError):
                        return True

                    print("\n" + "=" * 70)
                    output = self.formatter.format_incident_story(incident)
                    self.formatter.print_slowly(output, delay=0.04)

        return True

    def show_quick_breakdown(self, pattern_name: str) -> bool:
        """
        Show a quick breakdown (just the command breakdown, no extras).

        Args:
            pattern_name: Name of the pattern

        Returns:
            True if breakdown was shown, False if not available
        """
        return self.show_breakdown(pattern_name, show_simulation=False, show_incidents=False)

    def show_full_breakdown(self, pattern_name: str) -> bool:
        """
        Show full breakdown with simulation and incidents.

        Args:
            pattern_name: Name of the pattern

        Returns:
            True if breakdown was shown, False if not available
        """
        return self.show_breakdown(pattern_name, show_simulation=True, show_incidents=True)

    def has_breakdown(self, pattern_name: str) -> bool:
        """
        Check if a breakdown exists for a pattern.

        Args:
            pattern_name: Name of the pattern

        Returns:
            True if breakdown exists, False otherwise
        """
        breakdown = self.loader.load_breakdown(pattern_name)
        return breakdown is not None

    def list_available_breakdowns(self):
        """
        List all available breakdown patterns.

        Returns:
            List of pattern names that have breakdowns
        """
        import os
        breakdowns_dir = self.loader.base_path / "command_breakdowns"

        if not breakdowns_dir.exists():
            return []

        patterns = []
        for file in os.listdir(breakdowns_dir):
            if file.endswith('.json') and file != '.gitkeep':
                pattern_name = file[:-5]  # Remove .json extension
                patterns.append(pattern_name)

        return sorted(patterns)

    def _show_fallback_breakdown(self, pattern_name: str) -> None:
        """
        Show fallback message when content is not available.

        Args:
            pattern_name: Name of the pattern
        """
        from src.display import colorize
        from src.config import DISPLAY_SEPARATOR_WIDTH

        print()
        print("=" * DISPLAY_SEPARATOR_WIDTH)
        print(colorize("🎓 Command Breakdown", "orange"))
        print("=" * DISPLAY_SEPARATOR_WIDTH)
        print()
        print(colorize("⚠️  Educational content not yet available for this command.", "orange"))
        print()
        print("This command is dangerous and has been blocked for your safety.")
        print("Check the warning message above for details.")
        print()
        print("=" * DISPLAY_SEPARATOR_WIDTH)


# Global instance for easy access
_educational_breakdown = None


def get_educational_breakdown() -> EducationalBreakdown:
    """
    Get global EducationalBreakdown instance.

    Returns:
        EducationalBreakdown instance
    """
    global _educational_breakdown
    if _educational_breakdown is None:
        _educational_breakdown = EducationalBreakdown()
    return _educational_breakdown


def show_educational_mode(pattern_name: str) -> None:
    """
    Show educational breakdown mode for a pattern.

    Args:
        pattern_name: Name of the pattern (e.g., "rm_dangerous")
    """
    edu = get_educational_breakdown()

    # Ask user what they want
    choice = edu.show_breakdown_prompt(pattern_name)

    if choice == 'q':
        edu.show_quick_explanation(pattern_name)
    elif choice == 'f':
        edu.show_full_breakdown(pattern_name)
    # If 's', just skip (do nothing)
