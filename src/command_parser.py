"""
Command parser module for MairuCLI system directory protection.

This module provides utilities to parse commands and extract file paths
for protection checking.
"""

import re
import shlex
from typing import List, Dict, Any, Optional
from src.config import DISPLAY_MIN_QUOTE_LENGTH


class CommandParser:
    """Parse commands to extract file paths and operations."""

    # Commands that operate on files/directories with their path argument positions
    FILE_COMMANDS = {
        "rm": {"path_positions": [0], "has_options": True},
        "rmdir": {"path_positions": [0], "has_options": True},
        "mv": {"path_positions": [0, 1], "has_options": True},  # source, dest
        "cp": {"path_positions": [0, 1], "has_options": True},  # source, dest
        "chmod": {"path_positions": [1], "has_options": False},  # mode, path
        "chown": {"path_positions": [1], "has_options": False},  # owner, path
        "dd": {"special": "dd_parser"},
        "cat": {"path_positions": [0], "has_options": True},
        "touch": {"path_positions": [0], "has_options": True},
        "mkdir": {"path_positions": [0], "has_options": True},
        "ln": {"path_positions": [0, 1], "has_options": True},  # source, dest
    }

    def parse(self, command: str) -> Dict[str, Any]:
        """
        Parse command to extract operation and target paths.

        Args:
            command: Full command string

        Returns:
            Dictionary with:
                - command: str (command name)
                - paths: List[str] (extracted file paths)
                - operation: str (operation type)
                - has_redirect: bool
                - redirect_target: Optional[str]
        """
        if not command or not command.strip():
            return {
                "command": "",
                "paths": [],
                "operation": "",
                "has_redirect": False,
                "redirect_target": None
            }

        try:
            # Check for output redirection first
            redirect_target = self._check_redirect(command)

            # Split command into parts
            # On Windows, use posix=False to preserve backslashes
            import sys
            posix_mode = sys.platform != 'win32'
            parts = shlex.split(command, posix=posix_mode)
            if not parts:
                return {
                    "command": "",
                    "paths": [],
                    "operation": "",
                    "has_redirect": False,
                    "redirect_target": None
                }

            cmd = parts[0]
            args = parts[1:]

            # Extract paths based on command type
            paths = self._extract_paths(cmd, args)

            # Strip quotes from paths if present (Windows with posix=False)
            paths = [self._strip_quotes(p) for p in paths]

            # Add redirect target if present
            if redirect_target:
                paths.append(redirect_target)

            return {
                "command": cmd,
                "paths": paths,
                "operation": self._get_operation_type(cmd),
                "has_redirect": redirect_target is not None,
                "redirect_target": redirect_target
            }

        except Exception:
            # If parsing fails, return empty result (fail-safe)
            return {
                "command": "",
                "paths": [],
                "operation": "",
                "has_redirect": False,
                "redirect_target": None
            }

    def _extract_paths(self, cmd: str, args: List[str]) -> List[str]:
        """
        Extract file paths from command arguments.

        Args:
            cmd: Command name
            args: Command arguments

        Returns:
            List of extracted file paths
        """
        paths = []

        if cmd not in self.FILE_COMMANDS:
            return paths

        cmd_info = self.FILE_COMMANDS[cmd]

        # Handle special parsers
        if "special" in cmd_info:
            if cmd_info["special"] == "dd_parser":
                return self._parse_dd_command(args)

        # Handle standard path extraction
        if "path_positions" in cmd_info:
            # Filter out options (starting with -)
            non_option_args = []
            if cmd_info.get("has_options", False):
                for arg in args:
                    if not arg.startswith("-"):
                        non_option_args.append(arg)
            else:
                non_option_args = args

            # Extract paths at specified positions
            for pos in cmd_info["path_positions"]:
                if pos < len(non_option_args):
                    paths.append(non_option_args[pos])

        return paths

    def _parse_dd_command(self, args: List[str]) -> List[str]:
        """
        Parse dd command to extract if= and of= paths.

        Args:
            args: dd command arguments

        Returns:
            List of paths from if= and of= parameters
        """
        paths = []

        for arg in args:
            # Match if=<path> or of=<path>
            if_match = re.match(r'if=(.+)', arg)
            of_match = re.match(r'of=(.+)', arg)

            if if_match:
                paths.append(if_match.group(1))
            elif of_match:
                paths.append(of_match.group(1))

        return paths

    def _check_redirect(self, command: str) -> Optional[str]:
        """
        Check for output redirection and extract target file.

        Args:
            command: Full command string

        Returns:
            Redirect target path if found, None otherwise
        """
        # Match > or >> followed by a file path
        # Handle quoted paths
        quoted_pattern = r'(?:>>?)\s+["\']([^"\']+)["\']'
        match = re.search(quoted_pattern, command)
        if match:
            return match.group(1)

        # Handle unquoted paths
        unquoted_pattern = r'(?:>>?)\s+([^\s]+)'
        match = re.search(unquoted_pattern, command)
        if match:
            return match.group(1)

        return None

    def _get_operation_type(self, cmd: str) -> str:
        """
        Determine the type of operation being performed.

        Args:
            cmd: Command name

        Returns:
            Operation type string
        """
        operation_map = {
            "rm": "delete",
            "rmdir": "delete",
            "mv": "move",
            "cp": "copy",
            "chmod": "permission",
            "chown": "ownership",
            "dd": "disk_operation",
            "cat": "read",
            "touch": "create",
            "mkdir": "create",
            "ln": "link",
        }

        return operation_map.get(cmd, "unknown")

    def extract_all_paths(self, command: str) -> List[str]:
        """
        Convenience method to extract all paths from a command.

        Handles command chaining (;, &&, ||, |) by splitting and parsing
        each sub-command separately.

        Args:
            command: Full command string (may contain chained commands)

        Returns:
            List of all file paths found in the command
        """
        all_paths = []

        # Split by command chaining operators
        # Handle: ; && || |
        sub_commands = self._split_chained_commands(command)

        # Parse each sub-command
        for sub_cmd in sub_commands:
            parsed = self.parse(sub_cmd)
            all_paths.extend(parsed["paths"])

        return all_paths

    def _split_chained_commands(self, command: str) -> List[str]:
        """
        Split command string by chaining operators.

        Handles: ; && || |

        Args:
            command: Full command string

        Returns:
            List of individual commands
        """
        import re

        # Split by chaining operators while preserving quoted strings
        # Pattern matches: ; or && or || or |
        # But not inside quotes
        parts = []
        current = []
        in_quotes = False
        quote_char = None
        i = 0

        while i < len(command):
            char = command[i]

            # Handle quotes
            if char in ['"', "'"]:
                if not in_quotes:
                    in_quotes = True
                    quote_char = char
                elif char == quote_char:
                    in_quotes = False
                    quote_char = None
                current.append(char)
                i += 1
                continue

            # Handle operators (only outside quotes)
            if not in_quotes:
                # Check for && or ||
                if i + 1 < len(command):
                    two_char = command[i:i+2]
                    if two_char in ['&&', '||']:
                        if current:
                            parts.append(''.join(current).strip())
                            current = []
                        i += 2
                        continue

                # Check for ; or |
                if char in [';', '|']:
                    if current:
                        parts.append(''.join(current).strip())
                        current = []
                    i += 1
                    continue

            current.append(char)
            i += 1

        # Add remaining
        if current:
            parts.append(''.join(current).strip())

        # Filter out empty parts
        return [p for p in parts if p]

    def extract_redirection_target(self, command: str) -> Optional[str]:
        """
        Extract output redirection target from command.

        This is used to detect dangerous redirections like:
        - echo data > /dev/sda (disk write)
        - cat file > /proc/sysrq-trigger (kernel panic)
        - echo test > /etc/passwd (system file modification)

        Args:
            command: Full command string

        Returns:
            Target path if redirection found, None otherwise

        Examples:
            >>> parser = CommandParser()
            >>> parser.extract_redirection_target("echo test > /dev/sda")
            '/dev/sda'
            >>> parser.extract_redirection_target("cat file > /tmp/out")
            '/tmp/out'
            >>> parser.extract_redirection_target("ls -la")
            None
        """
        return self._check_redirect(command)

    def _strip_quotes(self, path: str) -> str:
        """
        Strip surrounding quotes from path.

        Args:
            path: Path that may have surrounding quotes

        Returns:
            Path with quotes removed
        """
        if len(path) >= DISPLAY_MIN_QUOTE_LENGTH:
            if (path[0] == '"' and path[-1] == '"') or \
               (path[0] == "'" and path[-1] == "'"):
                return path[1:-1]
        return path
