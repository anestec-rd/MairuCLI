# Day 11 Plan: Data-Driven Architecture & Critical Bug Fix

**Date:** 2025-11-26 (Planned)
**Estimated Time:** 3-4 hours
**Focus:** Complete data-driven refactoring and resolve Issue #4

---

## 📋 Context from Day 10

**What Happened on Day 10:**
- 30-minute critical bug fix session
- Fixed mkfs pattern (Issue #7)
- Created comprehensive test suite
- Documented fundamental AI safety limitations (Lesson 10)

**What Was Deferred:**
- Data-driven pattern loading (from original Day 10 plan)
- Issue #4: Builtin redirection detection
- Help command auto-generation
- Project completion planning

**Current Status:**
- ✅ All 157 tests passing
- ✅ Critical safety bug fixed
- ⚠️ Issue #4 still open (CRITICAL)
- ⚠️ Data-driven architecture not implemented

---

## 🎯 Day 11 Goals

### Primary Goals (Must Complete)

1. **Fix Issue #4: Builtin Redirection Detection** (CRITICAL)
   - Commands like `echo data > /dev/sda` not detected
   - Builtin commands execute before pattern detection
   - Core safety functionality compromised

2. **Implement Data-Driven Pattern Loading** (HIGH)
   - Move patterns from code to JSON
   - Enable easier pattern management
   - Foundation for future extensibility

3. **Project Completion Planning** (HIGH)
   - Define MVP scope
   - Set realistic timeline
   - Identify what to defer

### Secondary Goals (If Time Permits)

4. Help command auto-generation
5. Additional test coverage
6. Demo preparation

---

## 📋 Detailed Task Breakdown

### Phase 1: Critical Bug Fix - Issue #4 (60 minutes)

**Priority:** CRITICAL
**Estimated Time:** 1 hour
**Why First:** Safety-critical functionality

#### Background

**Problem:**
```bash
mairu> echo data > /dev/sda
# Currently: Builtin echo executes, writes to disk!
# Expected: Should be blocked with critical warning
```

**Root Cause:**
- Builtin commands execute before dangerous pattern detection
- Redirection to dangerous paths not checked
- Pattern matching happens too late

**Affected Commands:**
- `echo data > /dev/sda` - Direct disk write
- `cat file > /dev/sdb` - Redirect to disk
- `echo c > /proc/sysrq-trigger` - Kernel panic

---

#### Task 1.1: Add Redirection Detection to Command Parser (20 min)

**Goal:** Extract redirection targets from commands

**Implementation:**
```python
# In src/command_parser.py

def extract_redirection_target(self, command: str) -> Optional[str]:
    """
    Extract output redirection target from command.

    Examples:
        "echo test > /dev/sda" → "/dev/sda"
        "cat file > /tmp/out" → "/tmp/out"
        "ls -la" → None

    Returns:
        Target path if redirection found, None otherwise
    """
    # Parse for > redirection
    # Handle quotes and spaces
    # Return target path
```

**Testing:**
- `echo test > /dev/sda` → `/dev/sda`
- `cat file > /tmp/out` → `/tmp/out`
- `echo "test" > "/path with spaces"` → `/path with spaces`
- `ls -la` → `None`

**Files:**
- `src/command_parser.py`
- `tests/unit/test_command_parser.py`

---

#### Task 1.2: Add Redirection Check Before Builtin Execution (25 min)

**Goal:** Check for dangerous redirections before executing builtins

**Implementation:**
```python
# In src/main.py - process_command()

# Before executing builtin:
redirection_target = parser.extract_redirection_target(command)
if redirection_target:
    # Check if target is dangerous
    dangerous_targets = [
        r'/dev/sd[a-z]',      # SATA disks
        r'/dev/nvme\d+n\d+',  # NVMe disks
        r'/proc/sysrq-trigger', # Kernel panic
        r'/dev/mem',          # Memory access
        r'/etc/passwd',       # System files
        r'/etc/shadow',
        # ... other critical paths
    ]

    for pattern in dangerous_targets:
        if re.match(pattern, redirection_target):
            # Block and show warning
            level = "critical"
            pattern_name = "redirect_to_disk" # or appropriate
            # Show danger warning
            return
```

**Testing:**
- ✅ `echo data > /dev/sda` → Blocked
- ✅ `cat file > /proc/sysrq-trigger` → Blocked
- ✅ `echo test > /tmp/file` → Allowed
- ✅ Builtin commands without redirection still work

**Files:**
- `src/main.py`
- `tests/integration/test_builtin_redirection.py` (new)

---

#### Task 1.3: Integration Testing & Documentation (15 min)

**Testing:**
- Run all existing tests
- Add new integration tests
- Manual testing of affected commands
- Cross-platform testing (Windows/Linux)

**Documentation:**
- Update Issue #4 status to RESOLVED
- Update TODO.md
- Add to CHANGELOG.md
- Document in day11-summary.md

**Files:**
- `docs/issues.md`
- `TODO.md`
- `CHANGELOG.md`

---

### Phase 2: Data-Driven Pattern Loading (90 minutes)

**Priority:** HIGH
**Estimated Time:** 1.5 hours
**Reference:** `.kiro/specs/data-driven-patterns/`

#### Why This Matters

**Current State:**
- Patterns hardcoded in `interceptor.py`
- ~200 lines of pattern definitions
- Difficult to maintain and extend
- No separation of data and logic

**Target State:**
- Patterns in JSON files
- Easy to add new patterns
- Non-developers can contribute
- Clear separation of concerns

---

#### Task 2.1: Add Pattern Field to warning_catalog.json (20 min)

**Goal:** Migrate regex patterns from code to JSON

**Before:**
```python
# In interceptor.py
"rm_dangerous": {
    "pattern": r"rm\s+(-rf|-fr|-r\s+-f|-f\s+-r)\s+(/|~|\$HOME|\*|\.(?:\s|$)|\$\w+)",
    "category": "deletion",
    ...
}
```

**After:**
```json
// In data/warnings/warning_catalog.json
{
  "rm_dangerous": {
    "pattern": "rm\\s+(-rf|-fr|-r\\s+-f|-f\\s+-r)\\s+(/|~|\\$HOME|\\*|\\.(?:\\s|$)|\\$\\w+)",
    "category": "deletion",
    "severity": "critical",
    ...
  }
}
```

**Important:** Double backslashes in JSON!

**Files:**
- `data/warnings/warning_catalog.json`

**Testing:**
- JSON syntax validation
- Pattern compilation test

---

#### Task 2.2: Create caution_catalog.json (15 min)

**Goal:** Separate caution patterns into their own file

**Structure:**
```json
{
  "sudo_shell": {
    "pattern": "sudo\\s+(su|bash|sh|-i)(?:\\s|$)",
    "category": "privilege_escalation",
    "severity": "medium",
    "risk": "Entering root shell - all safety checks disabled",
    "impact": "One mistake could damage the entire system",
    "considerations": [
      "Do you really need full root access?",
      "Could you use 'sudo command' instead?",
      "Are you in the right directory?"
    ]
  },
  ...
}
```

**Files:**
- `data/warnings/caution_catalog.json` (new)

---

#### Task 2.3: Implement Pattern Loader (25 min)

**Goal:** Load patterns from JSON files

**Implementation:**
```python
# In src/interceptor.py

class PatternLoader:
    """Load patterns from JSON files."""

    def __init__(self, data_dir: str = "data/warnings"):
        self.data_dir = data_dir

    def load_all_patterns(self) -> Tuple[Dict, Dict]:
        """Load all patterns from JSON files."""
        dangerous = self._load_dangerous_patterns()
        caution = self._load_caution_patterns()
        return dangerous, caution

    def _load_dangerous_patterns(self) -> Dict:
        """Load dangerous patterns from warning_catalog.json."""
        # Load JSON
        # Validate structure
        # Return pattern dict

    def _load_caution_patterns(self) -> Dict:
        """Load caution patterns from caution_catalog.json."""
        # Load JSON
        # Validate structure
        # Return pattern dict
```

**Error Handling:**
- Missing files
- Invalid JSON
- Missing required fields
- Invalid regex patterns

**Files:**
- `src/interceptor.py`
- `tests/unit/test_pattern_loader.py` (new)

---

#### Task 2.4: Implement Pattern Compiler (20 min)

**Goal:** Compile regex patterns for performance

**Implementation:**
```python
class PatternCompiler:
    """Compile regex patterns for efficient matching."""

    def compile_patterns(self, patterns: Dict) -> Dict:
        """Compile all patterns in dictionary."""
        compiled = {}
        for name, data in patterns.items():
            try:
                data['compiled'] = re.compile(
                    data['pattern'],
                    re.IGNORECASE
                )
                compiled[name] = data
            except re.error as e:
                # Log error, skip pattern
                print(f"Warning: Invalid pattern {name}: {e}")
        return compiled
```

**Files:**
- `src/interceptor.py`
- `tests/unit/test_pattern_compiler.py` (new)

---

#### Task 2.5: Refactor check_command() (30 min)

**Goal:** Use loaded patterns instead of hardcoded ones

**Implementation:**
```python
# Load patterns at module level
_loader = PatternLoader()
_compiler = PatternCompiler()
DANGEROUS_PATTERNS, CAUTION_PATTERNS = _loader.load_all_patterns()
DANGEROUS_PATTERNS = _compiler.compile_patterns(DANGEROUS_PATTERNS)
CAUTION_PATTERNS = _compiler.compile_patterns(CAUTION_PATTERNS)

def check_command(command: str) -> Tuple[str, str]:
    """Check command using loaded patterns."""
    # Use compiled patterns
    # Same logic as before
    # Backward compatible
```

**Testing:**
- All existing tests must pass
- No regressions
- Performance should be same or better

**Files:**
- `src/interceptor.py`
- All existing test files

---

### Phase 3: Project Completion Planning (30 minutes)

**Priority:** HIGH
**Estimated Time:** 30 minutes

#### Task 3.1: Assess Current State (10 min)

**Review:**
- Open issues (check `docs/issues.md`)
- TODO items (check `TODO.md`)
- Test coverage
- Documentation completeness
- Cross-platform compatibility

**Questions:**
- What is absolutely required for MVP?
- What can be deferred?
- What is the realistic timeline?

---

#### Task 3.2: Define MVP Scope (10 min)

**Must Have (MVP):**
- ✅ All critical dangerous commands detected
- ✅ Caution-level warnings working
- ✅ Typo detection working
- ✅ Achievements system
- ✅ Statistics tracking
- ✅ Cross-platform support (Windows/Linux)
- ⚠️ Issue #4 resolved
- ⚠️ All tests passing
- ⚠️ Documentation complete

**Nice to Have (Post-MVP):**
- Educational breakdown
- Additional achievements
- Configuration file support
- Multi-language support
- Plugin system

---

#### Task 3.3: Create Timeline (10 min)

**Proposed Timeline:**
- **Day 11 (Today):** Complete data-driven refactoring + Issue #4
- **Day 12:** Polish, testing, documentation
- **Day 13:** Demo preparation, final testing
- **Demo Day:** Present MairuCLI

**Deliverables:**
- Working demo
- Complete documentation
- Test coverage report
- Known limitations documented

---

### Phase 4: Help Command Auto-Generation (45 minutes)

**Priority:** MEDIUM
**Estimated Time:** 45 minutes
**Condition:** If time permits after Phase 1-3

#### Task 4.1: Add Help Fields to JSON (15 min)

**Add to each pattern:**
```json
{
  "rm_dangerous": {
    "pattern": "...",
    "help_example": "rm -rf /",
    "help_description": "Recursive deletion of critical paths",
    ...
  }
}
```

**Files:**
- `data/warnings/warning_catalog.json`
- `data/warnings/caution_catalog.json`

---

#### Task 4.2: Implement HelpGenerator (20 min)

**Goal:** Auto-generate help text from patterns

**Implementation:**
```python
class HelpGenerator:
    """Generate help text from pattern catalogs."""

    def generate_dangerous_commands_help(self) -> str:
        """Generate dangerous commands section."""
        # Load patterns
        # Group by category
        # Format output

    def generate_caution_commands_help(self) -> str:
        """Generate caution commands section."""
        # Similar to above
```

**Files:**
- `src/builtins/mairu_commands.py`

---

#### Task 4.3: Update help Command (10 min)

**Replace hardcoded list with generated content**

**Files:**
- `src/builtins/mairu_commands.py`
- `tests/integration/test_help.py`

---

## ⏱️ Time Allocation

| Phase | Task | Time | Priority |
|-------|------|------|----------|
| 1 | Issue #4 Fix | 60 min | CRITICAL |
| 2 | Data-Driven Refactoring | 90 min | HIGH |
| 3 | Completion Planning | 30 min | HIGH |
| 4 | Help Auto-Generation | 45 min | MEDIUM |
| **Total** | | **225 min (3.75 hours)** | |

---

## 🎯 Success Criteria

### Must Complete
- ✅ Issue #4 resolved (builtin redirection)
- ✅ Data-driven pattern loading working
- ✅ All existing tests passing
- ✅ Project completion plan defined

### Should Complete
- ✅ Help command auto-generation
- ✅ Documentation updated
- ✅ CHANGELOG updated

### Nice to Have
- Additional test coverage
- Performance optimization
- Demo script prepared

---

## 🚨 Risk Management

### Risk 1: Refactoring Breaks Existing Functionality
**Mitigation:** Run tests after each step
**Fallback:** Revert to previous commit

### Risk 2: Issue #4 More Complex Than Expected
**Mitigation:** Start with Issue #4 (highest priority)
**Fallback:** Defer data-driven refactoring if needed

### Risk 3: Time Overrun
**Mitigation:** Prioritize critical tasks first
**Fallback:** Defer help auto-generation

---

## 📝 Notes

### Lessons from Day 10

**What We Learned:**
- AI cannot assess true safety impact
- Human oversight is non-negotiable
- Always test minimal syntax
- Safety bugs are highest priority

**How This Affects Day 11:**
- Extra scrutiny on Issue #4 fix
- Comprehensive testing required
- Human review of all safety code
- Document assumptions and limitations

### Quality Standards

- All tests must pass
- No regressions allowed
- Safety-critical code requires human review
- Documentation must be current

---

## 🎯 Day 11 Objectives Summary

**Primary Focus:** Fix critical bug and implement data-driven architecture

**Success Metrics:**
- Issue #4: ✅ Resolved
- Data-driven loading: ✅ Working
- All tests: ✅ Passing
- Project plan: ✅ Defined

**Stretch Goals:**
- Help auto-generation
- Additional test coverage
- Demo preparation started

---

**Day 11 will complete the core architecture and resolve the last critical safety bug. After this, MairuCLI will be feature-complete and ready for polish and demo preparation.**
