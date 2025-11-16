# MairuCLI Design Document

## Document Information

**Version:** 1.0
**Date:** 2025-11-16
**Status:** Draft
**Based on:** requirements-review.md (MVP Scope)

## Overview

MairuCLI is a Python-based CLI wrapper that intercepts dangerous commands and displays Halloween-themed educational warnings. The system operates as a lightweight shell wrapper, providing real-time command analysis without introducing noticeable latency.

### Design Principles

1. **Simplicity First**: MVP focuses on core functionality, extensibility for future
2. **Performance**: Pattern matching must complete within 50ms
3. **Non-Intrusive**: Pass-through for non-flagged commands with zero modification
4. **Educational**: Every warning teaches something valuable
5. **Entertaining**: Halloween theme makes learning memorable

### Scope Reminder (MVP)

**In Scope:**
- 5 dangerous command patterns
- 3 ASCII art responses
- 3 typo patterns
- Halloween color scheme
- Basic educational messages

**Out of Scope (Future):**
- Cross-platform beyond Linux/macOS
- Command history logging
- Override mechanisms
- Advanced pattern recognition (pipes, variables)

---

## Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────┐
│                        User                              │
└────────────────────┬────────────────────────────────────┘
                     │ Command Input
                     ▼
┌─────────────────────────────────────────────────────────┐
│                   MairuCLI Wrapper                       │
│  ┌───────────────────────────────────────────────────┐  │
│  │            Command Interceptor                     │  │
│  │  - Parse command                                   │  │
│  │  - Pattern matching (regex)                        │  │
│  │  - Decision: intercept or pass-through            │  │
│  └─────────────┬─────────────────┬───────────────────┘  │
│                │ Dangerous       │ Safe                  │
│                ▼                 ▼                       │
│  ┌─────────────────────┐  ┌──────────────────────────┐ │
│  │  Warning Display    │  │   Pass to System Shell   │ │
│  │  - ASCII Art        │  │   - Execute normally     │ │
│  │  - Colors           │  │   - Return output        │ │
│  │  - Education        │  │                          │ │
│  └─────────────────────┘  └──────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│                  System Shell (bash/zsh)                 │
└─────────────────────────────────────────────────────────┘
```

### Component Architecture

```
mairu-cli/
├── src/
│   ├── main.py              # Entry point, REPL loop
│   ├── interceptor.py       # Pattern matching engine
│   ├── display.py           # ASCII art & color rendering
│   ├── patterns.py          # Pattern database (hardcoded for MVP)
│   └── config.py            # Configuration (colors, enable/disable)
├── ascii_art/
│   ├── fired.txt            # "YOU'RE FIRED" art
│   ├── permission_denied.txt # chmod 777 art
│   └── data_destroyer.txt   # dd command art
├── tests/
│   ├── test_interceptor.py
│   └── test_display.py
└── README.md
```

---

## Component Design

### 0. Builtin Commands (`builtins.py`) - NEW

**Responsibility:** Implement essential shell builtin commands internally

**Why This Is Needed:**
MairuCLI must implement certain commands internally because they affect the shell's state (like `cd` changing the current directory). If we pass these to `subprocess`, they execute in a child process and don't affect MairuCLI's state.

**Builtin Commands to Implement:**

**Phase 1 (Essential):**
- `cd` - Change directory
- `pwd` - Print working directory
- `exit` / `quit` - Exit MairuCLI

**Phase 2 (Recommended):**
- `echo` - Print text
- `export` - Set environment variable
- `history` - Show command history

**Implementation:**

```python
import os
from pathlib import Path
from typing import List, Optional

class BuiltinCommands:
    """Internal implementation of shell builtin commands."""

    # Class variables for state
    _history: List[str] = []
    _prev_dir: Optional[Path] = None

    @classmethod
    def is_builtin(cls, cmd_name: str) -> bool:
        """Check if command is a builtin."""
        return cmd_name in ['cd', 'pwd', 'exit', 'quit', 'echo', 'export', 'history']

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
        """Print working directory."""
        print(os.getcwd())
        return True

    @classmethod
    def _cmd_echo(cls, args: List[str]) -> bool:
        """Echo command - print arguments."""
        print(" ".join(args))
        return True

    @classmethod
    def _cmd_export(cls, args: List[str]) -> bool:
        """Set environment variable."""
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
        """Show command history."""
        for i, cmd in enumerate(cls._history, 1):
            print(f"{i:4d}  {cmd}")
        return True

    @classmethod
    def add_to_history(cls, command: str) -> None:
        """Add command to history."""
        cls._history.append(command)
```

**Design Decisions:**
- Class-based design for state management (history, previous directory)
- Each builtin is a separate method (`_cmd_*`)
- Returns `True` to indicate command was handled
- Error messages match standard shell behavior
- `cd -` support for returning to previous directory

---

### 1. Main Entry Point (`main.py`)

**Responsibility:** Application lifecycle and REPL loop

**Key Functions:**

```python
def main() -> None:
    """
    Main entry point for MairuCLI.
    Displays welcome banner and starts REPL loop.
    """
    display_welcome_banner()
    repl_loop()

def repl_loop() -> None:
    """
    Read-Eval-Print Loop for command processing.
    Continues until user exits.
    """
    while True:
        command = get_user_input()
        if command == "exit":
            display_goodbye_message()
            break
        process_command(command)

def process_command(command: str) -> None:
    """
    Process a single command: intercept or pass-through.

    Args:
        command: User-entered command string
    """
    is_dangerous, pattern_name = interceptor.check_command(command)

    if is_dangerous:
        display.show_warning(pattern_name, command)
    else:
        execute_safe_command(command)
```

**Design Decisions:**
- Simple REPL loop (no complex shell emulation)
- Synchronous execution (no async needed for MVP)
- Exit command handled specially (no interception)

---

### 2. Command Interceptor (`interceptor.py`)

**Responsibility:** Pattern matching and command analysis

**Data Structures:**

```python
from typing import Dict, Tuple
import re

# Pattern database (hardcoded for MVP, JSON in future)
DANGEROUS_PATTERNS: Dict[str, Dict[str, str]] = {
    "rm_root": {
        "pattern": r"rm\s+(-rf|-fr|-r\s+-f|-f\s+-r)\s+(/|~|\$HOME)",
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
        "art_file": "fired.txt"  # Reuse fired art
    },
    "sudo_rm_var": {
        "pattern": r"sudo\s+rm\s+(-rf|-fr)\s+\$\w+",
        "category": "deletion",
        "severity": "high",
        "art_file": "fired.txt"  # Reuse fired art
    }
}

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
    },
    "grpe": {
        "pattern": r"^grpe\b",
        "correct": "grep",
        "message": "🕷️ Grep-ing for typos? Found one!"
    }
}
```

**Key Functions:**

```python
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
```

**Design Decisions:**
- Hardcoded patterns for MVP (easier to test, faster startup)
- Regex with IGNORECASE for flexibility
- Dangerous patterns checked before typos (priority)
- Simple linear search (5+3 patterns = acceptable performance)
- Future: Move to JSON file for community contributions

---

### 3. Display System (`display.py`)

**Responsibility:** ASCII art rendering, color management, message formatting

**Color Constants:**

```python
from typing import Dict

# Halloween color palette (ANSI 256-color codes)
COLORS: Dict[str, str] = {
    "orange": "\033[38;5;208m",
    "chocolate": "\033[38;5;130m",
    "purple": "\033[38;5;141m",
    "green": "\033[38;5;46m",
    "red": "\033[38;5;196m",
    "reset": "\033[0m"
}

# Emoji constants
EMOJI = {
    "fire": "🔥",
    "pumpkin": "🎃",
    "train": "🚂",
    "spider": "🕷️",
    "skull": "💀",
    "lightbulb": "💡"
}
```

**Key Functions:**

```python
def show_warning(pattern_name: str, command: str) -> None:
    """
    Display warning for dangerous command or typo.

    Args:
        pattern_name: Name of matched pattern
        command: The dangerous command entered
    """
    pattern_info = interceptor.get_pattern_info(pattern_name)

    if pattern_name.startswith("typo_"):
        show_typo_warning(pattern_info, command)
    else:
        show_danger_warning(pattern_info, command)

def show_danger_warning(pattern_info: Dict, command: str) -> None:
    """
    Display warning for dangerous command.

    Format:
    [ASCII Art]
    [Headline with emoji]
    [Explanation]
    [Real-world incident]
    [Safe alternative]
    """
    # Load ASCII art
    art = load_ascii_art(pattern_info["art_file"])
    print(colorize(art, "red"))

    # Display message based on category
    if pattern_info["category"] == "deletion":
        print(f"\n{EMOJI['fire']} YOU'RE FIRED! {EMOJI['fire']}")
        print(colorize("(And so is your entire filesystem!)", "orange"))
        print(f"\nThe command '{command}' attempts to delete EVERYTHING.")
        print("This is unrecoverable without backups.")
        print(f"\n{EMOJI['lightbulb']} Safe alternative: Use 'rm -i' for confirmation.")

    elif pattern_info["category"] == "permission":
        print(f"\n{EMOJI['skull']} PERMISSION DENIED! {EMOJI['skull']}")
        print(colorize("(By the security gods!)", "purple"))
        print(f"\nThe command '{command}' opens security holes.")
        print("Anyone can read, write, and execute your files.")
        print(f"\n{EMOJI['lightbulb']} Safe alternative: Use specific permissions like 644 or 755.")

    # ... other categories

def show_typo_warning(pattern_info: Dict, command: str) -> None:
    """
    Display entertaining message for typo.

    Format:
    [Emoji] [Fun message] [Emoji]
    [Brief explanation]
    """
    print(f"\n{pattern_info['message']}")
    print(colorize(f"Did you mean '{pattern_info['correct']}'?", "orange"))

def load_ascii_art(filename: str) -> str:
    """
    Load ASCII art from file.

    Args:
        filename: Name of ASCII art file

    Returns:
        ASCII art as string
    """
    art_path = Path(__file__).parent.parent / "ascii_art" / filename
    with open(art_path, "r", encoding="utf-8") as f:
        return f.read()

def colorize(text: str, color_name: str) -> str:
    """
    Apply ANSI color to text.

    Args:
        text: Text to colorize
        color_name: Name of color from COLORS dict

    Returns:
        Colorized text with reset code
    """
    return f"{COLORS[color_name]}{text}{COLORS['reset']}"

def display_welcome_banner() -> None:
    """
    Display Halloween-themed welcome banner on startup.
    """
    banner = f"""
{colorize("╔═══════════════════════════════════════════════════════════╗", "orange")}
{colorize("║", "orange")}  {EMOJI['pumpkin']} {colorize("Welcome to MairuCLI", "red")} {EMOJI['pumpkin']}                                  {colorize("║", "orange")}
{colorize("║", "orange")}  {colorize("Your friendly CLI safety wrapper with a spooky twist!", "chocolate")}  {colorize("║", "orange")}
{colorize("╚═══════════════════════════════════════════════════════════╝", "orange")}

{colorize("Type commands as usual. I'll keep you safe from scary mistakes!", "green")}
{colorize("Type 'exit' to leave (if you dare...)", "purple")}
"""
    print(banner)
```

**Design Decisions:**
- ANSI 256-color codes for better compatibility
- ASCII art stored in separate files (easier to edit/test)
- Message templates hardcoded for MVP (JSON in future)
- Emoji for visual appeal (Unicode 12.0 for compatibility)
- Color reset after every colored text (prevent bleeding)

---

### 4. Pattern Database (`patterns.py`)

**Responsibility:** Centralized pattern definitions and metadata

For MVP, patterns are hardcoded in `interceptor.py`. In future versions, this will be a separate module loading from JSON:

```python
# Future structure (not implemented in MVP)
def load_patterns_from_json(filepath: str) -> Dict:
    """Load pattern database from JSON file."""
    pass

def validate_pattern(pattern: Dict) -> bool:
    """Validate pattern structure and regex syntax."""
    pass
```

**Future JSON Structure:**

```json
{
  "dangerous_patterns": {
    "rm_root": {
      "pattern": "rm\\s+(-rf|-fr)\\s+(/|~|\\$HOME)",
      "category": "deletion",
      "severity": "critical",
      "art_file": "fired.txt",
      "messages": {
        "headline": "YOU'RE FIRED!",
        "subheadline": "(And so is your entire filesystem!)",
        "explanation": "This command deletes EVERYTHING on your system.",
        "consequence": "Unrecoverable without backups.",
        "incident": "GitLab lost 300GB in 2017 due to accidental rm -rf.",
        "safe_alternative": "Use 'rm -i' for interactive confirmation."
      }
    }
  },
  "typo_patterns": {
    "sl": {
      "pattern": "^sl$",
      "correct": "ls",
      "message": "🚂 Choo choo! All aboard the typo train!"
    }
  }
}
```

---

### 5. Configuration (`config.py`)

**Responsibility:** User preferences and system settings

**MVP Configuration:**

```python
from dataclasses import dataclass
from typing import Dict

@dataclass
class MairuConfig:
    """Configuration for MairuCLI."""

    # Color settings
    colors_enabled: bool = True
    color_scheme: str = "halloween"  # Future: support other themes

    # Display settings
    show_ascii_art: bool = True
    show_educational_messages: bool = True

    # Behavior settings
    intercept_dangerous: bool = True
    intercept_typos: bool = True

    # Performance settings
    pattern_match_timeout_ms: int = 50

# Global config instance
config = MairuConfig()

def load_config() -> MairuConfig:
    """
    Load configuration from file or use defaults.
    MVP: Returns default config (no file loading)
    """
    return MairuConfig()

def save_config(cfg: MairuConfig) -> None:
    """
    Save configuration to file.
    MVP: Not implemented (future feature)
    """
    pass
```

**Design Decisions:**
- Dataclass for type safety and simplicity
- Default values for all settings (no config file required)
- Config file loading deferred to future version
- Global config instance for easy access

---

## Data Models

### Pattern Data Structure

```python
from typing import TypedDict

class DangerousPattern(TypedDict):
    """Structure for dangerous command pattern."""
    pattern: str          # Regex pattern
    category: str         # deletion, permission, disk, database, etc.
    severity: str         # critical, high, medium, low
    art_file: str         # ASCII art filename

class TypoPattern(TypedDict):
    """Structure for typo pattern."""
    pattern: str          # Regex pattern
    correct: str          # Correct command
    message: str          # Fun message to display
```

### Command Analysis Result

```python
from dataclasses import dataclass

@dataclass
class CommandAnalysis:
    """Result of command analysis."""
    is_dangerous: bool
    pattern_name: str
    pattern_type: str  # "dangerous" or "typo"
    matched_text: str  # The part that matched
```

---

## Command Processing Flow (UPDATED)

### Three-Tier Command Processing

```
User Input: "cd /tmp"
     ↓
┌────────────────────────────────────┐
│  1. Check if Builtin Command      │
│     (cd, pwd, echo, export, etc.)  │
└────────┬───────────────────────────┘
         │ YES → Execute internally
         │       (affects MairuCLI state)
         │
         │ NO ↓
┌────────────────────────────────────┐
│  2. Check if Dangerous Pattern    │
│     (rm -rf /, chmod 777, etc.)    │
└────────┬───────────────────────────┘
         │ YES → Show warning
         │       (block execution)
         │
         │ NO ↓
┌────────────────────────────────────┐
│  3. Execute in System Shell        │
│     (ls, git, grep, etc.)          │
│     via subprocess.run()           │
└────────────────────────────────────┘
```

### Why Builtin Commands Are Necessary

**Problem:** Some commands must affect MairuCLI's own process state.

**Example - cd command:**
```python
# ❌ This doesn't work:
subprocess.run("cd /tmp", shell=True)
# The cd happens in a child process, MairuCLI stays in original directory

# ✅ This works:
os.chdir("/tmp")
# MairuCLI's process changes directory
```

**Commands That Need Internal Implementation:**
- `cd` - Changes current directory
- `pwd` - Shows current directory (could use subprocess, but faster internally)
- `export` - Sets environment variables for MairuCLI process
- `exit` / `quit` - Exits MairuCLI itself
- `history` - Shows MairuCLI's command history

**Commands That Can Use System Shell:**
- `ls`, `grep`, `git`, `cat`, `vim`, `nano`, etc.
- These don't need to affect MairuCLI's state
- System shell handles them perfectly

### Updated File Structure

```
mairu-cli/
├── src/
│   ├── main.py              # Entry point, REPL loop
│   ├── builtins.py          # NEW: Builtin command implementations
│   ├── interceptor.py       # Pattern matching engine
│   ├── display.py           # ASCII art & color rendering
│   ├── patterns.py          # Pattern database
│   └── config.py            # Configuration
├── ascii_art/
│   ├── fired.txt
│   ├── permission_denied.txt
│   └── data_destroyer.txt
├── tests/
│   ├── test_builtins.py     # NEW: Test builtin commands
│   ├── test_interceptor.py
│   └── test_display.py
└── README.md
```

## Implementation Strategy

### Phase 1: Core Infrastructure (Day 1-2, 12 hours) - UPDATED

**Goal:** Basic command interception AND builtin commands working

**Tasks:**
1. Set up project structure
2. **Implement `builtins.py` with cd, pwd, exit** (NEW - 2 hours)
3. Implement `main.py` REPL loop with three-tier processing (2 hours)
4. Implement `interceptor.py` with 5 dangerous patterns (4 hours)
5. Implement basic `display.py` (text only, no ASCII art yet) (2 hours)
6. Test pattern matching and builtin commands manually (2 hours)

**Deliverable:** CLI that can:
- ✅ Detect `rm -rf /` and print a warning
- ✅ Execute `cd /tmp` and actually change directory
- ✅ Execute `ls` and show files
- ✅ Execute `git status` and show output

---

### Phase 2: Visual Enhancement (Day 2-3, 8 hours) - UPDATED

**Goal:** Basic command interception working

**Tasks:**
1. Set up project structure
2. Implement `main.py` REPL loop
3. Implement `interceptor.py` with 5 dangerous patterns
4. Implement basic `display.py` (text only, no ASCII art yet)
5. Test pattern matching manually

**Deliverable:** CLI that can detect `rm -rf /` and print a warning

---

### Phase 2: Visual Enhancement (Day 2-3, 10 hours)

**Goal:** Halloween theme and ASCII art

**Tasks:**
1. Create 3 ASCII art files
2. Implement color rendering in `display.py`
3. Implement welcome banner
4. Add educational messages for each pattern
5. Test on dark terminal background

**Deliverable:** Fully themed warnings with ASCII art

---

### Phase 2.5: Additional Builtins (Day 3, 2 hours) - NEW

**Goal:** Add echo, export, history commands

**Tasks:**
1. Implement `echo` command (0.5 hours)
2. Implement `export` command (0.5 hours)
3. Implement `history` command (0.5 hours)
4. Test all builtins (0.5 hours)

**Deliverable:** Full set of essential builtin commands

---

### Phase 3: Typo Entertainment (Day 3-4, 4 hours) - UPDATED

**Goal:** Add typo detection and fun responses

**Tasks:**
1. Add 2 typo patterns to `interceptor.py` (reduced from 3 to save time)
2. Implement typo warning display
3. Test typo detection
4. Polish messages

**Deliverable:** Typo entertainment working (sl, cd.. only)

---

### Phase 4: Polish & Testing (Day 4, 4 hours)

**Goal:** Code quality and bug fixes

**Tasks:**
1. Add docstrings to all functions
2. Write basic unit tests
3. Manual end-to-end testing
4. Fix bugs
5. Code cleanup

**Deliverable:** Stable, tested codebase

---

### Phase 5: Demo Preparation (Day 5, 10 hours)

**Goal:** Demo video and submission

**Tasks:**
1. Write README.md
2. Create demo script
3. Record demo video (3 minutes)
4. Edit video
5. Prepare submission materials
6. Submit to Devpost

**Deliverable:** Submitted hackathon entry

---

## Testing Strategy

### Unit Tests

**Test Coverage (Minimum):**

```python
# test_interceptor.py
def test_rm_root_detection():
    """Test rm -rf / is detected."""
    assert check_command("rm -rf /")[0] == True

def test_safe_command_passthrough():
    """Test safe commands are not flagged."""
    assert check_command("ls -la")[0] == False

def test_typo_detection():
    """Test sl typo is detected."""
    assert check_command("sl")[0] == True

# test_display.py
def test_colorize():
    """Test color codes are applied correctly."""
    result = colorize("test", "red")
    assert "\033[38;5;196m" in result
    assert "\033[0m" in result
```

### Manual Testing Checklist

**Builtin Commands (NEW):**
- [ ] `cd /tmp` → Changes directory
- [ ] `pwd` → Shows /tmp
- [ ] `cd ~` → Goes to home
- [ ] `cd -` → Returns to previous directory
- [ ] `echo "Hello World"` → Prints text
- [ ] `export VAR=value` → Sets environment variable
- [ ] `history` → Shows command history

**Dangerous Commands:**
- [ ] `rm -rf /` → Shows "YOU'RE FIRED"
- [ ] `chmod 777 -R /` → Shows permission warning
- [ ] `dd if=/dev/zero of=/dev/sda` → Shows data destroyer warning
- [ ] `DROP DATABASE production` → Shows database warning
- [ ] `sudo rm -rf $VAR` → Shows variable warning

**Typos:**
- [ ] `sl` → Shows train message
- [ ] `cd..` → Shows stuck together message

**Safe Commands (System Shell):**
- [ ] `ls -la` → Executes normally
- [ ] `git status` → Executes normally
- [ ] `grep "pattern" file.txt` → Executes normally
- [ ] `cat file.txt` → Executes normally

**Integration Test:**
```bash
$ python mairu-cli.py
🎃 Welcome to MairuCLI 🎃

mairu> pwd
/home/user

mairu> cd /tmp
mairu> pwd
/tmp

mairu> ls
file1.txt  file2.txt

mairu> cd ~
mairu> pwd
/home/user

mairu> echo "Testing"
Testing

mairu> rm -rf /
🔥 YOU'RE FIRED! 🔥
[ASCII art]

mairu> ls
file1.txt  file2.txt  # Still works!

mairu> exit
👻 Thanks for using MairuCLI! Stay safe out there!
```

**Visual:**
- [ ] Colors display correctly on dark terminal
- [ ] ASCII art renders within 80 characters
- [ ] Welcome banner displays on startup
- [ ] No color bleeding between messages

---

## Performance Considerations

### Pattern Matching Optimization

**Target:** <50ms per command

**Strategy:**
- Linear search acceptable for 8 patterns (5 dangerous + 3 typo)
- Regex compilation happens once at startup
- No complex lookahead/lookbehind in patterns
- IGNORECASE flag for flexibility without multiple patterns

**Measurement:**

```python
import time

def check_command_with_timing(command: str) -> Tuple[bool, str, float]:
    """Check command and measure time."""
    start = time.perf_counter()
    result = check_command(command)
    elapsed_ms = (time.perf_counter() - start) * 1000
    return (*result, elapsed_ms)
```

### Memory Footprint

**Expected:**
- Pattern database: <1KB (8 patterns)
- ASCII art files: ~5KB total (3 files)
- Python runtime: ~20MB
- **Total: ~25MB** (acceptable for CLI tool)

---

## Error Handling

### Graceful Degradation

**Principle:** Never crash, always provide feedback

**Error Scenarios:**

1. **ASCII art file missing:**
   ```python
   try:
       art = load_ascii_art(filename)
   except FileNotFoundError:
       art = "[ASCII art not found]"
       logger.warning(f"ASCII art file missing: {filename}")
   ```

2. **Regex compilation error:**
   ```python
   try:
       compiled_pattern = re.compile(pattern)
   except re.error as e:
       logger.error(f"Invalid regex pattern: {pattern}, error: {e}")
       # Skip this pattern, continue with others
   ```

3. **Terminal doesn't support colors:**
   ```python
   if not sys.stdout.isatty():
       config.colors_enabled = False
   ```

4. **Command execution fails:**
   ```python
   try:
       subprocess.run(command, shell=True, check=True)
   except subprocess.CalledProcessError as e:
       print(f"Command failed with exit code {e.returncode}")
   ```

---

## Security Considerations

### Input Sanitization

**Risk:** Command injection through MairuCLI itself

**Mitigation:**
- MairuCLI only analyzes commands, doesn't modify them
- Pass-through commands executed via `subprocess.run(shell=True)`
- No string interpolation of user input into shell commands
- Pattern matching is read-only operation

### Pattern Database Integrity

**Risk:** Malicious patterns causing ReDoS (Regular Expression Denial of Service)

**Mitigation:**
- Patterns are hardcoded in MVP (trusted source)
- Future: Validate patterns before loading from JSON
- Timeout on pattern matching (50ms limit)

### Privacy

**Risk:** Command logging exposes sensitive data

**Mitigation:**
- MVP does not log commands
- Future: If logging added, must be opt-in and local only

---

## Known Limitations (MVP Scope)

### ⚠️ Critical Limitations

**MairuCLI is an educational tool, NOT a production security solution.**

#### 1. Command Chaining Bypass 🚨

**Problem:** Dangerous commands can bypass detection using shell operators.

**Examples:**
```bash
rm -rf / | grep important  # Pipe bypass
rm -rf / && echo "done"    # AND operator bypass
rm -rf / ; ls              # Semicolon bypass
rm -rf / || echo "failed"  # OR operator bypass
```

**Why This Happens:**
- Current pattern matching checks the full command string
- Shell operators are not parsed separately
- `subprocess.run(shell=True)` executes the entire chain

**Impact:**
- Users can accidentally or intentionally bypass warnings
- MairuCLI cannot guarantee 100% protection

**Mitigation (Future):**
- Parse command into tokens before pattern matching
- Detect shell operators and warn user
- Implement in Phase 4 if time permits (2-3 hours)

#### 2. Shell Injection Risk 🔓

**Problem:** `subprocess.run(shell=True)` is inherently risky.

**Why:**
- Allows arbitrary shell command execution
- Environment variable expansion
- Command substitution (`$(...)`, `` `...` ``)

**Example Risk:**
```bash
# If MairuCLI itself had a bug allowing user input into subprocess:
subprocess.run(f"echo {user_input}", shell=True)  # DANGEROUS
```

**Current Mitigation:**
- MairuCLI passes user commands directly without modification
- No string interpolation of user input
- Risk is limited to what user explicitly types

**Why We Accept This Risk:**
- Alternative (`shell=False`) breaks pipes, redirects, globs
- MairuCLI is educational, not a security boundary
- Users are already in a shell - MairuCLI adds warnings, not security

**Better Alternative (Not Implemented in MVP):**
```python
import shlex
args = shlex.split(command)
subprocess.run(args, shell=False)  # Safer but limited functionality
```

#### 3. Incomplete Pattern Coverage

**Problem:** Only 5 dangerous patterns implemented in MVP.

**Missing Patterns:**
- `git push -f` (force push)
- `iptables -F` (flush firewall)
- `kill -9 -1` (kill all processes)
- `mkfs` (format filesystem)
- Many others from CLI_Troubled.md

**Why:**
- 40-hour time constraint
- Focus on most common/critical patterns
- Extensible design allows future additions

#### 4. Variable Expansion Not Evaluated

**Problem:** Cannot detect if variable contains dangerous path.

**Example:**
```bash
DIR=""
rm -rf $DIR/  # Expands to rm -rf / but MairuCLI sees $DIR
```

**Why:**
- Would require shell environment simulation
- Complex to implement correctly
- Out of scope for MVP

### 📋 Documented Limitations for Users

**These limitations will be clearly stated in:**
1. README.md - "Limitations" section
2. Welcome banner - Brief disclaimer
3. Demo video - Honest disclosure
4. Submission materials - Technical limitations section

**Example README Section:**
```markdown
## ⚠️ Important Limitations

MairuCLI is an **educational tool** designed to teach CLI safety through
entertainment. It is NOT a replacement for:

- Proper access controls and permissions
- Regular backups
- Production-grade security tools
- Careful command review before execution

### Known Issues

1. **Command chaining bypass**: `rm -rf / && ls` will not be caught
2. **Limited pattern coverage**: Only 5 critical patterns in MVP
3. **Variable expansion**: Cannot evaluate `$VAR` contents
4. **Educational purpose only**: Do not rely on this for actual security

For production environments, use proper security practices and tools.
```

### 🔧 Optional Improvements (If Time Permits)

**Priority 1: Command Chaining Detection (2-3 hours)**
```python
def check_command_with_chaining(command: str) -> Tuple[bool, str]:
    """Enhanced check that detects shell operators."""
    # Check if command contains dangerous patterns
    for pattern_name, pattern_data in DANGEROUS_PATTERNS.items():
        if re.search(pattern_data["pattern"], command, re.IGNORECASE):
            # Warn if chaining detected
            if any(op in command for op in ["|", ";", "&&", "||"]):
                print("⚠️  Command chaining detected!")
                print("   MairuCLI cannot fully analyze chained commands.")
                print("   Blocking for safety.")
            return True, pattern_name
    return False, ""
```

**Priority 2: Safer Subprocess (5-8 hours, likely skip)**
- Implement `shlex` parsing
- Handle pipes/redirects manually
- Trade-off: Significant complexity for marginal security gain

**Decision:** Implement Priority 1 only if >5 hours remain after Phase 4

---

## Future Enhancements (Post-MVP)

### Phase 2 Features (If Time Permits)

1. **More Patterns:**
   - Git force push
   - iptables flush
   - kill -9 -1

2. **Enhanced ASCII Art:**
   - Animated ASCII (frame-by-frame)
   - More variations per category

3. **Configuration File:**
   - JSON config in `~/.mairurc`
   - Custom color schemes
   - Enable/disable specific patterns

### Long-Term Roadmap

1. **Community Patterns:**
   - JSON pattern database
   - User-submitted patterns
   - Pattern voting system

2. **Advanced Features:**
   - Command history with statistics
   - Learning mode (track which mistakes user makes)
   - Integration with shell history

3. **Cross-Platform:**
   - Windows support (PowerShell)
   - Fish shell support
   - Zsh plugin

4. **Localization:**
   - Japanese messages
   - Multi-language support

---

## Appendix

### ASCII Art Specifications

**File Format:**
- Plain text, UTF-8 encoding
- Maximum width: 80 characters
- No ANSI codes in file (colors applied at runtime)

**Example (`fired.txt`):**

```
        🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥
       🔥                         🔥
      🔥   YOU'RE FIRED!          🔥
     🔥                           🔥
    🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥
         ||           ||
         ||           ||
        /  \         /  \
```

### Color Testing Matrix

| Terminal | Light Theme | Dark Theme | Notes |
|----------|-------------|------------|-------|
| macOS Terminal | ❌ Skip | ✅ Test | Primary target |
| iTerm2 | ❌ Skip | ✅ Test | Popular on macOS |
| GNOME Terminal | ❌ Skip | ✅ Test | Linux default |
| Windows Terminal | ❌ Skip | ⚠️ Optional | WSL support |

### Dependencies

**Required:**
- Python 3.8+
- No external packages (stdlib only for MVP)

**Optional (Future):**
- `colorama` - Better Windows color support
- `prompt_toolkit` - Enhanced REPL
- `pyyaml` - YAML config support

---

## Design Review Checklist

- [x] Architecture diagram clear and complete
- [x] All MVP requirements addressed
- [x] Component responsibilities well-defined
- [x] Data structures documented
- [x] Implementation phases defined
- [x] Testing strategy outlined
- [x] Performance targets specified
- [x] Error handling considered
- [x] Security risks assessed
- [x] Future enhancements documented

---

**Design Approved By:** [Pending Developer Approval]
**Date:** 2025-11-16
**Next Step:** Create tasks.md with detailed implementation tasks
