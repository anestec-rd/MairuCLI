"""
MairuCLI-specific commands.

Provides MairuCLI-specific commands: help, stats
"""

from typing import List


def cmd_help(args: List[str]) -> bool:
    """
    Display help information with a spooky twist.

    Args:
        args: Command arguments (ignored)

    Returns:
        True (always handled)
    """
    from src.display import colorize, EMOJI

    print("\n" + "=" * 60)
    print(f"{EMOJI['pumpkin']} {colorize('MairuCLI Help', 'orange')} "
          f"{EMOJI['pumpkin']}")
    print("=" * 60)
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

    print(colorize("⚠️  Dangerous Commands (DON'T try these!):", "red"))
    print(f"  {EMOJI['fire']} rm -rf /        "
          "- Deletes EVERYTHING (seriously, don't)")
    print(f"  {EMOJI['skull']} chmod 777 file  "
          "- Makes files world-writable (bad idea)")
    print(f"  {EMOJI['fire']} dd if=/dev/zero "
          "- Overwrites your disk (yikes!)")
    print(f"  {EMOJI['fire']} DROP DATABASE   "
          "- Deletes entire database (career-ending)")
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
    print("=" * 60 + "\n")

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

    print("\n" + "=" * 60)
    pumpkin = EMOJI['pumpkin']
    title = colorize('MairuCLI Statistics', 'orange')
    print(f"{pumpkin} {title} {pumpkin}")
    print("=" * 60)
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

        # Display unlocked achievements
        from src.display import get_unlocked_achievements
        unlocked = get_unlocked_achievements()

        if unlocked:
            # Categorize achievements
            danger_achievements = [
                "First Blood", "Persistent Troublemaker",
                "Danger Addict", "Stubborn"
            ]

            danger_list = [ach for ach in unlocked
                           if ach in danger_achievements]
            other_list = [ach for ach in unlocked
                          if ach not in danger_achievements]

            # Display danger-related achievements
            if danger_list:
                print(colorize("💀 Your Troublemaking History:", "red"))
                print()
                for achievement in danger_list:
                    print(f"  {colorize('✓', 'green')} {achievement}")
                print()

            # Display other achievements
            if other_list:
                print(colorize("🏆 Unlocked Achievements:", "orange"))
                print()
                for achievement in other_list:
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
    print("=" * 60 + "\n")

    return True
