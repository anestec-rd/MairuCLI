# Day 7 Plan - Manual Testing, Safety Review & Additional Features

**Date:** 2025-11-23 (Sunday)
**Start Time:** 21:30
**Focus:** Complete system directory protection (Tasks 10, 12) + Stock task review

---

## Overview

Day 7 will complete the system directory protection feature with manual testing and safety review, then address additional tasks from the stock task list.

---

## Priority Tasks

### 🔴 Critical Priority: System Directory Protection Completion

#### Task 10: Manual Testing and Validation
**Status:** Not Started
**Estimated Time:** 20 minutes
**Requirements:** 7.1, 10.4

**Test Scenarios:**
1. **Windows System Directory Tests** (Safe commands only!)
   - [ ] Test: `echo test > C:\Windows\test.txt` (should block - critical)
   - [ ] Test: `rm C:\Windows\System32\test.dll` (should block - critical)
   - [ ] Test: `mv test.txt C:\Program Files\test.txt` (should warn - caution)
   - [ ] Test: `chmod 777 C:\Windows` (should block - critical)
   - [ ] Test: `rm ../../Windows/test.txt` (relative path - should block)
   - [ ] Test: `rm $WINDIR\test.txt` (environment variable - should block)
   - [ ] Test: `rm C:\Windows\*.dll` (wildcard - should block)

2. **Linux System Directory Tests** (Safe commands only!)
   - [ ] Test: `rm /etc/test.conf` (should block - critical)
   - [ ] Test: `mv test.txt /bin/test` (should block - critical)
   - [ ] Test: `chmod 777 /usr/bin/test` (should warn - caution)
   - [ ] Test: `rm ../../../etc/test` (relative path - should block)
   - [ ] Test: `rm $HOME/../../../etc/test` (environment variable - should block)

3. **Edge Cases**
   - [ ] Test: Mixed path separators (C:/Windows/System32)
   - [ ] Test: Case variations (c:\windows\system32)
   - [ ] Test: Spaces in paths ("C:\Program Files\test")
   - [ ] Test: Unicode characters in paths
   - [ ] Test: Very long paths

4. **Performance Verification**
   - [ ] Measure: Path resolution time (< 10ms target)
   - [ ] Measure: Command parsing time (< 10ms target)
   - [ ] Measure: Total check time (< 50ms target)
   - [ ] Verify: No noticeable delay in command processing

5. **Educational Message Verification**
   - [ ] Verify: Messages are clear and understandable
   - [ ] Verify: Safe alternatives are provided
   - [ ] Verify: Halloween theme is maintained
   - [ ] Verify: Age-appropriate language

#### Task 12: Final Safety Review
**Status:** Not Started
**Estimated Time:** 10 minutes
**Requirements:** 8.1, 8.2, 8.3, 8.4, 8.5

**Review Checklist:**
1. **Fail-Safe Mechanisms**
   - [ ] Review: Path resolution error handling
   - [ ] Review: Command parsing error handling
   - [ ] Review: Platform detection fallback
   - [ ] Verify: "When in doubt, block" principle applied

2. **Bypass Prevention**
   - [ ] Test: Symbolic link bypass attempts
   - [ ] Test: Path traversal bypass attempts (../../..)
   - [ ] Test: Environment variable bypass attempts
   - [ ] Test: Wildcard bypass attempts
   - [ ] Test: Case variation bypass attempts (Windows)

3. **Error Handling**
   - [ ] Test: Invalid path input
   - [ ] Test: Permission denied errors
   - [ ] Test: Non-existent path input
   - [ ] Test: Malformed command input
   - [ ] Verify: All errors handled gracefully

4. **Cross-Platform Compatibility**
   - [ ] Verify: Windows tests pass on Windows
   - [ ] Verify: Linux tests pass on Linux
   - [ ] Verify: Platform detection works correctly
   - [ ] Verify: Path separator handling is correct

5. **Code Review**
   - [ ] Review: PathResolver implementation
   - [ ] Review: CommandParser implementation
   - [ ] Review: check_system_directory implementation
   - [ ] Review: Integration in main.py
   - [ ] Verify: No security vulnerabilities

**After Completion:**
- [ ] Tag version v1.2.0
- [ ] Update CHANGELOG.md with v1.2.0 release notes
- [ ] Update README.md if needed

---

## 🟡 Medium Priority: Stock Task Items

### 1. Hook Testing
**Task:** "Hookを追加したので動作確認したい" (Test the hooks we added)
**Status:** Not Started
**Estimated Time:** 10 minutes

**Actions:**
- [ ] Manually register hooks via Kiro UI
- [ ] Test: run-unit-tests.kiro.hook
- [ ] Test: run-integration-tests.kiro.hook
- [ ] Test: test-system-protection.kiro.hook
- [ ] Document: How to use hooks in README or docs

### 2. Magic Number Constants
**Task:** "マジックナンバーの定数化" (Convert magic numbers to constants)
**Status:** Not Started
**Estimated Time:** 5-7 minutes (Phase 1 only)
**Reference:** See `docs/reports/MAGIC_NUMBERS_ANALYSIS.md` for detailed analysis

**Phase 1: Timing Constants (Day 7 - High Priority)**
- [ ] Add timing constants to `src/config.py`
  - TIMING_ASCII_CHAR_DELAY = 0.05
  - TIMING_PAUSE_SHORT = 0.3
  - TIMING_PAUSE_MEDIUM = 0.5
- [ ] Update `src/display/ascii_renderer.py` (1 instance)
- [ ] Update `src/display/warning_components.py` (4 instances)
- [ ] Update `src/display/achievements.py` (2 instances)
- [ ] Run tests to verify no functional changes

**Phase 2: Achievement Thresholds (Deferred to Day 8)**
- [ ] Add achievement threshold constants to `src/display/achievements.py`
- [ ] Update all achievement checks (8-10 instances)

**Phase 3: Display Formatting (Deferred to Day 8)**
- [ ] Add display constants to `src/config.py`
- [ ] Update separator lines in 4 files
- [ ] Update quote check in `src/command_parser.py`

**Note:** Phase 1 provides the highest impact with minimal time investment. Phases 2-3 can be completed later.

### 3. Expand Normal Commands
**Task:** "平常版のコマンドをもう少し充実" (Expand normal/safe commands)
**Status:** Not Started
**Estimated Time:** 20 minutes

**Current Builtins:**
- pwd, cd, ls, echo, clear, exit, help, stats, achievements

**Potential Additions:**
- [ ] whoami - Show current user
- [ ] date - Show current date/time
- [ ] history - Show command history
- [ ] alias - Create command aliases
- [ ] env - Show environment variables (filtered)

**Considerations:**
- Keep educational focus
- Maintain Halloween theme
- Don't duplicate system commands unnecessarily

### 4. chmod -R 000 Pattern
**Task:** "chmod -R 000 何も操作できなくなる" (Add chmod -R 000 pattern)
**Status:** Not Started
**Estimated Time:** 10 minutes

**Actions:**
- [ ] Add pattern to DANGEROUS_PATTERNS in interceptor.py
- [ ] Add warning message to warning_catalog.json
- [ ] Add variations to danger_variations.json
- [ ] Add unit test to test_interceptor.py
- [ ] Test manually

---

## 🟢 Low Priority: Polish & Enhancement

### 1. Top Page ASCII Art
**Task:** "トップページのAA（まだ暫定的）" (Top page ASCII art is still temporary)
**Status:** Deferred
**Note:** Can be done later if time permits

### 2. Timing Adjustments
**Task:** "もう少し演出時間の間を長めにする" (Make dramatic timing longer)
**Status:** Deferred
**Note:** Can be manually adjusted later

### 3. More Intense ASCII Art
**Task:** "AAをもう少し鬼気せまるものに" (Make ASCII art more intense)
**Status:** Deferred
**Note:** Conflicts with "Halloween party, not horror" theme - discuss first

### 4. Achievement for Normal Commands
**Task:** "正常コマンドを一通りやった際にも称号が欲しい" (Achievement for using all normal commands)
**Status:** Deferred
**Note:** Good idea for future enhancement

### 5. Hidden Horror Command
**Task:** "本格ホラーみたいな展開を迎える隠しコマンドがあっても良いかも"
**Status:** Deferred
**Note:** Fun easter egg idea, but low priority

---

## Deferred/Questionable Tasks

### lie Command
**Task:** "lieコマンドの追加" (Add 'lie' command that inverts true/false in files)
**Status:** Deferred
**Reason:** "これが教育的か？" (Is this educational?)

**Analysis:**
- Interesting concept (cat variant that inverts opposites)
- Questionable educational value
- Could be confusing rather than helpful
- Recommend: Defer or skip

**Decision:** Skip for now, revisit if time permits and educational value can be justified

---

## Time Allocation (90 minutes total)

| Task | Time | Priority |
|------|------|----------|
| Task 10: Manual Testing | 20 min | Critical |
| Task 12: Safety Review | 10 min | Critical |
| Version Tagging (v1.2.0) | 5 min | Critical |
| Hook Testing | 10 min | Medium |
| Magic Number Constants (Phase 1) | 7 min | Medium |
| chmod -R 000 Pattern | 10 min | Medium |
| Expand Normal Commands | 20 min | Medium |
| **Total** | **82 min** | |

**Note:** Magic numbers Phase 2 & 3 (10 min) deferred to Day 8

---

## Success Criteria

### Must Complete (Critical)
- [x] Task 10: Manual testing completed
- [x] Task 12: Safety review passed
- [x] Version v1.2.0 tagged
- [x] All tests passing
- [x] No security vulnerabilities found

### Should Complete (Medium)
- [ ] Hooks tested and documented
- [ ] Magic numbers converted to constants
- [ ] chmod -R 000 pattern added

### Nice to Have (Low)
- [ ] Normal commands expanded
- [ ] Documentation polished

---

## Risk Assessment

### High Risk Items
1. **Manual Testing Failures**
   - Risk: Tests reveal bugs or bypass methods
   - Mitigation: Fix immediately, re-test thoroughly
   - Fallback: Revert to v1.1 if critical issues found

2. **Safety Review Failures**
   - Risk: Security vulnerabilities discovered
   - Mitigation: Fix before tagging v1.2.0
   - Fallback: Defer release until fixed

### Medium Risk Items
1. **Time Overrun**
   - Risk: Tasks take longer than estimated
   - Mitigation: Prioritize critical tasks first
   - Fallback: Defer medium/low priority tasks

2. **Hook Registration Issues**
   - Risk: Hooks don't work as expected
   - Mitigation: Document issues, provide workarounds
   - Fallback: Keep hooks as templates only

---

## Next Steps After Day 7

### If All Tasks Complete
1. Prepare demo video/presentation
2. Polish documentation
3. Consider additional features from stock tasks
4. Plan Day 8 activities

### If Critical Tasks Only
1. Complete medium priority tasks in Day 8
2. Focus on polish and documentation
3. Prepare for final demo

---

## Notes

- **Safety First:** Never compromise on safety for speed
- **Test Thoroughly:** Manual testing is critical for safety features
- **Document Everything:** Keep track of what works and what doesn't
- **Ask for Help:** If unsure about safety, ask for review

---

**Ready to begin Day 7 with focus on safety and quality.**
