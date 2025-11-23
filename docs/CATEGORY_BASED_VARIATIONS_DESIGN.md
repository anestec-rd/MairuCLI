# Category-Based Warning Variations Design

## Problem Statement

### Current Architecture
Currently, `danger_variations.json` defines warning message variations on a **per-pattern basis**:

```json
{
  "rm_root": [variations...],
  "chmod_777": [variations...],
  "chmod_000": [variations...],
  ...
}
```

### Scalability Issues

**Current state:** 11 danger patterns
- Each pattern has 5-9 unique variations
- Total: ~70 individual variation entries
- Manageable but requires duplication

**Future state:** 50-60 danger patterns
- Would require 250-540 individual variation entries
- High maintenance burden
- Lots of duplication across similar patterns
- Difficult to maintain consistent tone/quality

### Example of Duplication

Multiple patterns share similar themes but duplicate content:

```json
"disk_destroyer": [
  {"title": "STORAGE APOCALYPSE!", "subtitle": "(Say goodbye to your data)"}
],
"dd_zero": [
  {"title": "ZERO APOCALYPSE!", "subtitle": "(Your disk is being zeroed)"}
],
"dd_random": [
  // Uses disk_destroyer variations
]
```

## Proposed Solution: Category-Based Variations

### Core Concept

Leverage the existing **category system** in `warning_catalog.json`:
- deletion
- permission
- disk
- database
- system

Create **shared variation pools** per category, with optional **pattern-specific overrides**.

### Architecture

#### 1. New File Structure

```
data/warnings/
├── warning_catalog.json          # Existing (defines categories)
├── category_variations.json      # NEW: Category-based variations
└── pattern_variations.json       # NEW: Pattern-specific overrides
```

#### 2. Category Variations (category_variations.json)

```json
{
  "version": "1.0",
  "categories": {
    "deletion": {
      "theme": "Data loss, disappearance, destruction",
      "variations": [
        {
          "title": "DATA DESTROYER DETECTED!",
          "subtitle": "(This will not end well)"
        },
        {
          "title": "POINT OF NO RETURN!",
          "subtitle": "(Backups? Anyone?)"
        },
        {
          "title": "CAREER ENDER!",
          "subtitle": "(Update your resume now)"
        },
        {
          "title": "SCARIER THAN GHOSTS!",
          "subtitle": "(Even monsters fear this command)"
        },
        {
          "title": "NO USE CRYING!",
          "subtitle": "(It's no use crying over spilt milk)"
        }
      ]
    },
    "permission": {
      "theme": "Access control, security, locks",
      "variations": [
        {
          "title": "PERMISSION DENIED!",
          "subtitle": "(Error 403: Forbidden by your future self)"
        },
        {
          "title": "SECURITY BREACH ALERT!",
          "subtitle": "(This is how hacks happen)"
        },
        {
          "title": "WIDE OPEN DOORS!",
          "subtitle": "(Might as well remove the locks)"
        },
        {
          "title": "EVERYONE'S INVITED!",
          "subtitle": "(Including the bad guys)"
        }
      ]
    },
    "disk": {
      "theme": "Hardware destruction, disk operations",
      "variations": [
        {
          "title": "DISK OBLITERATION!",
          "subtitle": "(Your disk is being shredded)"
        },
        {
          "title": "HARDWARE HAUNTING!",
          "subtitle": "(Your disk will become a ghost)"
        },
        {
          "title": "STORAGE GRAVEYARD!",
          "subtitle": "(Every byte gets a tombstone)"
        },
        {
          "title": "BYTE BURIAL!",
          "subtitle": "(Rest in peace, little bytes)"
        }
      ]
    },
    "database": {
      "theme": "Database operations, SQL, tables",
      "variations": [
        {
          "title": "DATABASE APOCALYPSE!",
          "subtitle": "(All your tables are belong to /dev/null)"
        },
        {
          "title": "SQL NIGHTMARE!",
          "subtitle": "(DROP is forever, SELECT is not)"
        },
        {
          "title": "MAGIC TRICK GONE WRONG!",
          "subtitle": "(Poof! Your data vanished... permanently)"
        },
        {
          "title": "DBA'S HAUNTING!",
          "subtitle": "(Your DBA will literally haunt you forever)"
        }
      ]
    },
    "system": {
      "theme": "System crashes, kernel panic, process issues",
      "variations": [
        {
          "title": "SYSTEM TANTRUM!",
          "subtitle": "(Kernel-chan is having a meltdown!)"
        },
        {
          "title": "PARTY TOO WILD!",
          "subtitle": "(The kernel can't handle this much fun!)"
        },
        {
          "title": "SYSTEM SCREAMING!",
          "subtitle": "(Not the fun Halloween kind of screaming)"
        },
        {
          "title": "REBOOT REQUIRED!",
          "subtitle": "(Time to kick everyone out and start over)"
        }
      ]
    }
  }
}
```

#### 3. Pattern-Specific Variations (pattern_variations.json)

For patterns that need **unique, specialized variations**:

```json
{
  "version": "1.0",
  "patterns": {
    "rm_root": {
      "reason": "Iconic pattern, deserves unique variations",
      "variations": [
        {
          "title": "YOU'RE FIRED!",
          "subtitle": "(And so is your entire filesystem!)"
        },
        {
          "title": "NOPE. JUST NOPE.",
          "subtitle": "(Not today, SATA!)"
        },
        {
          "title": "MEMORY LOSS!",
          "subtitle": "(RAM not found... Who are you again?)"
        }
      ]
    },
    "chmod_000": {
      "reason": "Unique ghost/lock theme",
      "variations": [
        {
          "title": "GHOST FILE!",
          "subtitle": "(It's there... but you can't touch it! 👻)"
        },
        {
          "title": "LOCKED IN A COFFIN!",
          "subtitle": "(Not even you have the key anymore)"
        },
        {
          "title": "SPECTRAL EXISTENCE!",
          "subtitle": "(Visible to all, accessible to none)"
        }
      ]
    },
    "fork_bomb": {
      "reason": "Unique party/multiplication theme",
      "variations": [
        {
          "title": "PARTY CRASHERS!",
          "subtitle": "(Everyone invited everyone... infinitely!)"
        },
        {
          "title": "ZOMBIE APOCALYPSE!",
          "subtitle": "(Processes multiplying like the undead!)"
        },
        {
          "title": "CANDY BOWL OVERWHELMED!",
          "subtitle": "(Too many hands reaching in at once!)"
        }
      ]
    },
    "kernel_panic": {
      "reason": "Unique overexcited kernel theme",
      "variations": [
        {
          "title": "KERNEL'S HALLOWEEN PARTY!",
          "subtitle": "(Someone's TOO excited for trick-or-treating!)"
        },
        {
          "title": "TOO MUCH CANDY!",
          "subtitle": "(Your kernel ate all the treats and crashed!)"
        },
        {
          "title": "OVEREXCITED KERNEL!",
          "subtitle": "(Calm down, Halloween isn't going anywhere!)"
        }
      ]
    }
  }
}
```

### Selection Logic

#### Priority Order

1. **Pattern-specific variations** (if defined in `pattern_variations.json`)
2. **Category variations** (from `category_variations.json`)
3. **Fallback** (generic error message)

#### Implementation Pseudocode

```python
def get_variation(pattern_name: str, category: str) -> dict:
    """
    Get a random variation for the given pattern.

    Priority:
    1. Pattern-specific variations
    2. Category variations
    3. Fallback
    """
    # Try pattern-specific first
    if pattern_name in pattern_variations:
        return random.choice(pattern_variations[pattern_name])

    # Fall back to category variations
    if category in category_variations:
        return random.choice(category_variations[category])

    # Ultimate fallback
    return {
        "title": "DANGER DETECTED!",
        "subtitle": "(This command is risky)"
    }
```

## Benefits

### 1. Scalability
- **11 patterns → 50 patterns:** Add 0-5 variations per pattern (if unique)
- **Category variations:** Reused across all patterns in category
- **Maintenance:** Update category variations once, affects all patterns

### 2. Consistency
- Patterns in same category share thematic consistency
- Easier to maintain tone and quality
- New patterns automatically get appropriate variations

### 3. Flexibility
- Iconic patterns (rm_root, chmod_000) keep unique identity
- Generic patterns (dd_random, mkfs_disk) share variations
- Easy to promote pattern from generic → specific

### 4. Reduced Duplication
- **Current:** ~70 variation entries (11 patterns × ~6 variations)
- **Proposed:** ~30 category variations + ~20 pattern-specific = 50 total
- **At 50 patterns:** ~30 category + ~30 pattern-specific = 60 total (vs 300 individual)

## Migration Strategy

### Phase 1: Create New Files (Non-Breaking)
1. Create `category_variations.json`
2. Create `pattern_variations.json`
3. Populate with current variations (categorized)
4. Keep `danger_variations.json` as-is

### Phase 2: Update Code (Backward Compatible)
1. Update `warning_components.py` to check new files first
2. Fall back to `danger_variations.json` if not found
3. Test thoroughly

### Phase 3: Deprecate Old File
1. Remove `danger_variations.json`
2. Update documentation
3. Clean up code

### Phase 4: Optimize
1. Review category variations for quality
2. Add more category variations
3. Identify patterns that should be promoted to pattern-specific

## Example: Adding New Pattern

### Current Approach (Per-Pattern)
```json
// In danger_variations.json
"new_pattern_50": [
  {"title": "...", "subtitle": "..."},
  {"title": "...", "subtitle": "..."},
  {"title": "...", "subtitle": "..."},
  {"title": "...", "subtitle": "..."},
  {"title": "...", "subtitle": "..."}
]
```
**Effort:** Write 5 new variations

### Proposed Approach (Category-Based)
```json
// In warning_catalog.json
"new_pattern_50": {
  "category": "disk",  // ← Just specify category
  ...
}
```
**Effort:** 0 new variations (uses existing disk category variations)

**Optional:** Add pattern-specific variations only if truly unique

## Data Structure Comparison

### Current Structure
```
danger_variations.json (1 file)
├── rm_root: [5 variations]
├── chmod_777: [9 variations]
├── chmod_000: [9 variations]
├── data_destroyer: [9 variations]
├── drop_database: [8 variations]
├── fork_bomb: [8 variations]
├── kernel_panic: [8 variations]
├── disk_destroyer: [7 variations]
├── data_void: [8 variations]
├── zero_wipe: [8 variations]
└── file_eraser: [8 variations]
Total: 87 variation entries
```

### Proposed Structure
```
category_variations.json
├── deletion: [8 variations]
├── permission: [8 variations]
├── disk: [8 variations]
├── database: [8 variations]
└── system: [8 variations]
Subtotal: 40 variations

pattern_variations.json
├── rm_root: [5 variations]
├── chmod_000: [5 variations]
├── fork_bomb: [5 variations]
└── kernel_panic: [5 variations]
Subtotal: 20 variations

Total: 60 variation entries (vs 87)
Reusability: High (40/60 = 67% reusable)
```

## Future Enhancements

### 1. Variation Weighting
```json
"deletion": {
  "variations": [
    {
      "title": "COMMON MESSAGE",
      "subtitle": "...",
      "weight": 3  // ← Appears 3x more often
    },
    {
      "title": "RARE MESSAGE",
      "subtitle": "...",
      "weight": 1
    }
  ]
}
```

### 2. Context-Aware Variations
```json
"deletion": {
  "variations": [
    {
      "title": "HALLOWEEN SPECIAL!",
      "subtitle": "...",
      "active_months": [10]  // ← Only in October
    }
  ]
}
```

### 3. User-Contributed Variations
- Community can contribute category variations
- Easier to review (thematic consistency)
- Automatically benefits all patterns in category

## Implementation Checklist

- [ ] Create `category_variations.json`
- [ ] Create `pattern_variations.json`
- [ ] Migrate existing variations to new structure
- [ ] Update `warning_components.py` selection logic
- [ ] Add unit tests for new selection logic
- [ ] Test with all 11 existing patterns
- [ ] Update documentation
- [ ] Deprecate `danger_variations.json`

## Conclusion

Category-based variations provide:
- **Better scalability** (11 → 50+ patterns)
- **Reduced duplication** (60 vs 300 entries)
- **Easier maintenance** (update once, affect many)
- **Consistent theming** (category-level coherence)
- **Flexibility** (pattern-specific overrides when needed)

This design positions MairuCLI for long-term growth while maintaining the quality and humor of warning messages.
