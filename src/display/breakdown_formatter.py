"""
Educational breakdown formatter for MairuCLI.

Formats command breakdowns, simulations, and incident stories with Halloween theme.
"""

from typing import Dict, List
from src.config import DISPLAY_SEPARATOR_WIDTH


class BreakdownFormatter:
    """Format educational content with Halloween theme."""

    def format_command_breakdown(self, breakdown: Dict) -> str:
        """
        Format command breakdown with parts explanation.

        Args:
            breakdown: Dictionary with command breakdown data

        Returns:
            Formatted string with Halloween theme
        """
        from src.display import colorize

        lines = []
        lines.append("\n" + "=" * DISPLAY_SEPARATOR_WIDTH)
        lines.append(colorize("🎓 Command Breakdown", "orange"))
        lines.append("=" * DISPLAY_SEPARATOR_WIDTH)
        lines.append("")

        # Command parts
        if 'parts' in breakdown:
            lines.append(colorize("📚 What each part means:", "green"))
            lines.append("")
            for part in breakdown['parts']:
                emoji = part.get('emoji', '•')
                text = part.get('part', '')
                meaning = part.get('meaning', '')
                danger = part.get('danger_level', '')

                lines.append(f"  {emoji} {colorize(text, 'orange')}")
                lines.append(f"     {meaning}")
                if danger:
                    lines.append(f"     Danger: {colorize(danger, 'red')}")
                lines.append("")

        # Translation
        if 'translation' in breakdown:
            lines.append(colorize("🌍 In plain English:", "purple"))
            lines.append(f"  {breakdown['translation']}")
            lines.append("")

        # Halloween analogy
        if 'halloween_analogy' in breakdown:
            lines.append(colorize("🎃 Halloween Analogy:", "chocolate"))
            lines.append(f"  {breakdown['halloween_analogy']}")
            lines.append("")

        # Safe alternatives
        if 'safe_alternatives' in breakdown:
            lines.append(colorize("✅ Safe Alternatives:", "green"))
            for alt in breakdown['safe_alternatives']:
                lines.append(f"  • {alt}")
            lines.append("")

        lines.append("=" * DISPLAY_SEPARATOR_WIDTH)
        return "\n".join(lines)

    def format_timeline_simulation(self, simulation: Dict) -> str:
        """
        Format timeline simulation showing what happens.

        Args:
            simulation: Dictionary with simulation data

        Returns:
            Formatted string with timeline
        """
        from src.display import colorize

        lines = []
        lines.append("\n" + "=" * DISPLAY_SEPARATOR_WIDTH)
        lines.append(colorize("⏱️  Timeline Simulation", "orange"))
        lines.append("=" * DISPLAY_SEPARATOR_WIDTH)
        lines.append("")

        if 'description' in simulation:
            lines.append(simulation['description'])
            lines.append("")

        # Timeline events
        if 'timeline' in simulation:
            lines.append(colorize("📅 What happens:", "purple"))
            lines.append("")
            for event in simulation['timeline']:
                time = event.get('time', '')
                emoji = event.get('emoji', '•')
                description = event.get('description', '')
                severity = event.get('severity', 'info')

                # Color based on severity
                color_map = {
                    'info': 'green',
                    'warning': 'orange',
                    'danger': 'red',
                    'critical': 'red'
                }
                color = color_map.get(severity, 'green')

                lines.append(f"  {colorize(time, color)} {emoji}")
                lines.append(f"    {description}")
                lines.append("")

        lines.append("=" * DISPLAY_SEPARATOR_WIDTH)
        return "\n".join(lines)

    def format_incident_story(self, incident: Dict) -> str:
        """
        Format real-world incident story.

        Args:
            incident: Dictionary with incident data

        Returns:
            Formatted string with Halloween framing
        """
        from src.display import colorize

        lines = []
        lines.append("\n" + "=" * DISPLAY_SEPARATOR_WIDTH)
        lines.append(colorize("👻 Real Horror Story", "red"))
        lines.append("=" * DISPLAY_SEPARATOR_WIDTH)
        lines.append("")

        # Title
        if 'title' in incident:
            lines.append(colorize(f"📰 {incident['title']}", "orange"))
            lines.append("")

        # Date and company
        if 'date' in incident or 'company' in incident:
            date = incident.get('date', 'Unknown date')
            company = incident.get('company', 'Unknown company')
            lines.append(f"  🗓️  {date}")
            lines.append(f"  🏢 {company}")
            lines.append("")

        # What happened
        if 'what_happened' in incident:
            lines.append(colorize("💀 What Happened:", "red"))
            lines.append(f"  {incident['what_happened']}")
            lines.append("")

        # Impact
        if 'impact' in incident:
            lines.append(colorize("💥 Impact:", "orange"))
            for impact in incident['impact']:
                lines.append(f"  • {impact}")
            lines.append("")

        # Lesson learned
        if 'lesson' in incident:
            lines.append(colorize("🎓 Lesson Learned:", "green"))
            lines.append(f"  {incident['lesson']}")
            lines.append("")

        # Source
        if 'source' in incident:
            lines.append(colorize("🔗 Source:", "purple"))
            lines.append(f"  {incident['source']}")
            lines.append("")

        lines.append("=" * DISPLAY_SEPARATOR_WIDTH)
        return "\n".join(lines)

    def format_quick_explanation(self, breakdown: Dict) -> str:
        """
        Format quick 5-second explanation.

        Args:
            breakdown: Dictionary with breakdown data

        Returns:
            Short formatted string
        """
        from src.display import colorize

        lines = []

        if 'quick_summary' in breakdown:
            lines.append("")
            lines.append(colorize("⚡ Quick Summary:", "orange"))
            lines.append(f"  {breakdown['quick_summary']}")
            lines.append("")
        elif 'translation' in breakdown:
            # Fallback to translation
            lines.append("")
            lines.append(colorize("⚡ Quick Summary:", "orange"))
            lines.append(f"  {breakdown['translation']}")
            lines.append("")

        return "\n".join(lines)

    def _format_section_border(self, title: str, color: str = "orange") -> str:
        """
        Format section border with title.

        Args:
            title: Section title
            color: Color for title

        Returns:
            Formatted border string
        """
        from src.display import colorize

        lines = []
        lines.append("=" * DISPLAY_SEPARATOR_WIDTH)
        lines.append(colorize(title, color))
        lines.append("=" * DISPLAY_SEPARATOR_WIDTH)
        return "\n".join(lines)
