"""
Shell utility commands for MairuCLI.

Provides utility commands: echo, clear, history, alias
"""

import os
import sys
from typing import List


# Shared state for history
_history: List[str] = []


def cmd_echo(args: List[str]) -> bool:
    """
    Echo command - print arguments.

    Args:
        args: Arguments to print

    Returns:
        True (always handled)
    """
    print(" ".join(args))
    return True


def cmd_clear(args: List[str]) -> bool:
    """
    Clear the terminal screen.

    Args:
        args: Command arguments (ignored)

    Returns:
        True (always handled)
    """
    if sys.platform == "win32":
        os.system("cls")
    else:
        os.system("clear")

    return True


def cmd_cls(args: List[str]) -> bool:
    """
    Clear the terminal screen (Windows style).
    Alias for clear command.

    Args:
        args: Command arguments (ignored)

    Returns:
        True (always handled)
    """
    return cmd_clear(args)


def cmd_history(args: List[str]) -> bool:
    """
    Show command history.

    Args:
        args: Command arguments (ignored)

    Returns:
        True (always handled)
    """
    for i, cmd in enumerate(_history, 1):
        print(f"{i:4d}  {cmd}")
    return True


def cmd_alias(args: List[str]) -> bool:
    """
    Display available command aliases.

    Args:
        args: Command arguments (ignored)

    Returns:
        True (always handled)
    """
    from src.display import colorize, EMOJI

    print()
    print(colorize("Available Aliases:", "orange"))
    print()
    print(f"  {colorize('ls', 'green')} / {colorize('dir', 'green')}   "
          "- List directory contents")
    print(f"  {colorize('clear', 'green')} / {colorize('cls', 'green')} "
          "- Clear terminal screen")
    print(f"  {colorize('env', 'green')}         "
          "- Show environment variables (same as export)")
    print(f"  {colorize('exit', 'green')} / {colorize('quit', 'green')} "
          "- Exit MairuCLI")
    print()
    print(f"{EMOJI['pumpkin']} Tip: These work on both Windows and Unix!")
    print()

    return True


def add_to_history(command: str) -> None:
    """
    Add command to history.

    Args:
        command: Command to add to history
    """
    _history.append(command)


def get_history() -> List[str]:
    """
    Get command history.

    Returns:
        List of commands in history
    """
    return _history.copy()
