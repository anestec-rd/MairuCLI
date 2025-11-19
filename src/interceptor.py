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

# Caution patterns (risky but not immediately catastrophic)
CAUTION_PATTERNS: Dict[str, Dict] = {
    "sudo_shell": {
        "pattern": r"sudo\s+(su|bash|sh|-i)(?:\s|$)",
        "category": "privilege_escalation",
        "severity": "medium",
        "risk": "Entering root shell - all safety checks disabled",
        "impact": "One mistake could damage the entire system",
        "considerations": [
            "Do you really need full root access?",
            "Could you use 'sudo command' instead?",
            "Are you in the right directory?"
        ]
    },
    "chmod_permissive": {
        "pattern": r"chmod\s+(-R\s+)?(666|755|775)",
        "category": "permissions",
        "severity": "medium",
        "risk": "Making files readable/writable by others",
        "impact": "Potential security vulnerability or data exposure",
        "considerations": [
            "Who needs access to this file?",
            "Is 644 (read-only for others) sufficient?",
            "Are you setting permissions on sensitive data?"
        ]
    },
    "firewall_disable": {
        "pattern": (
            r"(iptables\s+-F|ufw\s+disable|"
            r"systemctl\s+stop\s+firewalld)"
        ),
        "category": "security",
        "severity": "high",
        "risk": "Disabling firewall protection",
        "impact": "System exposed to network attacks",
        "considerations": [
            "Is this a temporary debugging step?",
            "Will you re-enable the firewall?",
            "Are you on a trusted network?"
        ]
    },
    "selinux_disable": {
        "pattern": r"setenforce\s+0",
        "category": "security",
        "severity": "high",
        "risk": "Disabling SELinux mandatory access control",
        "impact": "Weakens system security significantly",
        "considerations": [
            "Could you fix the SELinux policy instead?",
            "Is this permanent or temporary?",
            "Do you understand the security implications?"
        ]
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


def check_command(command: str) -> Tuple[str, str]:
    """
    Check if command matches any dangerous, caution, or typo pattern.

    Args:
        command: User-entered command string

    Returns:
        Tuple of (level, pattern_name)
        level: "critical", "caution", or "safe"
        pattern_name: Name of matched pattern, or empty string if safe

    Performance: Must complete within 50ms
    """
    # Check critical patterns first (highest priority)
    for pattern_name, pattern_data in DANGEROUS_PATTERNS.items():
        if re.search(pattern_data["pattern"], command, re.IGNORECASE):
            return "critical", pattern_name

    # Check caution patterns (medium priority)
    for pattern_name, pattern_data in CAUTION_PATTERNS.items():
        if re.search(pattern_data["pattern"], command, re.IGNORECASE):
            return "caution", pattern_name

    # Check typo patterns (treated as critical for blocking)
    for pattern_name, pattern_data in TYPO_PATTERNS.items():
        if re.search(pattern_data["pattern"], command, re.IGNORECASE):
            return "critical", f"typo_{pattern_name}"

    return "safe", ""


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
