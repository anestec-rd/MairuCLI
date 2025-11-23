"""
Display commands for MairuCLI.

Provides visual display commands: tree
"""

from pathlib import Path
from typing import List


def cmd_tree(args: List[str]) -> bool:
    """
    Display directory tree structure (simplified version).

    Args:
        args: Directory path (optional)

    Returns:
        True (always handled)
    """
    from src.display import colorize, EMOJI

    target_dir = Path(args[0]) if args else Path.cwd()

    if not target_dir.exists():
        print(f"❌ Directory not found: {target_dir}")
        return True

    if not target_dir.is_dir():
        print(f"❌ Not a directory: {target_dir}")
        return True

    print(f"🌳 {colorize(str(target_dir), 'orange')}")

    def print_tree(directory: Path, prefix: str = "", max_depth: int = 3, current_depth: int = 0):
        """Recursively print directory tree."""
        if current_depth >= max_depth:
            return

        try:
            entries = sorted(directory.iterdir(), key=lambda p: (not p.is_dir(), p.name))
            entries = [e for e in entries if not e.name.startswith('.')]  # Skip hidden files

            for i, entry in enumerate(entries[:20]):  # Limit to 20 entries per directory
                is_last = i == len(entries) - 1
                current_prefix = "└── " if is_last else "├── "
                next_prefix = "    " if is_last else "│   "

                if entry.is_dir():
                    print(f"{prefix}{current_prefix}{colorize(entry.name, 'purple')}/")
                    print_tree(entry, prefix + next_prefix, max_depth, current_depth + 1)
                else:
                    print(f"{prefix}{current_prefix}{colorize(entry.name, 'green')}")

            if len(entries) > 20:
                print(f"{prefix}... ({len(entries) - 20} more items)")

        except PermissionError:
            print(f"{prefix}❌ Permission denied")

    print_tree(target_dir)
    print()
    print(f"{EMOJI['pumpkin']} Tip: tree shows up to 3 levels deep")

    return True
