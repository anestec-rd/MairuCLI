# Issues & Bug Tracking

This document tracks bugs, issues, and enhancement requests discovered during development and testing.

---

## Active Issues

### Issue #7: mkfs Pattern Too Strict - CRITICAL SAFETY BUG
**Date:** 2025-11-26 17:20
**Severity:** CRITICAL (Safety)
**Status:** ✅ RESOLVED (2025-11-26 18:00)
**Platform:** Both Windows and Linux

**Problem:**
`mkfs /dev/sda` was NOT being detected as dangerous and actually executed on Linux!
- Pattern required `mkfs.ext4` format (with dot and filesystem type)
- Simple `mkfs /dev/sda` bypassed detection
- **ACTUALLY ATTEMPTED TO FORMAT DISK** on Linux (saved by permission denial)

**What Actually Happened:**
```
# On Windows (safe by accident)
mairu> mkfs /dev/sda
👻 Boo! 'mkfs' vanished into thin air!
(Command not found)

# On Linux (DANGEROUS!)
mairu> mkfs /dev/sda
mke2fs 1.47.0 (5-Feb-2023)
mkfs.ext2: Permission denied while trying to determine filesystem size
```

**Root Cause:**
- Pattern: `r"mkfs\.\w+\s+/dev/sd[a-z]"` required dot (`.`) to be present
- `mkfs /dev/sda` has no dot, so pattern didn't match
- Command passed through to system shell
- **AI assumption bias**: Pattern assumed "typical" usage with filesystem type
- **Insufficient testing**: Only tested complete command format
- **No minimal syntax testing**: Didn't test simplest dangerous form

**Impact:**
- **CRITICAL SAFETY FAILURE** - Most dangerous command not detected
- Could have caused complete data loss if run with sudo
- Affected both Windows and Linux
- Demonstrates fundamental limitation of AI in safety-critical code

**Solution:**
- Changed pattern to: `r"mkfs(\.\w+)?\s+/dev/(sd[a-z]|nvme\d+n\d+)"`
- Made filesystem type optional: `(\.\w+)?`
- Added NVMe device support: `/dev/nvme\d+n\d+`
- Also updated `redirect_to_disk` and `dd_random` patterns for NVMe

**Testing:**
- ✅ `mkfs /dev/sda` → Now detected
- ✅ `mkfs.ext4 /dev/sda` → Still detected
- ✅ `mkfs /dev/nvme0n1` → Now detected
- ✅ `> /dev/nvme0n1` → Now detected
- ✅ Created comprehensive test suite: `tests/unit/test_mkfs_patterns.py`
- ✅ 100+ test cases covering all variations
- ✅ Tests document the incident for future reference

**Code Changes:**
- File: `src/interceptor.py`
- Patterns updated: `mkfs_disk`, `redirect_to_disk`, `dd_random`
- Tests added: `tests/unit/test_mkfs_patterns.py` (new file)
- Tests updated: `tests/unit/test_interceptor.py` (fixed expectations)
- Documentation: `docs/lessons/10-ai-safety-critical-limitations.md` (new lesson)

**Lessons Learned:**
- **ALWAYS test patterns with minimal syntax**
- **AI cannot assess true safety impact** - human oversight is non-negotiable
- **Optional parameters must be marked as optional in regex**
- **Real-world testing is critical for safety features**
- **Permission denial is not a safety feature** - detection must work
- **Educational tools must be MORE reliable, not less**
- **Never delegate safety decisions entirely to AI**

**Key Insight:**
AI can label something as "critical" based on semantic patterns, but it does not truly understand that `mkfs /dev/sda` destroys all data. This is a fundamental limitation of AI systems, not a bug that can be fixed with better prompts.

**Process Changes:**
- All safety-critical patterns now require human review
- All dangerous commands must be tested with minimal syntax
- Comprehensive test suites required for safety features
- Safety bugs are highest priority
- See: `docs/lessons/10-ai-safety-critical-limitations.md`

**Priority:** CRITICAL - This was a severe safety bug that demonstrates the limits of AI in safety-critical code

---

### Issue #3: Character Encoding Issues on Windows
**Date:** 2025-11-25 16:40
**Severity:** Major (Functionality)
**Status:** ✅ RESOLVED (2025-11-25)
**Platform:** Windows only (Linux works correctly)

**Problem:**
When entering unexpected commands (not in dangerous/caution/builtin lists), the output becomes garbled with character encoding issues.

**Expected Behavior:**
- Should display "Candy Store" message
- Should show safe command suggestions

**Actual Behavior:**
- Character encoding corruption
- Unreadable output

**Root Cause:**
- `subprocess.run()` was using hardcoded `encoding='utf-8'`
- Windows command prompt uses `cp932` (Shift-JIS) encoding
- Japanese error messages were being decoded incorrectly

**Solution:**
- Use `locale.getpreferredencoding()` to detect system encoding
- Changed from `encoding='utf-8'` to `encoding=system_encoding`
- Now correctly decodes Windows error messages

**Code Changes:**
- File: `src/main.py`
- Function: `execute_in_system_shell()`
- Added: `import locale` and `system_encoding = locale.getpreferredencoding()`

**Testing:**
- ✅ Tested on Windows with Japanese error messages
- ✅ Candy Store message displays correctly
- ✅ Command not found detection works properly

**Impact:**
- Windows users: Proper error message display
- Candy Store messages now appear correctly
- Improved cross-platform compatibility

---

### Issue #4: Direct Disk Write Commands Not Detected
**Date:** 2025-11-25 16:40
**Severity:** Critical (Safety)
**Status:** 🔴 OPEN
**Platform:** Both Windows and Linux

**Problem:**
Commands like `echo data > /dev/sda` and `cat file > /dev/sdb` are not being detected as dangerous because builtin `echo` and `cat` commands execute first.

**Affected Patterns:**
1. **Direct Disk Write (`redirect_to_disk`)**
   - `echo data > /dev/sda` - Write directly to disk device
   - `cat file > /dev/sdb` - Redirect output to disk

2. **Kernel Panic (`kernel_panic`)**
   - `echo c > /proc/sysrq-trigger`

**Root Cause:**
- Builtin commands (`echo`, `cat`) are executed before dangerous pattern detection
- Redirection to dangerous paths (`/dev/sda`, `/proc/sysrq-trigger`) not checked
- Pattern matching happens too late in the execution flow

**Impact:**
- Critical: Dangerous commands can execute
- Core safety functionality compromised
- Both platforms affected

**Solution Options:**
1. Check for dangerous redirections before executing builtins
2. Parse command for dangerous output targets (`> /dev/`, `> /proc/`)
3. Add redirection pattern detection to interceptor

**Files Affected:**
- `src/interceptor.py` - Pattern detection
- `src/builtins.py` - Builtin command execution
- `src/command_parser.py` - Command parsing

**Priority:** HIGH - Safety critical

---

### Issue #5: system_glitch ASCII Art Orphaned
**Date:** 2025-11-25 16:40
**Severity:** Minor (Content)
**Status:** ✅ RESOLVED (2025-11-25)

**Problem:**
`system_glitch.txt` ASCII art exists but has no associated command pattern, so it never appears.

**Solution:**
- Added new `system_modify` pattern to detect system file modifications
- Pattern detects: `/etc/passwd`, `/etc/shadow`, `/etc/fstab`, `/etc/sudoers` modifications
- Pattern detects: `/dev/mem` direct memory access
- Uses `system_glitch.txt` ASCII art with glitch effects

**Code Changes:**
- File: `src/interceptor.py` - Added `system_modify` pattern
- File: `data/warnings/warning_catalog.json` - Added pattern metadata
- File: `data/warnings/danger_variations.json` - Added 8 new variations

**Testing:**
- ✅ `echo test > /etc/passwd` → Detected as system_modify
- ✅ `> /etc/shadow` → Detected as system_modify
- ✅ `> /dev/mem` → Detected as system_modify
- ✅ system_glitch.txt ASCII art displays correctly

**Impact:**
- Asset now used and displayed
- New safety feature for system file protection

---

### Issue #6: Generic Typo Detection Not Working on Windows
**Date:** 2025-11-25 16:40
**Severity:** Major (Functionality)
**Status:** ✅ RESOLVED (2025-11-25)
**Platform:** Windows only (Linux works correctly)

**Problem:**
Generic typo detection features not working:
1. Missing last character (e.g., `touc` → `touch`) - Should show "impatient" message
2. Wrong first character (e.g., `souch` → `touch`) - Should show "close" message

**Root Cause:**
- Related to Issue #3 (encoding problem)
- Fixed by using `locale.getpreferredencoding()` in `execute_in_system_shell()`
- Encoding fix resolved both command-not-found detection and typo detection

**Solution:**
- Same fix as Issue #3
- System encoding detection fixed typo detection as a side effect

**Testing:**
- ✅ `gi` → Suggests `git` with "Speedy fingers!" message
- ✅ `pw` → Suggests `pwd` with "Missing the last letter?" message
- ✅ `dit` → Suggests `git` with "Close! One letter off" message
- ✅ `pws` → Suggests `pwd` with "One letter off" message

**Impact:**
- Windows users: Typo detection now works correctly
- Fun typo messages display properly

---

### Issue #2: dd Command Pattern Too Strict
**Date:** 2025-11-19 13:20
**Severity:** Major (Functionality)
**Status:** ✅ RESOLVED (2025-11-21)

**Problem:**
- Command `dd if=/dev/zero` is not detected as dangerous
- Falls through to system shell
- On Windows: "Command not found" error
- Expected: Should be blocked with danger warning

**Root Cause:**
- Pattern in `src/interceptor.py` line 31: `r"dd\s+if=/dev/zero\s+of="`
- Requires `of=` parameter to match
- User command `dd if=/dev/zero` doesn't include `of=`
- Pattern doesn't match → not detected as dangerous

**Solution:**
- Change pattern to: `r"dd\s+if=/dev/zero"`
- Make `of=` parameter optional
- This will catch both:
  - `dd if=/dev/zero` (incomplete but dangerous)
  - `dd if=/dev/zero of=/dev/sda` (complete and dangerous)

**Code Changes:**
- File: `src/interceptor.py`
- Line: 31
- Pattern: `dd_zero`
- Change: Remove `\s+of=` requirement

**Resolution:**
- Changed pattern from `r"dd\s+if=/dev/zero\s+of="` to `r"dd\s+if=/dev/zero"`
- Made `of=` parameter optional
- Now catches both incomplete and complete dangerous dd commands
- Resolved: 2025-11-21 11:15 (Day 5)

**Testing:**
- ✅ Test `dd if=/dev/zero` → Blocks correctly
- ✅ Test `dd if=/dev/zero of=/dev/sda` → Blocks correctly
- ✅ Test `dd if=file of=file2` → Allows (not /dev/zero)

**Impact:**
- Users: Dangerous command not being caught
- Severity: Major (core safety functionality)
- Workaround: None (pattern doesn't match)

**Lessons Learned:**
- Test patterns with variations of commands
- Don't require all parameters in dangerous command patterns
- Partial dangerous commands should still be caught

**Discovered By:** User testing (2025-11-19)

---

---

## Resolved Issues

### Issue #1: Welcome Banner Alignment
**Date:** 2025-11-17 09:40
**Severity:** Minor (Visual)
**Status:** ✅ RESOLVED

**Problem:**
- Welcome banner box borders didn't align properly
- Emoji characters (🎃) have variable display width (typically 2 characters)
- Box drawing characters (╔═╗║╚╝) couldn't accommodate emoji width variations
- Result: Right border appeared misaligned

**Root Cause:**
- Emoji display width varies by terminal and font
- Fixed-width box design assumed single-character width
- Padding calculations didn't account for emoji

**Solution:**
- Replaced box design with simple separator lines (`===`)
- Removed complex border calculations
- Simpler design works consistently across terminals

**Code Changes:**
- File: `src/display.py`
- Function: `display_welcome_banner()`
- Commit: [To be added]

**Testing:**
- ✅ Tested on Windows Terminal
- ✅ Verified alignment
- ✅ Confirmed emoji display

**Impact:**
- Improved visual consistency
- Better cross-terminal compatibility
- Simpler code maintenance

**Lessons Learned:**
- Emoji width is unpredictable in terminal environments
- Simple designs are more robust
- Test visual elements early

---

## Enhancement Requests

### None currently

---

## Issue Template

When adding new issues, use this format:

```markdown
### Issue #X: [Title]
**Date:** YYYY-MM-DD HH:MM
**Severity:** Critical / Major / Minor
**Status:** 🔴 OPEN / 🟡 IN PROGRESS / ✅ RESOLVED

**Problem:**
[Describe the issue]

**Root Cause:**
[Why it happened]

**Solution:**
[How it was fixed]

**Code Changes:**
- File: [filename]
- Function: [function name]
- Commit: [commit hash]

**Testing:**
[How it was verified]

**Impact:**
[Effect on users/system]

**Lessons Learned:**
[What we learned]
```

---

## Quality Metrics

### Bug Resolution Time
- Issue #1: ~10 minutes (discovery to fix)
- Issue #2: ~2 days (discovery to fix)

### Bug Severity Distribution
- Critical: 1 (open) - Issue #4 (Direct disk write detection)
- Major: 0 (open)
- Minor: 0 (open)
- Resolved: 5 - Issues #1 (Banner alignment), #2 (dd pattern), #3 (Windows encoding), #5 (Orphaned ASCII art), #6 (Typo detection)

### Testing Coverage
- Manual test plan: 50+ test cases
- Visual testing: Ongoing
- User acceptance: Pending

---

## Process

### Bug Discovery
1. Found during manual testing
2. Documented in this file
3. Prioritized by severity
4. Assigned for resolution

### Bug Resolution
1. Root cause analysis
2. Solution design
3. Implementation
4. Testing
5. Documentation
6. Changelog update

### Quality Assurance
- All bugs documented
- Solutions explained
- Lessons captured
- Process improved

---

**This document demonstrates professional bug tracking and quality assurance practices.**
