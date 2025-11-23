# Warning Variations Management

## Purpose

Guide developers on how to add and manage warning message variations in MairuCLI.

---

## File Structure

```
data/warnings/
├── warning_catalog.json       # Pattern definitions (category, severity, etc.)
├── category_variations.json   # Shared variations by category (8 per category)
└── pattern_variations.json    # Pattern-specific variations (4 per pattern)
```

---

## How Variations Are Selected

### Merge Strategy (Current Implementation)

When displaying a warning, the system **merges** variations from multiple sources:

1. **Get category variations** (8 variations)
   - From `category_variations.json`
   - Based on pattern's category (deletion, permission, disk, etc.)

2. **Get pattern-specific variations** (0-4 variations)
   - From `pattern_variations.json`
   - Only if pattern has unique theme

3. **Merge both lists** (8-12 total variations)
   - Combine category + pattern-specific
   - Select random variation from merged list

4. **Fallback** (if nothing found)
   - Use legacy `danger_variations.json`
   - Or hardcoded fallback

### Example Flow

```
User runs: rm -rf /

1. Load pattern info from warning_catalog.json
   → variation_set: "rm_root"
   → category: "deletion"

2. Get category variations (8 variations)
   → "DATA DESTROYER DETECTED!"
   → "POINT OF NO RETURN!"
   → "CAREER ENDER!"
   → ... (5 more)

3. Get pattern-specific variations (4 variations)
   → "YOU'RE FIRED!"
   → "NOPE. JUST NOPE."
   → "MEMORY LOSS!"
   → "GAME OVER!"

4. Merge: 8 + 4 = 12 total variations

5. Select random variation from all 12
```

---

## Adding New Danger Patterns

### Step 1: Add to warning_catalog.json

```json
{
  "new_pattern": {
    "category": "disk",           // Choose existing category
    "severity": "critical",
    "variation_set": "new_pattern",
    "ascii_art": "disk_destroyer.txt",
    "color": "red",
    "emoji": "fire",
    "explanation": "What this command does",
    "consequence": "Why it's dangerous",
    "advice": ["Safe alternative 1", "Safe alternative 2"]
  }
}
```

### Step 2: Decide on Variations

**Option A: Use Category Variations Only (Recommended)**

If the pattern fits well with existing category theme:
- ✅ Do nothing else
- ✅ Pattern will use 8 category variations
- ✅ Fast and consistent

**Option B: Add Pattern-Specific Variations (Optional)**

If the pattern has a unique theme worth highlighting:
- Add 3-4 variations to `pattern_variations.json`
- Pattern will use 8 category + 4 specific = 12 total

```json
// In pattern_variations.json
{
  "new_pattern": {
    "reason": "Unique vampire theme - data sucking",
    "variations": [
      {"title": "VAMPIRE ATTACK!", "subtitle": "(Sucking your data dry!)"},
      {"title": "BLOOD MOON RISING!", "subtitle": "(Your bytes are the sacrifice!)"},
      {"title": "GARLIC WON'T HELP!", "subtitle": "(This vampire wants data, not blood!)"},
      {"title": "STAKE THROUGH THE DISK!", "subtitle": "(Permanent data death!)"}
    ]
  }
}
```

---

## Guidelines for Pattern-Specific Variations

### When to Add Pattern-Specific Variations

✅ **Add when:**
- Pattern has truly unique theme (ghost files, overexcited kernel, vampire data)
- Theme doesn't fit category variations well
- You have 3-4 creative, high-quality variations

❌ **Don't add when:**
- Pattern is generic (just another disk destroyer)
- Variations would be similar to category variations
- You only have 1-2 variations

### Quality Standards

Pattern-specific variations should be:
- **Unique**: Different from category variations
- **Thematic**: Follow a consistent theme
- **Creative**: Memorable and engaging
- **Educational**: Still convey the danger

### Quantity Guidelines

- **Minimum**: 3 variations (if adding any)
- **Recommended**: 4 variations
- **Maximum**: 6 variations (avoid overwhelming)

**Why 3-4?**
- Combined with 8 category variations = 11-12 total
- Provides variety without duplication
- Keeps pattern identity without dominating

---

## Examples

### Example 1: Generic Pattern (No Pattern-Specific)

```json
// warning_catalog.json
"shred_disk": {
  "category": "disk",
  "variation_set": "shred_disk",
  ...
}

// pattern_variations.json
// (nothing added)

// Result: Uses 8 disk category variations
```

### Example 2: Unique Theme (With Pattern-Specific)

```json
// warning_catalog.json
"chmod_000": {
  "category": "permission",
  "variation_set": "chmod_000",
  ...
}

// pattern_variations.json
"chmod_000": {
  "reason": "Unique ghost/lock theme - visible but inaccessible",
  "variations": [
    {"title": "GHOST FILE!", "subtitle": "(It's there... but you can't touch it! 👻)"},
    {"title": "LOCKED IN A COFFIN!", "subtitle": "(Not even you have the key anymore)"},
    {"title": "SPECTRAL EXISTENCE!", "subtitle": "(Visible to all, accessible to none)"},
    {"title": "ETERNAL SEAL!", "subtitle": "(Locked tighter than a vampire's tomb)"}
  ]
}

// Result: Uses 9 permission + 4 ghost = 13 total variations
```

---

## Category Variations

### Current Categories

1. **deletion** (8 variations)
   - Theme: Data loss, disappearance, destruction
   - Used by: rm_dangerous, mv_to_null, overwrite_file

2. **permission** (9 variations)
   - Theme: Access control, security, locks
   - Used by: chmod_777, chmod_000

3. **disk** (8 variations)
   - Theme: Hardware destruction, disk operations
   - Used by: dd_zero, redirect_to_disk, mkfs_disk, dd_random

4. **database** (8 variations)
   - Theme: Database operations, SQL, tables
   - Used by: drop_database

5. **system** (8 variations)
   - Theme: System crashes, kernel panic, process issues
   - Used by: fork_bomb, kernel_panic

### Adding New Category

If you need a new category (rare):

1. Add to `category_variations.json`
2. Create 8 thematic variations
3. Update this documentation

---

## Maintenance

### Reviewing Variations

Periodically review:
- Are pattern-specific variations still unique?
- Can any pattern-specific be moved to category?
- Are category variations high quality?

### Refactoring

If multiple patterns share similar pattern-specific variations:
- Consider moving to category variations
- Or creating a new category

---

## Anti-Patterns

### ❌ Don't: Add pattern-specific for every pattern

**Bad:**
```json
// pattern_variations.json with 50 patterns
"pattern_1": {...},
"pattern_2": {...},
"pattern_3": {...},
...
"pattern_50": {...}
```

**Why:** Defeats the purpose of category system

### ❌ Don't: Duplicate category variations

**Bad:**
```json
// pattern_variations.json
"new_pattern": {
  "variations": [
    {"title": "DATA DESTROYER!", "subtitle": "..."}, // Already in deletion category
    {"title": "DISK OBLITERATION!", "subtitle": "..."} // Already in disk category
  ]
}
```

**Why:** Wastes effort, creates confusion

### ❌ Don't: Add low-quality variations

**Bad:**
```json
"new_pattern": {
  "variations": [
    {"title": "BAD!", "subtitle": "(Not good)"},
    {"title": "DANGER!", "subtitle": "(Be careful)"}
  ]
}
```

**Why:** Generic, not memorable, not educational

---

## Testing

After adding variations:

```bash
# Run variation tests
python -m pytest tests/unit/test_content_loader_variations.py -v

# Manual test
python tests/manual/test_category_variations.py
```

---

## Summary

**Golden Rules:**
1. **Most patterns use category variations only** (8 variations)
2. **Add pattern-specific only for unique themes** (3-4 variations)
3. **Merged result gives 8-12 total variations** (good variety)
4. **Document your reasoning** in pattern_variations.json

**Decision Tree:**
```
Does pattern have unique theme?
├─ No  → Use category variations only (8 variations)
└─ Yes → Add 3-4 pattern-specific (8 + 4 = 12 variations)
```

**Benefits:**
- ✅ Scalable (50+ patterns without duplication)
- ✅ Consistent (category themes maintained)
- ✅ Flexible (unique patterns can shine)
- ✅ Balanced (8-12 variations per pattern)
