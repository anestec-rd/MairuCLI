# Design Document - System Directory Protection

## Overview

This document outlines the technical design for implementing system directory protection in MairuCLI. The feature will add a new security layer that prevents accidental modification or deletion of critical system directories, protecting beginners and children from irreversible system damage.

## Architecture

### High-Level Architecture

```
User Input
    ↓
Command Parser
    ↓
[NEW] System Directory Protection Check ← (Highest Priority)
    ↓
Dangerous Pattern Check
    ↓
Caution Pattern Check
    ↓
System Shell Execution
```

### Integration Points

1. **Command Processing Flow** (`src/main.py`)
   - Add system directory check before dangerous pattern check
   - New Layer 1.5: System Directory Protection (between parsing and pattern matching)

2. **Interceptor Module** (`src/interceptor.py`)
   - Add new function: `check_system_directory(command: str) -> Tuple[str, str, str]`
   - Returns: (level, protection_type, target_path)

3. **Display System** (`src/display/`)
   - Create new warning component: `SystemProtectionWarning`
   - Reuse existing warning display infrastructure

## Components and Interfaces

### 1. Protected Directory Database

**Location:** `src/interceptor.py`

```python
# Platform-specific protected directories
PROTECTED_DIRECTORIES = {
    "win32": {
        "critical": [
            r"C:\Windows",
            r"C:\Windows\System32",
            r"C:\Windows\SysWOW64",
        ],
        "caution": [
            r"C:\Program Files",
            r"C:\Program Files (x86)",
            r"C:\ProgramData",
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
            "/var/log"
        ]
    },
    "darwin": {  # macOS
        "critical": [
            "/System", "/bin", "/sbin",
            "/etc", "/var", "/private"
        ],
        "caution": [
            "/Library", "/Applications",
            "/usr/bin", "/usr/sbin"
        ]
    }
}
```

### 2. Path Resolution Module

**Location:** `src/path_resolver.py` (new file)

```python
class PathResolver:
    """Resolves and normalizes file paths for protection checking."""

    def __init__(self):
        self.platform = sys.platform

    def resolve_path(self, path: str) -> str:
        """
        Resolve relative path to absolute path.

        Args:
            path: Raw path from command (may be relative)

        Returns:
            Absolute normalized path
        """
        # Expand environment variables
        path = os.path.expandvars(path)

        # Expand user home directory (~)
        path = os.path.expanduser(path)

        # Convert to absolute path
        path = os.path.abspath(path)

        # Normalize path separators
        path = os.path.normpath(path)

        return path

    def extract_paths_from_command(self, command: str) -> List[str]:
        """
        Extract file paths from command string.

        Args:
            command: Full command string

        Returns:
            List of extracted paths
        """
        # Parse command to identify file path arguments
        # Handle various command formats (rm, mv, chmod, etc.)
        pass
```

### 3. System Directory Checker

**Location:** `src/interceptor.py`

```python
def check_system_directory(command: str) -> Tuple[str, str, str]:
    """
    Check if command targets protected system directories.

    Args:
        command: User-entered command string

    Returns:
        Tuple of (level, protection_type, target_path)
        level: "critical", "caution", or "safe"
        protection_type: "system_critical", "system_caution", or ""
        target_path: The protected path that was targeted

    Performance: Must complete within 50ms
    """
    # Get platform-specific protected directories
    platform = sys.platform
    if platform not in PROTECTED_DIRECTORIES:
        return "safe", "", ""

    # Extract paths from command
    resolver = PathResolver()
    paths = resolver.extract_paths_from_command(command)

    # Check each path against protected directories
    for path in paths:
        try:
            resolved_path = resolver.resolve_path(path)

            # Check critical directories first
            for protected_dir in PROTECTED_DIRECTORIES[platform]["critical"]:
                if resolved_path.startswith(protected_dir):
                    return "critical", "system_critical", resolved_path

            # Check caution directories
            for protected_dir in PROTECTED_DIRECTORIES[platform]["caution"]:
                if resolved_path.startswith(protected_dir):
                    return "caution", "system_caution", resolved_path

        except Exception:
            # If path resolution fails, err on side of caution
            return "critical", "system_critical", path

    return "safe", "", ""
```

### 4. Command Parser Enhancement

**Location:** `src/command_parser.py` (new file)

```python
class CommandParser:
    """Parse commands to extract file paths and operations."""

    # Commands that operate on files/directories
    FILE_COMMANDS = {
        "rm": {"path_args": [0]},  # rm <path>
        "rmdir": {"path_args": [0]},
        "mv": {"path_args": [0, 1]},  # mv <source> <dest>
        "cp": {"path_args": [0, 1]},
        "chmod": {"path_args": [1]},  # chmod <mode> <path>
        "chown": {"path_args": [1]},  # chown <owner> <path>
        "dd": {"special": "dd_parser"},  # dd if=<path> of=<path>
    }

    def parse(self, command: str) -> Dict[str, Any]:
        """
        Parse command to extract operation and target paths.

        Returns:
            {
                "command": str,
                "paths": List[str],
                "operation": str,
                "has_redirect": bool,
                "redirect_target": str
            }
        """
        parts = shlex.split(command)
        if not parts:
            return {"command": "", "paths": [], "operation": ""}

        cmd = parts[0]
        args = parts[1:]

        # Check for output redirection
        redirect_target = self._check_redirect(command)

        # Extract paths based on command type
        paths = self._extract_paths(cmd, args)

        return {
            "command": cmd,
            "paths": paths,
            "operation": self._get_operation_type(cmd),
            "has_redirect": redirect_target is not None,
            "redirect_target": redirect_target
        }
```

### 5. System Protection Warning Component

**Location:** `src/display/system_protection_warning.py` (new file)

```python
class SystemProtectionWarning:
    """Display system directory protection warnings."""

    def __init__(self, renderer: AsciiRenderer):
        self.renderer = renderer

    def display(self, level: str, target_path: str, command: str) -> None:
        """
        Display system protection warning.

        Args:
            level: "critical" or "caution"
            target_path: The protected path being targeted
            command: The blocked command
        """
        if level == "critical":
            self._display_critical_warning(target_path, command)
        else:
            self._display_caution_warning(target_path, command)

    def _display_critical_warning(self, target_path: str, command: str):
        """Display critical system directory warning."""
        print()
        print("=" * 60)
        print(f"🛑 {self.renderer.colorize('STOP RIGHT THERE!', 'red')}")
        print("=" * 60)
        print()

        # Identify directory type
        dir_info = self._get_directory_info(target_path)

        print(f"You're trying to modify: {self.renderer.colorize(target_path, 'orange')}")
        print()
        print(f"💡 {self.renderer.colorize('What you should know:', 'purple')}")
        print(f"  - {dir_info['description']}")
        print(f"  - {dir_info['risk']}")
        print(f"  - {dir_info['consequence']}")
        print()
        print(f"🎃 {self.renderer.colorize('Safe alternative:', 'green')}")
        for alt in dir_info['alternatives']:
            print(f"  - {alt}")
        print()
        print(self.renderer.colorize("Command blocked for your safety.", "red"))
        print("=" * 60)
        print()
```

## Data Models

### Directory Information

```python
DIRECTORY_INFO = {
    "C:\\Windows": {
        "description": "Windows system directory contains core OS files",
        "risk": "Modifying files here can make Windows unbootable",
        "consequence": "System may fail to start, requiring reinstallation",
        "alternatives": [
            "Work in your user directory: C:\\Users\\YourName\\",
            "Use Documents, Downloads, or Desktop folders",
            "Ask an experienced user if you need to modify system files"
        ]
    },
    "C:\\Windows\\System32": {
        "description": "System32 contains essential Windows components",
        "risk": "Deleting files here will break Windows immediately",
        "consequence": "Windows will crash and become unbootable",
        "alternatives": [
            "NEVER modify System32 unless you're an expert",
            "Use your user directory for all personal files",
            "System files are protected for a reason!"
        ]
    },
    "/etc": {
        "description": "/etc contains system configuration files",
        "risk": "Incorrect changes can break system services",
        "consequence": "System may become unstable or unbootable",
        "alternatives": [
            "Work in your home directory: /home/username/",
            "Use ~/Documents or ~/Downloads for personal files",
            "Learn about configuration before modifying /etc"
        ]
    },
    # ... more directory info
}
```

## Error Handling

### Path Resolution Errors

```python
try:
    resolved_path = resolver.resolve_path(path)
except PermissionError:
    # Cannot access path - treat as protected
    return "critical", "system_critical", path
except FileNotFoundError:
    # Path doesn't exist yet - check parent directory
    parent = os.path.dirname(path)
    return check_system_directory(f"dummy {parent}")
except Exception as e:
    # Unknown error - err on side of caution
    logger.warning(f"Path resolution failed: {e}")
    return "critical", "system_critical", path
```

### Edge Cases

1. **Symbolic Links**
   ```python
   # Resolve symlinks to real paths
   if os.path.islink(path):
       real_path = os.path.realpath(path)
       # Check real path against protected directories
   ```

2. **Wildcards**
   ```python
   # Detect wildcards in protected directories
   if '*' in path or '?' in path:
       # Expand wildcards and check each result
       expanded = glob.glob(path)
       for expanded_path in expanded:
           # Check each expanded path
   ```

3. **Case Sensitivity**
   ```python
   # Handle case-insensitive file systems (Windows, macOS)
   if sys.platform in ['win32', 'darwin']:
       resolved_path = resolved_path.lower()
       protected_dir = protected_dir.lower()
   ```

## Testing Strategy

### Unit Tests

**File:** `tests/unit/test_path_resolver.py`
```python
def test_resolve_relative_path():
    """Test relative path resolution."""
    resolver = PathResolver()
    result = resolver.resolve_path("../Windows")
    assert result.endswith("Windows")

def test_expand_environment_variables():
    """Test environment variable expansion."""
    resolver = PathResolver()
    result = resolver.resolve_path("$WINDIR")
    assert "Windows" in result
```

**File:** `tests/unit/test_system_directory_check.py`
```python
def test_detect_windows_system32():
    """Test detection of System32 directory."""
    level, ptype, path = check_system_directory("rm C:\\Windows\\System32\\test.dll")
    assert level == "critical"
    assert ptype == "system_critical"

def test_detect_relative_path_to_system():
    """Test detection via relative path."""
    # Assuming current dir is C:\Users\Test
    level, ptype, path = check_system_directory("rm ../../Windows/test.txt")
    assert level == "critical"
```

### Integration Tests

**File:** `tests/integration/test_system_protection_flow.py`
```python
def test_complete_protection_flow():
    """Test complete command blocking flow."""
    # Simulate user entering dangerous command
    command = "rm -rf C:\\Windows\\System32"

    # Process command
    result = process_command(command)

    # Verify command was blocked
    assert result == ""  # Not executed
    # Verify warning was displayed (check output)
    # Verify statistics were updated
```

### Manual Tests

**File:** `tests/manual/system_protection_tests.md`
- Test on actual Windows system
- Test on actual Linux system
- Test with various path formats
- Verify educational messages are clear
- Test performance (< 50ms)

## Performance Considerations

### Optimization Strategies

1. **Path Caching**
   ```python
   class PathResolver:
       def __init__(self):
           self._cache = {}  # Cache resolved paths

       def resolve_path(self, path: str) -> str:
           if path in self._cache:
               return self._cache[path]
           resolved = self._resolve_uncached(path)
           self._cache[path] = resolved
           return resolved
   ```

2. **Early Exit**
   ```python
   # Check command type first
   if command_type not in FILE_COMMANDS:
       return "safe", "", ""  # Not a file operation
   ```

3. **Lazy Loading**
   ```python
   # Load directory info only when needed
   def _get_directory_info(self, path: str) -> Dict:
       if path not in self._info_cache:
           self._info_cache[path] = self._load_directory_info(path)
       return self._info_cache[path]
   ```

## Implementation Plan

### Phase 1: Core Infrastructure (30 min)
1. Create `PathResolver` class
2. Create `CommandParser` class
3. Add `PROTECTED_DIRECTORIES` database
4. Add `check_system_directory()` function

### Phase 2: Integration (20 min)
1. Integrate into `process_command()` flow
2. Add system protection check before pattern matching
3. Update statistics tracking

### Phase 3: Display (15 min)
1. Create `SystemProtectionWarning` component
2. Add directory information database
3. Implement educational messages

### Phase 4: Testing (20 min)
1. Write unit tests
2. Write integration tests
3. Manual testing on Windows/Linux

### Phase 5: Documentation (5 min)
1. Update CHANGELOG.md
2. Update README.md
3. Add to DANGEROUS_PATTERNS.md

**Total Estimated Time:** 90 minutes

## Security Considerations

1. **Fail-Safe Design**: If path resolution fails, block the command
2. **No Bypass**: Check resolved paths, not raw input
3. **Platform-Specific**: Use appropriate paths for each OS
4. **Comprehensive**: Cover all dangerous file operations
5. **Layered**: System protection + pattern matching + caution warnings

## Future Enhancements

1. **Custom Protected Directories**: Allow users to add their own protected paths
2. **Whitelist**: Allow specific safe operations in system directories
3. **Audit Log**: Log all blocked system directory access attempts
4. **Parent Controls**: Additional restrictions for child accounts
5. **Learning Mode**: Gradually reduce protection as user gains experience
