"""
Statistics tracking for MairuCLI display system.

Tracks dangerous commands blocked, typos caught, and repeat attempts.
"""

from typing import Dict


class Statistics:
    """Tracks command statistics."""

    def __init__(self):
        """Initialize statistics counters."""
        self._stats = {
            "dangerous_blocked": 0,
            "typos_caught": 0,
            "safe_commands_used": 0
        }
        self._warned_commands: Dict[str, int] = {}
        self._safe_commands_used: set = set()

    def increment_dangerous_blocked(self) -> None:
        """Increment dangerous command counter."""
        self._stats["dangerous_blocked"] += 1

    def increment_typos_caught(self) -> None:
        """Increment typo counter."""
        self._stats["typos_caught"] += 1

    def track_repeat_command(self, command: str) -> int:
        """
        Track repeat command and return count.

        Args:
            command: The command being repeated

        Returns:
            Number of times this command has been attempted
        """
        if command in self._warned_commands:
            self._warned_commands[command] += 1
        else:
            self._warned_commands[command] = 1

        return self._warned_commands[command]

    def get_stats(self) -> Dict[str, int]:
        """
        Get current statistics.

        Returns:
            Dictionary with statistics
        """
        return self._stats.copy()

    def get_max_repeats(self) -> int:
        """
        Get maximum repeat count for any command.

        Returns:
            Maximum number of repeats, or 0 if no repeats
        """
        if self._warned_commands:
            return max(self._warned_commands.values())
        return 0

    def get_total_blocks(self) -> int:
        """
        Get total number of dangerous commands blocked.

        Returns:
            Total dangerous blocks count
        """
        return self._stats["dangerous_blocked"]

    def get_total_typos(self) -> int:
        """
        Get total number of typos caught.

        Returns:
            Total typos count
        """
        return self._stats["typos_caught"]

    def track_safe_command(self, command: str) -> None:
        """
        Track safe command usage.

        Args:
            command: The safe command being used
        """
        self._safe_commands_used.add(command)
        self._stats["safe_commands_used"] = (
            len(self._safe_commands_used)
        )

    def get_safe_commands_count(self) -> int:
        """
        Get number of unique safe commands used.

        Returns:
            Number of unique safe commands
        """
        return len(self._safe_commands_used)
