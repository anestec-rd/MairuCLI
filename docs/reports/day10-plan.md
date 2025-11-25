# Day 10 Plan: Data-Driven Refactoring and Critical Bug Fix

**Date:** 2025-11-26 (Planned)
**Estimated Time:** 3-4 hours
**Focus:** Data-driven architecture implementation, critical bug fix, and project completion planning

---

## 🎯 Session Goals

### Primary Goals
1. **Implement Data-Driven Pattern Loading** (High Priority)
2. **Fix Builtin Redirection Detection** (Critical - Issue #4)
3. **Plan Project Completion** (Timeline and scope)

### Secondary Goals (If Time Permits)
4. Educational breakdown implementation
5. Final testing and validation
6. Demo preparation

---

## 📋 Detailed Task Breakdown

### Phase 1: Data-Driven Refactoring (90 minutes)

**Priority:** HIGH
**Estimated Time:** 1.5 hours
**Reference:** `.kiro/specs/data-driven-patterns/`

#### Task 1.1: Add Pattern Field to JSON Files (20 min)
- [ ] Add `"pattern"` field to all entries in `warning_catalog.json`
- [ ] Migrate regex patterns from `interceptor.py`
- [ ] Ensure proper escaping (double backslashes in JSON)
- [ ] Validate JSON syntax

**Files:**
- `data/warnings/warning_catalog.json`

**Testing:**
- JSON syntax validation
- Pattern compilation test

---

#### Task 1.2: Create caution_catalog.json (15 min)
- [ ] Create new file `data/warnings/caution_catalog.json`
- [ ] Migrate all CAUTION_PATTERNS from `interceptor.py`
- [ ] Add `"pattern"` field to each entry
- [ ] Include risk, impact, and considerations fields

**Files:**
- `data/warnings/caution_catalog.json` (new)

---

#### Task 1.3: Implement PatternLoader Class (25 min)
- [ ] Create `PatternLoader` class in `interceptor.py`
- [ ] Implement `load_all_patterns()` method
- [ ] Implement `_load_dangerous_patterns()` method
- [ ] Implement `_load_caution_patterns()` method
- [ ] Add error handling for missing files

**Files:**
- `src/interceptor.py`

**Testing:**
- Unit test for pattern loading
- Error handling test

---

#### Task 1.4: Implement PatternCompiler Class (20 min)
- [ ] Create `PatternCompiler` class in `interceptor.py`
- [ ] Implement `compile_patterns()` method
- [ ] Implement `_compile_pattern_dict()` method
- [ ] Add error handling for invalid regex

**Files:**
- `src/interceptor.py`

**Testing:**
- Regex compilation test
- Invalid pattern handling test

---

#### Task 1.5: Refactor Interceptor (30 min)
- [ ] Create `CommandInterceptor` class
- [ ] Update `check_command()` to use compiled patterns
- [ ] Add backward compatibility layer
- [ ] Remove hardcoded pattern dictionaries
- [ ] Run all existing tests

**Files:**
- `src/interceptor.py`

**Testing:**
- All unit tests must pass
- Integration tests must pass
- Manual smoke test

---

### Phase 2: Critical Bug Fix - Issue #4 (60 minutes)

**Priority:** CRITICAL
**Estimated Time:** 1 hour
**Reference:** `docs/issues.md` Issue #4, `TODO.md`

#### Task 2.1: Add Redirection Target Extraction (20 min)
- [ ] Add `extract_redirection_target()` to `command_parser.py`
- [ ] Parse command for `>` redirection
- [ ] Extract target path
- [ ] Handle edge cases (quotes, spaces)

**Files:**
- `src/command_parser.py`

**Testing:**
- Unit test for various redirection patterns
- Edge case testing

---

#### Task 2.2: Add Redirection Check to process_command() (20 min)
- [ ] Add redirection check before builtin execution
- [ ] Check for dangerous targets:
  - `/dev/sd*` (disk devices)
  - `/proc/sysrq-trigger` (kernel panic)
  - `/dev/mem` (memory access)
- [ ] Block dangerous redirections
- [ ] Show appropriate warning

**Files:**
- `src/main.py`

**Testing:**
- Test `echo data > /dev/sda` → Blocked
- Test `cat file > /proc/sysrq-trigger` → Blocked
- Test `echo test > /tmp/file` → Allowed

---

#### Task 2.3: Integration Testing (20 min)
- [ ] Test all affected patterns
- [ ] Verify builtin commands still work
- [ ] Verify dangerous redirections blocked
- [ ] Update Issue #4 status to RESOLVED

**Files:**
- `docs/issues.md`
- `TODO.md`

---

### Phase 3: Help Command Auto-Generation (45 minutes)

**Priority:** MEDIUM
**Estimated Time:** 45 minutes
**Reference:** `.kiro/specs/data-driven-patterns/design.md`

#### Task 3.1: Add help_example and help_description to JSON (15 min)
- [ ] Add fields to all patterns in `warning_catalog.json`
- [ ] Add fields to all patterns in `caution_catalog.json`
- [ ] Ensure descriptions are concise (50 chars or less)

**Files:**
- `data/warnings/warning_catalog.json`
- `data/warnings/caution_catalog.json`

---

#### Task 3.2: Implement HelpGenerator Class (20 min)
- [ ] Create `HelpGenerator` class
- [ ] Implement `generate_dangerous_commands_help()`
- [ ] Implement `generate_caution_commands_help()`
- [ ] Group patterns by category

**Files:**
- `src/builtins/mairu_commands.py`

---

#### Task 3.3: Update help Command (10 min)
- [ ] Replace hardcoded list with `HelpGenerator`
- [ ] Add caution commands section
- [ ] Verify all patterns appear
- [ ] Test help output

**Files:**
- `src/builtins/mairu_commands.py`

---

### Phase 4: Project Completion Planning (30 minutes)

**Priority:** HIGH
**Estimated Time:** 30 minutes

#### Task 4.1: Assess Remaining Work
- [ ] Review all open issues
- [ ] Review TODO list
- [ ] Identify must-have vs. nice-to-have
- [ ] Estimate time for each remaining task

---

#### Task 4.2: Create Completion Timeline
- [ ] Define project completion criteria
- [ ] Set realistic deadline
- [ ] Prioritize remaining tasks
- [ ] Identify what to defer

---

#### Task 4.3: Update Documentation
- [ ] Update README.md if needed
- [ ] Update CHANGELOG.md
- [ ] Prepare demo script
- [ ] Document known limitations

---

## ⏱️ Time Allocation

| Phase | Task | Time | Priority |
|-------|------|------|----------|
| 1 | Data-Driven Refactoring | 90 min | HIGH |
| 2 | Critical Bug Fix (Issue #4) | 60 min | CRITICAL |
| 3 | Help Auto-Generation | 45 min | MEDIUM |
| 4 | Completion Planning | 30 min | HIGH |
| **Total** | | **225 min (3.75 hours)** | |

---

## 🎯 Success Criteria

### Must Complete
- ✅ Data-driven pattern loading working
- ✅ Issue #4 resolved (builtin redirection)
- ✅ All existing tests passing
- ✅ Project completion plan defined

### Should Complete
- ✅ Help command auto-generation
- ✅ Caution commands in help
- ✅ Documentation updated

### Nice to Have
- Educational breakdown implementation
- Additional test coverage
- Performance optimization

---

## 🚨 Risk Management

### Known Risks

**Risk 1: Refactoring Breaks Existing Functionality**
- **Mitigation:** Run tests after each step
- **Fallback:** Revert to previous commit

**Risk 2: Time Overrun**
- **Mitigation:** Prioritize critical tasks first
- **Fallback:** Defer nice-to-have features

**Risk 3: Test Coverage Gaps**
- **Mitigation:** Focus on critical path testing
- **Fallback:** Document known limitations

---

## 📊 Deferred Items

### Low Priority (Defer if Needed)
- [ ] Educational breakdown full implementation
- [ ] Additional achievement types
- [ ] Performance optimization
- [ ] Additional ASCII art variations
- [ ] Multi-language support

### Future Enhancements (Post-Demo)
- [ ] Configuration file support
- [ ] Custom pattern addition by users
- [ ] Statistics dashboard
- [ ] Plugin system

---

## 🎬 Demo Preparation Checklist

### Before Demo
- [ ] All critical issues resolved
- [ ] Core features working
- [ ] Cross-platform tested
- [ ] Demo script prepared
- [ ] Known limitations documented

### Demo Script
- [ ] Welcome banner
- [ ] Safe commands (ls, pwd, help)
- [ ] Dangerous commands (rm -rf /, chmod 777)
- [ ] Typo detection (sl, gi)
- [ ] Achievements
- [ ] Statistics

---

## 💭 Decision Points

### Question 1: Scope for Day 10
**Options:**
A. Complete all planned tasks (3.75 hours)
B. Focus on critical items only (2.5 hours)
C. Add educational breakdown (4.5 hours)

**Recommendation:** Option A - Complete all planned tasks

---

### Question 2: Project Completion
**Options:**
A. Aim for completion by Day 11
B. Extend to Day 12 for polish
C. Define MVP and defer enhancements

**Recommendation:** Option C - Define MVP, defer enhancements

---

### Question 3: Educational Breakdown
**Options:**
A. Implement in Day 10 (if time permits)
B. Defer to Day 11
C. Simplify scope

**Recommendation:** Option B - Defer to Day 11 if needed

---

## 📝 Notes

### Context from Day 9
- 5 major accomplishments completed
- 3 issues resolved
- 1 critical issue remaining (Issue #4)
- Comprehensive spec created for data-driven architecture

### Time Pressure Considerations
- Test coverage becoming challenging
- Need to balance features vs. completion
- Demo readiness is priority
- Documentation must be complete

### Quality Standards
- All tests must pass
- No regressions allowed
- Documentation must be current
- Known issues must be documented

---

## 🎯 Day 10 Objectives Summary

**Primary Focus:** Implement data-driven architecture and fix critical bug

**Success Metrics:**
- Data-driven pattern loading: ✅ Working
- Issue #4: ✅ Resolved
- Help auto-generation: ✅ Working
- Project plan: ✅ Defined

**Stretch Goals:**
- Educational breakdown started
- Additional test coverage
- Demo script polished

---

**Day 10 will be a critical implementation day. Focus on completing the data-driven refactoring and fixing the last critical bug to achieve a stable, demo-ready state.**
