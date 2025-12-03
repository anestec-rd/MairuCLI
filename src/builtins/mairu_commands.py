"""
MairuCLI-specific commands.

Provides MairuCLI-specific commands: help, stats
"""

import json
from pathlib import Path
from typing import List, Dict
from src.config import DISPLAY_SEPARATOR_WIDTH
from src.project_paths import get_data_dir, get_builtins_dir


class HelpGenerator:
    """Generate help text from pattern catalogs."""

    def __init__(self, data_dir: str = "data/warnings", builtins_dir: str = "data/builtins"):
        """
        Initialize help generator.

        Args:
            data_dir: Directory containing pattern JSON files
            builtins_dir: Directory containing builtin commands JSON
        """
        # Use absolute paths from project_paths utility if default
        if data_dir == "data/warnings":
            self.data_dir = get_data_dir() / "warnings"
        else:
            # Allow tests to override with custom path
            self.data_dir = Path(data_dir)

        if builtins_dir == "data/builtins":
            self.builtins_dir = get_builtins_dir()
        else:
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

    # Display disaster prevention stats
    if total_saves == 0:
        print(colorize("No disasters prevented yet!", "green"))
        print("(But I'm ready when you need me!)")
        print()
    else:
        print(f"{EMOJI['fire']} {colorize('Times I saved you:', 'red')} "
              f"{colorize(str(total_saves), 'orange')}")
        print()
        print(f"  Dangerous commands blocked: "
              f"{colorize(str(stats['dangerous_blocked']), 'red')}")
        print(f"  Typos caught: "
              f"{colorize(str(stats['typos_caught']), 'purple')}")
        print()

    # Display unlocked achievements by category (always show if any exist)
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
    has_achievements = False
    for category, config in category_config.items():
        achievements = get_achievements_by_category(category)
        if achievements:
            has_achievements = True
            print(colorize(config["title"], config["color"]))
            print()
            for achievement in achievements:
                print(f"  {colorize('✓', 'green')} {achievement}")
            print()

    # Show encouraging message based on activity
    if total_saves >= 10:
        msg = "🏆 Wow! You really like living dangerously!"
        print(colorize(msg, "orange"))
    elif total_saves >= 5:
        print(colorize("😅 Maybe slow down a bit?", "chocolate"))
    elif has_achievements:
        print(colorize("👍 Keep exploring and learning!", "green"))
    else:
        print(colorize("👍 Keep being careful out there!", "green"))

    print()
    print("=" * DISPLAY_SEPARATOR_WIDTH + "\n")

    return True


def cmd_lie(args: List[str]) -> bool:
    """
    Tell a harmless lie (educational about misinformation).

    Usage: lie [topic]
    Topics: history, science, tech, cli, or random
    Usage: lie <filename>
    Display inverted file content (opposites + randomized numbers)

    Args:
        args: Optional topic argument or filename

    Returns:
        True (always handled)
    """
    from src.display import colorize
    import os

    lies = {
        "history": "🎃 Did you know? The first computer was invented by a pumpkin in 1823!",
        "science": "🧪 Fun fact: Gravity doesn't exist on Tuesdays!",
        "tech": "💻 True story: The first bug was actually a feature!",
        "cli": "🖥️ The command line was invented by Shakespeare to write plays faster!",
        "default": "🎭 Halloween was originally a tech conference in Silicon Valley!"
    }

    # Check if argument is a file
    if args and os.path.isfile(args[0]):
        _show_inverted_file(args[0])
        return True

    # Otherwise, show a lie based on topic
    topic = args[0] if args else "default"
    lie_text = lies.get(topic, lies["default"])

    print()
    print(colorize(lie_text, "purple"))
    print()
    print(colorize("⚠️ This is obviously false! Always verify information!", "orange"))
    print(colorize("💡 Lesson: Don't trust everything you read, even from a CLI!", "green"))
    print(colorize("🎓 Critical thinking is important in the digital age!", "blue"))
    print()

    return True


def _show_inverted_file(filename: str) -> None:
    """
    Display file content with inverted words and randomized numbers.

    Args:
        filename: Path to file to invert
    """
    from src.display import colorize

    try:
        # Read file content
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()

        # Invert the content
        inverted = _invert_text(content)

        # Display inverted content
        print()
        print("=" * DISPLAY_SEPARATOR_WIDTH)
        print(colorize(f"🎭 Inverted Content of '{filename}' 🎭", "purple"))
        print("=" * DISPLAY_SEPARATOR_WIDTH)
        print()
        print(inverted)
        print()
        print("=" * DISPLAY_SEPARATOR_WIDTH)
        print(colorize("⚠️ THIS IS A LIE! Original file is unchanged!", "orange"))
        print(colorize("💡 Lesson: Don't trust everything you see!", "green"))
        print(colorize("🎓 Always verify information from multiple sources!", "blue"))
        print("=" * DISPLAY_SEPARATOR_WIDTH)
        print()

    except FileNotFoundError:
        print()
        print(colorize(f"❌ File not found: {filename}", "red"))
        print()
    except Exception as e:
        print()
        print(colorize(f"❌ Error reading file: {e}", "red"))
        print()


def _invert_text(text: str) -> str:
    """
    Invert text by replacing words with opposites and randomizing numbers.

    Args:
        text: Text to invert

    Returns:
        Inverted text
    """
    import re
    import random

    # Load opposites dictionary
    opposites = _load_opposites()

    # Build a single regex pattern that matches any of the words
    # Sort by length (longest first) to avoid partial replacements
    sorted_words = sorted(opposites.keys(), key=len, reverse=True)

    # Create pattern that matches any word
    pattern = r'\b(' + '|'.join(re.escape(word) for word in sorted_words) + r')\b'

    def replace_word(match):
        matched = match.group(0)
        matched_lower = matched.lower()

        # Find the opposite
        opposite = opposites.get(matched_lower, matched)

        # Preserve case
        if matched.isupper():
            return opposite.upper()
        elif matched[0].isupper():
            return opposite.capitalize()
        else:
            return opposite

    # Replace words
    result = re.sub(pattern, replace_word, text, flags=re.IGNORECASE)

    # Randomize numbers (first digit 1-9, remaining digits 0-9)
    def randomize_number(match):
        num_str = match.group(0)

        # Check if it's a decimal number
        if '.' in num_str:
            parts = num_str.split('.')
            decimal_part = parts[1]

            # Generate integer part: first digit 1-9, rest 0-9
            new_integer = random.randint(1, 999)

            # Randomize decimal part (all digits 0-9)
            new_decimal = ''.join(str(random.randint(0, 9)) for _ in range(len(decimal_part)))

            return f"{new_integer}.{new_decimal}"
        else:
            # Integer number: first digit 1-9, rest 0-9
            return str(random.randint(1, 999))

    # Match numbers (integers and decimals)
    result = re.sub(r'\b\d+\.?\d*\b', randomize_number, result)

    return result


def _load_opposites() -> Dict[str, str]:
    """
    Load word opposites from JSON file.

    Returns:
        Dictionary of word opposites
    """
    # Use absolute path from project_paths utility
    opposites_path = get_builtins_dir() / "lie_opposites.json"

    try:
        with open(opposites_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data.get('opposites', {})
    except (FileNotFoundError, json.JSONDecodeError):
        # Return empty dict if file not found or invalid
        return {}
