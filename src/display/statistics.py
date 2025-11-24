"""
Statistics tracking for MairuCLI display system.

Tracks dangerous commands blocked, typos caught, and repeat attempts.

Statistics tracked:
- dangerous_blocked: Number of dangerous commands blocked
- typos_caught: Number of typos caught
- safe_commands_used: Number of unique safe commands used
- caution_shown/proceeded/cancelled: Caution warning statistics
- system_protection_blocks: Number of system directory protection blocks

The statistics system supports achievement tracking by providing
methods to check command usage and repeat patterns.
"""

from typing import Dict


class Statistics:
    """Tracks command statistics."""

    def __init__(self):
        """Initialize statistics counters."""
        self._stats = {
            "dangerous_blocked": 0,
            "typos_caught": 0,
            "safe_commands_used": 0,
            "caution_shown": 0,
            "caution_proceeded": 0,
            "caution_cancelled": 0,
            "system_protection_blocks": 0
        }
        self._warned_commands: Dict[str, int] = {}
        self._safe_commands_used: set = set()
        self._protected_dirs_attempted: set = set()

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

    def has_used_command(self, command: str) -> bool:
        """
        Check if a specific command has been used.

        Args:
            command: The command to check

        Returns:
            True if command has been used, False otherwise
        """
        return command in self._safe_commands_used

    def get_safe_commands_count(self) -> int:
        """
        Get number of unique safe commands used.

        Returns:
            Number of unique safe commands
        """
        return len(self._safe_commands_used)

    def increment_caution_shown(self) -> None:
        """Increment caution warning counter."""
        self._stats["caution_shown"] += 1

    def increment_caution_proceeded(self) -> None:
        """Increment caution proceeded counter."""
        self._stats["caution_proceeded"] += 1

    def increment_caution_cancelled(self) -> None:
        """Increment caution cancelled counter."""
        self._stats["caution_cancelled"] += 1

    def get_caution_stats(self) -> Dict[str, int]:
        """
        Get caution warning statistics.

        Returns:
            Dictionary with caution stats
        """
        return {
            "shown": self._stats["caution_shown"],
            "proceeded": self._stats["caution_proceeded"],
            "cancelled": self._stats["caution_cancelled"]
        }

    def track_system_protection_block(self, directory: str) -> None:
        """
        Track system directory protection block.

        Args:
            directory: The protected directory that was attempted
        """
        self._stats["system_protection_blocks"] += 1
        self._protected_dirs_attempted.add(directory)

    def get_system_protection_blocks(self) -> int:
        """
        Get total number of system protection blocks.

        Returns:
            Total system protection blocks count
        """
        return self._stats["system_protection_blocks"]

    def get_unique_protected_dirs_count(self) -> int:
        """
        Get number of unique protected directories attempted.

        Returns:
            Number of unique protected directories
        """
        return len(self._protected_dirs_attempted)
