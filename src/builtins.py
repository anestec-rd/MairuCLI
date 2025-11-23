"""
Builtin command implementations for MairuCLI.

This module provides internal implementations of shell builtin commands
that must run in MairuCLI's process (cd, pwd, echo, etc.).
"""

import os
import re
import sys
import getpass
import datetime
import socket
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
            'cls', 'env', 'alias', 'cat', 'touch', 'mkdir',
            'find', 'grep', 'which', 'whoami', 'date', 'hostname',
            'tree'
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

        print(colorize("Navigation & File Management:", "green"))
        print("  cd [path]    - Change directory")
        print("  pwd          - Print working directory")
        print("  ls / dir     - List directory contents")
        print("  tree [path]  - Show directory tree structure")
        print("  touch <file> - Create empty file")
        print("  mkdir <dir>  - Create directory")
        print("  cat [file]   - Display file contents =^.^=")
        print()

        print(colorize("Search & Find:", "green"))
        print("  find <pattern> - Find files by name")
        print("  grep <pattern> <file> - Search text in files")
        print("  which <cmd>  - Show command location")
        print()

        print(colorize("System Info:", "green"))
        print("  whoami       - Show current username")
        print("  hostname     - Show computer name")
        print("  date         - Show current date and time")
        print("  env          - Show environment variables")
        print()

        print(colorize("Utilities:", "green"))
        print("  echo [text]  - Print text to screen")
        print("  clear / cls  - Clear terminal screen")
        print("  history      - Show command history")
        print("  alias        - Show available command aliases")
        print()

        print(colorize("MairuCLI Specific:", "green"))
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

            # Display unlocked achievements
            from src.display import get_unlocked_achievements
            unlocked = get_unlocked_achievements()

            if unlocked:
                # Categorize achievements
                danger_achievements = [
                    "First Blood", "Persistent Troublemaker",
                    "Danger Addict", "Stubborn"
                ]

                danger_list = [ach for ach in unlocked
                               if ach in danger_achievements]
                other_list = [ach for ach in unlocked
                              if ach not in danger_achievements]

                # Display danger-related achievements
                if danger_list:
                    print(colorize("💀 Your Troublemaking History:", "red"))
                    print()
                    for achievement in danger_list:
                        print(f"  {colorize('✓', 'green')} {achievement}")
                    print()

                # Display other achievements
                if other_list:
                    print(colorize("🏆 Unlocked Achievements:", "orange"))
                    print()
                    for achievement in other_list:
                        print(f"  {colorize('✓', 'green')} {achievement}")
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

    @classmethod
    def _cmd_touch(cls, args: List[str]) -> bool:
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

    @classmethod
    def _cmd_mkdir(cls, args: List[str]) -> bool:
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

    @classmethod
    def _cmd_find(cls, args: List[str]) -> bool:
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

    @classmethod
    def _cmd_grep(cls, args: List[str]) -> bool:
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

    @classmethod
    def _cmd_which(cls, args: List[str]) -> bool:
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

        path_env = os.environ.get('PATH', '')
        path_dirs = path_env.split(os.pathsep)

        for cmd_name in args:
            found = False

            # Check if it's a builtin first
            if cls.is_builtin(cmd_name):
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

    @classmethod
    def _cmd_whoami(cls, args: List[str]) -> bool:
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

    @classmethod
    def _cmd_date(cls, args: List[str]) -> bool:
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

    @classmethod
    def _cmd_hostname(cls, args: List[str]) -> bool:
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

    @classmethod
    def _cmd_tree(cls, args: List[str]) -> bool:
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
