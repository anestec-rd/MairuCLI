# Design Document: Data-Driven Pattern Configuration

## Overview

This design eliminates the duplication between `src/interceptor.py` and `data/warnings/warning_catalog.json` by establishing JSON files as the single source of truth for all pattern configuration. The interceptor will load pattern definitions (including regex patterns) from JSON files at startup, removing the need to maintain pattern information in two places.

### Design Goals

1. **Single Source of Truth**: All pattern information exists only in JSON files
2. **Data-Driven**: Pattern detection logic reads from configuration, not hardcoded dictionaries
3. **Backward Compatibility**: Existing detection behavior and performance remain unchanged
4. **Maintainability**: Adding new patterns requires only JSON changes
5. **Validation**: JSON structure is validated on load with clear error messages

## Architecture

### Current Architecture (Problem)

```
┌─────────────────────────────────────────────────────────┐
│ src/interceptor.py                                      │
│                                                         │
│ DANGEROUS_PATTERNS = {                                 │
│   "rm_dangerous": {                                    │
│     "pattern": r"rm\s+(-rf|-fr)...",  ← Regex here   │
│     "category": "deletion",            ← Duplicate    │
│     "severity": "critical",            ← Duplicate    │
│     "art_file": "fired.txt"            ← Duplicate    │
│   }                                                    │
│ }                                                      │
└─────────────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────────────┐
│ data/warnings/warning_catalog.json                      │
│                                                         │
│ "rm_dangerous": {                                      │
│   "category": "deletion",              ← Duplicate    │
│   "severity": "critical",              ← Duplicate    │
│   "ascii_art": "fired.txt",            ← Duplicate    │
│   "explanation": "...",                                │
│   "advice": [...]                                      │
│ }                                                      │
└─────────────────────────────────────────────────────────┘
```

### New Architecture (Solution)

```
┌─────────────────────────────────────────────────────────┐
│ data/warnings/warning_catalog.json                      │
│ (Single Source of Truth)                                │
│                                                         │
│ "rm_dangerous": {                                      │
│   "pattern": "rm\\s+(-rf|-fr)...",     ← Regex here   │
│   "category": "deletion",                              │
│   "severity": "critical",                              │
│   "ascii_art": "fired.txt",                            │
│   "explanation": "...",                                │
│   "advice": [...]                                      │
│ }                                                      │
└─────────────────────────────────────────────────────────┘
                    ↓ Load at startup
┌─────────────────────────────────────────────────────────┐
│ src/interceptor.py                                      │
│                                                         │
│ class PatternMatcher:                                  │
│   def __init__(self):                                  │
│     self.patterns = load_patterns_from_json()         │
│     self.compiled_patterns = compile_patterns()       │
│                                                         │
│   def check_command(self, cmd):                        │
│     # Use compiled patterns from JSON                  │
└─────────────────────────────────────────────────────────┘
```


## Components and Interfaces

### 1. Pattern Loader

```python
class PatternLoader:
    """Loads pattern definitions from JSON files."""

    def __init__(self, data_dir: Path):
        """Initialize with data directory path."""
        self.data_dir = data_dir
        self.dangerous_patterns = {}
        self.caution_patterns = {}
        self.typo_patterns = {}

    def load_all_patterns(self) -> None:
        """Load all pattern types from JSON files."""
        self.dangerous_patterns = self._load_dangerous_patterns()
        self.caution_patterns = self._load_caution_patterns()
        self.typo_patterns = self._load_typo_patterns()

    def _load_dangerous_patterns(self) -> Dict:
        """Load dangerous patterns from warning_catalog.json."""
        catalog_path = self.data_dir / "warnings" / "warning_catalog.json"
        with open(catalog_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data.get("warnings", {})

    def _load_caution_patterns(self) -> Dict:
        """Load caution patterns from caution_catalog.json."""
        catalog_path = self.data_dir / "warnings" / "caution_catalog.json"
        if not catalog_path.exists():
            return {}  # Fallback to empty if file doesn't exist
        with open(catalog_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data.get("cautions", {})

    def _load_typo_patterns(self) -> Dict:
        """Load typo patterns from typo_messages.json."""
        typo_path = self.data_dir / "warnings" / "typo_messages.json"
        if not typo_path.exists():
            return {}
        with open(typo_path, 'r', encoding='utf-8') as f:
            return json.load(f)
```

### 2. Pattern Compiler

```python
class PatternCompiler:
    """Compiles regex patterns for efficient matching."""

    def __init__(self):
        """Initialize compiler."""
        self.compiled_dangerous = {}
        self.compiled_caution = {}
        self.compiled_typo = {}

    def compile_patterns(
        self,
        dangerous: Dict,
        caution: Dict,
        typo: Dict
    ) -> None:
        """Compile all regex patterns."""
        self.compiled_dangerous = self._compile_pattern_dict(dangerous)
        self.compiled_caution = self._compile_pattern_dict(caution)
        self.compiled_typo = self._compile_pattern_dict(typo)

    def _compile_pattern_dict(self, patterns: Dict) -> Dict:
        """Compile patterns in a dictionary."""
        compiled = {}
        for name, data in patterns.items():
            try:
                pattern_str = data.get("pattern", "")
                if pattern_str:
                    compiled[name] = {
                        "regex": re.compile(pattern_str, re.IGNORECASE),
                        "data": data
                    }
            except re.error as e:
                print(f"Warning: Failed to compile pattern '{name}': {e}")
                # Skip invalid patterns
        return compiled
```


### 3. Refactored Interceptor

```python
# New interceptor.py structure

class CommandInterceptor:
    """Main interceptor class using data-driven patterns."""

    def __init__(self, data_dir: Path = Path("data")):
        """Initialize interceptor with pattern loading."""
        self.loader = PatternLoader(data_dir)
        self.compiler = PatternCompiler()
        self._load_and_compile_patterns()

    def _load_and_compile_patterns(self) -> None:
        """Load patterns from JSON and compile regex."""
        try:
            self.loader.load_all_patterns()
            self.compiler.compile_patterns(
                self.loader.dangerous_patterns,
                self.loader.caution_patterns,
                self.loader.typo_patterns
            )
        except Exception as e:
            print(f"Error loading patterns: {e}")
            # Fall back to empty patterns (fail-safe)

    def check_command(self, command: str) -> Tuple[str, str]:
        """Check command against all patterns."""
        # Check dangerous patterns first
        for name, compiled in self.compiler.compiled_dangerous.items():
            if compiled["regex"].search(command):
                return "critical", name

        # Check caution patterns
        for name, compiled in self.compiler.compiled_caution.items():
            if compiled["regex"].search(command):
                return "caution", name

        # Check typo patterns
        for name, compiled in self.compiler.compiled_typo.items():
            if compiled["regex"].search(command):
                return "critical", f"typo_{name}"

        # Check generic typos
        is_typo, correct_cmd, message = check_generic_typo(command)
        if is_typo:
            return "critical", f"typo_generic_{command.split()[0]}"

        return "safe", ""

    def get_pattern_info(self, pattern_name: str) -> Dict:
        """Get pattern information for display."""
        if pattern_name.startswith("typo_"):
            typo_name = pattern_name.replace("typo_", "").replace("generic_", "")
            return self.loader.typo_patterns.get(typo_name, {})
        elif pattern_name in self.loader.dangerous_patterns:
            return self.loader.dangerous_patterns[pattern_name]
        elif pattern_name in self.loader.caution_patterns:
            return self.loader.caution_patterns[pattern_name]
        return {}


# Module-level functions for backward compatibility
_interceptor = None

def _get_interceptor() -> CommandInterceptor:
    """Get or create singleton interceptor instance."""
    global _interceptor
    if _interceptor is None:
        _interceptor = CommandInterceptor()
    return _interceptor

def check_command(command: str) -> Tuple[str, str]:
    """Backward compatible check_command function."""
    return _get_interceptor().check_command(command)

def get_pattern_info(pattern_name: str) -> Dict[str, str]:
    """Backward compatible get_pattern_info function."""
    return _get_interceptor().get_pattern_info(pattern_name)
```


## Data Models

### Enhanced warning_catalog.json

```json
{
  "version": "1.2",
  "warnings": {
    "rm_dangerous": {
      "pattern": "rm\\s+(-rf|-fr|-r\\s+-f|-f\\s+-r)\\s+(/|~|\\$HOME|\\*|\\.(?:\\s|$)|\\$\\w+)",
      "category": "deletion",
      "severity": "critical",
      "variation_set": "rm_root",
      "ascii_art": "fired.txt",
      "color": "red",
      "emoji": "fire",
      "explanation": "This 'rm -rf' command targets critical system locations!",
      "consequence": "Could delete root (/), home (~), current dir (*), or variables.",
      "advice": [
        "Use 'rm -i' for interactive confirmation",
        "Always specify exact file/folder names",
        "Use 'trash-cli' instead of rm for safety"
      ],
      "timing": {
        "art_delay": 0.05,
        "pause_after_art": 0.3,
        "pause_before_explanation": 0.5,
        "pause_before_achievement": 0.3
      }
    },
    "chmod_777": {
      "pattern": "chmod\\s+(-R\\s+)?777",
      "category": "permission",
      "severity": "high",
      "variation_set": "chmod_777",
      "ascii_art": "permission_denied.txt",
      "color": "purple",
      "emoji": "skull",
      "explanation": "chmod 777 gives EVERYONE full access to your files.",
      "consequence": "This is a major security risk!",
      "advice": [
        "Use specific permissions like 'chmod 755' or 'chmod 644'",
        "Only give write access when necessary"
      ],
      "timing": {
        "art_delay": 0.05,
        "pause_after_art": 0.3,
        "pause_before_explanation": 0.5,
        "pause_before_achievement": 0.3
      }
    }
  }
}
```

### New caution_catalog.json

```json
{
  "version": "1.0",
  "cautions": {
    "sudo_shell": {
      "pattern": "sudo\\s+(su|bash|sh|-i)(?:\\s|$)",
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
      "pattern": "chmod\\s+(-R\\s+)?(666|755|775)",
      "category": "permissions",
      "severity": "medium",
      "risk": "Making files readable/writable by others",
      "impact": "Potential security vulnerability or data exposure",
      "considerations": [
        "Who needs access to this file?",
        "Is 644 (read-only for others) sufficient?",
        "Are you setting permissions on sensitive data?"
      ]
    }
  }
}
```

### Enhanced typo_messages.json

```json
{
  "sl": {
    "pattern": "^sl$",
    "correct": "ls",
    "message": "🚂 Choo choo! All aboard the typo train!",
    "ascii_art": "steam_locomotive.txt"
  },
  "gti": {
    "pattern": "^gti\\b",
    "correct": "git",
    "message": "🚗 GTI? That's a car! You meant 'git', right?",
    "ascii_art": null
  },
  "cd_stuck": {
    "pattern": "^cd\\.\\.$",
    "correct": "cd ..",
    "message": "🎃 Stuck together? Let me help you separate!",
    "ascii_art": null
  }
}
```


## Migration Strategy

### Phase 1: Add Pattern Field to JSON (Non-Breaking)

1. Add `"pattern"` field to all entries in `warning_catalog.json`
2. Keep existing `interceptor.py` unchanged
3. Validate that JSON is valid and patterns compile
4. No functional changes yet

**Example:**
```json
"rm_dangerous": {
  "pattern": "rm\\s+(-rf|-fr)...",  // ← Add this field
  "category": "deletion",
  "severity": "critical",
  // ... existing fields
}
```

### Phase 2: Create New Pattern Loading Classes

1. Implement `PatternLoader` class
2. Implement `PatternCompiler` class
3. Write unit tests for both classes
4. No changes to existing code yet

### Phase 3: Create caution_catalog.json

1. Extract `CAUTION_PATTERNS` from `interceptor.py` to new JSON file
2. Add `"pattern"` field to each entry
3. Validate JSON structure

### Phase 4: Refactor Interceptor (Breaking Change)

1. Create `CommandInterceptor` class
2. Update module-level functions to use new class
3. Remove hardcoded `DANGEROUS_PATTERNS`, `CAUTION_PATTERNS`, `TYPO_PATTERNS`
4. Run all tests to ensure backward compatibility

### Phase 5: Cleanup

1. Remove old pattern dictionaries from `interceptor.py`
2. Update documentation
3. Add migration notes to CHANGELOG.md

### Phase 6: Validation (Optional)

1. Add JSON schema validation
2. Create validation script to check JSON files
3. Add pre-commit hook for JSON validation


## Error Handling

### Pattern Loading Errors

1. **Missing JSON file**: Log warning and use empty pattern dict (fail-safe)
2. **Invalid JSON syntax**: Log error with line number, use empty patterns
3. **Missing pattern field**: Skip that pattern, log warning
4. **Invalid regex pattern**: Skip that pattern, log compilation error

### Runtime Errors

1. **Pattern matching errors**: Catch exceptions, treat as non-match
2. **Missing pattern info**: Return empty dict, let display handle gracefully

### Graceful Degradation

```python
def _load_dangerous_patterns(self) -> Dict:
    """Load dangerous patterns with error handling."""
    try:
        catalog_path = self.data_dir / "warnings" / "warning_catalog.json"
        with open(catalog_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data.get("warnings", {})
    except FileNotFoundError:
        print(f"Warning: {catalog_path} not found. Using empty patterns.")
        return {}
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {catalog_path}: {e}")
        return {}
    except Exception as e:
        print(f"Error loading patterns: {e}")
        return {}
```

## Performance Considerations

### Startup Performance

- **Pattern Loading**: ~10-20ms for all JSON files
- **Regex Compilation**: ~5-10ms for all patterns
- **Total Startup Overhead**: ~15-30ms (acceptable)

### Runtime Performance

- **Pattern Matching**: Same as before (compiled regex)
- **Memory Usage**: Slightly higher (JSON data + compiled patterns)
- **No Performance Regression**: Matching speed unchanged

### Optimization Strategies

1. **Lazy Loading**: Load patterns only when first needed
2. **Caching**: Keep compiled patterns in memory
3. **Pattern Ordering**: Check most common patterns first

## Testing Strategy

### Unit Tests

1. **PatternLoader**
   - Test loading valid JSON files
   - Test handling missing files
   - Test handling invalid JSON
   - Test handling missing pattern fields

2. **PatternCompiler**
   - Test compiling valid regex patterns
   - Test handling invalid regex
   - Test pattern matching after compilation

3. **CommandInterceptor**
   - Test pattern detection with JSON-loaded patterns
   - Test backward compatibility with existing tests
   - Test error handling

### Integration Tests

1. Test complete flow: JSON → Load → Compile → Match
2. Test all existing dangerous patterns still work
3. Test all existing caution patterns still work
4. Test all existing typo patterns still work

### Migration Tests

1. Compare detection results before and after migration
2. Verify no patterns are lost during migration
3. Verify performance is maintained


## Backward Compatibility

### Maintained APIs

All existing functions maintain their signatures:

```python
# These remain unchanged
def check_command(command: str) -> Tuple[str, str]:
    """Check if command matches any pattern."""

def get_pattern_info(pattern_name: str) -> Dict[str, str]:
    """Retrieve pattern information for display."""

def check_system_directory(command: str) -> Tuple[str, str, str]:
    """Check if command targets protected directories."""
```

### Internal Changes Only

- Pattern dictionaries replaced with JSON loading
- Pattern matching logic unchanged
- External code (main.py, display.py) requires no changes

### Migration Path for External Code

**No changes required!** The refactoring is internal to `interceptor.py`.

## JSON Schema (Optional Validation)

### warning_catalog.json Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["version", "warnings"],
  "properties": {
    "version": {
      "type": "string"
    },
    "warnings": {
      "type": "object",
      "patternProperties": {
        "^[a-z_]+$": {
          "type": "object",
          "required": ["pattern", "category", "severity"],
          "properties": {
            "pattern": {
              "type": "string",
              "description": "Regular expression pattern"
            },
            "category": {
              "type": "string",
              "enum": ["deletion", "permission", "disk", "database", "system"]
            },
            "severity": {
              "type": "string",
              "enum": ["critical", "high", "medium", "low"]
            },
            "variation_set": {
              "type": "string"
            },
            "ascii_art": {
              "type": "string"
            },
            "color": {
              "type": "string"
            },
            "emoji": {
              "type": "string"
            },
            "explanation": {
              "type": "string"
            },
            "consequence": {
              "type": "string"
            },
            "advice": {
              "type": "array",
              "items": {
                "type": "string"
              }
            },
            "timing": {
              "type": "object",
              "properties": {
                "art_delay": {
                  "type": "number"
                },
                "pause_after_art": {
                  "type": "number"
                },
                "pause_before_explanation": {
                  "type": "number"
                },
                "pause_before_achievement": {
                  "type": "number"
                }
              }
            }
          }
        }
      }
    }
  }
}
```


## Implementation Notes

### Regex Pattern Escaping in JSON

When moving regex patterns from Python to JSON, double-escape backslashes:

**Python:**
```python
"pattern": r"rm\s+(-rf|-fr)"
```

**JSON:**
```json
"pattern": "rm\\s+(-rf|-fr)"
```

### Pattern Compilation Caching

Compile patterns once at startup and reuse:

```python
# Good: Compile once
self.compiled_patterns = {
    name: re.compile(data["pattern"], re.IGNORECASE)
    for name, data in patterns.items()
}

# Bad: Compile every time
for name, data in patterns.items():
    if re.search(data["pattern"], command):  # Compiles every call!
        return name
```

### File Organization

```
data/
└── warnings/
    ├── warning_catalog.json      # Dangerous patterns (with regex)
    ├── caution_catalog.json      # Caution patterns (with regex)
    ├── typo_messages.json        # Typo patterns (with regex)
    ├── danger_variations.json    # Display variations (no change)
    ├── category_variations.json  # Category variations (no change)
    └── pattern_variations.json   # Pattern variations (no change)
```

## Benefits

### For Developers

1. **Single Source of Truth**: Update patterns in one place
2. **No Code Changes**: Add patterns by editing JSON
3. **Easy Testing**: Validate JSON structure independently
4. **Clear Separation**: Pattern detection vs. display logic

### For Maintainability

1. **Reduced Duplication**: No more sync issues between files
2. **Data-Driven**: Non-developers can contribute patterns
3. **Validation**: JSON schema catches errors early
4. **Extensibility**: Easy to add new pattern types

### For Performance

1. **No Regression**: Same compiled regex performance
2. **Startup Cost**: Minimal (~15-30ms)
3. **Runtime Cost**: Zero (patterns pre-compiled)

## Future Enhancements

### Hot Reload (Phase 2)

```python
def reload_patterns(self) -> None:
    """Reload patterns from JSON without restart."""
    self._load_and_compile_patterns()
    print("Patterns reloaded successfully")
```

### Pattern Validation Tool

```bash
# Validate all JSON pattern files
python -m src.tools.validate_patterns

# Output:
# ✓ warning_catalog.json: 13 patterns valid
# ✓ caution_catalog.json: 7 patterns valid
# ✓ typo_messages.json: 6 patterns valid
# ✗ Error in warning_catalog.json: Invalid regex in 'rm_dangerous'
```

### Pattern Testing Tool

```bash
# Test pattern matching
python -m src.tools.test_pattern "rm -rf /"

# Output:
# Pattern matched: rm_dangerous
# Level: critical
# Category: deletion
# Severity: critical
```

## Summary

This design eliminates duplication by:
1. Adding `"pattern"` field to JSON files
2. Loading patterns from JSON at startup
3. Removing hardcoded pattern dictionaries from Python
4. Maintaining backward compatibility throughout

The result is a cleaner, more maintainable codebase where JSON files are the single source of truth for all pattern configuration.


## Help Command Auto-Generation

### Current Problem

The help command in `src/builtins/mairu_commands.py` has a hardcoded list of dangerous commands:

```python
print(f"  {EMOJI['fire']} rm -rf /        - Deletes EVERYTHING")
print(f"  {EMOJI['unlock']} chmod 777 file  - Makes files world-writable")
# ... more hardcoded entries
```

**Issues:**
1. Duplication with `warning_catalog.json`
2. Missing patterns (e.g., `mv_to_null` not shown)
3. Manual updates required when adding new patterns
4. Inconsistent descriptions

### Solution: Dynamic Help Generation

```python
class HelpGenerator:
    """Generates help command output from JSON patterns."""

    def __init__(self, pattern_loader: PatternLoader):
        """Initialize with pattern loader."""
        self.loader = pattern_loader

    def generate_dangerous_commands_help(self) -> str:
        """Generate dangerous commands section for help."""
        lines = []
        lines.append(colorize("💀 Dangerous Commands (DON'T try these!):", "red"))

        # Group patterns by category
        by_category = self._group_by_category(
            self.loader.dangerous_patterns
        )

        # Display each pattern
        for category in ["deletion", "permission", "disk", "database", "system"]:
            if category in by_category:
                for pattern_name, data in by_category[category].items():
                    emoji = EMOJI.get(data.get("emoji", "fire"), "🔥")
                    cmd_example = data.get("help_example", pattern_name)
                    description = data.get("help_description",
                                         data.get("explanation", "")[:50])
                    lines.append(f"  {emoji} {cmd_example:20} - {description}")

        return "\n".join(lines)

    def generate_caution_commands_help(self) -> str:
        """Generate caution commands section for help."""
        lines = []
        lines.append(colorize("⚠️  Caution Commands (Think twice!):", "orange"))

        for pattern_name, data in self.loader.caution_patterns.items():
            emoji = EMOJI.get("warning", "⚠️")
            cmd_example = data.get("help_example", pattern_name)
            description = data.get("help_description",
                                 data.get("risk", "")[:50])
            lines.append(f"  {emoji} {cmd_example:20} - {description}")

        return "\n".join(lines)

    def _group_by_category(self, patterns: Dict) -> Dict:
        """Group patterns by category."""
        grouped = {}
        for name, data in patterns.items():
            category = data.get("category", "other")
            if category not in grouped:
                grouped[category] = {}
            grouped[category][name] = data
        return grouped
```

### Enhanced JSON Structure

Add `help_example` and `help_description` fields to patterns:

```json
{
  "rm_dangerous": {
    "pattern": "rm\\s+(-rf|-fr)...",
    "category": "deletion",
    "severity": "critical",
    "emoji": "fire",
    "help_example": "rm -rf /",
    "help_description": "Deletes EVERYTHING (seriously, don't)",
    "explanation": "This 'rm -rf' command targets critical system locations!",
    ...
  },
  "mv_to_null": {
    "pattern": "mv\\s+.+\\s+/dev/null",
    "category": "deletion",
    "severity": "high",
    "emoji": "void",
    "help_example": "mv file /dev/null",
    "help_description": "Sends files to the void (unrecoverable)",
    "explanation": "Moving files to /dev/null makes them disappear forever!",
    ...
  }
}
```

### Integration with Help Command

```python
# In src/builtins/mairu_commands.py

def help_command() -> None:
    """Display help information."""
    # ... existing code ...

    # Load patterns and generate help dynamically
    from src.interceptor import _get_interceptor
    interceptor = _get_interceptor()
    help_gen = HelpGenerator(interceptor.loader)

    # Display dangerous commands (auto-generated)
    print(help_gen.generate_dangerous_commands_help())
    print()

    # Display caution commands (auto-generated)
    print(help_gen.generate_caution_commands_help())
    print()

    # ... rest of help ...
```

### Benefits

1. **Single Source of Truth**: Help content comes from JSON
2. **Automatic Updates**: New patterns appear in help automatically
3. **Consistency**: Same descriptions everywhere
4. **Completeness**: All patterns shown (no missing entries)
5. **Maintainability**: Add pattern once, appears everywhere

