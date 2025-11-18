# Data-Driven Content Management

## Content Organization Philosophy

MairuCLI uses a data-driven approach where content (messages, variations, ASCII art) is stored in JSON files, not hardcoded in Python.

## When Adding New Content

### New Warning Messages

**ALWAYS add to JSON, NOT Python code:**

**❌ Wrong (Hardcoded):**
```python
# In warning_components.py
if pattern == "new_pattern":
    print("New warning message")
```

**✅ Correct (Data-Driven):**
```json
// In data/warnings/warning_catalog.json
{
  "new_pattern": {
    "category": "deletion",
    "severity": "high",
    "variation_set": "new_pattern",
    "ascii_art": "new_art.txt",
    ...
  }
}
```

### New Warning Variations

**Add to `data/warnings/danger_variations.json`:**

```json
{
  "new_pattern": [
    {
      "title": "WARNING TITLE!",
      "subtitle": "(Catchy subtitle)"
    },
    {
      "title": "ALTERNATIVE TITLE!",
      "subtitle": "(Different angle)"
    }
  ]
}
```

### New ASCII Art

1. Create file in `data/ascii_art/`
2. Reference in `warning_catalog.json`
3. Test rendering

### New Typo Patterns

**Add to `data/warnings/typo_messages.json`:**

```json
{
  "new_typo": {
    "message": "🎃 Fun message about the typo!",
    "correct": "correct_command",
    "ascii_art": null
  }
}
```

## Benefits of Data-Driven Approach

1. **No code changes** needed for content updates
2. **Easy to add variations** without touching Python
3. **Non-developers can contribute** content
4. **Testable** - validate JSON structure
5. **Maintainable** - clear separation of code and content

## File Locations

```
data/
├── warnings/
│   ├── warning_catalog.json     # Master catalog
│   ├── danger_variations.json   # Message variations
│   ├── typo_messages.json       # Typo messages
│   └── repeat_warnings.json     # Repeat warnings
└── ascii_art/
    ├── fired.txt
    ├── permission_denied.txt
    └── data_destroyer.txt
```

## Adding New Warning Pattern (Complete Flow)

### Step 1: Add Pattern Detection
```python
# In src/interceptor.py
DANGEROUS_PATTERNS = {
    "new_pattern": {
        "pattern": r"dangerous_regex",
        "category": "deletion",
        "severity": "high",
        "art_file": "new_art.txt"
    }
}
```

### Step 2: Add to Warning Catalog
```json
// In data/warnings/warning_catalog.json
{
  "new_pattern": {
    "category": "deletion",
    "severity": "high",
    "variation_set": "new_pattern",
    "ascii_art": "new_art.txt",
    "color": "red",
    "emoji": "fire",
    "explanation": "What this command does",
    "consequence": "Why it's dangerous",
    "advice": [
      "Safe alternative 1",
      "Safe alternative 2"
    ],
    "timing": {
      "art_delay": 0.05,
      "pause_after_art": 0.3,
      "pause_before_explanation": 0.5,
      "pause_before_achievement": 0.3
    }
  }
}
```

### Step 3: Add Variations
```json
// In data/warnings/danger_variations.json
{
  "new_pattern": [
    {"title": "TITLE 1!", "subtitle": "(Subtitle 1)"},
    {"title": "TITLE 2!", "subtitle": "(Subtitle 2)"},
    {"title": "TITLE 3!", "subtitle": "(Subtitle 3)"}
  ]
}
```

### Step 4: Add ASCII Art (Optional)
```
// In data/ascii_art/new_art.txt
    ___________
   /           \
  |   DANGER!   |
   \___________/
```

### Step 5: Test
```bash
python -m src.main
mairu> [trigger new pattern]
```

## Important Rules

1. **Content in JSON, logic in Python**
2. **One source of truth** - don't duplicate content
3. **Validate JSON** - ensure proper structure
4. **Test after adding** - verify it loads and displays
5. **Keep consistent** - follow existing patterns

## Validation

**Before committing new content:**
1. Ensure JSON is valid (no syntax errors)
2. Test that content loads without errors
3. Verify display looks correct
4. Check timing feels right

## Content Guidelines

### Warning Messages
- Keep titles punchy (3-5 words)
- Subtitles should be witty/memorable
- Explanations should be educational
- Advice should be actionable

### ASCII Art
- Max width: 60-80 characters
- Test on different terminals
- Keep Halloween theme
- Comedic, not scary

### Variations
- Aim for 3-5 variations per pattern
- Mix serious and humorous
- Avoid repetition
- Keep consistent tone

## Reference

See `.kiro/specs/display-refactoring/design.md` for architecture details.
