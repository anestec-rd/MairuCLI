"""
File operation commands for MairuCLI.

Provides file management commands: ls, cat, touch, mkdir
"""

import subprocess
import sys
from pathlib import Path
from typing import List


def cmd_ls(args: List[str]) -> bool:
    """
    List directory contents (cross-platform).

    Args:
        args: Command arguments (path, flags)

    Returns:
        True (always handled)
    """
    # Determine which command to use based on platform
    if sys.platform == "win32":
        # Windows: use dir
        cmd = ["cmd", "/c", "dir"] + args
    else:
        # Unix: use ls
        cmd = ["ls", "--color=auto"] + args

    try:
        subprocess.run(cmd, check=False)
    except Exception as e:
        print(f"ls: error: {e}")

    return True


def cmd_dir(args: List[str]) -> bool:
    """
    List directory contents (Windows style).
    Alias for ls command.

    Args:
        args: Command arguments

    Returns:
        True (always handled)
    """
    return cmd_ls(args)


def cmd_cat(args: List[str]) -> bool:
    """
    Display file contents (with a Halloween twist!).

    Args:
        args: File paths to display

    Returns:
        True (always handled)
    """
    from src.display import colorize

    if not args:
        print()
        print(colorize("=^.^= Meow! Cat here!", "purple"))
        print()
        print(colorize("Usage:", "orange"), "cat <filename>")
        print()
        print("🎃 Halloween tip: Black cats are good luck in some "
              "cultures!")
        print()
        return True

    for filename in args:
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
                print()
                print(f"{colorize('=^.^=', 'purple')} "
                      f"{colorize(filename, 'orange')}:")
                print()
                print(content)
                if not content.endswith('\n'):
                    print()
        except FileNotFoundError:
            print()
            print(f"{colorize('=^.^=', 'purple')} Meow? File not found: "
                  f"{colorize(filename, 'red')}")
            print()
        except PermissionError:
            print()
            print(f"{colorize('=^.^=', 'purple')} Hiss! Permission "
                  f"denied: {colorize(filename, 'red')}")
            print()
        except Exception as e:
            print()
            print(f"{colorize('=^.^=', 'purple')} *confused meow* "
                  f"Error reading {filename}: {e}")
            print()

    return True


def cmd_touch(args: List[str]) -> bool:
    """
    Create empty file or update timestamp.

    Args:
        args: File paths to create/touch

    Returns:
        True (always handled)
    """
    from src.display import colorize, EMOJI

    if not args:
        print(f"{EMOJI['pumpkin']} Usage: touch <filename>")
        print("Creates an empty file or updates its timestamp")
        return True

    for filename in args:
        try:
            Path(filename).touch()
            print(f"✨ Created/touched: {colorize(filename, 'green')}")
        except PermissionError:
            print(f"❌ Permission denied: {colorize(filename, 'red')}")
        except Exception as e:
            print(f"❌ Error: {e}")

    return True


def cmd_mkdir(args: List[str]) -> bool:
    """
    Create directory.

    Args:
        args: Directory paths to create

    Returns:
        True (always handled)
    """
    from src.display import colorize, EMOJI

    if not args:
        print(f"{EMOJI['pumpkin']} Usage: mkdir <directory>")
        print("Creates a new directory")
        return True

    for dirname in args:
        try:
            Path(dirname).mkdir(parents=False, exist_ok=False)
            print(f"📁 Created directory: {colorize(dirname, 'green')}")
        except FileExistsError:
            print(f"⚠️  Directory already exists: {colorize(dirname, 'chocolate')}")
        except PermissionError:
            print(f"❌ Permission denied: {colorize(dirname, 'red')}")
        except Exception as e:
            print(f"❌ Error: {e}")

    return True
