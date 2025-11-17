# Design Document: Display Module Refactoring

## Overview

This design refactors the monolithic `display.py` module into a modular, maintainable architecture. The refactoring separates concerns into focused components while maintaining backward compatibility and the existing Halloween-themed user experience.

### Design Goals

1. **Modularity**: Each component has a single, clear responsibility
2. **Maintainability**: New warnings/variations can be added without modifying existing code
3. **Data-Driven**: Content (messages, ASCII art) is managed through configuration files
4. **Backward Compatibility**: Existing API and behavior remain unchanged
5. **Extensibility**: Easy to add new warning types and display effects

## Architecture

### High-Level Structure

```
src/
├── display.py                    # Public API (facade pattern)
└── display/
    ├── __init__.py
    ├── ascii_renderer.py         # ASCII art loading and rendering
    ├── message_formatter.py      # Message template formatting
    ├── warning_components.py     # Warning display components
    ├── achievements.py           # Achievement tracking and display
    ├── statistics.py             # Statistics tracking
    └── content_loader.py         # Load content from data files

data/
├── warnings/
│   ├── warning_catalog.json     # Master catalog of all warnings
│   ├── danger_variations.json   # Dangerous command variations
│   └── typo_messages.json       # Typo message variations
└── ascii_art/
    ├── fired.txt
    ├── permission_denied.txt
    └── data_destroyer.txt
```

### Component Responsibilities

#### 1. display.py (Public API)
- Maintains existing function signatures for backward compatibility
- Delegates to appropriate internal components
- Acts as facade for the display system

#### 2. ascii_renderer.py
- Loads ASCII art files from disk
- Applies color schemes to ASCII art
- Handles dramatic timing effects (line-by-line display)
- Provides fallback for missing files

#### 3. message_formatter.py
- Defines message templates for different warning types
- Populates templates with dynamic content
- Applies color codes and emoji through template placeholders
- Validates template data

#### 4. warning_components.py
- Base warning component class
- Specific warning implementations (DangerWarning, TypoWarning, RepeatWarning)
- Strategy pattern for selecting warning variations
- Coordinates ASCII art, messages, and timing

#### 5. achievements.py
- Tracks achievement progress
- Checks for newly unlocked achievements
- Displays achievement notifications

#### 6. statistics.py
- Tracks command statistics (blocks, typos)
- Tracks repeat command attempts
- Provides statistics queries

#### 7. content_loader.py
- Loads warning catalog and variations from JSON files
- Validates content structure
- Provides content lookup by pattern name
- Handles missing/invalid content gracefully

## Components and Interfaces

### ASCII Renderer

```python
class AsciiRenderer:
    """Handles ASCII art loading and rendering."""

    def load_art(self, filename: str) -> str:
        """Load ASCII art from file with error handling."""

    def display_art(
        self,
        art: str,
        color: str,
        delay: float = 0.05
    ) -> None:
        """Display ASCII art with color and timing effects."""

    def display_art_slowly(
        self,
        art: str,
        color: str,
        delay: float = 0.05
    ) -> None:
        """Display ASCII art line by line with dramatic effect."""
```

### Message Formatter

```python
class MessageTemplate:
    """Represents a message template with placeholders."""

    def __init__(self, template: str, required_fields: List[str]):
        """Initialize template with structure and required fields."""

    def format(self, **kwargs) -> str:
        """Populate template with provided values."""

    def validate(self, **kwargs) -> bool:
        """Check if all required fields are provided."""


class MessageFormatter:
    """Formats warning messages using templates."""

    def format_danger_warning(
        self,
        title: str,
        subtitle: str,
        explanation: str,
        advice: str,
        command: str,
        emoji: str
    ) -> str:
        """Format a danger warning message."""

    def format_typo_warning(
        self,
        message: str,
        typed_command: str,
        correct_command: str
    ) -> str:
        """Format a typo warning message."""

    def format_repeat_warning(
        self,
        count: int,
        command: str
    ) -> str:
        """Format a repeat command warning message."""
```

### Warning Components

```python
class WarningComponent(ABC):
    """Base class for all warning components."""

    def __init__(
        self,
        ascii_renderer: AsciiRenderer,
        message_formatter: MessageFormatter
    ):
        """Initialize with required dependencies."""

    @abstractmethod
    def display(self, pattern_name: str, command: str) -> None:
        """Display the warning."""


class DangerWarning(WarningComponent):
    """Displays warnings for dangerous commands."""

    def __init__(
        self,
        ascii_renderer: AsciiRenderer,
        message_formatter: MessageFormatter,
        content_loader: ContentLoader
    ):
        """Initialize with dependencies and content loader."""

    def display(self, pattern_name: str, command: str) -> None:
        """Display danger warning with ASCII art and message."""
        # 1. Load content from catalog
        # 2. Select random variation
        # 3. Display ASCII art with timing
        # 4. Display formatted message
        # 5. Show safe alternatives


class TypoWarning(WarningComponent):
    """Displays warnings for typos."""

    def display(self, pattern_name: str, command: str) -> None:
        """Display typo warning with suggestion."""


class RepeatWarning(WarningComponent):
    """Displays escalating warnings for repeated commands."""

    def display(self, command: str, count: int) -> None:
        """Display repeat warning based on attempt count."""
```

### Content Loader

```python
class ContentLoader:
    """Loads and manages warning content from data files."""

    def __init__(self, data_dir: Path):
        """Initialize with data directory path."""

    def load_catalog(self) -> Dict:
        """Load the master warning catalog."""

    def get_warning_content(self, pattern_name: str) -> Dict:
        """Get warning content for a specific pattern."""

    def get_variations(self, category: str) -> List[Tuple[str, str]]:
        """Get all variations for a warning category."""

    def validate_content(self, content: Dict) -> bool:
        """Validate content structure."""
```

### Statistics and Achievements

```python
class Statistics:
    """Tracks command statistics."""

    def __init__(self):
        """Initialize statistics counters."""

    def increment_dangerous_blocked(self) -> None:
        """Increment dangerous command counter."""

    def increment_typos_caught(self) -> None:
        """Increment typo counter."""

    def track_repeat_command(self, command: str) -> int:
        """Track repeat command and return count."""

    def get_stats(self) -> Dict[str, int]:
        """Get current statistics."""


class AchievementTracker:
    """Tracks and displays achievements."""

    def __init__(self, statistics: Statistics):
        """Initialize with statistics dependency."""

    def check_achievements(self) -> None:
        """Check for newly unlocked achievements."""

    def show_achievement(self, title: str, description: str) -> None:
        """Display achievement notification."""
```

## Data Models

### Warning Catalog (warning_catalog.json)

```json
{
  "version": "1.0",
  "warnings": {
    "rm_root": {
      "category": "deletion",
      "severity": "critical",
      "variation_set": "rm_root",
      "ascii_art": "fired.txt",
      "color": "red",
      "emoji": "fire",
      "explanation": "The command 'rm -rf /' attempts to delete EVERYTHING.",
      "consequence": "This is unrecoverable without backups.",
      "advice": [
        "Use 'rm -i' for interactive confirmation",
        "Use 'trash-cli' instead of rm"
      ],
      "timing": {
        "art_delay": 0.05,
        "pause_after_art": 0.3,
        "pause_before_explanation": 0.5,
        "pause_before_achievement": 0.3
      }
    },
    "chmod_777": {
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

### Danger Variations (danger_variations.json)

```json
{
  "rm_root": [
    {
      "title": "YOU'RE FIRED!",
      "subtitle": "(And so is your entire filesystem!)"
    },
    {
      "title": "GAME OVER!",
      "subtitle": "(No continues, no save points)"
    },
    {
      "title": "NOPE. JUST NOPE.",
      "subtitle": "(Not today, Satan)"
    }
  ],
  "chmod_777": [
    {
      "title": "PERMISSION DENIED!",
      "subtitle": "(By your future self)"
    },
    {
      "title": "SECURITY BREACH ALERT!",
      "subtitle": "(This is how hacks happen)"
    }
  ],
  "data_destroyer": [
    {
      "title": "DATA DESTROYER DETECTED!",
      "subtitle": "(This will not end well)"
    },
    {
      "title": "DISK ANNIHILATOR!",
      "subtitle": "(Say goodbye to your data)"
    }
  ]
}
```

### Typo Messages (typo_messages.json)

```json
{
  "sl": {
    "message": "🚂 Choo choo! All aboard the typo train!",
    "correct": "ls",
    "ascii_art": "steam_locomotive.txt"
  },
  "cd_stuck": {
    "message": "🎃 Stuck together? Let me help you separate!",
    "correct": "cd ..",
    "ascii_art": null
  }
}
```

### Repeat Warning Messages (repeat_warnings.json)

```json
{
  "2": {
    "emoji": "eyes",
    "title": "Wait...",
    "lines": [
      "Haven't we been here before?",
      "",
      "I JUST warned you about this!",
      "Did you think I was joking?"
    ]
  },
  "3": {
    "emoji": "facepalm",
    "title": "Seriously?",
    "lines": [
      "I told you so...",
      "",
      "This is the THIRD time you've tried this!",
      "How about trying something different?"
    ]
  },
  "default": {
    "emoji": null,
    "title": "...",
    "lines": [
      "",
      "[Command log: '{command}' - Attempt #{count}]",
      "[No comment.]"
    ]
  }
}
```

## Error Handling

### Content Loading Errors

1. **Missing catalog file**: Use hardcoded fallback content
2. **Invalid JSON**: Log error and use fallback content
3. **Missing variation set**: Use generic warning message
4. **Missing ASCII art file**: Display placeholder text

### Runtime Errors

1. **Template formatting errors**: Log error and display plain text
2. **Color code errors**: Fall back to no-color display
3. **Timing errors**: Display without delays

### Graceful Degradation

The system should degrade gracefully:
- Missing content → Use fallbacks
- Invalid data → Log and continue
- File errors → Display text-only warnings
- Never crash the main CLI loop

## Testing Strategy

### Unit Tests

1. **AsciiRenderer**
   - Test file loading with valid/invalid paths
   - Test color application
   - Test timing effects

2. **MessageFormatter**
   - Test template population
   - Test field validation
   - Test color code insertion

3. **ContentLoader**
   - Test JSON loading and parsing
   - Test content validation
   - Test error handling for missing files

4. **Warning Components**
   - Test each warning type display
   - Test variation selection
   - Test integration with dependencies

5. **Statistics and Achievements**
   - Test counter increments
   - Test achievement triggers
   - Test repeat command tracking

### Integration Tests

1. Test complete warning display flow
2. Test backward compatibility with existing API
3. Test content reload without restart
4. Test error handling across components

### Manual Testing

1. Verify visual output matches original
2. Test timing effects feel natural
3. Verify colors display correctly on different terminals
4. Test with missing/corrupted data files

## Migration Strategy

### Phase 1: Create New Components (No Breaking Changes)

1. Create new directory structure
2. Implement all new components
3. Keep existing display.py unchanged
4. Write comprehensive tests for new components

### Phase 2: Create Data Files

1. Extract warning variations to JSON files
2. Create warning catalog
3. Validate all content loads correctly

### Phase 3: Refactor display.py (Maintain API)

1. Update display.py to use new components internally
2. Keep all existing function signatures
3. Ensure identical output
4. Run all existing tests

### Phase 4: Cleanup

1. Remove old code from display.py
2. Update documentation
3. Add migration notes to CHANGELOG.md

## Performance Considerations

### Loading Performance

- Load content files once at startup
- Cache loaded content in memory
- Lazy load ASCII art files only when needed

### Display Performance

- Timing delays are intentional (dramatic effect)
- File I/O should complete within 10ms
- Total warning display should complete within 2 seconds

### Memory Usage

- Content files should be < 100KB total
- In-memory cache should be < 1MB
- No memory leaks from repeated warnings

## Backward Compatibility

### Maintained APIs

All existing functions in display.py maintain their signatures:

```python
# These remain unchanged
def display_welcome_banner() -> None
def display_goodbye_message() -> None
def show_warning(pattern_name: str, command: str) -> None
def show_achievement(title: str, description: str) -> None
def get_stats() -> Dict[str, int]
def colorize(text: str, color_name: str) -> str
```

### Internal Changes Only

- All refactoring happens inside display/ subdirectory
- External code continues to import from display.py
- No changes required to main.py or interceptor.py

## Future Enhancements

### Potential Extensions

1. **Plugin System**: Allow third-party warning components
2. **Theme Support**: Multiple color schemes beyond Halloween
3. **Localization**: Multi-language support for messages
4. **Custom Variations**: User-defined warning messages
5. **Animation Effects**: More sophisticated ASCII art animations
6. **Sound Effects**: Optional audio warnings (if terminal supports)

### Configuration Options

Future config.json could include:

```json
{
  "display": {
    "theme": "halloween",
    "enable_colors": true,
    "enable_emoji": true,
    "enable_timing": true,
    "timing_speed": 1.0,
    "custom_variations_path": null
  }
}
```

## Dependencies

### New Dependencies

- None (uses only Python standard library)

### Internal Dependencies

```
display.py (facade)
  ├── display/ascii_renderer.py
  ├── display/message_formatter.py
  ├── display/warning_components.py
  │     ├── display/ascii_renderer.py
  │     ├── display/message_formatter.py
  │     └── display/content_loader.py
  ├── display/achievements.py
  │     └── display/statistics.py
  └── display/statistics.py
```

No circular dependencies allowed.

## Implementation Notes

### Code Style

- Follow existing MairuCLI standards
- Type hints for all functions
- Docstrings for all public methods
- Maximum line length: 100 characters

### File Organization

- Keep individual files under 300 lines
- One class per file (except small helper classes)
- Clear naming conventions
- Logical grouping of related functionality

### Documentation

- Update README.md with new architecture
- Document content file formats
- Provide examples for adding new warnings
- Include migration guide for contributors
