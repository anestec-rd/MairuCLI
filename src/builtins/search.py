"""
Search commands for MairuCLI.

Provides search and find commands: find, grep, which
"""

import os
import re
import sys
from pathlib import Path
from typing import List


def cmd_find(args: List[str]) -> bool:
    """
    Find files by name pattern (simplified version).

    Args:
        args: Pattern to search for

    Returns:
        True (always handled)
    """
    from src.display import colorize, EMOJI

    if not args:
        print(f"{EMOJI['pumpkin']} Usage: find <pattern>")
        print("Searches for files matching the pattern in current directory")
        print()
        print("Examples:")
        print("  find *.py      - Find all Python files")
        print("  find test      - Find files containing 'test'")
        return True

    pattern = args[0]
    current_dir = Path.cwd()
    found_count = 0

    print(f"🔍 Searching for '{colorize(pattern, 'orange')}' in {current_dir}...")
    print()

    try:
        # Use rglob for recursive search
        if '*' in pattern or '?' in pattern:
            # Glob pattern
            matches = list(current_dir.rglob(pattern))
        else:
            # Simple substring search
            matches = [p for p in current_dir.rglob('*')
                      if pattern.lower() in p.name.lower()]

        for match in sorted(matches)[:50]:  # Limit to 50 results
            relative_path = match.relative_to(current_dir)
            if match.is_dir():
                print(f"  📁 {colorize(str(relative_path), 'purple')}/")
            else:
                print(f"  📄 {colorize(str(relative_path), 'green')}")
            found_count += 1

        print()
        if found_count == 0:
            print(f"{EMOJI['ghost']} No files found matching '{pattern}'")
        elif found_count == 50:
            print(f"✨ Found {colorize(str(found_count), 'orange')}+ matches (showing first 50)")
        else:
            print(f"✨ Found {colorize(str(found_count), 'orange')} match(es)")

    except Exception as e:
        print(f"❌ Error searching: {e}")

    return True


def cmd_grep(args: List[str]) -> bool:
    """
    Search for pattern in files (simplified version).

    Args:
        args: Pattern and file(s) to search

    Returns:
        True (always handled)
    """
    from src.display import colorize, EMOJI

    if len(args) < 2:
        print(f"{EMOJI['pumpkin']} Usage: grep <pattern> <file>")
        print("Searches for text pattern in file(s)")
        print()
        print("Examples:")
        print("  grep TODO file.txt       - Find 'TODO' in file.txt")
        print("  grep 'hello' *.py        - Find 'hello' in Python files")
        return True

    pattern = args[0]
    files = args[1:]
    total_matches = 0

    print(f"🔍 Searching for '{colorize(pattern, 'orange')}'...")
    print()

    for file_pattern in files:
        # Handle wildcards
        if '*' in file_pattern or '?' in file_pattern:
            matching_files = list(Path.cwd().glob(file_pattern))
        else:
            matching_files = [Path(file_pattern)]

        for filepath in matching_files:
            if not filepath.is_file():
                continue

            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    file_matches = 0
                    for line_num, line in enumerate(f, 1):
                        if re.search(pattern, line, re.IGNORECASE):
                            if file_matches == 0:
                                print(f"{colorize(str(filepath), 'purple')}:")
                            # Highlight the match
                            highlighted = re.sub(
                                f'({re.escape(pattern)})',
                                lambda m: colorize(m.group(1), 'orange'),
                                line.rstrip(),
                                flags=re.IGNORECASE
                            )
                            print(f"  {colorize(str(line_num), 'chocolate')}: {highlighted}")
                            file_matches += 1
                            total_matches += 1

                    if file_matches > 0:
                        print()

            except PermissionError:
                print(f"❌ Permission denied: {filepath}")
            except Exception as e:
                print(f"❌ Error reading {filepath}: {e}")

    if total_matches == 0:
        print(f"{EMOJI['ghost']} No matches found for '{pattern}'")
    else:
        print(f"✨ Found {colorize(str(total_matches), 'orange')} match(es)")

    return True


def cmd_which(args: List[str]) -> bool:
    """
    Show location of command in PATH.

    Args:
        args: Command name(s) to locate

    Returns:
        True (always handled)
    """
    from src.display import colorize, EMOJI

    if not args:
        print(f"{EMOJI['pumpkin']} Usage: which <command>")
        print("Shows the location of a command in your PATH")
        return True

    # Import here to avoid circular dependency
    from src.builtins import BuiltinCommands

    path_env = os.environ.get('PATH', '')
    path_dirs = path_env.split(os.pathsep)

    for cmd_name in args:
        found = False

        # Check if it's a builtin first
        if BuiltinCommands.is_builtin(cmd_name):
            print(f"{colorize(cmd_name, 'green')}: MairuCLI builtin command")
            found = True
            continue

        # Search in PATH
        for path_dir in path_dirs:
            if sys.platform == "win32":
                # Windows: check with common extensions
                for ext in ['', '.exe', '.bat', '.cmd', '.com']:
                    cmd_path = Path(path_dir) / f"{cmd_name}{ext}"
                    if cmd_path.is_file():
                        print(f"{colorize(cmd_name, 'green')}: {cmd_path}")
                        found = True
                        break
            else:
                # Unix: check without extension
                cmd_path = Path(path_dir) / cmd_name
                if cmd_path.is_file() and os.access(cmd_path, os.X_OK):
                    print(f"{colorize(cmd_name, 'green')}: {cmd_path}")
                    found = True
                    break

            if found:
                break

        if not found:
            print(f"{EMOJI['ghost']} {cmd_name}: not found in PATH")

    return True
