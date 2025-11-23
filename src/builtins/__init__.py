"""
Builtin command implementations for MairuCLI.

This package provides internal implementations of shell builtin commands
organized by category for better maintainability.
"""

from typing import List

# Import all command modules
from . import navigation
from . import file_operations
from . import search
from . import system_info
from . import display
from . import shell_utils
from . import mairu_commands


class BuiltinCommands:
    """
    Internal implementation of shell builtin commands.

    This class serves as a thin wrapper that delegates to specialized
    command modules organized by category.
    """

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
            # Navigation
            'cd', 'pwd',
            # File operations
            'ls', 'dir', 'cat', 'touch', 'mkdir',
            # Search
            'find', 'grep', 'which',
            # System info
            'whoami', 'date', 'hostname', 'env', 'export',
            # Display
            'tree',
            # Shell utils
            'echo', 'clear', 'cls', 'history', 'alias',
            # MairuCLI specific
            'help', 'stats',
            # Exit commands (handled in main.py)
            'exit', 'quit'
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
        # Map command names to their handler functions
        command_map = {
            # Navigation
            'cd': navigation.cmd_cd,
            'pwd': navigation.cmd_pwd,
            # File operations
            'ls': file_operations.cmd_ls,
            'dir': file_operations.cmd_dir,
            'cat': file_operations.cmd_cat,
            'touch': file_operations.cmd_touch,
            'mkdir': file_operations.cmd_mkdir,
            # Search
            'find': search.cmd_find,
            'grep': search.cmd_grep,
            'which': search.cmd_which,
            # System info
            'whoami': system_info.cmd_whoami,
            'date': system_info.cmd_date,
            'hostname': system_info.cmd_hostname,
            'env': system_info.cmd_env,
            'export': system_info.cmd_export,
            # Display
            'tree': display.cmd_tree,
            # Shell utils
            'echo': shell_utils.cmd_echo,
            'clear': shell_utils.cmd_clear,
            'cls': shell_utils.cmd_cls,
            'history': shell_utils.cmd_history,
            'alias': shell_utils.cmd_alias,
            # MairuCLI specific
            'help': mairu_commands.cmd_help,
            'stats': mairu_commands.cmd_stats,
        }

        handler = command_map.get(cmd_name)
        if handler:
            return handler(args)
        return False

    @classmethod
    def add_to_history(cls, command: str) -> None:
        """
        Add command to history.

        Args:
            command: Command to add to history
        """
        shell_utils.add_to_history(command)

    @classmethod
    def get_history(cls) -> List[str]:
        """
        Get command history.

        Returns:
            List of commands in history
        """
        return shell_utils.get_history()


# Export the main class
__all__ = ['BuiltinCommands']
