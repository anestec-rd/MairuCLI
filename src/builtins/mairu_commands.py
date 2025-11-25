"""
MairuCLI-specific commands.

Provides MairuCLI-specific commands: help, stats
"""

from typing import List
from src.config import DISPLAY_SEPARATOR_WIDTH


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

    print(colorize("Navigation & File Management:", "green"))
    print("  cd [path]    - Change directory")
    print("  pwd          - Print working directory")
    print("  ls / dir     - List directory contents")
    print("  tree [path]  - Show directory tree structure")
    print("  touch <file> - Create empty file")
    print("  mkdir <dir>  - Create directory")
    print("  cat [file]   - Display file contents =^.^=")
    print()

    print(colorize("Search & Find:", "green"))
    print("  find <pattern> - Find files by name")
    print("  grep <pattern> <file> - Search text in files")
    print("  which <cmd>  - Show command location")
    print()

    print(colorize("System Info:", "green"))
    print("  whoami       - Show current username")
    print("  hostname     - Show computer name")
    print("  date         - Show current date and time")
    print("  env          - Show environment variables")
    print()

    print(colorize("Utilities:", "green"))
    print("  echo [text]  - Print text to screen")
    print("  clear / cls  - Clear terminal screen")
    print("  history      - Show command history")
    print("  alias        - Show available command aliases")
    print()

    print(colorize("MairuCLI Specific:", "green"))
    print("  stats        - Show how many times I saved you")
    print("  help         - Show this help message")
    print("  exit/quit    - Exit MairuCLI")
    print()

    print(colorize("System Commands:", "purple"))
    print("  Any other command will be passed to your system shell")
    print("  (after safety checks, of course!)")
    print()

    print(colorize("💀 Dangerous Commands (DON'T try these!):", "red"))
    print(f"  {EMOJI['fire']} rm -rf /        "
          "- Deletes EVERYTHING (seriously, don't)")
    print(f"  {EMOJI['unlock']} chmod 777 file  "
          "- Makes files world-writable (bad idea)")
    print(f"  {EMOJI['lock']} chmod 000 file  "
          "- Locks file completely (even you can't access)")
    print(f"  {EMOJI['bomb']} dd if=/dev/zero "
          "- Overwrites your disk (yikes!)")
    print(f"  {EMOJI['disk']} > /dev/sda      "
          "- Destroys disk directly (instant data loss)")
    print(f"  {EMOJI['disk']} mkfs /dev/sda   "
          "- Formats entire disk (everything gone)")
    print(f"  {EMOJI['skull']} echo c > /proc/sysrq-trigger "
          "- Crashes kernel (instant reboot)")
    print(f"  {EMOJI['shredder']} shred /dev/sda  "
          "- Secure wipes disk (unrecoverable)")
    print(f"  {EMOJI['fire']} DROP DATABASE   "
          "- Deletes entire database (career-ending)")
    print(f"  {EMOJI['fire']} :()\u007b :|:& \u007d;: "
          "- Fork bomb (freezes system)")
    print()

    print(colorize("⚠️  Caution Commands (Think twice!):", "purple"))
    print(f"  {EMOJI['skull']} sudo su         "
          "- Enters root shell (all safety off)")
    print(f"  {EMOJI['skull']} chmod 666/755   "
          "- Makes files readable by others")
    print(f"  {EMOJI['skull']} iptables -F     "
          "- Disables firewall (security risk)")
    print(f"  {EMOJI['skull']} setenforce 0    "
          "- Disables SELinux (weakens security)")
    print(f"  {EMOJI['skull']} kill -9 <pid>   "
          "- Force kills process (may lose data)")
    print(f"  {EMOJI['skull']} git push --force "
          "- Overwrites remote (may lose teammates' work)")
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
