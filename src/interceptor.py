"""
Command interceptor for MairuCLI.

This module provides pattern matching to detect dangerous commands and typos.
"""

import json
import os
import re
import sys
from typing import Dict, Tuple, Optional

try:
    import jsonschema
    JSONSCHEMA_AVAILABLE = True
except ImportError:
    JSONSCHEMA_AVAILABLE = False


class PatternLoader:
    """Load patterns from JSON files for data-driven architecture."""

    def __init__(self, data_dir: str = "data/warnings", validate_schema: bool = True):
        """
        Initialize pattern loader.

        Args:
            data_dir: Directory containing pattern JSON files
            validate_schema: Whether to validate JSON against schemas (default: True)
        """
        self.data_dir = data_dir
        self.validate_schema = validate_schema and JSONSCHEMA_AVAILABLE
        self._schemas = {}

        if validate_schema and not JSONSCHEMA_AVAILABLE:
            print("Warning: jsonschema library not available. Schema validation disabled.")
            print("Install with: pip install jsonschema")

    def _load_schema(self, schema_name: str) -> Optional[Dict]:
        """
        Load JSON schema from file.

        Args:
            schema_name: Name of schema file (without .json extension)

        Returns:
            Schema dictionary or None if not found
        """
        if schema_name in self._schemas:
            return self._schemas[schema_name]

        schema_path = os.path.join(self.data_dir, "schemas", f"{schema_name}.json")

        try:
            with open(schema_path, 'r', encoding='utf-8') as f:
                schema = json.load(f)
            self._schemas[schema_name] = schema
            return schema
        except FileNotFoundError:
            print(f"Warning: Schema file {schema_path} not found. Skipping validation.")
            return None
        except json.JSONDecodeError as e:
            print(f"Warning: Invalid JSON in schema {schema_path}: {e}")
            return None

    def _validate_json(self, data: Dict, schema_name: str, file_path: str) -> bool:
        """
        Validate JSON data against schema.

        Args:
            data: JSON data to validate
            schema_name: Name of schema to validate against
            file_path: Path to file being validated (for error messages)

        Returns:
            True if valid or validation disabled, False if invalid
        """
        if not self.validate_schema:
            return True

        schema = self._load_schema(schema_name)
        if schema is None:
            return True  # Skip validation if schema not available

        try:
            jsonschema.validate(instance=data, schema=schema)
            return True
        except jsonschema.ValidationError as e:
            print(f"Validation error in {file_path}:")
            print(f"  Path: {' -> '.join(str(p) for p in e.path)}")
            print(f"  Error: {e.message}")
            return False
        except jsonschema.SchemaError as e:
            print(f"Schema error in {schema_name}: {e.message}")
            return False

    def load_all_patterns(self) -> Tuple[Dict, Dict, Dict]:
        """
        Load all patterns from JSON files.

        Returns:
            Tuple of (dangerous_patterns, caution_patterns, typo_patterns)
        """
        dangerous = self._load_dangerous_patterns()
        caution = self._load_caution_patterns()
        typo = self._load_typo_patterns()
        return dangerous, caution, typo

    def _load_dangerous_patterns(self) -> Dict:
        """
        Load dangerous patterns from warning_catalog.json.

        Returns:
            Dictionary of dangerous patterns (ordered by specificity)
        """
        catalog_path = os.path.join(self.data_dir, "warning_catalog.json")

        try:
            with open(catalog_path, 'r', encoding='utf-8') as f:
                catalog = json.load(f)

            # Validate against schema
            if not self._validate_json(catalog, "warning_catalog_schema", catalog_path):
                print(f"Warning: Validation failed for {catalog_path}. Using patterns anyway.")

            patterns = {}
            for name, data in catalog.get('warnings', {}).items():
                if 'pattern' in data:
                    patterns[name] = {
                        'pattern': data['pattern'],
                        'category': data.get('category', 'unknown'),
                        'severity': data.get('severity', 'medium'),
                        'art_file': data.get('ascii_art', 'default.txt')
                    }

            # Sort patterns by specificity (more specific patterns first)
            # This ensures system_modify is checked before overwrite_file
            return self._sort_patterns_by_specificity(patterns)

        except FileNotFoundError:
            print(f"Warning: {catalog_path} not found. Using empty patterns.")
            return {}
        except json.JSONDecodeError as e:
            print(f"Warning: Invalid JSON in {catalog_path}: {e}")
            return {}

    def _sort_patterns_by_specificity(self, patterns: Dict) -> Dict:
        """
        Sort patterns by specificity (more specific first).

        More specific patterns should be checked first to avoid
        false matches by generic patterns.

        Args:
            patterns: Dictionary of patterns

        Returns:
            Ordered dictionary with specific patterns first
        """
        # Define priority order (higher number = higher priority)
        priority_map = {
            'system_modify': 100,  # Very specific (targets /etc/passwd, etc.)
            'kernel_panic': 90,    # Very specific (targets /proc/sysrq-trigger)
            'mkfs_disk': 80,       # Specific (targets /dev/sd*, /dev/nvme*)
            'redirect_to_disk': 80,
            'dd_random': 80,
            'dd_zero': 80,
            'fork_bomb': 70,       # Specific pattern
            'drop_database': 70,
            'rm_dangerous': 60,    # Moderately specific
            'chmod_777': 60,
            'chmod_000': 60,
            'mv_to_null': 60,
            'shred_secure': 60,
            'overwrite_file': 10,  # Generic (matches any > /path)
        }

        # Sort by priority (highest first)
        sorted_items = sorted(
            patterns.items(),
            key=lambda x: priority_map.get(x[0], 50),
            reverse=True
        )

        # Return as ordered dict
        return dict(sorted_items)

    def _load_caution_patterns(self) -> Dict:
        """
        Load caution patterns from caution_catalog.json.

        Returns:
            Dictionary of caution patterns
        """
        catalog_path = os.path.join(self.data_dir, "caution_catalog.json")

        try:
            with open(catalog_path, 'r', encoding='utf-8') as f:
                catalog = json.load(f)

            # Validate against schema
            if not self._validate_json(catalog, "caution_catalog_schema", catalog_path):
                print(f"Warning: Validation failed for {catalog_path}. Using patterns anyway.")

            patterns = {}
            for name, data in catalog.get('cautions', {}).items():
                if 'pattern' in data:
                    patterns[name] = data

            return patterns

        except FileNotFoundError:
            print(f"Warning: {catalog_path} not found. Using empty patterns.")
            return {}
        except json.JSONDecodeError as e:
            print(f"Warning: Invalid JSON in {catalog_path}: {e}")
            return {}

    def _load_typo_patterns(self) -> Dict:
        """
        Load typo patterns from typo_messages.json.

        Returns:
            Dictionary of typo patterns
        """
        typo_path = os.path.join(self.data_dir, "typo_messages.json")

        try:
            with open(typo_path, 'r', encoding='utf-8') as f:
                typo_data = json.load(f)

            # Validate against schema
            if not self._validate_json(typo_data, "typo_messages_schema", typo_path):
                print(f"Warning: Validation failed for {typo_path}. Using patterns anyway.")

            patterns = {}
            for name, data in typo_data.get('typos', {}).items():
                if 'pattern' in data:
                    patterns[name] = data

            return patterns

        except FileNotFoundError:
            print(f"Warning: {typo_path} not found. Using empty patterns.")
            return {}
        except json.JSONDecodeError as e:
            print(f"Warning: Invalid JSON in {typo_path}: {e}")
            return {}


class PatternCompiler:
    """Compile regex patterns for efficient matching."""

    def compile_patterns(self, patterns: Dict) -> Dict:
        """
        Compile all patterns in dictionary.

        Args:
            patterns: Dictionary of pattern data

        Returns:
            Dictionary with compiled regex patterns
        """
        compiled = {}

        for name, data in patterns.items():
            try:
                # Compile the pattern
                data['compiled'] = re.compile(data['pattern'], re.IGNORECASE)
                compiled[name] = data
            except re.error as e:
                print(f"Warning: Invalid pattern '{name}': {e}")
                # Skip invalid patterns
                continue

        return compiled


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


# All patterns (Dangerous, Caution, and Typo) are now loaded from JSON files
# See: data/warnings/warning_catalog.json, caution_catalog.json, and typo_messages.json
# This enables data-driven architecture where patterns can be managed without code changes


# Common command list for generic typo detection
# Loaded from builtin_commands.json to avoid duplication
def _load_common_commands() -> list:
    """Load common command names from builtin_commands.json."""
    try:
        builtin_path = os.path.join("data", "builtins", "builtin_commands.json")
        with open(builtin_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        commands = []
        for category_data in data.get('categories', {}).values():
            for cmd in category_data.get('commands', []):
                # Extract command name (first word before space or special chars)
                name = cmd.get('name', '').split()[0].split('/')[0].strip('<>')
                # Skip generic descriptions like "Any other command"
                if name and name.lower() not in ['any', 'other'] and name not in commands:
                    commands.append(name)

        return commands
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Warning: Could not load common commands: {e}")
        # Fallback to minimal list
        return ["ls", "cd", "pwd", "cat", "echo", "help", "exit"]

COMMON_COMMANDS = _load_common_commands()


# Load patterns from JSON files (data-driven architecture)
# JSON files are the ONLY source of pattern definitions
_loader = PatternLoader()
_compiler = PatternCompiler()

# Load patterns from JSON
_loaded_dangerous, _loaded_caution, _loaded_typo = _loader.load_all_patterns()

# Compile patterns for performance
DANGEROUS_PATTERNS = _compiler.compile_patterns(_loaded_dangerous)
CAUTION_PATTERNS = _compiler.compile_patterns(_loaded_caution)
TYPO_PATTERNS = _compiler.compile_patterns(_loaded_typo)

# Validate that patterns were loaded successfully
if not DANGEROUS_PATTERNS:
    raise RuntimeError(
        "Failed to load dangerous patterns from data/warnings/warning_catalog.json. "
        "This file is required for MairuCLI to function."
    )

if not CAUTION_PATTERNS:
    print("Warning: No caution patterns loaded from data/warnings/caution_catalog.json")
    CAUTION_PATTERNS = {}  # Empty dict is acceptable for caution patterns

if not TYPO_PATTERNS:
    print("Warning: No typo patterns loaded from data/warnings/typo_messages.json")
    TYPO_PATTERNS = {}  # Empty dict is acceptable for typo patterns


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


def check_redirection_target(target: str) -> Tuple[bool, str]:
    """
    Check if a redirection target is dangerous.

    This function checks output redirection targets (from > or >>)
    against known dangerous paths.

    Args:
        target: The redirection target path (e.g., "/dev/sda", "/etc/passwd")

    Returns:
        Tuple of (is_dangerous, pattern_name)
        is_dangerous: True if target is dangerous, False otherwise
        pattern_name: Name of matched pattern, or empty string if safe

    Examples:
        >>> check_redirection_target("/dev/sda")
        (True, "redirect_to_disk")
        >>> check_redirection_target("/tmp/file")
        (False, "")
    """
    import re

    # Define dangerous redirection patterns
    # These match the patterns in warning_catalog.json
    dangerous_patterns = [
        (r'^/dev/sd[a-z]$', 'redirect_to_disk'),           # SATA disks
        (r'^/dev/nvme\d+n\d+$', 'redirect_to_disk'),       # NVMe disks
        (r'^/proc/sysrq-trigger$', 'kernel_panic'),        # Kernel panic
        (r'^/dev/mem$', 'system_modify'),                  # Memory access
        (r'^/etc/passwd$', 'system_modify'),               # System files
        (r'^/etc/shadow$', 'system_modify'),
        (r'^/etc/fstab$', 'system_modify'),
        (r'^/etc/sudoers$', 'system_modify'),
        (r'^/etc/hosts$', 'system_modify'),
        (r'^/etc/group$', 'system_modify'),
    ]

    for pattern, pattern_name in dangerous_patterns:
        if re.match(pattern, target, re.IGNORECASE):
            return True, pattern_name

    return False, ""


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
        # Use compiled pattern if available (faster)
        if 'compiled' in pattern_data:
            if pattern_data['compiled'].search(command):
                return "critical", pattern_name
        else:
            # Fallback to re.search for backward compatibility
            if re.search(pattern_data["pattern"], command, re.IGNORECASE):
                return "critical", pattern_name

    # Check caution patterns (medium priority)
    for pattern_name, pattern_data in CAUTION_PATTERNS.items():
        # Use compiled pattern if available (faster)
        if 'compiled' in pattern_data:
            if pattern_data['compiled'].search(command):
                return "caution", pattern_name
        else:
            # Fallback to re.search for backward compatibility
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

    # Extract paths from command (handles command chaining)
    try:
        paths = parser.extract_all_paths(command)
    except Exception:
        # If parsing fails, err on side of caution (fail-safe)
        # Command chaining or complex syntax might hide dangerous operations
        return "critical", "system_critical", command

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
