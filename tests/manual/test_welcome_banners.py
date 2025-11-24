"""
Manual test script to preview different welcome banner designs.

Run this to see all welcome banner options and choose the best one.
"""

import os
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.display.ascii_renderer import AsciiRenderer


def show_banner_option(name: str, file_path: str, description: str):
    """Display a banner option with description."""
    renderer = AsciiRenderer()

    print("\n" + "=" * 80)
    print(f"OPTION: {name}")
    print(f"Description: {description}")
    print("=" * 80)

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Apply colors
            colored = renderer.colorize(content, "orange")
            print(colored)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"Error loading banner: {e}")

    print("=" * 80)


def main():
    """Show all welcome banner options."""
    print("\n🎃 MairuCLI Welcome Banner Options 🎃\n")
    print("Testing different ASCII art designs for the startup screen...")

    base_path = "data/ascii_art"

    # Option 1: Kiro Ghost
    show_banner_option(
        "1. Kiro Ghost",
        os.path.join(base_path, "welcome_kiro_ghost.txt"),
        "Cute ghost character representing Kiro (project name origin)"
    )

    input("\nPress Enter to see next option...")

    # Option 2: Jack-o'-lantern
    show_banner_option(
        "2. Jack-o'-lantern",
        os.path.join(base_path, "welcome_jack.txt"),
        "Classic Halloween pumpkin - simple and recognizable"
    )

    input("\nPress Enter to see next option...")

    # Option 3: MairuCLI Banner
    show_banner_option(
        "3. MairuCLI Text Banner",
        os.path.join(base_path, "welcome_mairu_banner.txt"),
        "Bold ASCII text logo - professional and clear"
    )

    input("\nPress Enter to see next option...")

    # Option 4: Halloween Party
    show_banner_option(
        "4. Halloween Party",
        os.path.join(base_path, "welcome_halloween_party.txt"),
        "Full Halloween theme with emojis and text logo"
    )

    print("\n" + "=" * 80)
    print("Which option do you prefer?")
    print("1. Kiro Ghost (cute, project identity)")
    print("2. Jack-o'-lantern (classic, simple)")
    print("3. MairuCLI Text Banner (professional, clear)")
    print("4. Halloween Party (festive, full theme)")
    print("=" * 80)


if __name__ == "__main__":
    main()
