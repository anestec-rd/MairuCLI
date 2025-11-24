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
    Echo command - print arguments with environment variable expansion.

    Supports:
    - $VAR or ${VAR} syntax (Unix-style)
    - %VAR% syntax (Windows-style)

    Args:
        args: Arguments to print

    Returns:
        True (always handled)
    """
    import re

    # Join arguments
    text = " ".join(args)

    # Expand environment variables
    # Unix-style: $VAR or ${VAR}
    def expand_unix_var(match):
        """Expand Unix-style environment variable ($VAR or ${VAR})."""
        var_name = match.group(1) or match.group(2)
        return os.environ.get(var_name, match.group(0))

    text = re.sub(r'\$\{([^}]+)\}|\$(\w+)', expand_unix_var, text)

    # Windows-style: %VAR%
    def expand_windows_var(match):
        """Expand Windows-style environment variable (%VAR%)."""
        var_name = match.group(1)
        return os.environ.get(var_name, match.group(0))

    text = re.sub(r'%(\w+)%', expand_windows_var, text)

    print(text)
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
