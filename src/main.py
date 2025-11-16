"""
Main entry point for MairuCLI.

This module provides the REPL loop and command processing logic.
"""

import subprocess
import sys

from src.builtins import BuiltinCommands
from src.display import (
    colorize,
    display_goodbye_message,
    display_welcome_banner,
    show_warning
)
from src.interceptor import check_command


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
    1. Check if builtin command → execute internally
    2. Check if dangerous command → warn and block
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

    # Layer 1: Check if builtin command
    if BuiltinCommands.is_builtin(cmd_name):
        BuiltinCommands.execute_builtin(cmd_name, args)
        return ""

    # Layer 2: Check if dangerous command
    is_dangerous, pattern_name = check_command(command)
    if is_dangerous:
        show_warning(pattern_name, command)
        return ""

    # Layer 3: Execute in system shell (safe command)
    execute_in_system_shell(command)
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
        subprocess.run(
            command,
            shell=True,
            capture_output=False,
            text=True
        )
        # Exit code is automatically handled by subprocess
    except FileNotFoundError:
        print(f"Command not found: {command.split()[0]}")
    except Exception as e:
        print(f"Error executing command: {e}")


if __name__ == "__main__":
    main()
