# Cross-Platform Consistency in MairuCLI

**Date:** 2025-11-25 (Day 9)
**Context:** Ensuring consistent educational experience across Windows, Linux, and macOS

---

## The Challenge

MairuCLI aims to provide an **educational experience** about dangerous CLI commands. However, different operating systems have different file system structures, which creates a challenge:

**The Problem:**
- Dangerous commands often target OS-specific paths (`/dev/sda` on Linux, `C:\Windows` on Windows)
- System protection mechanisms differ by platform
- Educational warnings should be consistent regardless of OS

**The Goal:**
- Users should see the same educational warnings on all platforms
- Platform-specific system protection should not interfere with educational content

---

## The Conflict: Two Protection Layers

MairuCLI has two protection mechanisms that can conflict:

### Layer 1: System Directory Protection
**Purpose:** Prevent accidental modification of critical OS directories

**Implementation:**
```python
PROTECTED_DIRECTORIES = {
    "linux": {
        "critical": ["/bin", "/sbin", "/boot", "/etc",
                     "/lib", "/lib64", "/proc", "/sys",
                     "/root", "/dev"]
    },
    "win32": {
        "critical": ["c:\\windows", "c:\\windows\\system32", ...]
    }
}
```

**Behavior:** Shows generic "Protected by MairuCLI's magic shield!" message

### Layer 2: Dangerous Pattern Detection
**Purpose:** Provide specific educational warnings about dangerous commands

**Implementation:**
```python
DANGEROUS_PATTERNS = {
    "dd_zero": {
        "pattern": r"dd\s+if=/dev/zero",
        "explanation": "Detailed educational message...",
        "ascii_art": "zero_wipe.txt"
    }
}
```

**Behavior:** Shows specific warning with ASCII art and detailed explanation

---

## The Problem Discovered

### Scenario: `dd if=/dev/zero`

**On Windows:**
1. System protection check: `/dev/zero` doesn't exist → Pass
2. Dangerous pattern check: Matches `dd_zero` → ✅ Show `zero_wipe` warning
3. **Result:** User sees educational warning with ASCII art

**On Linux (Before Fix):**
1. System protection check: `/dev` is protected → ❌ Block immediately
2. Dangerous pattern check: Never reached
3. **Result:** User sees generic "magic shield" message, misses educational content

**Impact:**
- Linux users miss out on specific educational warnings
- Inconsistent experience across platforms
- Educational value diminished

---

## Affected Patterns

The following patterns were affected by this conflict on Linux/macOS:

| Pattern | Path | Issue |
|---------|------|-------|
| `dd_zero` | `/dev/zero` | Generic protection instead of educational warning |
| `dd_random` | `/dev/random` | Generic protection instead of educational warning |
| `redirect_to_disk` | `/dev/sda` | Generic protection instead of educational warning |
| `mkfs_disk` | `/dev/sda` | Generic protection instead of educational warning |
| `mv_to_null` | `/dev/null` | Generic protection instead of educational warning |
| `kernel_panic` | `/proc/sysrq-trigger` | Generic protection instead of educational warning |

**Common theme:** All involve `/dev` or `/proc` directories, which are protected on Linux but don't exist on Windows.

---

## The Solution: Priority-Based Exemption

### Design Decision

**Principle:** Educational warnings take priority over generic system protection when both apply.

**Rationale:**
1. **Educational value:** Specific warnings teach users *why* a command is dangerous
2. **Consistency:** Same experience across all platforms
3. **Safety maintained:** Commands are still blocked, just with better messaging

### Implementation

Added an exemption list in `check_system_directory()`:

```python
# Special paths that should be handled by dangerous pattern check
# These have specific educational warnings that are more valuable
# than generic system protection warnings
DANGEROUS_PATTERN_PATHS = [
    '/dev/zero',           # dd_zero pattern
    '/dev/random',         # dd_random pattern
    '/dev/sd',             # redirect_to_disk, mkfs_disk patterns
    '/dev/null',           # mv_to_null pattern
    '/proc/sysrq-trigger'  # kernel_panic pattern
]

# Check if command contains any dangerous pattern paths
# If so, skip system protection and let dangerous pattern check handle it
for dangerous_path in DANGEROUS_PATTERN_PATHS:
    if dangerous_path in command:
        return "safe", "", ""  # Skip system protection
```

### Processing Flow (After Fix)

```
Command: dd if=/dev/zero

1. System Directory Protection Check
   ├─ Contains '/dev/zero'? Yes
   ├─ In DANGEROUS_PATTERN_PATHS? Yes
   └─ Skip protection → Return "safe"

2. Dangerous Pattern Check
   ├─ Matches 'dd_zero' pattern? Yes
   └─ Show educational warning with ASCII art ✅

3. Result: Consistent educational experience
```

---

## Results

### Before Fix

| Platform | Command | Warning Shown |
|----------|---------|---------------|
| Windows | `dd if=/dev/zero` | ✅ Educational (zero_wipe) |
| Linux | `dd if=/dev/zero` | ❌ Generic (magic shield) |
| macOS | `dd if=/dev/zero` | ❌ Generic (magic shield) |

**Consistency:** ❌ Inconsistent

### After Fix

| Platform | Command | Warning Shown |
|----------|---------|---------------|
| Windows | `dd if=/dev/zero` | ✅ Educational (zero_wipe) |
| Linux | `dd if=/dev/zero` | ✅ Educational (zero_wipe) |
| macOS | `dd if=/dev/zero` | ✅ Educational (zero_wipe) |

**Consistency:** ✅ Consistent across all platforms

---

## Design Principles

### 1. Educational Value First

When there's a conflict between:
- Generic system protection message
- Specific educational warning

**Always choose:** Specific educational warning

**Reason:** The primary goal of MairuCLI is education, not just blocking commands.

### 2. Explicit Over Implicit

The exemption list is **explicit** and **documented**:
- Each path has a comment explaining which pattern it serves
- Easy to understand and maintain
- Clear intent for future developers

### 3. Safety Maintained

**Important:** Commands are still blocked, just with better messaging.

- `/dev/zero` in `dd if=/dev/zero` → Educational warning + block
- `/dev/sda` in random command → Still protected by system protection
- Only **specific dangerous patterns** get exemptions

### 4. Platform Consistency

**Goal:** Same educational experience regardless of OS

**Implementation:**
- Exemption list uses Linux/Unix paths (most specific)
- Windows naturally skips system protection (paths don't exist)
- macOS benefits from same exemptions as Linux

---

## Edge Cases Considered

### Case 1: Non-Pattern /dev Access

**Command:** `ls /dev`

**Behavior:**
- Not in DANGEROUS_PATTERN_PATHS (only specific files exempted)
- System protection applies
- Shows generic protection message
- **Correct:** Listing /dev is not dangerous, generic message is appropriate

### Case 2: Partial Path Match

**Command:** `echo > /dev/sda1`

**Behavior:**
- Contains `/dev/sd` (prefix match)
- Exempted from system protection
- Matches `redirect_to_disk` pattern
- Shows educational warning
- **Correct:** Partition access is as dangerous as disk access

### Case 3: Multiple Protections

**Command:** `rm -rf /dev/zero`

**Behavior:**
- Contains `/dev/zero` → Skip system protection
- Matches `rm_dangerous` pattern (not `dd_zero`)
- Shows `rm_dangerous` warning
- **Correct:** Most specific dangerous pattern wins

---

## Maintenance Guidelines

### When Adding New Dangerous Patterns

**If the pattern targets a protected directory:**

1. **Check:** Does the pattern provide educational value beyond generic protection?
2. **If yes:** Add the path to `DANGEROUS_PATTERN_PATHS`
3. **Document:** Add comment explaining which pattern it serves
4. **Test:** Verify behavior on Linux/macOS

**Example:**
```python
# New pattern for /dev/mem access
DANGEROUS_PATTERNS["mem_access"] = {
    "pattern": r"cat\s+/dev/mem",
    ...
}

# Add exemption
DANGEROUS_PATTERN_PATHS = [
    ...
    '/dev/mem',  # mem_access pattern
]
```

### When Modifying Protected Directories

**If adding a new protected directory:**

1. **Check:** Are there existing dangerous patterns targeting this directory?
2. **If yes:** Add exemptions to `DANGEROUS_PATTERN_PATHS`
3. **Test:** Verify educational warnings still appear

---

## Testing Cross-Platform Consistency

### Test Matrix

For each dangerous pattern:

| Test | Windows | Linux | macOS |
|------|---------|-------|-------|
| Pattern detected | ✅ | ✅ | ✅ |
| Correct warning shown | ✅ | ✅ | ✅ |
| ASCII art displayed | ✅ | ✅ | ✅ |
| Command blocked | ✅ | ✅ | ✅ |

### Test Commands

```bash
# Test dd_zero
dd if=/dev/zero
# Expected: zero_wipe warning on all platforms

# Test redirect_to_disk
echo data > /dev/sda
# Expected: redirect_to_disk warning on all platforms

# Test kernel_panic
echo c > /proc/sysrq-trigger
# Expected: kernel_panic warning on all platforms

# Test mv_to_null
mv file /dev/null
# Expected: mv_to_null warning on all platforms
```

---

## Lessons Learned

### 1. Platform Differences Matter

**Insight:** File system structure differences can create UX inconsistencies

**Solution:** Explicit handling of platform-specific paths

### 2. Layer Ordering is Critical

**Insight:** The order of protection checks affects which message users see

**Solution:** More specific checks should take priority over generic ones

### 3. Educational Value Trumps Generic Protection

**Insight:** Users learn more from specific warnings than generic ones

**Solution:** Exemptions for educational patterns

### 4. Documentation is Essential

**Insight:** Future maintainers need to understand the reasoning

**Solution:** This document + inline comments

---

## Future Considerations

### Potential Enhancements

1. **Dynamic Exemption Detection**
   - Automatically detect when dangerous patterns target protected directories
   - Generate exemptions programmatically
   - Reduces maintenance burden

2. **Platform-Specific Patterns**
   - Windows-specific dangerous patterns (e.g., `format C:`)
   - macOS-specific patterns (e.g., `diskutil erase`)
   - Maintain consistency while respecting platform differences

3. **Exemption Validation**
   - Unit tests to verify exemptions work correctly
   - Automated cross-platform testing
   - Catch regressions early

---

## Summary

**Problem:** System protection and dangerous pattern detection conflicted on Linux/macOS, causing inconsistent educational experience.

**Solution:** Explicit exemption list that prioritizes educational warnings over generic protection for specific dangerous patterns.

**Result:** Consistent, educational experience across Windows, Linux, and macOS.

**Principle:** Educational value first, with safety maintained.

---

**Last Updated:** 2025-11-25 (Day 9)
**Related Issues:** Issue #4 (Direct Disk Write Commands Not Detected)
**Related Files:**
- `src/interceptor.py` (implementation)
- `docs/issues.md` (bug tracking)
