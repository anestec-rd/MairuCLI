"""
MairuCLI-specific commands.

Provides MairuCLI-specific commands: help, stats
"""

import json
from pathlib import Path
from typing import List, Dict
from src.config import DISPLAY_SEPARATOR_WIDTH


class HelpGenerator:
    """Generate help text from pattern catalogs."""

    def __init__(self, data_dir: str = "data/warnings", builtins_dir: str = "data/builtins"):
        """
        Initialize help generator.

        Args:
            data_dir: Directory containing pattern JSON files
            builtins_dir: Directory containing builtin commands JSON
        """
        self.data_dir = Path(data_dir)
        self.builtins_dir = Path(builtins_dir)

    def _load_patterns(self, filename: str, key: str) -> Dict:
        """
        Load patterns from JSON file.

        Args:
            filename: JSON filename
            key: Key to extract patterns from

        Returns:
            Dictionary of patterns
        """
        try:
            file_path = self.data_dir / filename
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data.get(key, {})
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def _group_by_category(self, patterns: Dict) -> Dict[str, List]:
        """
        Group patterns by category.

        Args:
            patterns: Dictionary of patterns

        Returns:
            Dictionary mapping category to list of patterns
        """
        grouped = {}
        for name, data in patterns.items():
            category = data.get('category', 'other')
            if category not in grouped:
                grouped[category] = []
            grouped[category].append({
                'name': name,
                'example': data.get('help_example', name),
                'description': data.get('help_description', 'No description')
            })
        return grouped

    def generate_dangerous_commands_help(self) -> List[str]:
        """
        Generate help text for dangerous commands.

        Returns:
            List of formatted help lines
        """
        from src.display import EMOJI

        patterns = self._load_patterns('warning_catalog.json', 'warnings')
        if not patterns:
            return ["  (No dangerous patterns loaded)"]

        lines = []
        for name, data in patterns.items():
            example = data.get('help_example', name)
            description = data.get('help_description', 'Dangerous command')

            # Use pattern-specific emoji if available
            emoji_key = data.get('emoji', 'fire')
            emoji = EMOJI.get(emoji_key, EMOJI['fire'])

            # Pad example to 20 chars for alignment
            padded_example = f"{example:<20}"
            lines.append(f"  {emoji} {padded_example} - {description}")

        return lines

    def generate_caution_commands_help(self) -> List[str]:
        """
        Generate help text for caution commands.

        Returns:
            List of formatted help lines
        """
        from src.display import EMOJI

        patterns = self._load_patterns('caution_catalog.json', 'cautions')
        if not patterns:
            return ["  (No caution patterns loaded)"]

        lines = []
        for name, data in patterns.items():
            example = data.get('help_example', name)
            description = data.get('help_description', 'Caution command')

            # Use warning emoji for all caution commands
            emoji = EMOJI['warning']

            # Pad example to 20 chars for alignment
            padded_example = f"{example:<20}"
            lines.append(f"  {emoji} {padded_example} - {description}")

        return lines

    def generate_builtin_commands_help(self) -> Dict[str, Dict]:
        """
        Generate help text for builtin commands from JSON.

        Returns:
            Dictionary of categories with their commands
        """
        builtin_path = self.builtins_dir / "builtin_commands.json"

        try:
            with open(builtin_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data.get('categories', {})
        except FileNotFoundError:
            print(f"Warning: {builtin_path} not found.")
            return {}
        except json.JSONDecodeError as e:
            print(f"Warning: Invalid JSON in {builtin_path}: {e}")
            return {}


def cmd_help(args: List[str]) -> bool:
    """
    Display help information with a spooky twist.

    Args:
        args: Command arguments (ignored)

    Returns:
        True (always handled)
    """
    from src.display import colorize, EMOJI

    print("\n" + "=" * DISPLAY_SEPARATOR_WIDTH)
    print(f"{EMOJI['pumpkin']} {colorize('MairuCLI Help', 'orange')} "
          f"{EMOJI['pumpkin']}")
    print("=" * DISPLAY_SEPARATOR_WIDTH)
    print()

    # Generate builtin commands help from JSON
    help_gen = HelpGenerator()
    builtin_categories = help_gen.generate_builtin_commands_help()

    for category_key, category_data in builtin_categories.items():
        title = category_data.get('title', 'Commands')
        color = category_data.get('color', 'green')
        commands = category_data.get('commands', [])

        print(colorize(f"{title}:", color))
        for cmd in commands:
            name = cmd.get('name', '')
            description = cmd.get('description', '')
            emoji = cmd.get('emoji', '')

            # Pad name to 13 chars for alignment
            padded_name = f"{name:<13}"
            if emoji:
                print(f"  {emoji} {padded_name} - {description}")
            else:
                print(f"  {padded_name} - {description}")
        print()

    # Generate dangerous commands help from JSON
    print(colorize("💀 Dangerous Commands (DON'T try these!):", "red"))
    dangerous_lines = help_gen.generate_dangerous_commands_help()
    for line in dangerous_lines:
        print(line)
    print()

    # Generate caution commands help from JSON
    print(colorize("⚠️  Caution Commands (Think twice!):", "purple"))
    caution_lines = help_gen.generate_caution_commands_help()
    for line in caution_lines:
        print(line)
    print()

    print(colorize("Fun Typos to Try:", "chocolate"))
    print(f"  {EMOJI['train']} sl              "
          "- Choo choo! (instead of ls)")
    print(f"  {EMOJI['pumpkin']} cd..            "
          "- Stuck together? (instead of cd ..)")
    print()

    print(colorize("Remember:", "orange"))
    print("  This is an EDUCATIONAL tool, not a security solution!")
    print("  I'll warn you about dangerous commands, but I can't")
    print("  protect you from everything. Stay curious, stay safe!")
    print()
    print("=" * DISPLAY_SEPARATOR_WIDTH + "\n")

    return True


def cmd_stats(args: List[str]) -> bool:
    """
    Display statistics about blocked commands.

    Args:
        args: Command arguments (ignored)

    Returns:
        True (always handled)
    """
    from src.display import colorize, EMOJI, get_stats

    stats = get_stats()

    print("\n" + "=" * DISPLAY_SEPARATOR_WIDTH)
    pumpkin = EMOJI['pumpkin']
    title = colorize('MairuCLI Statistics', 'orange')
    print(f"{pumpkin} {title} {pumpkin}")
    print("=" * DISPLAY_SEPARATOR_WIDTH)
    print()

    total_saves = stats["dangerous_blocked"] + stats["typos_caught"]

    if total_saves == 0:
        print(colorize("No disasters prevented yet!", "green"))
        print("(But I'm ready when you need me!)")
    else:
        print(f"{EMOJI['fire']} {colorize('Times I saved you:', 'red')} "
              f"{colorize(str(total_saves), 'orange')}")
        print()
        print(f"  Dangerous commands blocked: "
              f"{colorize(str(stats['dangerous_blocked']), 'red')}")
        print(f"  Typos caught: "
              f"{colorize(str(stats['typos_caught']), 'purple')}")
        print()

        # Display unlocked achievements by category
        from src.display import get_achievements_by_category

        # Category display configuration
        category_config = {
            "danger": {
                "title": "💀 Your Troublemaking History:",
                "color": "red"
            },
            "safe": {
                "title": "🏆 Safe Explorer Achievements:",
                "color": "green"
            },
            "exploration": {
                "title": "🚂 Exploration Achievements:",
                "color": "purple"
            },
            "system_protection": {
                "title": "🛡️ System Protection Achievements:",
                "color": "orange"
            }
        }

        # Display achievements by category
        for category, config in category_config.items():
            achievements = get_achievements_by_category(category)
            if achievements:
                print(colorize(config["title"], config["color"]))
                print()
                for achievement in achievements:
                    print(f"  {colorize('✓', 'green')} {achievement}")
                print()

        if total_saves >= 10:
            msg = "🏆 Wow! You really like living dangerously!"
            print(colorize(msg, "orange"))
        elif total_saves >= 5:
            print(colorize("😅 Maybe slow down a bit?", "chocolate"))
        else:
            print(colorize("👍 Keep being careful out there!", "green"))

    print()
    print("=" * DISPLAY_SEPARATOR_WIDTH + "\n")

    return True
