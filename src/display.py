"""
Display system for MairuCLI.

This module handles ASCII art rendering, color management,
and message formatting.
"""

import random
from pathlib import Path
from typing import Dict, List


# Halloween color palette (ANSI 256-color codes)
# Reference: .kiro/steering/halloween-theme.md
COLORS: Dict[str, str] = {
    "orange": "\033[38;5;208m",
    "chocolate": "\033[38;5;130m",
    "purple": "\033[38;5;141m",
    "green": "\033[38;5;46m",
    "red": "\033[38;5;196m",
    "reset": "\033[0m"
}

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

# Track warned commands for "I told you so" feature
_warned_commands: Dict[str, int] = {}

# Track statistics
_stats = {
    "dangerous_blocked": 0,
    "typos_caught": 0
}

# Track achievements
_achievements: List[str] = []

# Warning message variations for different patterns
WARNING_VARIATIONS = {
    "rm_root": [
        ("YOU'RE FIRED!", "(And so is your entire filesystem!)"),
        ("GAME OVER!", "(No continues, no save points)"),
        ("NOPE. JUST NOPE.", "(Not today, Satan)"),
        ("ABORT! ABORT!", "(This is not a drill!)"),
        ("DENIED!", "(Your filesystem thanks me)")
    ],
    "chmod_777": [
        ("PERMISSION DENIED!", "(By your future self)"),
        ("SECURITY BREACH ALERT!", "(This is how hacks happen)"),
        ("WIDE OPEN DOORS!", "(Might as well remove the locks)"),
        ("EVERYONE'S INVITED!", "(Including the bad guys)")
    ],
    "data_destroyer": [
        ("DATA DESTROYER DETECTED!", "(This will not end well)"),
        ("DISK ANNIHILATOR!", "(Say goodbye to your data)"),
        ("POINT OF NO RETURN!", "(Backups? Anyone?)"),
        ("CAREER ENDER!", "(Update your resume now)")
    ]
}


def colorize(text: str, color_name: str) -> str:
    """
    Apply ANSI color to text.

    Args:
        text: Text to colorize
        color_name: Name of color from COLORS dict

    Returns:
        Colorized text with reset code
    """
    return f"{COLORS[color_name]}{text}{COLORS['reset']}"


def display_welcome_banner() -> None:
    """
    Display Halloween-themed welcome banner on startup.
    """
    orange_line = colorize(
        "╔═══════════════════════════════════════════════════════════╗",
        "orange"
    )
    orange_bar = colorize("║", "orange")
    pumpkin = EMOJI['pumpkin']
    title = colorize("Welcome to MairuCLI", "red")
    subtitle = colorize(
        "Your friendly CLI safety wrapper with a spooky twist!",
        "chocolate"
    )
    bottom_line = colorize(
        "╚═══════════════════════════════════════════════════════════╝",
        "orange"
    )
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

    spaces = " " * 18
    banner = f"""
{orange_line}
{orange_bar}  {pumpkin} {title} {pumpkin}{spaces}{orange_bar}
{orange_bar}  {subtitle}  {orange_bar}
{bottom_line}

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
        _stats["typos_caught"] += 1
    else:
        _stats["dangerous_blocked"] += 1

    # Check if this command was already warned about
    if command in _warned_commands:
        _warned_commands[command] += 1
        show_repeat_warning(command, _warned_commands[command])
    else:
        _warned_commands[command] = 1

    if pattern_name.startswith("typo_"):
        show_typo_warning(pattern_name, command)
    else:
        show_danger_warning(pattern_name, command)

    # Check for achievements
    check_achievements()


def show_repeat_warning(command: str, count: int) -> None:
    """
    Display escalating sarcastic message for repeated dangerous commands.

    Args:
        command: The dangerous command (again!)
        count: Number of times user tried this command
    """
    print("\n" + "=" * 60)

    if count == 2:
        # First repeat - gentle reminder
        print(f"{EMOJI['eyes']} {colorize('Wait...', 'orange')}")
        print(colorize("Haven't we been here before?", "chocolate"))
        print()
        print(f"{colorize('I JUST warned you about this!', 'red')}")
        print("Did you think I was joking?")

    elif count == 3:
        # Second repeat - getting annoyed
        print(f"{EMOJI['facepalm']} {colorize('Seriously?', 'red')}")
        print(colorize("I told you so...", "orange"))
        print()
        print("This is the THIRD time you've tried this!")
        print("Are you testing me, or just not listening?")

    elif count == 4:
        # Third repeat - exasperated
        print(f"{EMOJI['facepalm']}{EMOJI['facepalm']} "
              f"{colorize('REALLY?!', 'red')} "
              f"{EMOJI['facepalm']}{EMOJI['facepalm']}")
        print()
        print(colorize("Okay, I give up.", "chocolate"))
        print("You clearly want to learn the hard way.")
        print("But I'm STILL not letting you run this command.")

    else:
        # Fourth+ repeat - just disappointed
        print(f"{EMOJI['ghost']} {colorize('*sigh*', 'purple')}")
        print()
        print(f"Attempt #{count}. Still blocked.")
        print("I'm not mad, just... disappointed.")

    print("=" * 60)
    print()


def show_danger_warning(pattern_name: str, command: str) -> None:
    """
    Display warning for dangerous command with ASCII art.

    Args:
        pattern_name: Name of matched dangerous pattern
        command: The dangerous command entered
    """
    from src.interceptor import get_pattern_info

    pattern_info = get_pattern_info(pattern_name)

    # Load ASCII art (will show placeholder if file doesn't exist yet)
    art = load_ascii_art(pattern_info.get("art_file", "fired.txt"))

    # Display warning based on pattern category
    print("\n" + "=" * 60)

    # Get random variation for this pattern type
    if pattern_name == "rm_root":
        variation_key = "rm_root"
    elif pattern_name == "chmod_777":
        variation_key = "chmod_777"
    else:
        variation_key = "data_destroyer"

    variations = WARNING_VARIATIONS[variation_key]
    title_text, subtitle_text = random.choice(variations)

    if pattern_name == "rm_root":
        print(colorize(art, "red"))
        fire = EMOJI['fire']
        title = colorize(title_text, 'red')
        print(f"{fire} {title} {fire}")
        subtitle = colorize(subtitle_text, "orange")
        print(subtitle)
        print()
        print("The command 'rm -rf /' attempts to delete EVERYTHING.")
        print("This is unrecoverable without backups.")
        print()
        print(f"{EMOJI['lightbulb']} {colorize('Safe alternative:', 'green')}")
        print("  - Use 'rm -i' for interactive confirmation")
        print("  - Use 'trash-cli' instead of rm")

    elif pattern_name == "chmod_777":
        print(colorize(art, "purple"))
        skull = EMOJI['skull']
        title = colorize(title_text, 'red')
        print(f"{skull} {title} {skull}")
        subtitle = colorize(subtitle_text, "orange")
        print(subtitle)
        print()
        print("chmod 777 gives EVERYONE full access to your files.")
        print("This is a major security risk!")
        print()
        print(f"{EMOJI['lightbulb']} {colorize('Safe alternative:', 'green')}")
        print("  - Use specific permissions like 'chmod 755' or 'chmod 644'")
        print("  - Only give write access when necessary")

    elif pattern_name in ["dd_zero", "drop_database", "sudo_rm_var"]:
        print(colorize(art, "red"))
        fire = EMOJI['fire']
        title = colorize(title_text, 'red')
        print(f"{fire} {title} {fire}")
        subtitle = colorize(subtitle_text, "orange")
        print(subtitle)
        print()
        print(f"The command '{command}' is extremely dangerous.")
        print("It can cause irreversible data loss.")
        print()
        print(f"{EMOJI['lightbulb']} {colorize('Safe alternative:', 'green')}")
        print("  - Always backup before destructive operations")
        print("  - Test commands in a safe environment first")

    print()
    print(colorize(f"Blocked command: {command}", "chocolate"))
    print("=" * 60 + "\n")


def show_typo_warning(pattern_name: str, command: str) -> None:
    """
    Display fun warning for typo with suggestion.

    Args:
        pattern_name: Name of matched typo pattern (with 'typo_' prefix)
        command: The typo command entered
    """
    from src.interceptor import get_pattern_info

    pattern_info = get_pattern_info(pattern_name)

    print("\n" + "=" * 60)
    print(pattern_info.get("message", "Oops! Typo detected!"))
    print()
    print(f"You typed: {colorize(command, 'red')}")
    print(f"Did you mean: {colorize(pattern_info['correct'], 'green')}?")
    print("=" * 60 + "\n")


def check_achievements() -> None:
    """
    Check if user has unlocked any achievements.
    Display achievement notification if newly unlocked.
    """
    total_blocks = _stats["dangerous_blocked"]
    total_typos = _stats["typos_caught"]

    # Achievement: First Blood
    if total_blocks == 1 and "first_blood" not in _achievements:
        _achievements.append("first_blood")
        show_achievement(
            "First Blood",
            "Blocked your first dangerous command!"
        )

    # Achievement: Persistent Troublemaker
    if total_blocks >= 5 and "persistent" not in _achievements:
        _achievements.append("persistent")
        show_achievement(
            "Persistent Troublemaker",
            "Tried 5 dangerous commands. Impressive dedication!"
        )

    # Achievement: Typo Master
    if total_typos >= 3 and "typo_master" not in _achievements:
        _achievements.append("typo_master")
        show_achievement(
            "Typo Master",
            "Made 3 typos. Your keyboard needs calibration!"
        )

    # Achievement: Danger Addict
    if total_blocks >= 10 and "danger_addict" not in _achievements:
        _achievements.append("danger_addict")
        show_achievement(
            "Danger Addict",
            "10 dangerous commands blocked. Do you have a death wish?"
        )

    # Achievement: Stubborn
    max_repeats = max(_warned_commands.values()) if _warned_commands else 0
    if max_repeats >= 3 and "stubborn" not in _achievements:
        _achievements.append("stubborn")
        show_achievement(
            "Stubborn",
            "Tried the same command 3 times. I admire your persistence!"
        )


def show_achievement(title: str, description: str) -> None:
    """
    Display achievement unlock notification.

    Args:
        title: Achievement title
        description: Achievement description
    """
    print()
    print("=" * 60)
    print(f"🏆 {colorize('ACHIEVEMENT UNLOCKED!', 'orange')} 🏆")
    print()
    print(f"  {colorize(title, 'purple')}")
    print(f"  {description}")
    print("=" * 60)
    print()


def get_stats() -> Dict[str, int]:
    """
    Get current statistics.

    Returns:
        Dictionary with statistics
    """
    return _stats.copy()


def load_ascii_art(filename: str) -> str:
    """
    Load ASCII art from file.

    Args:
        filename: Name of ASCII art file

    Returns:
        ASCII art as string, or placeholder if file not found
    """
    try:
        art_path = Path(__file__).parent.parent / "ascii_art" / filename
        with open(art_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return f"[ASCII art not found: {filename}]"
    except Exception as e:
        return f"[Error loading ASCII art: {e}]"
