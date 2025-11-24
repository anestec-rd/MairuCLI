# Magic Numbers Analysis - Refactoring Plan

**Date:** 2025-11-23
**Purpose:** Identify and plan refactoring of magic numbers to named constants

---

## Summary

**Total Magic Numbers Found:** ~25-30 instances
**Estimated Refactoring Time:** 15-20 minutes
**Priority:** Medium (improves maintainability)
**Risk:** Low (no functional changes)

---

## Categories of Magic Numbers

### 1. Timing Values (High Priority)
**Impact:** Affects user experience, frequently adjusted

#### Display Timing
- `0.05` - ASCII art character delay (default)
- `0.3` - Pause after art / after achievement
- `0.5` - Pause before explanation / before achievement

**Files:**
- `src/display/ascii_renderer.py` (1 instance)
- `src/display/warning_components.py` (4 instances)
- `src/display/achievements.py` (2 instances)

**Recommendation:** Create timing constants in `src/config.py`

```python
# Timing constants (in seconds)
TIMING_ASCII_CHAR_DELAY = 0.05
TIMING_PAUSE_SHORT = 0.3
TIMING_PAUSE_MEDIUM = 0.5
```

---

### 2. Achievement Thresholds (Medium Priority)
**Impact:** Affects achievement unlock conditions

#### Threshold Values
- `1` - First Blood (first dangerous command)
- `3` - Typo Master, Stubborn, Boundary Tester, System Adventurer
- `5` - Persistent Troublemaker, Explorer
- `8` - Balanced User (safe commands)

**Files:**
- `src/display/achievements.py` (8-10 instances)

**Recommendation:** Create achievement constants in `src/display/achievements.py`

```python
# Achievement thresholds
ACHIEVEMENT_FIRST_BLOOD = 1
ACHIEVEMENT_THRESHOLD_LOW = 3
ACHIEVEMENT_THRESHOLD_MEDIUM = 5
ACHIEVEMENT_THRESHOLD_HIGH = 8
```

---

### 3. Display Formatting (Low Priority)
**Impact:** Visual formatting, rarely changed

#### Formatting Values
- `60` - Separator line width (`"=" * 60`)
- `2` - Quote length check (`len(path) >= 2`)

**Files:**
- `src/display/achievements.py` (2 instances)
- `src/display/caution_warning.py` (2 instances)
- `src/display/warning_components.py` (1 instance)
- `src/command_parser.py` (1 instance)

**Recommendation:** Create display constants in `src/config.py`

```python
# Display constants
DISPLAY_SEPARATOR_WIDTH = 60
DISPLAY_MIN_QUOTE_LENGTH = 2
```

---

### 4. ANSI Color Codes (Low Priority)
**Impact:** Already well-organized, low priority

#### Color Values
- `208` - Orange
- `130` - Chocolate
- `141` - Purple
- `46` - Green
- `196` - Red

**Files:**
- `src/display/ascii_renderer.py` (already in COLORS dict)

**Recommendation:** Already well-organized, no change needed

---

### 5. Regex Pattern Numbers (Low Priority)
**Impact:** Part of regex patterns, context-specific

#### Pattern Values
- `777`, `666`, `755`, `775` - chmod permissions
- `644` - recommended permission

**Files:**
- `src/interceptor.py` (in regex patterns)

**Recommendation:** Keep as-is (part of regex syntax, self-documenting)

---

### 6. Performance Settings (Already Done)
**Impact:** Already in config

#### Performance Values
- `50` - Pattern match timeout (ms)

**Files:**
- `src/config.py` (already as constant: `pattern_match_timeout_ms`)

**Recommendation:** Already done ✅

---

## Refactoring Plan

### Phase 1: Timing Constants (5 minutes)
**Priority:** High
**Files to modify:** 3 files

1. Add constants to `src/config.py`:
```python
# Timing constants (in seconds)
TIMING_ASCII_CHAR_DELAY = 0.05  # Delay between ASCII art characters
TIMING_PAUSE_SHORT = 0.3        # Short pause (after art, after achievement)
TIMING_PAUSE_MEDIUM = 0.5       # Medium pause (before explanation, before achievement)
```

2. Update `src/display/ascii_renderer.py`:
```python
from src.config import TIMING_ASCII_CHAR_DELAY

def display_art_slowly(self, art: str, color: str, delay: float = TIMING_ASCII_CHAR_DELAY):
```

3. Update `src/display/warning_components.py`:
```python
from src.config import TIMING_ASCII_CHAR_DELAY, TIMING_PAUSE_SHORT, TIMING_PAUSE_MEDIUM

art_delay = timing.get("art_delay", TIMING_ASCII_CHAR_DELAY)
time.sleep(timing.get("pause_after_art", TIMING_PAUSE_SHORT))
time.sleep(timing.get("pause_before_explanation", TIMING_PAUSE_MEDIUM))
time.sleep(timing.get("pause_before_achievement", TIMING_PAUSE_SHORT))
```

4. Update `src/display/achievements.py`:
```python
from src.config import TIMING_PAUSE_SHORT, TIMING_PAUSE_MEDIUM

time.sleep(TIMING_PAUSE_MEDIUM)  # Pause before achievement
time.sleep(TIMING_PAUSE_SHORT)   # Brief pause after achievement
```

---

### Phase 2: Achievement Thresholds (5 minutes)
**Priority:** Medium
**Files to modify:** 1 file

1. Add constants to `src/display/achievements.py`:
```python
# Achievement thresholds
ACHIEVEMENT_FIRST_BLOOD = 1
ACHIEVEMENT_THRESHOLD_LOW = 3    # Typo Master, Stubborn, etc.
ACHIEVEMENT_THRESHOLD_MEDIUM = 5 # Persistent Troublemaker, Explorer
ACHIEVEMENT_THRESHOLD_HIGH = 8   # Balanced User
```

2. Update all achievement checks:
```python
if total_blocks == ACHIEVEMENT_FIRST_BLOOD and "first_blood" not in self._unlocked:
if total_blocks >= ACHIEVEMENT_THRESHOLD_MEDIUM and "persistent" not in self._unlocked:
if total_typos >= ACHIEVEMENT_THRESHOLD_LOW and "typo_master" not in self._unlocked:
# ... etc
```

---

### Phase 3: Display Formatting (5 minutes)
**Priority:** Low
**Files to modify:** 4 files

1. Add constants to `src/config.py`:
```python
# Display constants
DISPLAY_SEPARATOR_WIDTH = 60
DISPLAY_MIN_QUOTE_LENGTH = 2
```

2. Update separator lines in multiple files:
```python
from src.config import DISPLAY_SEPARATOR_WIDTH

print("=" * DISPLAY_SEPARATOR_WIDTH)
```

3. Update quote check in `src/command_parser.py`:
```python
from src.config import DISPLAY_MIN_QUOTE_LENGTH

if len(path) >= DISPLAY_MIN_QUOTE_LENGTH:
```

---

## Benefits of Refactoring

### Maintainability
- ✅ Single source of truth for timing values
- ✅ Easy to adjust timing globally
- ✅ Clear intent with named constants

### Readability
- ✅ `TIMING_PAUSE_MEDIUM` is clearer than `0.5`
- ✅ `ACHIEVEMENT_THRESHOLD_LOW` is clearer than `3`
- ✅ Self-documenting code

### Flexibility
- ✅ Easy to add configuration file support later
- ✅ Easy to add user preferences for timing
- ✅ Easy to adjust thresholds for difficulty

---

## Testing Strategy

### After Each Phase
1. Run all unit tests: `python -m pytest tests/unit/`
2. Run integration tests: `python -m pytest tests/integration/`
3. Manual smoke test: Start MairuCLI and trigger warnings

### Verification
- [ ] All tests pass
- [ ] No functional changes
- [ ] Timing feels the same
- [ ] Achievements unlock at same thresholds

---

## Risk Assessment

### Low Risk
- No logic changes
- Only replacing literals with constants
- Easy to revert if issues found

### Potential Issues
1. **Import errors** - Circular imports if not careful
   - Mitigation: Keep constants in config.py, import carefully

2. **Typos in constant names** - Could break functionality
   - Mitigation: Run tests after each phase

3. **Performance impact** - Negligible (constants are compiled)
   - Mitigation: None needed

---

## Estimated Time Breakdown

| Phase | Time | Priority | Files |
|-------|------|----------|-------|
| Phase 1: Timing | 5 min | High | 3 files |
| Phase 2: Achievements | 5 min | Medium | 1 file |
| Phase 3: Display | 5 min | Low | 4 files |
| Testing | 5 min | - | - |
| **Total** | **20 min** | | **8 files** |

---

## Recommendation

### For Day 7
**Recommended:** Complete Phase 1 (Timing) only
- **Time:** 5-7 minutes
- **Impact:** High (most frequently adjusted values)
- **Risk:** Low
- **Files:** 3 files

### Defer to Later
**Phase 2 & 3:** Can be done in Day 8 or later
- Not critical for v1.2.0 release
- Nice-to-have for code quality
- Can be done incrementally

---

## Alternative: Quick Win Approach

If time is very limited, focus on **timing constants only**:

1. Add to `src/config.py` (1 minute):
```python
# Timing constants
TIMING_ASCII_CHAR_DELAY = 0.05
TIMING_PAUSE_SHORT = 0.3
TIMING_PAUSE_MEDIUM = 0.5
```

2. Update only the most critical file: `src/display/warning_components.py` (2 minutes)

3. Test (2 minutes)

**Total:** 5 minutes for biggest impact

---

## Conclusion

**Full Refactoring:** 20 minutes for all phases
**Recommended for Day 7:** 5-7 minutes for Phase 1 only
**Defer:** Phase 2 & 3 to Day 8

**Decision:** Proceed with Phase 1 (timing constants) on Day 7, defer rest to later.
