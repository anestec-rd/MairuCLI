"""
Builtin command implementations for MairuCLI.

This module provides internal implementations of shell builtin commands
that must run in MairuCLI's process (cd, pwd, echo, etc.).
"""

import os
from pathlib import Path
from typing import List, Optional


class BuiltinCommands:
    """Internal implementation of shell builtin commands."""

    # Class variables for state
    _history: List[str] = []
    _prev_dir: Optional[Path] = None

    @classmethod
    def is_builtin(cls, cmd_name: str) -> bool:
        """
        Check if command is a builtin.

        Args:
            cmd_name: Name of the command

        Returns:
            True if command is a builtin, False otherwise
        """
        return cmd_name in [
            'cd', 'pwd', 'exit', 'quit', 'echo', 'export',
            'history', 'help', 'stats', 'ls', 'dir', 'clear',
            'cls', 'env', 'alias', 'cat'
        ]

    @classmethod
    def execute_builtin(cls, cmd_name: str, args: List[str]) -> bool:
        """
        Execute a builtin command.

        Args:
            cmd_name: Name of the builtin command
            args: Command arguments

        Returns:
            True if command was handled successfully
        """
        handler = getattr(cls, f"_cmd_{cmd_name}", None)
        if handler:
            return handler(args)
        return False

    @classmethod
    def _cmd_cd(cls, args: List[str]) -> bool:
        """
        Change directory command.
        Supports: cd, cd ~, cd -, cd /path

        Args:
            args: Command arguments

        Returns:
            True (always handled)
        """
        if not args:
            # cd without args → go to home
            target = Path.home()
        elif args[0] == "~":
            target = Path.home()
        elif args[0] == "-":
            # cd - → go to previous directory
            if cls._prev_dir:
                target = cls._prev_dir
            else:
                print("cd: no previous directory")
                return True
        else:
            target = Path(args[0]).expanduser()

        try:
            cls._prev_dir = Path.cwd()  # Save current for cd -
            os.chdir(target)
            return True
        except FileNotFoundError:
            print(f"cd: no such file or directory: {target}")
            return True
        except PermissionError:
            print(f"cd: permission denied: {target}")
            return True

    @classmethod
    def _cmd_pwd(cls, args: List[str]) -> bool:
        """
        Print working directory.

        Args:
            args: Command arguments (ignored)

        Returns:
            True (always handled)
        """
        print(os.getcwd())
        return True

    @classmethod
    def _cmd_echo(cls, args: List[str]) -> bool:
        """
        Echo command - print arguments.

        Args:
            args: Arguments to print

        Returns:
            True (always handled)
        """
        print(" ".join(args))
        return True

    @classmethod
    def _cmd_export(cls, args: List[str]) -> bool:
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

    @classmethod
    def _cmd_history(cls, args: List[str]) -> bool:
        """
        Show command history.

        Args:
            args: Command arguments (ignored)

        Returns:
            True (always handled)
        """
        for i, cmd in enumerate(cls._history, 1):
            print(f"{i:4d}  {cmd}")
        return True

    @classmethod
    def _cmd_help(cls, args: List[str]) -> bool:
        """
        Display help information with a spooky twist.

        Args:
            args: Command arguments (ignored)

        Returns:
            True (always handled)
        """
        from src.display import colorize, EMOJI

        print("\n" + "=" * 60)
        print(f"{EMOJI['pumpkin']} {colorize('MairuCLI Help', 'orange')} "
              f"{EMOJI['pumpkin']}")
        print("=" * 60)
        print()

        print(colorize("Safe Commands (Go ahead, try these!):", "green"))
        print("  cd [path]    - Change directory")
        print("  pwd          - Print working directory")
        print("  ls / dir     - List directory contents")
        print("  cat [file]   - Display file contents =^.^=")
        print("  clear / cls  - Clear terminal screen")
        print("  echo [text]  - Print text to screen")
        print("  export VAR=value - Set environment variable")
        print("  env          - Show environment variables")
        print("  history      - Show command history")
        print("  alias        - Show available command aliases")
        print("  stats        - Show how many times I saved you")
        print("  help         - Show this help message")
        print("  exit/quit    - Exit MairuCLI")
        print()

        print(colorize("System Commands:", "purple"))
        print("  Any other command will be passed to your system shell")
        print("  (after safety checks, of course!)")
        print()

        print(colorize("⚠️  Dangerous Commands (DON'T try these!):", "red"))
        print(f"  {EMOJI['fire']} rm -rf /        "
              "- Deletes EVERYTHING (seriously, don't)")
        print(f"  {EMOJI['skull']} chmod 777 file  "
              "- Makes files world-writable (bad idea)")
        print(f"  {EMOJI['fire']} dd if=/dev/zero "
              "- Overwrites your disk (yikes!)")
        print(f"  {EMOJI['fire']} DROP DATABASE   "
              "- Deletes entire database (career-ending)")
        print()

        print(colorize("Fun Typos to Try:", "chocolate"))
        print(f"  {EMOJI['train']} sl              "
              "- Choo choo! (instead of ls)")
        print(f"  {EMOJI['pumpkin']} cd..            "
              "- Stuck together? (instead of cd ..)")
        print()

        print(colorize("Remember:", "orange"))
        print("  This is an EDUCATIONAL tool, not a security solution!")
        print("  I'll warn you about dangerous commands, but I can't")
        print("  protect you from everything. Stay curious, stay safe!")
        print()
        print("=" * 60 + "\n")

        return True

    @classmethod
    def _cmd_stats(cls, args: List[str]) -> bool:
        """
        Display statistics about blocked commands.

        Args:
            args: Command arguments (ignored)

        Returns:
            True (always handled)
        """
        from src.display import colorize, EMOJI, get_stats

        stats = get_stats()

        print("\n" + "=" * 60)
        pumpkin = EMOJI['pumpkin']
        title = colorize('MairuCLI Statistics', 'orange')
        print(f"{pumpkin} {title} {pumpkin}")
        print("=" * 60)
        print()

        total_saves = stats["dangerous_blocked"] + stats["typos_caught"]

        if total_saves == 0:
            print(colorize("No disasters prevented yet!", "green"))
            print("(But I'm ready when you need me!)")
        else:
            print(f"{EMOJI['fire']} {colorize('Times I saved you:', 'red')} "
                  f"{colorize(str(total_saves), 'orange')}")
            print()
            print(f"  Dangerous commands blocked: "
                  f"{colorize(str(stats['dangerous_blocked']), 'red')}")
            print(f"  Typos caught: "
                  f"{colorize(str(stats['typos_caught']), 'purple')}")
            print()

            if total_saves >= 10:
                msg = "🏆 Wow! You really like living dangerously!"
                print(colorize(msg, "orange"))
            elif total_saves >= 5:
                print(colorize("😅 Maybe slow down a bit?", "chocolate"))
            else:
                print(colorize("👍 Keep being careful out there!", "green"))

        print()
        print("=" * 60 + "\n")

        return True

    @classmethod
    def _cmd_ls(cls, args: List[str]) -> bool:
        """
        List directory contents (cross-platform).

        Args:
            args: Command arguments (path, flags)

        Returns:
            True (always handled)
        """
        import subprocess
        import sys

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

    @classmethod
    def _cmd_dir(cls, args: List[str]) -> bool:
        """
        List directory contents (Windows style).
        Alias for ls command.

        Args:
            args: Command arguments

        Returns:
            True (always handled)
        """
        return cls._cmd_ls(args)

    @classmethod
    def _cmd_clear(cls, args: List[str]) -> bool:
        """
        Clear the terminal screen.

        Args:
            args: Command arguments (ignored)

        Returns:
            True (always handled)
        """
        import sys

        if sys.platform == "win32":
            os.system("cls")
        else:
            os.system("clear")

        return True

    @classmethod
    def _cmd_cls(cls, args: List[str]) -> bool:
        """
        Clear the terminal screen (Windows style).
        Alias for clear command.

        Args:
            args: Command arguments (ignored)

        Returns:
            True (always handled)
        """
        return cls._cmd_clear(args)

    @classmethod
    def _cmd_env(cls, args: List[str]) -> bool:
        """
        Display environment variables.
        Alias for export command without arguments.

        Args:
            args: Command arguments (ignored)

        Returns:
            True (always handled)
        """
        return cls._cmd_export([])

    @classmethod
    def _cmd_alias(cls, args: List[str]) -> bool:
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

    @classmethod
    def _cmd_cat(cls, args: List[str]) -> bool:
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

    @classmethod
    def add_to_history(cls, command: str) -> None:
        """
        Add command to history.

        Args:
            command: Command to add to history
        """
        cls._history.append(command)
