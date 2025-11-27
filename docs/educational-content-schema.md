# Educational Content JSON Schema

This document describes the JSON schema for educational content in MairuCLI's Educational Breakdown Mode.

## Overview

Educational content is stored in three types of JSON files:
1. **Command Breakdowns** - Explain what each part of a command means
2. **Timeline Simulations** - Show step-by-step consequences
3. **Incident Stories** - Real-world production disasters

All files are located in `data/educational/`.

---

## Command Breakdown Schema

**Location:** `data/educational/command_breakdowns/{pattern_name}.json`

### Structure

```json
{
  "command": "string",
  "quick_summary": "string",
  "parts": [
    {
      "part": "string",
      "emoji": "string",
      "meaning": "string",
      "danger_level": "string"
    }
  ],
  "translation": "string",
  "halloween_analogy": "string",
  "safe_alternatives": ["string"],
  "related_incidents": ["string"]
}
```

### Field Descriptions

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `command` | string | Yes | The full dangerous command (e.g., "rm -rf /") |
| `quick_summary` | string | Yes | 1-2 sentence summary for quick mode |
| `parts` | array | Yes | Array of command part objects |
| `parts[].part` | string | Yes | The command part (e.g., "rm", "-r", "-f", "/") |
| `parts[].emoji` | string | Yes | Emoji representing this part (e.g., "🗑️", "🔄") |
| `parts[].meaning` | string | Yes | Plain-language explanation |
| `parts[].danger_level` | string | Yes | Danger assessment (e.g., "Safe when used carefully", "CRITICAL") |
| `translation` | string | Yes | Plain-language translation of full command |
| `halloween_analogy` | string | Yes | Halloween-themed analogy for educational impact |
| `safe_alternatives` | array | Yes | List of safe alternative commands/practices |
| `related_incidents` | array | No | Array of incident IDs (references incidents/*.json) |

### Example

```json
{
  "command": "rm -rf /",
  "quick_summary": "Deletes EVERYTHING on your computer - all files, all programs, the operating system itself. Instant digital apocalypse.",
  "parts": [
    {
      "part": "rm",
      "emoji": "🗑️",
      "meaning": "Remove - deletes files and directories",
      "danger_level": "Safe when used carefully"
    },
    {
      "part": "-r",
      "emoji": "🔄",
      "meaning": "Recursive - goes into every folder and subfolder",
      "danger_level": "Dangerous - affects everything inside"
    },
    {
      "part": "-f",
      "emoji": "⚡",
      "meaning": "Force - no confirmation, no questions asked",
      "danger_level": "CRITICAL - removes safety checks"
    },
    {
      "part": "/",
      "emoji": "💀",
      "meaning": "Root directory - the top of your entire file system",
      "danger_level": "CATASTROPHIC - targets everything"
    }
  ],
  "translation": "Delete everything, recursively, without asking, starting from the root of the entire system.",
  "halloween_analogy": "It's like setting your entire house on fire, including the foundation, while you're still inside. No 'undo' button, no fire extinguisher, just... gone.",
  "safe_alternatives": [
    "rm -i filename - Interactive mode asks before each deletion",
    "rm -rf ./specific_folder - Only delete a specific folder",
    "trash-cli - Moves files to trash instead of permanent deletion",
    "Always double-check the path before pressing Enter!"
  ],
  "related_incidents": ["gitlab_2017"]
}
```

---

## Timeline Simulation Schema

**Location:** `data/educational/simulations/{pattern_name}.json`

### Structure

```json
{
  "pattern": "string",
  "timeline": [
    {
      "time": "string",
      "emoji": "string",
      "event": "string",
      "severity": "string"
    }
  ],
  "final_message": "string"
}
```

### Field Descriptions

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `pattern` | string | Yes | Pattern name matching the breakdown file |
| `timeline` | array | Yes | Array of timeline event objects |
| `timeline[].time` | string | Yes | Timestamp (e.g., "T+0s", "T+1s", "T+∞") |
| `timeline[].emoji` | string | Yes | Emoji representing the event |
| `timeline[].event` | string | Yes | Description of what happens |
| `timeline[].severity` | string | Yes | Severity level: "info", "warning", "critical", "fatal" |
| `final_message` | string | Yes | Halloween-themed summary message |

### Example

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
      "time": "T+2s",
      "emoji": "💀",
      "event": "/lib deleted (system libraries gone)",
      "severity": "critical"
    },
    {
      "time": "T+5s",
      "emoji": "🔥",
      "event": "/home deleted (all your files gone)",
      "severity": "fatal"
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

---

## Incident Story Schema

**Location:** `data/educational/incidents/{incident_id}.json`

### Structure

```json
{
  "id": "string",
  "title": "string",
  "emoji": "string",
  "date": "string",
  "company": "string",
  "related_patterns": ["string"],
  "summary": {
    "what_happened": "string",
    "intended_target": "string",
    "actual_target": "string",
    "data_lost": "string",
    "time_lost": "string",
    "downtime": "string",
    "affected": "string"
  },
  "timeline": ["string"],
  "lesson": "string",
  "source": {
    "title": "string",
    "url": "string",
    "date": "string"
  },
  "halloween_twist": "string"
}
```

### Field Descriptions

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | Yes | Unique incident identifier (e.g., "gitlab_2017") |
| `title` | string | Yes | Halloween-themed title |
| `emoji` | string | Yes | Emoji for the incident |
| `date` | string | Yes | Date of incident (YYYY-MM-DD) |
| `company` | string | Yes | Company/organization name |
| `related_patterns` | array | Yes | Array of pattern names this relates to |
| `summary` | object | Yes | Structured summary of the incident |
| `summary.what_happened` | string | Yes | Brief description |
| `summary.intended_target` | string | No | What they meant to target |
| `summary.actual_target` | string | No | What they actually hit |
| `summary.data_lost` | string | No | Amount of data lost |
| `summary.time_lost` | string | No | Time period of data lost |
| `summary.downtime` | string | No | Duration of downtime |
| `summary.affected` | string | No | Who/what was affected |
| `timeline` | array | Yes | Array of timeline strings (emoji + text) |
| `lesson` | string | Yes | Key lesson learned |
| `source` | object | Yes | Source information |
| `source.title` | string | Yes | Title of source document |
| `source.url` | string | Yes | URL to official source |
| `source.date` | string | Yes | Publication date |
| `halloween_twist` | string | Yes | Halloween-themed commentary |

### Example

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

---

## Adding New Educational Content

### Step 1: Create Command Breakdown

Create `data/educational/command_breakdowns/{pattern_name}.json`:

1. Use the schema above
2. Keep explanations concise (1 sentence per part)
3. Use appropriate emojis for danger level
4. Provide 2-3 safe alternatives
5. Link to related incidents if available

### Step 2: Create Timeline Simulation

Create `data/educational/simulations/{pattern_name}.json`:

1. Start with T+0s (beginning)
2. Show progressive damage (6-10 events)
3. Use appropriate severity levels
4. End with final summary message
5. Keep Halloween theme

### Step 3: Add Incident Story (Optional)

Create `data/educational/incidents/{incident_id}.json`:

1. Verify all facts before adding
2. Include official source URL
3. Balance facts with Halloween theme
4. Keep timeline to 8-12 key events
5. Add lesson learned

### Step 4: Test

```bash
python -m src.main
mairu> [trigger your pattern]
# Select [2] Full breakdown
# Verify all content displays correctly
```

---

## Content Guidelines

### Command Breakdowns
- Keep explanations concise (1 sentence per part)
- Use appropriate emojis for danger level
- Provide plain-language translation
- Include 2-3 safe alternatives

### Timeline Simulations
- Start with T+0s (beginning)
- Show progressive damage
- Use appropriate severity levels
- End with final summary message
- Keep total events to 6-10 for readability

### Incident Stories
- Verify all facts before adding
- Include official source URL
- Balance facts with Halloween theme
- Keep timeline to 8-12 key events
- Add lesson learned

### Halloween Theme
- Use appropriate emojis (🎃, 🔥, 💀, 👻, etc.)
- Balance education with humor
- Frame incidents as "spooky stories" while remaining factual
- Use analogies related to Halloween themes
- Maintain "Halloween Party" aesthetic (fun, not scary)

---

## Validation

Before committing new content:

1. **JSON Validity:** Ensure proper JSON syntax
2. **Schema Compliance:** All required fields present
3. **Content Quality:** Clear, educational, appropriate
4. **Source Verification:** URLs work, facts accurate
5. **Display Testing:** Content renders correctly
6. **Timing:** Feels natural (not too fast/slow)

---

## Current Coverage

### Patterns with Full Content
- ✅ rm_dangerous (rm -rf /)
- ✅ chmod_777
- ✅ chmod_000
- ✅ dd_zero
- ✅ fork_bomb

### Patterns Pending Content
- ⏳ redirect_to_disk
- ⏳ mkfs_disk
- ⏳ mv_to_null
- ⏳ overwrite_file
- ⏳ dd_random
- ⏳ kernel_panic

### Incidents Documented
- ✅ GitLab 2017 Database Incident

---

## Future Enhancements

1. **Localization:** Japanese translations
2. **Interactive Quiz:** Test understanding after breakdown
3. **Community Contributions:** User-submitted incidents
4. **Video Links:** Link to educational videos
5. **Difficulty Levels:** Beginner/Intermediate/Advanced explanations
6. **Related Commands:** Link to similar dangerous patterns

---

## References

- Design Document: `.kiro/specs/educational-breakdown/design.md`
- Requirements: `.kiro/specs/educational-breakdown/requirements.md`
- Implementation: `src/display/educational_breakdown.py`
- Content Loader: `src/display/educational_loader.py`
- Formatter: `src/display/breakdown_formatter.py`

---

**Last Updated:** 2025-11-27
