# Time Tracking Standards

## Purpose

Ensure accurate time tracking for all development sessions and tasks.

---

## Automated Time Tracking Script

**MANDATORY: Use the time tracking script for all sessions**

### Script Location
`scripts/get_current_time.py`

### Required Usage

**At Session Start:**
```bash
python scripts/get_current_time.py start
```
This creates/updates `session_time.txt` with session start time.

**Before Each Commit:**
```bash
python scripts/get_current_time.py
```
This updates the current time in `session_time.txt`.

**To Get Session Times:**
```bash
python scripts/get_current_time.py get
```
This displays: `Session: HH:MM - HH:MM`

### Why Use the Script?

- ✅ Eliminates time estimation errors
- ✅ Provides accurate timestamps
- ✅ Consistent time format (HH:MM)
- ✅ Automatic session tracking
- ✅ Easy to use in commit messages

### Integration with Workflow

1. **Session Start:** Run `python scripts/get_current_time.py start`
2. **Work on tasks:** Script tracks time automatically
3. **Before commit:** Run `python scripts/get_current_time.py` to update
4. **In commit message:** Use times from `session_time.txt`

**Note:** `session_time.txt` is gitignored and not committed.

---

## Rules

### 1. Always Get Current Time

**NEVER estimate or calculate time manually.**

**ALWAYS use the time tracking script or system time.**

**Methods to get accurate time (in priority order):**
1. **Use time tracking script:** `python scripts/get_current_time.py`
2. Use system command: `Get-Date -Format "HH:mm"` (Windows) or `date +%H:%M` (Unix)
3. Ask user: "What is the current time?"

### 2. Record Time at Key Points

**Record time at:**
- Session start
- Phase/task start
- Phase/task completion
- Session end

**Format:**
```
Start: HH:MM
End: HH:MM
Duration: X minutes
```

### 3. Time Tracking in Commits

**Include accurate time in commit messages:**
```
Time: HH:MM - HH:MM (X minutes)
```

**Example:**
```
feat: Implement feature X

Time: 14:25 - 14:45 (20 minutes)
Status: Complete
```

### 4. Time Tracking in Summaries

**Always include:**
- Actual start time
- Actual end time
- Actual duration
- Estimated vs actual comparison (if estimate existed)

**Example:**
```
## Phase 1: Issue #4 Fix
- Estimated: 60 minutes
- Actual: 14:25 - 14:40 (15 minutes)
- Efficiency: 4x faster than estimated
```

---

## Common Mistakes to Avoid

### ❌ Don't: Estimate time without checking

**Bad:**
```
Time: ~30 minutes
Duration: approximately 45 minutes
```

### ✅ Do: Get exact time

**Good:**
```
Time: 14:25 - 14:45 (20 minutes)
```

---

### ❌ Don't: Calculate elapsed time mentally

**Bad:**
```
Started at 14:25, so it's been about 30 minutes...
```

### ✅ Do: Ask for current time

**Good:**
```
User, what is the current time?
Current: 14:45
Started: 14:25
Elapsed: 20 minutes
```

---

## Implementation

### At Session Start

```markdown
**Session Start:** [Ask user for time]
**Goals:** [List goals]
```

### At Task Completion

```markdown
**Task:** [Task name]
**Start:** [Recorded time]
**End:** [Ask user for current time]
**Duration:** [Calculate: End - Start]
**Status:** Complete/Incomplete
```

### At Session End

```markdown
**Session Summary:**
- Start: [Time]
- End: [Ask user for current time]
- Total Duration: [Calculate]
- Tasks Completed: [List]
- Efficiency: [Actual vs Estimated]
```

---

## Why This Matters

### Accurate Planning

- Learn actual time requirements
- Improve future estimates
- Identify bottlenecks

### Performance Tracking

- Measure productivity
- Identify efficient approaches
- Celebrate wins (faster than expected)

### Honest Reporting

- Build trust with accurate data
- No inflated or deflated times
- Clear accountability

---

## Summary

**Golden Rule:** Never guess time. Always ask or check.

**Process:**
1. Record start time (ask user)
2. Work on task
3. Record end time (ask user)
4. Calculate duration
5. Document accurately

**Remember:** Accurate time tracking helps everyone make better decisions.

---

**This steering file ensures honest and accurate time tracking for all development work.**
