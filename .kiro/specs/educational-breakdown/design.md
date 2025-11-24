# Design Document - Educational Breakdown Mode

## Overview

The Educational Breakdown Mode enhances MairuCLI's educational value by providing interactive, detailed explanations of dangerous commands. When users attempt dangerous or caution-level commands, the system offers three levels of explanation:

1. **Quick Explanation** (5 seconds) - Brief summary
2. **Full Breakdown** (20 seconds) - Command parts + simulation + incident
3. **Skip** - Return to prompt

This feature addresses two key educational gaps:
- Users don't understand command arguments (e.g., "What does -rf mean?")
- Users lack concrete understanding of consequences

The design follows MairuCLI's data-driven architecture, storing all educational content in JSON files for easy maintenance and scalability.

## Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         User Input                          │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                    Command Interceptor                      │
│              (Detects CRITICAL/CAUTION)                     │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                  Breakdown Mode Prompt                      │
│         [1] Quick  [2] Full  [3] Skip                       │
└─────────────────────┬───────────────────────────────────────┘
                      │
        ┌─────────────┼─────────────┐
        │             │             │
        ▼             ▼             ▼
    ┌───────┐   ┌─────────┐   ┌────────┐
    │ Quick │   │  Full   │   │  Skip  │
    └───┬───┘   └────┬────┘   └───┬────┘
        │            │             │
        │            ▼             │
        │    ┌──────────────┐     │
        │    │   Breakdown  │     │
        │    │   Simulation │     │
        │    │   Incident   │     │
        │    └──────┬───────┘     │
        │           │             │
        └───────────┴─────────────┘
                    │
                    ▼
            ┌───────────────┐
            │ Return Prompt │
            └───────────────┘
```

### Component Architecture

```
src/
├── display/
│   ├── educational_breakdown.py    # NEW: Main breakdown display
│   ├── breakdown_formatter.py      # NEW: Format breakdown content
│   └── educational_loader.py       # NEW: Load educational JSON
│
data/
└── educational/                     # NEW: Educational content
    ├── command_breakdowns/
    │   ├── rm_dangerous.json
    │   ├── chmod_777.json
    │   └── ...
    ├── simulations/
    │   ├── rm_dangerous.json
    │   ├── chmod_777.json
    │   └── ...
    └── incidents/
        ├── gitlab_2017.json
        └── ...
```

## Components and Interfaces

### 1. EducationalBreakdown (Main Component)

**Purpose:** Orchestrate the breakdown mode experience

**Interface:**
```python
class EducationalBreakdown:
    def __init__(self, loader: EducationalLoader, formatter: BreakdownFormatter):
        """Initialize with loader and formatter."""

    def show_breakdown_prompt(self, pattern_name: str) -> str:
        """
        Show breakdown mode options and get user choice.

        Args:
            pattern_name: Name of the detected pattern

        Returns:
            User choice: "quick", "full", or "skip"
        """

    def show_quick_explanation(self, pattern_name: str) -> None:
        """
        Display 5-second quick explanation.

        Args:
            pattern_name: Name of the detected pattern
        """

    def show_full_breakdown(self, pattern_name: str) -> None:
        """
        Display full breakdown with all components.

        Args:
            pattern_name: Name of the detected pattern

        Components shown:
        1. Command breakdown
        2. Timeline simulation
        3. Incident story (if available)
        """
```

### 2. EducationalLoader (Content Loader)

**Purpose:** Load educational content from JSON files

**Interface:**
```python
class EducationalLoader:
    def __init__(self, base_path: str = "data/educational"):
        """Initialize with base path to educational content."""

    def load_breakdown(self, pattern_name: str) -> Optional[Dict]:
        """
        Load command breakdown for pattern.

        Args:
            pattern_name: Name of the pattern

        Returns:
            Breakdown data or None if not found
        """

    def load_simulation(self, pattern_name: str) -> Optional[Dict]:
        """
        Load timeline simulation for pattern.

        Args:
            pattern_name: Name of the pattern

        Returns:
            Simulation data or None if not found
        """

    def load_incident(self, incident_id: str) -> Optional[Dict]:
        """
        Load incident story by ID.

        Args:
            incident_id: Incident identifier (e.g., "gitlab_2017")

        Returns:
            Incident data or None if not found
        """

    def get_related_incidents(self, pattern_name: str) -> List[str]:
        """
        Get list of incident IDs related to pattern.

        Args:
            pattern_name: Name of the pattern

        Returns:
            List of incident IDs
        """
```

### 3. BreakdownFormatter (Display Formatter)

**Purpose:** Format educational content for display

**Interface:**
```python
class BreakdownFormatter:
    def format_command_breakdown(self, breakdown_data: Dict) -> str:
        """
        Format command breakdown for display.

        Args:
            breakdown_data: Breakdown JSON data

        Returns:
            Formatted string with Halloween theme
        """

    def format_timeline_simulation(self, simulation_data: Dict) -> str:
        """
        Format timeline simulation for display.

        Args:
            simulation_data: Simulation JSON data

        Returns:
            Formatted timeline with emojis and timing
        """

    def format_incident_story(self, incident_data: Dict) -> str:
        """
        Format incident story for display.

        Args:
            incident_data: Incident JSON data

        Returns:
            Formatted story with Halloween framing
        """

    def format_quick_explanation(self, pattern_name: str) -> str:
        """
        Format quick 5-second explanation.

        Args:
            pattern_name: Name of the pattern

        Returns:
            Brief formatted explanation
        """
```

## Data Models

### Command Breakdown JSON Schema

**File:** `data/educational/command_breakdowns/{pattern_name}.json`

```json
{
  "pattern": "rm_dangerous",
  "command_parts": [
    {
      "part": "rm",
      "emoji": "🔪",
      "meaning": "Remove (delete forever)",
      "danger_level": "medium"
    },
    {
      "part": "-r",
      "emoji": "🌀",
      "meaning": "Recursive (go into ALL folders)",
      "danger_level": "high"
    },
    {
      "part": "-f",
      "emoji": "💪",
      "meaning": "Force (no questions asked, ignore errors)",
      "danger_level": "high"
    },
    {
      "part": "/",
      "emoji": "🌍",
      "meaning": "Root (the ENTIRE system)",
      "danger_level": "critical"
    }
  ],
  "translation": "Delete EVERYTHING, don't ask, ignore problems",
  "halloween_analogy": "Like opening all the doors in a haunted house at once! 🎃",
  "safe_alternatives": [
    "Use 'rm -i' for interactive confirmation",
    "Use 'trash-cli' for recoverable deletion"
  ]
}
```

### Timeline Simulation JSON Schema

**File:** `data/educational/simulations/{pattern_name}.json`

```json
{
  "pattern": "rm_dangerous",
  "timeline": [
    {
      "time": "T+0s",
      "emoji": "🎬",
      "event": "Starting deletion...",
      "severity": "info"
    },
    {
      "time": "T+1s",
      "emoji": "💀",
      "event": "/bin deleted (all commands gone)",
      "severity": "critical"
    },
    {
      "time": "T+15s",
      "emoji": "🖥️",
      "event": "System crashes",
      "severity": "fatal"
    },
    {
      "time": "T+∞",
      "emoji": "⚰️",
      "event": "Unbootable. Game Over.",
      "severity": "fatal"
    }
  ],
  "final_message": "Your computer is now a very expensive paperweight! 🎃"
}
```

### Incident Story JSON Schema

**File:** `data/educational/incidents/{incident_id}.json`

```json
{
  "id": "gitlab_2017",
  "title": "The Ghost of GitLab Past",
  "emoji": "🎃",
  "date": "2017-01-31",
  "company": "GitLab.com",
  "related_patterns": ["rm_dangerous"],
  "summary": {
    "what_happened": "Engineer accidentally ran rm command on production database",
    "intended_target": "db2 (replica server)",
    "actual_target": "db1 (production server)",
    "data_lost": "300GB reduced to 4.5GB",
    "time_lost": "6 hours of data",
    "downtime": "Several hours",
    "affected": "Thousands of users"
  },
  "timeline": [
    "📅 January 31, 2017",
    "🏢 GitLab.com (major dev platform)",
    "👤 Engineer working late, tired and frustrated",
    "💻 Meant to run command on db2 (replica)",
    "😱 Actually ran on db1 (PRODUCTION!)",
    "⏱️ Realized after 2 seconds, but too late",
    "💾 300GB → 4.5GB remaining",
    "🔥 6 hours of user data lost"
  ],
  "lesson": "Even experienced engineers make mistakes when tired. That's why MairuCLI exists! 🛡️",
  "source": {
    "title": "GitLab.com Database Incident",
    "url": "https://about.gitlab.com/blog/2017/02/01/gitlab-dot-com-database-incident/",
    "date": "2017-02-01"
  },
  "halloween_twist": "The scariest part? All their backups were haunted (broken)! 👻"
}
```

### chmod Story Mode JSON Schema

**File:** `data/educational/simulations/chmod_777_attack.json`

```json
{
  "pattern": "chmod_777",
  "story_mode": true,
  "title": "The Tale of the Unlocked Door",
  "chapters": [
    {
      "number": 1,
      "title": "The Careless Command",
      "emoji": "🔓",
      "content": [
        "You just tried: chmod 777 important.txt",
        "",
        "What does '777' mean?",
        "7 = Owner:   Read + Write + Execute",
        "7 = Group:   Read + Write + Execute",
        "7 = Others:  Read + Write + Execute",
        "",
        "Translation: EVERYONE can do ANYTHING! 🚨"
      ]
    },
    {
      "number": 2,
      "title": "The Midnight Visitor",
      "emoji": "🐺",
      "content": [
        "⏰ 2:00 AM - A hacker scans your system...",
        "🐺 'Oho! A file with 777 permissions!'",
        "📝 Hacker modifies important.txt",
        "🔒 Hacker runs: chmod 000 important.txt",
        "😈 'Good luck fixing that!'"
      ]
    },
    {
      "number": 3,
      "title": "The Morning Horror",
      "emoji": "☀️",
      "content": [
        "You: 'Let me fix that file...'",
        "💻 chmod 644 important.txt",
        "❌ Permission denied!",
        "😱 You can't even READ it anymore!",
        "🔒 The file is locked forever"
      ]
    },
    {
      "number": 4,
      "title": "The Lesson",
      "emoji": "🎓",
      "content": [
        "chmod 777 = Leaving your door unlocked",
        "chmod 000 = Door locked, you lost the key",
        "",
        "💡 Safe alternative:",
        "chmod 644 important.txt",
        "(You: read+write, Others: read-only)"
      ]
    }
  ]
}
```

## Error Handling

### Missing Content Files

**Strategy:** Graceful degradation

```python
def show_full_breakdown(self, pattern_name: str) -> None:
    """Show full breakdown with graceful fallback."""

    # Try to load breakdown
    breakdown = self.loader.load_breakdown(pattern_name)
    if breakdown:
        print(self.formatter.format_command_breakdown(breakdown))
    else:
        print("🎃 Command breakdown not available yet.")

    # Try to load simulation
    simulation = self.loader.load_simulation(pattern_name)
    if simulation:
        print(self.formatter.format_timeline_simulation(simulation))
    else:
        print("🎃 Simulation not available yet.")

    # Try to load incidents
    incidents = self.loader.get_related_incidents(pattern_name)
    if incidents:
        incident_data = self.loader.load_incident(incidents[0])
        if incident_data:
            print(self.formatter.format_incident_story(incident_data))
    else:
        print("🎃 No related incidents documented yet.")
```

### Malformed JSON

**Strategy:** Log error and skip content

```python
def load_breakdown(self, pattern_name: str) -> Optional[Dict]:
    """Load breakdown with error handling."""
    try:
        file_path = f"{self.base_path}/command_breakdowns/{pattern_name}.json"
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return None
    except json.JSONDecodeError as e:
        print(f"⚠️ Warning: Malformed JSON in {pattern_name}.json: {e}")
        return None
    except Exception as e:
        print(f"⚠️ Warning: Error loading {pattern_name}: {e}")
        return None
```

## Testing Strategy

### Unit Tests

**Test Coverage:**
1. `EducationalLoader` - File loading and error handling
2. `BreakdownFormatter` - Format output correctness
3. `EducationalBreakdown` - User interaction flow

**Example Tests:**
```python
def test_load_breakdown_success():
    """Test successful breakdown loading."""
    loader = EducationalLoader("test_data")
    breakdown = loader.load_breakdown("rm_dangerous")
    assert breakdown is not None
    assert breakdown["pattern"] == "rm_dangerous"
    assert len(breakdown["command_parts"]) > 0

def test_load_breakdown_missing_file():
    """Test graceful handling of missing file."""
    loader = EducationalLoader("test_data")
    breakdown = loader.load_breakdown("nonexistent")
    assert breakdown is None

def test_format_command_breakdown():
    """Test breakdown formatting."""
    formatter = BreakdownFormatter()
    breakdown_data = {
        "pattern": "rm_dangerous",
        "command_parts": [
            {"part": "rm", "emoji": "🔪", "meaning": "Remove"}
        ],
        "translation": "Delete everything"
    }
    output = formatter.format_command_breakdown(breakdown_data)
    assert "🔪" in output
    assert "rm" in output
    assert "Remove" in output
```

### Integration Tests

**Test Scenarios:**
1. Full breakdown flow (prompt → choice → display)
2. Quick explanation flow
3. Skip flow
4. Missing content graceful degradation

### Manual Tests

**Test Cases:**
1. Try `rm -rf /` → Select [2] Full → Verify all components display
2. Try `chmod 777 file` → Select [1] Quick → Verify 5-second summary
3. Try `dd if=/dev/zero` → Select [3] Skip → Verify immediate return
4. Try pattern with missing JSON → Verify graceful fallback messages

## Performance Considerations

### Content Caching

**Strategy:** Cache loaded JSON files in memory

```python
class EducationalLoader:
    def __init__(self, base_path: str = "data/educational"):
        self.base_path = base_path
        self._breakdown_cache: Dict[str, Dict] = {}
        self._simulation_cache: Dict[str, Dict] = {}
        self._incident_cache: Dict[str, Dict] = {}

    def load_breakdown(self, pattern_name: str) -> Optional[Dict]:
        """Load with caching."""
        if pattern_name in self._breakdown_cache:
            return self._breakdown_cache[pattern_name]

        breakdown = self._load_breakdown_from_file(pattern_name)
        if breakdown:
            self._breakdown_cache[pattern_name] = breakdown
        return breakdown
```

### Display Timing

**Requirements:**
- Breakdown prompt: < 50ms
- Content loading: < 100ms
- Full display: < 500ms total

## Integration Points

### Integration with Existing Warning System

**Modification to `main.py`:**

```python
# After dangerous command detected
if level == "critical" or level == "caution":
    # Show existing warning
    display_warning(pattern_name, command)

    # NEW: Offer breakdown mode
    breakdown = EducationalBreakdown(loader, formatter)
    choice = breakdown.show_breakdown_prompt(pattern_name)

    if choice == "quick":
        breakdown.show_quick_explanation(pattern_name)
    elif choice == "full":
        breakdown.show_full_breakdown(pattern_name)
    # else: skip, continue to prompt

    return  # Block command
```

### Integration with ContentLoader

**Reuse existing pattern:**
- Similar to `ContentLoader` for warnings
- Same JSON-based approach
- Same error handling strategy
- Consistent with MairuCLI architecture

## Scalability

### Adding New Content

**Process:**
1. Create JSON file in appropriate directory
2. Follow schema structure
3. No code changes required
4. Content automatically discovered

**Example: Adding new pattern**
```bash
# 1. Create breakdown
echo '{...}' > data/educational/command_breakdowns/new_pattern.json

# 2. Create simulation
echo '{...}' > data/educational/simulations/new_pattern.json

# 3. Done! System automatically loads it
```

### Content Growth

**Estimated file sizes:**
- Breakdown JSON: ~1-2 KB
- Simulation JSON: ~1-2 KB
- Incident JSON: ~2-3 KB
- Total per pattern: ~5 KB

**For 20 patterns:**
- Total size: ~100 KB
- Load time: < 10ms (cached)
- Memory usage: < 1 MB

## Halloween Theme Integration

### Visual Elements

**Emojis by context:**
- Danger levels: 🔪 (medium), 🔥 (high), 💀 (critical)
- Time: ⏱️, ⏰
- Events: 🎬 (start), 💥 (impact), ⚰️ (end)
- Characters: 🐺 (attacker), 👤 (user), 🎃 (system)

### Tone Guidelines

**Balance:**
- 70% Educational (facts, explanations, advice)
- 30% Entertainment (humor, analogies, Halloween theme)

**Examples:**
- ✅ "chmod 777 = Leaving your door unlocked 🔓"
- ✅ "The scariest part? All their backups were haunted! 👻"
- ❌ "You're an idiot for trying this" (too harsh)
- ❌ "This is very dangerous please don't" (too boring)

## Future Enhancements

### Phase 2 Features (Post-MVP)

1. **Interactive Quiz Mode**
   - Test understanding after breakdown
   - "What does -f mean?" → Multiple choice

2. **Progress Tracking**
   - Track which breakdowns user has seen
   - Unlock "Expert" achievement

3. **Custom Content**
   - Allow users to add their own incidents
   - Community-contributed stories

4. **Localization**
   - Japanese translations
   - Maintain Halloween theme across languages

## Summary

The Educational Breakdown Mode enhances MairuCLI's educational value through:

1. **Interactive Learning** - User chooses detail level
2. **Command Understanding** - Break down complex arguments
3. **Consequence Visualization** - Timeline simulations
4. **Real-World Context** - Verified incident stories
5. **Scalable Architecture** - JSON-based content management
6. **Halloween Theme** - Entertaining while educational

**Implementation Priority:**
1. Core components (Loader, Formatter, Breakdown)
2. Basic content (3-5 patterns)
3. Integration with warning system
4. Additional content (remaining patterns)
5. Polish and testing
