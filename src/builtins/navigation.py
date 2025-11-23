"""
Navigation commands for MairuCLI.

Provides directory navigation commands: cd, pwd
"""

import os
from pathlib import Path
from typing import List, Optional


# Shared state for cd command
_prev_dir: Optional[Path] = None


def cmd_cd(args: List[str]) -> bool:
    """
    Change directory command.
    Supports: cd, cd ~, cd -, cd /path

    Args:
        args: Command arguments

    Returns:
        True (always handled)
    """
    global _prev_dir

    if not args:
        # cd without args → go to home
        target = Path.home()
    elif args[0] == "~":
        target = Path.home()
    elif args[0] == "-":
        # cd - → go to previous directory
        if _prev_dir:
            target = _prev_dir
        else:
            print("cd: no previous directory")
            return True
    else:
        target = Path(args[0]).expanduser()

    try:
        _prev_dir = Path.cwd()  # Save current for cd -
        os.chdir(target)
        return True
    except FileNotFoundError:
        print(f"cd: no such file or directory: {target}")
        return True
    except PermissionError:
        print(f"cd: permission denied: {target}")
        return True


def cmd_pwd(args: List[str]) -> bool:
    """
    Print working directory.

    Args:
        args: Command arguments (ignored)

    Returns:
        True (always handled)
    """
    print(os.getcwd())
    return True
