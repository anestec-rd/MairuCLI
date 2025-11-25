"""
Main entry point for MairuCLI.

This module provides the REPL loop and command processing logic.
"""

import random
import subprocess
import sys

from src.builtins import BuiltinCommands
from src.display import (
    colorize,
    display_goodbye_message,
    display_welcome_banner,
    show_warning,
    show_caution_warning,
    track_safe_command
)
from src.interceptor import check_command


# Command not found message variations (Halloween-themed)
COMMAND_NOT_FOUND_MESSAGES = [
    {
        "emoji": "🍬",
        "message": "Sorry, we don't sell '{cmd}' at the candy store.",
        "subtitle": "(Command not found)"
    },
    {
        "emoji": "👻",
        "message": "Boo! '{cmd}' vanished into thin air!",
        "subtitle": "(Command not found)"
    },
    {
        "emoji": "🎃",
        "message": "'{cmd}' is not in my trick-or-treat bag!",
        "subtitle": "(Command not found)"
    },
    {
        "emoji": "🦇",
        "message": "'{cmd}' flew away with the bats!",
        "subtitle": "(Command not found)"
    },
    {
        "emoji": "🕷️",
        "message": (
            "'{cmd}' got caught in a spider web... and disappeared!"
        ),
        "subtitle": "(Command not found)"
    },
    {
        "emoji": "🧙",
        "message": "Even my magic can't summon '{cmd}'!",
        "subtitle": "(Command not found)"
    },
    {
        "emoji": "💀",
        "message": "'{cmd}' is dead... because it never existed!",
        "subtitle": "(Command not found)"
    },
    {
        "emoji": "🌙",
        "message": (
            "'{cmd}' only appears on a full moon... which is not today!"
        ),
        "subtitle": "(Command not found)"
    }
]


def show_command_not_found(cmd_name: str) -> None:
    """
    Display a random Halloween-themed 'command not found' message.

    Args:
        cmd_name: Name of the command that was not found
    """
    variation = random.choice(COMMAND_NOT_FOUND_MESSAGES)
    print(f"{variation['emoji']} {variation['message'].format(cmd=cmd_name)}")
    print(f"   {variation['subtitle']}")


def main() -> None:
    """
    Main entry point for MairuCLI.
    Displays welcome banner and starts REPL loop.
    """
    display_welcome_banner()

    try:
        repl_loop()
    except KeyboardInterrupt:
        print("\n")
        display_goodbye_message()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


def repl_loop() -> None:
    """
    Read-Eval-Print Loop for command processing.
    Continues until user exits.
    """
    while True:
        try:
            # Display colored prompt
            prompt = colorize("mairu> ", "orange")
            command = input(prompt).strip()

            if not command:
                continue

            result = process_command(command)
            if result == "EXIT":
                display_goodbye_message()
                break

        except EOFError:
            print()
            display_goodbye_message()
            break
        except KeyboardInterrupt:
            print()
            continue


def process_command(command: str) -> str:
    """
    Process a single command through three-layer routing:
    1. Check if dangerous command → warn and block (HIGHEST PRIORITY)
    2. Check if builtin command → execute internally
    3. Otherwise → execute in system shell

    Args:
        command: User-entered command string

    Returns:
        "EXIT" if user wants to exit, otherwise empty string
    """
    # Add to history
    BuiltinCommands.add_to_history(command)

    # Check for exit command
    if command in ["exit", "quit"]:
        return "EXIT"

    # Parse command into parts
    parts = command.split()
    if not parts:
        return ""

    cmd_name = parts[0]
    args = parts[1:]

    # Layer 1: Check system directory protection (HIGHEST PRIORITY)
    from src.interceptor import check_system_directory
    sys_level, sys_type, sys_path = check_system_directory(command)

    if sys_level == "critical":
        # Critical system directory - block immediately
        from src.display import show_system_protection_warning
        show_system_protection_warning("critical", sys_path, command)
        # Statistics are already updated by show_system_protection_warning
        return ""
    elif sys_level == "caution":
        # Caution system directory - warn and ask for confirmation
        from src.display import show_system_protection_warning
        if not show_system_protection_warning("caution", sys_path, command):
            print(colorize("Command cancelled.", "chocolate"))
            return ""
        # User confirmed - continue to next checks

    # Layer 2: Check if dangerous or caution command (BEFORE builtin execution)
    level, pattern_name = check_command(command)

    if level == "critical":
        # Critical: Block with warning
        show_warning(pattern_name, command)
        return ""
    elif level == "caution":
        # Caution: Warn and ask for confirmation
        if not show_caution_warning(pattern_name, command):
            print(colorize("Command cancelled.", "chocolate"))
            return ""
        # User confirmed - proceed to next checks

    # Layer 3: Check if builtin command
    if BuiltinCommands.is_builtin(cmd_name):
        BuiltinCommands.execute_builtin(cmd_name, args)
        # Track safe command usage for achievements
        track_safe_command(cmd_name)
        return ""

    # Layer 4: Execute in system shell (safe or confirmed caution command)
    execute_in_system_shell(command)
    # Track safe command usage for achievements
    track_safe_command(cmd_name)
    return ""


def execute_in_system_shell(command: str) -> None:
    """
    Execute command in system shell using subprocess.

    Args:
        command: Command to execute

    Note:
        Uses shell=True to support pipes, redirects, and globs.
        This is safe because dangerous commands are already filtered.
    """
    try:
        # Detect system encoding (Windows uses cp932, Unix uses utf-8)
        import locale
        system_encoding = locale.getpreferredencoding()

        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            encoding=system_encoding,
            errors='replace'  # Replace decode errors with �
        )

        # Print stdout if any
        if result.stdout:
            print(result.stdout, end='')

        # Check if command was not found (Windows/Unix)
        if result.returncode != 0 and result.stderr:
            stderr_lower = result.stderr.lower()
            # Windows PowerShell: "用語 'xxx' は、コマンドレット..."
            # Windows CMD: "'xxx' は、内部コマンドまたは外部コマンド..."
            # Windows: "'xxx' is not recognized..."
            # Unix: "command not found"
            if ('not recognized' in stderr_lower or
                    'command not found' in stderr_lower or
                    '内部コマンドまたは外部コマンド' in result.stderr or
                    '用語' in result.stderr and 'コマンドレット' in result.stderr or
                    'not found' in stderr_lower):
                cmd_name = (
                    command.split()[0] if command.split() else command
                )
                show_command_not_found(cmd_name)
            else:
                # Other errors - print as is
                print(result.stderr, end='')

    except FileNotFoundError:
        cmd_name = command.split()[0] if command.split() else command
        show_command_not_found(cmd_name)
    except Exception as e:
        print(f"Error executing command: {e}")


if __name__ == "__main__":
    main()
