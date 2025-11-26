"""
Command interceptor for MairuCLI.

This module provides pattern matching to detect dangerous commands and typos.
"""

import re
import sys
from typing import Dict, Tuple


# Protected system directories by platform
# These directories are critical for system operation and should not be modified
PROTECTED_DIRECTORIES = {
    "win32": {
        "critical": [
            r"c:\windows",
            r"c:\windows\system32",
            r"c:\windows\syswow64",
            r"c:\windows\winsxs",
        ],
        "caution": [
            r"c:\program files",
            r"c:\program files (x86)",
            r"c:\programdata",
        ]
    },
    "linux": {
        "critical": [
            "/bin", "/sbin", "/boot", "/etc",
            "/lib", "/lib64", "/proc", "/sys",
            "/root", "/dev"
        ],
        "caution": [
            "/usr/bin", "/usr/sbin", "/usr/lib",
            "/var/log", "/usr"
        ]
    },
    "darwin": {  # macOS
        "critical": [
            "/system", "/bin", "/sbin",
            "/etc", "/var", "/private"
        ],
        "caution": [
            "/library", "/applications",
            "/usr/bin", "/usr/sbin", "/usr"
        ]
    }
}


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
    "chmod_000": {
        "pattern": r"chmod\s+(-R\s+)?000",
        "category": "permission",
        "severity": "critical",
        "art_file": "permission_denied.txt"
    },
    "dd_zero": {
        "pattern": r"dd\s+if=/dev/zero",
        "category": "disk",
        "severity": "critical",
        "art_file": "zero_wipe.txt"
    },
    "drop_database": {
        "pattern": r"DROP\s+DATABASE",
        "category": "database",
        "severity": "critical",
        "art_file": "database_drop.txt"
    },
    "fork_bomb": {
        "pattern": r":\(\)\s*\{\s*:\s*\|\s*:\s*&\s*\}\s*;?\s*:",
        "category": "system",
        "severity": "critical",
        "art_file": "fork_bomb.txt"
    },
    "redirect_to_disk": {
        "pattern": r">\s*/dev/(sd[a-z]|nvme\d+n\d+)",
        "category": "disk",
        "severity": "critical",
        "art_file": "disk_destroyer.txt"
    },
    "mkfs_disk": {
        "pattern": r"mkfs(\.\w+)?\s+/dev/(sd[a-z]|nvme\d+n\d+)",
        "category": "disk",
        "severity": "critical",
        "art_file": "disk_destroyer.txt"
    },
    "mv_to_null": {
        "pattern": r"mv\s+.+\s+/dev/null",
        "category": "deletion",
        "severity": "high",
        "art_file": "data_void.txt"
    },
    "system_modify": {
        "pattern": (
            r"(>\s*/etc/(passwd|shadow|fstab|hosts|sudoers|group)|"
            r"echo\s+.*>\s*/etc/(passwd|shadow|fstab|hosts|sudoers|group)|"
            r"cat\s+.*>\s*/etc/(passwd|shadow|fstab|hosts|sudoers|group)|"
            r">\s*/dev/mem|"
            r"dd\s+.*of=/dev/mem|"
            r"chmod\s+.*\s+/etc/(passwd|shadow|sudoers)|"
            r"chown\s+.*\s+/etc/(passwd|shadow|sudoers)|"
            r"rm\s+.*\s+/etc/(passwd|shadow|fstab|sudoers|group))"
        ),
        "category": "system",
        "severity": "critical",
        "art_file": "system_glitch.txt"
    },
    "overwrite_file": {
        "pattern": r"^\s*>\s+/\w+",
        "category": "deletion",
        "severity": "medium",
        "art_file": "file_eraser.txt"
    },
    "dd_random": {
        "pattern": r"dd\s+if=/dev/random\s+of=/dev/(sd[a-z]|nvme\d+n\d+)",
        "category": "disk",
        "severity": "critical",
        "art_file": "disk_destroyer.txt"
    },
    "kernel_panic": {
        "pattern": r"echo\s+c\s*>\s*/proc/sysrq-trigger",
        "category": "system",
        "severity": "critical",
        "art_file": "kernel_panic.txt"
    },
    "shred_secure": {
        "pattern": r"shred\s+.*(/dev/sd[a-z]|/dev/nvme|-n\s+\d{2,})",
        "category": "disk",
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
    },
    "kill_force": {
        "pattern": r"kill\s+-9\s+\d+",
        "category": "process",
        "severity": "medium",
        "risk": "Force-killing process without cleanup",
        "impact": "May cause data loss or corruption",
        "considerations": [
            "Did you try 'kill' (SIGTERM) first?",
            "Will the process lose unsaved data?",
            "Is this a critical system process?"
        ]
    },
    "rm_node_modules": {
        "pattern": r"rm\s+-rf\s+node_modules",
        "category": "deletion",
        "severity": "low",
        "risk": "Deleting node_modules directory",
        "impact": "Will need to run 'npm install' again (takes time)",
        "considerations": [
            "This will take a while to reinstall",
            "Are you sure you want to delete dependencies?",
            "Consider 'npm ci' for a clean install instead"
        ]
    },
    "git_force_push": {
        "pattern": r"git\s+push\s+(--force|-f)(?:\s|$)",
        "category": "version_control",
        "severity": "high",
        "risk": "Force-pushing to remote repository",
        "impact": "May overwrite teammates' work",
        "considerations": [
            "Have you coordinated with your team?",
            "Could you use '--force-with-lease' instead?",
            "Are you pushing to a shared branch?"
        ]
    }
}

# Typo patterns (special cases that need custom messages)
# Note: Generic typo detection handles most common typos automatically
# Only define patterns here if they need special handling or custom messages
TYPO_PATTERNS: Dict[str, Dict[str, str]] = {
    "sl": {
        "pattern": r"^sl$",
        "correct": "ls",
        "message": "🚂 Choo choo! All aboard the typo train!"
    },
    "gti": {
        "pattern": r"^gti\b",
        "correct": "git",
        "message": "🚗 GTI? That's a car! You meant 'git', right?"
    },
    "tou": {
        "pattern": r"^tou\b",
        "correct": "touch",
        "message": "⚡ Whoa, speedy fingers! You meant 'touch', right?"
    },
    "cd_stuck": {
        "pattern": r"^cd\.\.$",
        "correct": "cd ..",
        "message": "🎃 Stuck together? Let me help you separate!"
    },
    "ls_stuck": {
        "pattern": r"^ls-[a-z]+$",
        "correct": "ls -[options]",
        "message": "🎯 Missing space! Try 'ls -la' instead of 'ls-la'!"
    },
    "git_stuck": {
        "pattern": r"^git-[a-z]+$",
        "correct": "git [command]",
        "message": "📝 Oops! Git commands need space: 'git status'!"
    }
}


# Common command list for generic typo detection
COMMON_COMMANDS = [
    "ls", "cd", "pwd", "cat", "echo", "touch", "mkdir", "rm", "mv", "cp",
    "chmod", "chown", "grep", "find", "which", "whoami", "date", "hostname",
    "git", "exit", "clear", "help", "history", "alias", "tree"
]


def check_generic_typo(command: str) -> Tuple[bool, str, str]:
    """
    Check for generic typo patterns (missing last character, etc.).

    Args:
        command: First word of the command

    Returns:
        Tuple of (is_typo, correct_command, message)
    """
    cmd_word = command.split()[0] if command.split() else command

    # Check if command is missing last character
    for correct_cmd in COMMON_COMMANDS:
        if len(correct_cmd) > 2 and cmd_word == correct_cmd[:-1]:
            return (
                True,
                correct_cmd,
                f"⚡ Speedy fingers! Missing the last letter? Try '{correct_cmd}'!"
            )

    # Check if command has one character wrong (simple substitution)
    for correct_cmd in COMMON_COMMANDS:
        if len(cmd_word) == len(correct_cmd) and len(cmd_word) > 2:
            diff_count = sum(1 for a, b in zip(cmd_word, correct_cmd) if a != b)
            if diff_count == 1:
                return (
                    True,
                    correct_cmd,
                    f"🎃 Close! One letter off. Did you mean '{correct_cmd}'?"
                )

    return False, "", ""


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

    # Check specific typo patterns (treated as critical for blocking)
    for pattern_name, pattern_data in TYPO_PATTERNS.items():
        if re.search(pattern_data["pattern"], command, re.IGNORECASE):
            return "critical", f"typo_{pattern_name}"

    # Check generic typo patterns
    is_typo, correct_cmd, message = check_generic_typo(command)
    if is_typo:
        # Create a dynamic typo pattern
        cmd_word = command.split()[0] if command.split() else command
        TYPO_PATTERNS[f"generic_{cmd_word}"] = {
            "pattern": f"^{re.escape(cmd_word)}\\b",
            "correct": correct_cmd,
            "message": message
        }
        return "critical", f"typo_generic_{cmd_word}"

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


def check_system_directory(command: str) -> Tuple[str, str, str]:
    """
    Check if command targets protected system directories.

    This is the highest priority check and runs before dangerous pattern
    matching. It prevents accidental modification of critical system
    directories.

    Args:
        command: User-entered command string

    Returns:
        Tuple of (level, protection_type, target_path)
        level: "critical", "caution", or "safe"
        protection_type: "system_critical", "system_caution", or ""
        target_path: The protected path that was targeted, or ""

    Performance: Must complete within 50ms
    """
    from src.command_parser import CommandParser
    from src.path_resolver import PathResolver

    # Special paths that should be handled by dangerous pattern check
    # These have specific educational warnings that are more valuable
    # than generic system protection warnings
    DANGEROUS_PATTERN_PATHS = [
        '/dev/zero',      # dd_zero pattern
        '/dev/random',    # dd_random pattern
        '/dev/sd',        # redirect_to_disk, mkfs_disk patterns (prefix match)
        '/dev/null',      # mv_to_null pattern
        '/proc/sysrq-trigger'  # kernel_panic pattern
    ]

    # Check if command contains any dangerous pattern paths
    # If so, skip system protection and let dangerous pattern check handle it
    for dangerous_path in DANGEROUS_PATTERN_PATHS:
        if dangerous_path in command:
            return "safe", "", ""

    # Get platform-specific protected directories
    platform = sys.platform
    if platform not in PROTECTED_DIRECTORIES:
        # Unknown platform - no system protection (fail-open for compatibility)
        return "safe", "", ""

    # Initialize parsers
    parser = CommandParser()
    resolver = PathResolver()

    # Extract paths from command
    try:
        paths = parser.extract_all_paths(command)
    except Exception:
        # If parsing fails, assume safe (fail-open for usability)
        return "safe", "", ""

    if not paths:
        # No paths found - safe
        return "safe", "", ""

    # Check each path against protected directories
    for path in paths:
        try:
            # Resolve path to absolute normalized form
            resolved_path = resolver.resolve_path(path)

            # Check critical directories first (highest priority)
            for protected_dir in PROTECTED_DIRECTORIES[platform]["critical"]:
                # Normalize protected directory for comparison
                normalized_protected = resolver.normalize_for_comparison(
                    protected_dir
                )

                # Ensure both paths end with separator for accurate comparison
                check_path = resolved_path
                check_protected = normalized_protected
                if not check_protected.endswith(('\\', '/')):
                    import os
                    check_protected += os.sep

                # Check if resolved path starts with protected directory
                if check_path.startswith(check_protected) or \
                   check_path == normalized_protected:
                    return "critical", "system_critical", resolved_path

            # Check caution directories
            for protected_dir in PROTECTED_DIRECTORIES[platform]["caution"]:
                normalized_protected = resolver.normalize_for_comparison(
                    protected_dir
                )

                # Ensure both paths end with separator for accurate comparison
                check_path = resolved_path
                check_protected = normalized_protected
                if not check_protected.endswith(('\\', '/')):
                    import os
                    check_protected += os.sep

                if check_path.startswith(check_protected) or \
                   check_path == normalized_protected:
                    return "caution", "system_caution", resolved_path

        except (ValueError, PermissionError, OSError):
            # If path resolution fails, err on side of caution (fail-safe)
            # Block the command to prevent potential system damage
            return "critical", "system_critical", path

    # No protected directories targeted - safe
    return "safe", "", ""
