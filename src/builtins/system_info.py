"""
System information commands for MairuCLI.

Provides system info commands: whoami, date, hostname, env, export
"""

import os
import getpass
import datetime
import socket
from typing import List


def cmd_whoami(args: List[str]) -> bool:
    """
    Display current username.

    Args:
        args: Command arguments (unused)

    Returns:
        True (always handled)
    """
    from src.display import colorize

    try:
        username = getpass.getuser()
        print(f"👤 {colorize(username, 'orange')}")
    except Exception:
        print("👤 (unknown)")

    return True


def cmd_date(args: List[str]) -> bool:
    """
    Display current date and time.

    Args:
        args: Command arguments (unused)

    Returns:
        True (always handled)
    """
    from src.display import colorize

    now = datetime.datetime.now()
    formatted_date = now.strftime("%Y-%m-%d %H:%M:%S %A")
    print(f"📅 {colorize(formatted_date, 'purple')}")

    return True


def cmd_hostname(args: List[str]) -> bool:
    """
    Display hostname.

    Args:
        args: Command arguments (unused)

    Returns:
        True (always handled)
    """
    from src.display import colorize

    try:
        hostname = socket.gethostname()
        print(f"🖥️  {colorize(hostname, 'orange')}")
    except Exception:
        print("🖥️  (unknown)")

    return True


def cmd_export(args: List[str]) -> bool:
    """
    Set environment variable.

    Args:
        args: Variable assignments (VAR=value)

    Returns:
        True (always handled)
    """
    if not args:
        # export without args → show all env vars
        for key, value in sorted(os.environ.items()):
            print(f"{key}={value}")
        return True

    # export VAR=value
    for arg in args:
        if "=" in arg:
            key, value = arg.split("=", 1)
            os.environ[key] = value
        else:
            print(f"export: invalid format: {arg}")
    return True


def cmd_env(args: List[str]) -> bool:
    """
    Display environment variables.
    Alias for export command without arguments.

    Args:
        args: Command arguments (ignored)

    Returns:
        True (always handled)
    """
    return cmd_export([])
