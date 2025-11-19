"""
Command interceptor for MairuCLI.

This module provides pattern matching to detect dangerous commands and typos.
"""

import re
from typing import Dict, Tuple


# Dangerous command patterns
# Reference: docs/reference/cli-dangers.md
DANGEROUS_PATTERNS: Dict[str, Dict[str, str]] = {
    "rm_dangerous": {
        "pattern": (
            r"rm\s+(-rf|-fr|-r\s+-f|-f\s+-r)\s+"
            r"(/|~|\$HOME|\*|\.(?:\s|$)|\$\w+)"
        ),
        "category": "deletion",
        "severity": "critical",
        "art_file": "fired.txt"
    },
    "chmod_777": {
        "pattern": r"chmod\s+(-R\s+)?777",
        "category": "permission",
        "severity": "high",
        "art_file": "permission_denied.txt"
    },
    "dd_zero": {
        "pattern": r"dd\s+if=/dev/zero\s+of=",
        "category": "disk",
        "severity": "critical",
        "art_file": "data_destroyer.txt"
    },
    "drop_database": {
        "pattern": r"DROP\s+DATABASE",
        "category": "database",
        "severity": "critical",
        "art_file": "fired.txt"
    },
    "fork_bomb": {
        "pattern": r":\(\)\{:\|:&\};:",
        "category": "system",
        "severity": "critical",
        "art_file": "data_destroyer.txt"
    },
    "redirect_to_disk": {
        "pattern": r">\s*/dev/sd[a-z]",
        "category": "disk",
        "severity": "critical",
        "art_file": "data_destroyer.txt"
    },
    "mkfs_disk": {
        "pattern": r"mkfs\.\w+\s+/dev/sd[a-z]",
        "category": "disk",
        "severity": "critical",
        "art_file": "data_destroyer.txt"
    },
    "mv_to_null": {
        "pattern": r"mv\s+.+\s+/dev/null",
        "category": "deletion",
        "severity": "high",
        "art_file": "fired.txt"
    },
    "overwrite_file": {
        "pattern": r"^\s*>\s+/\w+",
        "category": "deletion",
        "severity": "medium",
        "art_file": "permission_denied.txt"
    },
    "dd_random": {
        "pattern": r"dd\s+if=/dev/random\s+of=/dev/sd[a-z]",
        "category": "disk",
        "severity": "critical",
        "art_file": "data_destroyer.txt"
    },
    "kernel_panic": {
        "pattern": r"echo\s+c\s*>\s*/proc/sysrq-trigger",
        "category": "system",
        "severity": "critical",
        "art_file": "data_destroyer.txt"
    }
}

# Typo patterns
TYPO_PATTERNS: Dict[str, Dict[str, str]] = {
    "sl": {
        "pattern": r"^sl$",
        "correct": "ls",
        "message": "🚂 Choo choo! All aboard the typo train!"
    },
    "cd_stuck": {
        "pattern": r"^cd\.\.$",
        "correct": "cd ..",
        "message": "🎃 Stuck together? Let me help you separate!"
    }
}


def check_command(command: str) -> Tuple[bool, str]:
    """
    Check if command matches any dangerous or typo pattern.

    Args:
        command: User-entered command string

    Returns:
        Tuple of (is_dangerous, pattern_name)
        If not dangerous, pattern_name is empty string

    Performance: Must complete within 50ms
    """
    # Check dangerous patterns first (higher priority)
    for pattern_name, pattern_data in DANGEROUS_PATTERNS.items():
        if re.search(pattern_data["pattern"], command, re.IGNORECASE):
            return True, pattern_name

    # Check typo patterns
    for pattern_name, pattern_data in TYPO_PATTERNS.items():
        if re.search(pattern_data["pattern"], command, re.IGNORECASE):
            return True, f"typo_{pattern_name}"

    return False, ""


def get_pattern_info(pattern_name: str) -> Dict[str, str]:
    """
    Retrieve pattern information for display.

    Args:
        pattern_name: Name of the matched pattern

    Returns:
        Dictionary with pattern details (category, severity, art_file, etc.)
    """
    if pattern_name.startswith("typo_"):
        typo_name = pattern_name.replace("typo_", "")
        return TYPO_PATTERNS[typo_name]
    else:
        return DANGEROUS_PATTERNS[pattern_name]
