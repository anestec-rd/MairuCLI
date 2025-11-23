---
inclusion: always
---

# Magic Number Guidelines for MairuCLI

## Purpose

Prevent magic numbers (hardcoded numeric literals) in code by using named constants. This improves code maintainability, readability, and makes it easier to adjust values globally.

---

## What is a Magic Number?

A **magic number** is a numeric literal that appears directly in code without explanation of its meaning or purpose.

### Examples of Magic Numbers

❌ **Bad (Magic Number):**
```python
time.sleep(0.5)  # What does 0.5 mean? Why 0.5?
if total_blocks >= 5:  # Why 5? What does 5 represent?
print("=" * 60)  # Why 60? What if we want to change it?
```

✅ **Good (Named Constant):**
```python
time.sleep(TIMING_PAUSE_MEDIUM)  # Clear intent
if total_blocks >= ACHIEVEMENT_THRESHOLD_MEDIUM:  # Self-documenting
print("=" * DISPLAY_SEPARATOR_WIDTH)  # Easy to adjust globally
```

---

## When to Use Named Constants

### Always Use Constants For:

1. **Timing Values**
   - Animation delays
   - Pause durations
   - Timeout values
   - Example: `0.05`, `0.3`, `0.5`

2. **Thresholds**
   - Achievement unlock conditions
   - Warning level triggers
   - Retry limits
   - Example: `3`, `5`, `8`

3. **Display Formatting**
   - Line widths
   - Padding sizes
   - Column counts
   - Example: `60`, `80`

4. **Configuration Values**
   - Buffer sizes
   - Maximum lengths
   - Default values
   - Example: `100`, `1024`

### Exceptions (OK to Use Literals):

1. **Mathematical Constants**
   - `0`, `1`, `-1` in arithmetic
   - Array indices: `[0]`, `[-1]`
   - Boolean conversions: `if x == 0:`

2. **Self-Documenting Context**
   - Regex patterns: `r"chmod\s+777"` (777 is the permission value)
   - Format strings: `f"{value:2d}"` (2 is field width)
   - Range iterations: `range(10)` when 10 is obvious from context

3. **One-Time Use**
   - Values used only once in a very specific context
   - Values that are self-explanatory in context

---

## Where to Define Constants

### 1. Global Configuration (`src/config.py`)

Use for values that:
- Affect multiple modules
- Might become user-configurable
- Are system-wide settings

```python
# src/config.py

# Timing constants (in seconds)
TIMING_ASCII_CHAR_DELAY = 0.05  # Delay between ASCII art characters
TIMING_PAUSE_SHORT = 0.3        # Short pause (after art, after achievement)
TIMING_PAUSE_MEDIUM = 0.5       # Medium pause (before explanation)
TIMING_PAUSE_LONG = 1.0         # Long pause (dramatic effect)

# Display constants
DISPLAY_SEPARATOR_WIDTH = 60    # Width of separator lines (=====)
DISPLAY_MIN_QUOTE_LENGTH = 2    # Minimum length for quoted strings

# Performance constants
PATTERN_MATCH_TIMEOUT_MS = 50   # Maximum time for pattern matching
```

### 2. Module-Level Constants

Use for values that:
- Are specific to one module
- Won't be used elsewhere
- Are implementation details

```python
# src/display/achievements.py

# Achievement thresholds
ACHIEVEMENT_FIRST_BLOOD = 1          # First dangerous command blocked
ACHIEVEMENT_THRESHOLD_LOW = 3        # Typo Master, Stubborn, etc.
ACHIEVEMENT_THRESHOLD_MEDIUM = 5     # Persistent Troublemaker, Explorer
ACHIEVEMENT_THRESHOLD_HIGH = 8       # Balanced User
ACHIEVEMENT_THRESHOLD_EXPERT = 10    # Expert level achievements
```

### 3. Class-Level Constants

Use for values that:
- Are specific to a class
- Define class behavior
- Are part of class configuration

```python
class WarningDisplay:
    # Display configuration
    MAX_LINE_LENGTH = 80
    INDENT_SIZE = 4
    MAX_ADVICE_ITEMS = 5
```

---

## Naming Conventions

### Format: `CATEGORY_DESCRIPTION`

**Categories:**
- `TIMING_` - Time-related values
- `ACHIEVEMENT_` - Achievement thresholds
- `DISPLAY_` - Display formatting
- `MAX_` / `MIN_` - Limits and boundaries
- `DEFAULT_` - Default values

**Examples:**
```python
TIMING_PAUSE_SHORT = 0.3
ACHIEVEMENT_THRESHOLD_LOW = 3
DISPLAY_SEPARATOR_WIDTH = 60
MAX_RETRY_ATTEMPTS = 3
DEFAULT_COLOR_SCHEME = "halloween"
```

### Descriptive Names

✅ **Good:**
```python
TIMING_PAUSE_BEFORE_EXPLANATION = 0.5
ACHIEVEMENT_PERSISTENT_TROUBLEMAKER_THRESHOLD = 5
DISPLAY_ACHIEVEMENT_SEPARATOR_WIDTH = 60
```

❌ **Bad:**
```python
PAUSE = 0.5  # Which pause?
THRESHOLD = 5  # Threshold for what?
WIDTH = 60  # Width of what?
```

---

## Adding Constants: Step-by-Step

### When Adding New Code

1. **Write the code first** (with magic numbers if needed)
2. **Identify numeric literals** that aren't self-explanatory
3. **Create named constants** at appropriate location
4. **Replace literals** with constants
5. **Add comments** explaining what the constant represents

### Example Workflow

**Step 1: Initial code (with magic number)**
```python
def show_warning(self):
    time.sleep(0.5)
    print("=" * 60)
```

**Step 2: Identify magic numbers**
- `0.5` - pause duration (not obvious why 0.5)
- `60` - separator width (not obvious why 60)

**Step 3: Create constants**
```python
# In src/config.py
TIMING_PAUSE_MEDIUM = 0.5  # Medium pause for dramatic effect
DISPLAY_SEPARATOR_WIDTH = 60  # Standard terminal width
```

**Step 4: Replace in code**
```python
from src.config import TIMING_PAUSE_MEDIUM, DISPLAY_SEPARATOR_WIDTH

def show_warning(self):
    time.sleep(TIMING_PAUSE_MEDIUM)
    print("=" * DISPLAY_SEPARATOR_WIDTH)
```

---

## Refactoring Existing Magic Numbers

### Priority Order

1. **High Priority:** Timing values (frequently adjusted)
2. **Medium Priority:** Thresholds (affect behavior)
3. **Low Priority:** Display formatting (rarely changed)

### Refactoring Process

1. **Search for magic numbers:**
   ```bash
   # Find decimal numbers
   grep -r "\b0\.\d\+" src/

   # Find integers (2 or more)
   grep -r "\b[2-9]\d*\b" src/
   ```

2. **Categorize findings:**
   - Timing values → `src/config.py`
   - Achievement thresholds → `src/display/achievements.py`
   - Display formatting → `src/config.py`
   - Module-specific → respective module

3. **Create constants** with descriptive names

4. **Replace one category at a time** (easier to test)

5. **Run tests** after each category

6. **Commit** with clear message: `refactor: replace timing magic numbers with constants`

---

## Testing After Refactoring

### Verification Checklist

- [ ] All unit tests pass
- [ ] All integration tests pass
- [ ] Manual smoke test (start MairuCLI, trigger warnings)
- [ ] Timing feels the same (no noticeable changes)
- [ ] Achievements unlock at same thresholds
- [ ] Display looks the same

### Common Issues

**Issue:** Import errors
- **Cause:** Circular imports
- **Fix:** Keep constants in config.py, import carefully

**Issue:** Tests fail
- **Cause:** Typo in constant name
- **Fix:** Double-check constant names match

**Issue:** Timing feels different
- **Cause:** Wrong constant value
- **Fix:** Verify constant values match original literals

---

## Examples from MairuCLI

### Timing Constants (Phase 1 - Completed)

**Before:**
```python
# src/display/warning_components.py
time.sleep(0.3)  # Magic number
time.sleep(0.5)  # Magic number
```

**After:**
```python
# src/config.py
TIMING_PAUSE_SHORT = 0.3
TIMING_PAUSE_MEDIUM = 0.5

# src/display/warning_components.py
from src.config import TIMING_PAUSE_SHORT, TIMING_PAUSE_MEDIUM

time.sleep(TIMING_PAUSE_SHORT)
time.sleep(TIMING_PAUSE_MEDIUM)
```

### Achievement Thresholds (Phase 2 - Planned)

**Before:**
```python
# src/display/achievements.py
if total_blocks >= 5 and "persistent" not in self._unlocked:  # Magic number
if total_typos >= 3 and "typo_master" not in self._unlocked:  # Magic number
```

**After:**
```python
# src/display/achievements.py
ACHIEVEMENT_THRESHOLD_LOW = 3
ACHIEVEMENT_THRESHOLD_MEDIUM = 5

if total_blocks >= ACHIEVEMENT_THRESHOLD_MEDIUM and "persistent" not in self._unlocked:
if total_typos >= ACHIEVEMENT_THRESHOLD_LOW and "typo_master" not in self._unlocked:
```

---

## Benefits

### Maintainability
- ✅ Single source of truth for values
- ✅ Easy to adjust globally
- ✅ Clear intent and purpose

### Readability
- ✅ Self-documenting code
- ✅ Easier to understand
- ✅ Less need for comments

### Flexibility
- ✅ Easy to add configuration file support
- ✅ Easy to add user preferences
- ✅ Easy to adjust for different contexts

### Testing
- ✅ Easy to test with different values
- ✅ Easy to mock for unit tests
- ✅ Clear what values affect behavior

---

## Anti-Patterns to Avoid

### ❌ Over-Abstraction

Don't create constants for every number:
```python
# Bad - too much abstraction
ZERO = 0
ONE = 1
TWO = 2
```

### ❌ Unclear Names

Don't use vague names:
```python
# Bad - what does VALUE mean?
VALUE = 5
CONSTANT = 0.3
NUMBER = 60
```

### ❌ Wrong Location

Don't put all constants in one place:
```python
# Bad - mixing unrelated constants
TIMING_PAUSE = 0.3
ACHIEVEMENT_THRESHOLD = 5
DATABASE_PORT = 5432
API_KEY = "abc123"
```

---

## Quick Reference

### When Adding New Code

1. Write code with literals first
2. Identify non-obvious numbers
3. Create named constants
4. Replace literals
5. Test

### When Reviewing Code

Ask yourself:
- "What does this number mean?"
- "Would I understand this in 6 months?"
- "Could this value change?"
- "Is this used elsewhere?"

If answer is unclear → Use a named constant

---

## Summary

**Golden Rule:** If a number's purpose isn't immediately obvious from context, use a named constant.

**Priority:**
1. Timing values (high)
2. Thresholds (medium)
3. Display formatting (low)

**Location:**
- Global → `src/config.py`
- Module-specific → module file
- Class-specific → class definition

**Naming:** `CATEGORY_DESCRIPTION` (e.g., `TIMING_PAUSE_SHORT`)

**Testing:** Always run tests after refactoring

---

**This steering file ensures consistent handling of numeric values as MairuCLI grows.**
