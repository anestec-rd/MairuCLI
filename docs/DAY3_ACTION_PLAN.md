# Day 3 Action Plan - Display Refactoring Implementation

**Target Date:** 2025-11-18 (Tuesday)
**Estimated Time:** 2.5-3 hours
**Goal:** Complete foundation and core components

## Quick Start

1. Open `.kiro/specs/display-refactoring/tasks.md`
2. Click "Start task" next to Task 1
3. Follow the plan below

## Session Breakdown

### Phase 1: Foundation (30 min)

**Task 1: Set up project structure and data files**

```bash
# What you'll do:
- Create src/display/ directory
- Create src/display/__init__.py
- Create data/warnings/ directory
- Create data/ascii_art/ directory
- Move ascii_art/*.txt to data/ascii_art/
- Test that imports still work
```

**Expected outcome:**
```
src/
├── display/
│   └── __init__.py
data/
├── warnings/
└── ascii_art/
    ├── fired.txt
    ├── permission_denied.txt
    └── data_destroyer.txt
```

### Phase 2: Content System (45 min)

**Task 2.1: Create ContentLoader class**

File: `src/display/content_loader.py`

Key methods:
- `load_catalog()` - Load warning_catalog.json
- `get_warning_content(pattern_name)` - Get specific warning
- `get_variations(category)` - Get message variations
- Error handling for missing/invalid files

**Task 2.2: Create JSON data files**

Files to create:
1. `data/warnings/warning_catalog.json` - Master catalog
2. `data/warnings/danger_variations.json` - Message variations
3. `data/warnings/typo_messages.json` - Typo messages
4. `data/warnings/repeat_warnings.json` - Repeat warnings

**Test:** Load each file and print content to verify

### Phase 3: ASCII Renderer (30 min)

**Task 3.1: Create AsciiRenderer class**

File: `src/display/ascii_renderer.py`

Key methods:
- `load_art(filename)` - Load from data/ascii_art/
- `display_art(art, color)` - Display with color
- `display_art_slowly(art, color, delay)` - Line-by-line with timing

**Test:** Display fired.txt with red color

### Phase 4: Message Formatter (45 min)

**Task 4.1: Create MessageTemplate class**

File: `src/display/message_formatter.py`

Key features:
- Template with placeholders
- Field validation
- Format with kwargs

**Task 4.2: Create MessageFormatter class**

Key methods:
- `format_danger_warning(...)` - Format danger message
- `format_typo_warning(...)` - Format typo message
- `format_repeat_warning(...)` - Format repeat message

**Test:** Format a sample danger warning

### Phase 5: Statistics & Achievements (30 min)

**Task 5.1: Create Statistics class**

File: `src/display/statistics.py`

Extract from display.py:
- `_stats` dict → Statistics class
- `_warned_commands` dict → track_repeat_command()
- Counter methods

**Task 5.2: Create AchievementTracker class**

File: `src/display/achievements.py`

Extract from display.py:
- `_achievements` list → AchievementTracker
- `check_achievements()` logic
- `show_achievement()` method

**Test:** Increment counters and trigger achievement

## Testing Checklist

After each task:
- [ ] Code runs without errors
- [ ] Imports work correctly
- [ ] Files load successfully
- [ ] Output looks correct

## If You Get Stuck

1. Check `design.md` for architecture details
2. Look at existing `display.py` for reference
3. Test with simple print statements first
4. Commit working code before moving on

## What NOT to Do Yet

- ❌ Don't modify existing display.py yet
- ❌ Don't implement warning components yet (Task 6)
- ❌ Don't write unit tests yet (optional tasks)
- ❌ Don't worry about integration yet

## Success Criteria for Day 3

By end of session, you should have:
- ✅ New directory structure in place
- ✅ All JSON data files created and loading
- ✅ ContentLoader working
- ✅ AsciiRenderer working
- ✅ MessageFormatter working
- ✅ Statistics and Achievements extracted

## Commands to Run

```bash
# Start the session
cd mairu-cli

# After creating files, test imports
python -c "from src.display.content_loader import ContentLoader; print('OK')"
python -c "from src.display.ascii_renderer import AsciiRenderer; print('OK')"
python -c "from src.display.message_formatter import MessageFormatter; print('OK')"
python -c "from src.display.statistics import Statistics; print('OK')"
python -c "from src.display.achievements import AchievementTracker; print('OK')"

# Test content loading
python -c "from src.display.content_loader import ContentLoader; cl = ContentLoader(); print(cl.load_catalog())"

# Test ASCII rendering
python -c "from src.display.ascii_renderer import AsciiRenderer; ar = AsciiRenderer(); art = ar.load_art('fired.txt'); ar.display_art(art, 'red')"
```

## Commit Strategy

Commit after each major task:
```bash
git add .
git commit -m "feat(display): implement ContentLoader"
git commit -m "feat(display): implement AsciiRenderer"
git commit -m "feat(display): implement MessageFormatter"
git commit -m "feat(display): extract Statistics and Achievements"
```

## Next Session Preview (Day 4)

- Implement warning components (DangerWarning, TypoWarning, RepeatWarning)
- Refactor display.py to use new components
- Test integration with existing code

---

**Remember:** Take breaks, test frequently, and don't rush. Quality over speed! 🎃
