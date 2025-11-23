# System Directory Protection - Manual Testing Checklist

**Date:** 2025-11-23 (Day 7)
**Task:** Task 10 - Manual Testing and Validation
**Tester:** _________________
**Platform:** Windows / Linux / macOS (circle one)

---

## Pre-Test Setup

- [ ] Ensure all unit tests pass: `python -m pytest tests/unit/ -v`
- [ ] Ensure all integration tests pass: `python -m pytest tests/integration/ -v`
- [ ] Backup any important data (precaution)
- [ ] Have terminal ready for testing

---

## Automated Test Script

### Run Automated Tests

```bash
python tests/manual/test_system_protection_manual.py
```

- [ ] All platform-specific tests passed
- [ ] All edge case tests passed
- [ ] Performance test passed (< 50ms average)
- [ ] No unexpected errors or crashes

**Notes:**
```
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________
```

---

## Manual Interactive Testing

### Test 1: Windows System32 Protection (Windows only)

**Command to test in MairuCLI:**
```
mairu> echo test > C:\Windows\System32\test.txt
```

**Expected Behavior:**
- [ ] Command is blocked immediately
- [ ] Critical warning displayed
- [ ] ASCII art shown (data_destroyer.txt or similar)
- [ ] Educational message explains why it's dangerous
- [ ] Safe alternative provided
- [ ] No actual file created

**Actual Behavior:**
```
_________________________________________________________________
_________________________________________________________________
```

---

### Test 2: Linux /etc Protection (Linux only)

**Command to test in MairuCLI:**
```
mairu> rm /etc/test.conf
```

**Expected Behavior:**
- [ ] Command is blocked immediately
- [ ] Critical warning displayed
- [ ] ASCII art shown
- [ ] Educational message explains why it's dangerous
- [ ] Safe alternative provided
- [ ] No actual file deleted

**Actual Behavior:**
```
_________________________________________________________________
_________________________________________________________________
```

---

### Test 3: Program Files Caution (Windows only)

**Command to test in MairuCLI:**
```
mairu> mv test.txt "C:\Program Files\test.txt"
```

**Expected Behavior:**
- [ ] Caution warning displayed
- [ ] User prompted for confirmation (y/n)
- [ ] Explanation of risks shown
- [ ] If 'n' entered, command cancelled
- [ ] If 'y' entered, command proceeds (but will fail safely - file doesn't exist)

**Actual Behavior:**
```
_________________________________________________________________
_________________________________________________________________
```

---

### Test 4: /usr Caution (Linux only)

**Command to test in MairuCLI:**
```
mairu> chmod 777 /usr/bin/test
```

**Expected Behavior:**
- [ ] Caution warning displayed
- [ ] User prompted for confirmation (y/n)
- [ ] Explanation of risks shown
- [ ] If 'n' entered, command cancelled
- [ ] If 'y' entered, command proceeds (but will fail safely - file doesn't exist)

**Actual Behavior:**
```
_________________________________________________________________
_________________________________________________________________
```

---

### Test 5: Relative Path Detection

**Command to test in MairuCLI:**
```
# Windows:
mairu> rm ..\..\Windows\test.txt

# Linux:
mairu> rm ../../../etc/test.conf
```

**Expected Behavior:**
- [ ] Relative path resolved to absolute path
- [ ] System directory detected
- [ ] Critical warning displayed
- [ ] Command blocked

**Actual Behavior:**
```
_________________________________________________________________
_________________________________________________________________
```

---

### Test 6: Environment Variable Expansion

**Command to test in MairuCLI:**
```
# Windows:
mairu> rm $WINDIR\test.txt

# Linux:
mairu> rm $HOME/../../../etc/test
```

**Expected Behavior:**
- [ ] Environment variable expanded
- [ ] System directory detected
- [ ] Critical warning displayed
- [ ] Command blocked

**Actual Behavior:**
```
_________________________________________________________________
_________________________________________________________________
```

---

### Test 7: Wildcard Detection

**Command to test in MairuCLI:**
```
# Windows:
mairu> rm C:\Windows\*.dll

# Linux:
mairu> rm /etc/*.conf
```

**Expected Behavior:**
- [ ] Wildcard detected in system directory
- [ ] Critical warning displayed
- [ ] Command blocked
- [ ] Warning mentions wildcard danger

**Actual Behavior:**
```
_________________________________________________________________
_________________________________________________________________
```

---

### Test 8: Safe User Directory

**Command to test in MairuCLI:**
```
# Windows:
mairu> rm C:\Users\TestUser\test.txt

# Linux:
mairu> rm /home/testuser/test.txt
```

**Expected Behavior:**
- [ ] No system directory warning
- [ ] Normal dangerous pattern check applies (if rm -rf)
- [ ] Command proceeds to system shell
- [ ] Fails gracefully (file doesn't exist)

**Actual Behavior:**
```
_________________________________________________________________
_________________________________________________________________
```

---

### Test 9: Mixed Path Separators (Windows only)

**Command to test in MairuCLI:**
```
mairu> rm C:/Windows/System32/test.dll
```

**Expected Behavior:**
- [ ] Forward slashes normalized to backslashes
- [ ] System directory detected
- [ ] Critical warning displayed
- [ ] Command blocked

**Actual Behavior:**
```
_________________________________________________________________
_________________________________________________________________
```

---

### Test 10: Case Insensitivity (Windows only)

**Command to test in MairuCLI:**
```
mairu> rm c:\windows\system32\test.dll
```

**Expected Behavior:**
- [ ] Case variations handled correctly
- [ ] System directory detected
- [ ] Critical warning displayed
- [ ] Command blocked

**Actual Behavior:**
```
_________________________________________________________________
_________________________________________________________________
```

---

## Educational Message Quality

### Message Clarity

- [ ] Messages are easy to understand
- [ ] Language is age-appropriate (suitable for children/beginners)
- [ ] Technical terms are explained
- [ ] No jargon without explanation

### Message Content

- [ ] Explains WHAT the directory contains
- [ ] Explains WHY it's dangerous
- [ ] Provides SAFE alternatives
- [ ] Maintains Halloween theme (where appropriate)

### Message Formatting

- [ ] ASCII art displays correctly
- [ ] Colors are visible and appropriate
- [ ] Text is properly aligned
- [ ] No formatting issues or garbled text

**Notes on message quality:**
```
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________
```

---

## Performance Verification

### Timing Test

Run several commands and observe response time:

```
mairu> rm C:\Windows\test.txt
mairu> rm test.txt
mairu> mv test.txt dest.txt
mairu> chmod 777 test.txt
```

- [ ] No noticeable delay (< 100ms perceived)
- [ ] Response feels instant
- [ ] No lag or stuttering
- [ ] Smooth user experience

**Measured times (if available):**
```
_________________________________________________________________
```

---

## Edge Cases

### Empty/Invalid Input

```
mairu>
mairu>
mairu> rm
```

- [ ] Empty commands handled gracefully
- [ ] No crashes or errors
- [ ] Appropriate error messages

### Special Characters

```
mairu> rm "C:\Program Files\test file.txt"
mairu> rm /usr/local/test\ file.txt
```

- [ ] Quoted paths handled correctly
- [ ] Spaces in paths work
- [ ] Escaped characters work

### Long Paths

```
mairu> rm C:\Windows\System32\very\long\path\that\goes\deep\test.txt
```

- [ ] Long paths handled correctly
- [ ] No buffer overflows
- [ ] No performance issues

**Edge case notes:**
```
_________________________________________________________________
_________________________________________________________________
```

---

## Cross-Platform Compatibility

### Platform Detection

- [ ] Correct platform detected (Windows/Linux/macOS)
- [ ] Correct protected directories used for platform
- [ ] Path separators handled correctly for platform

### Platform-Specific Features

**Windows:**
- [ ] Backslash paths work
- [ ] Forward slash paths work
- [ ] Case insensitivity works
- [ ] Drive letters handled (C:, D:, etc.)

**Linux:**
- [ ] Forward slash paths work
- [ ] Case sensitivity works
- [ ] Root directory (/) handled
- [ ] Symbolic links considered

**Notes:**
```
_________________________________________________________________
_________________________________________________________________
```

---

## Integration with Existing Features

### Dangerous Pattern Check

```
mairu> rm -rf /
```

- [ ] System directory check runs FIRST
- [ ] Dangerous pattern check runs SECOND (if needed)
- [ ] No conflicts between checks
- [ ] Correct warning displayed

### Statistics Tracking

```
mairu> stats
```

- [ ] Blocked commands counted correctly
- [ ] System protection blocks tracked separately
- [ ] Statistics display correctly

### Achievements

- [ ] "Boundary Tester" achievement unlocks (3 system blocks)
- [ ] "System Adventurer" achievement unlocks (3 different dirs)
- [ ] Achievements display correctly

**Integration notes:**
```
_________________________________________________________________
_________________________________________________________________
```

---

## Real User Scenarios

### Scenario 1: Curious Child

**Behavior:** Tries to delete Windows folder after seeing it in File Explorer

```
mairu> rm C:\Windows
```

- [ ] Command blocked
- [ ] Clear explanation provided
- [ ] Child understands why it's dangerous
- [ ] Safe alternative suggested

### Scenario 2: Beginner Learning CLI

**Behavior:** Follows online tutorial that uses /etc as example

```
mairu> echo "test" > /etc/myconfig.conf
```

- [ ] Command blocked
- [ ] Explanation helps learning
- [ ] Suggests safe practice directory
- [ ] Doesn't discourage learning

### Scenario 3: Accidental Typo

**Behavior:** Meant to type ~/Windows but typed /Windows

```
mairu> rm /Windows/test.txt
```

- [ ] Typo caught by protection
- [ ] User realizes mistake
- [ ] Grateful for protection

**Scenario notes:**
```
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________
```

---

## Issues Found

### Critical Issues (Must Fix)

```
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________
```

### Medium Issues (Should Fix)

```
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________
```

### Minor Issues (Nice to Fix)

```
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________
```

---

## Final Assessment

### Overall Functionality

- [ ] All critical features working
- [ ] No major bugs found
- [ ] Performance acceptable
- [ ] User experience good

### Safety Verification

- [ ] No bypass methods found
- [ ] All protected directories covered
- [ ] Fail-safe mechanisms work
- [ ] Error handling comprehensive

### Readiness for v1.2.0

- [ ] Ready to tag v1.2.0
- [ ] Needs minor fixes first
- [ ] Needs major fixes first

**Final notes:**
```
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________
```

---

## Sign-Off

**Tester:** _________________
**Date:** _________________
**Time Spent:** _______ minutes
**Result:** PASS / FAIL (circle one)

**Recommendation:**
- [ ] Approve for v1.2.0 release
- [ ] Approve with minor fixes
- [ ] Requires additional testing
- [ ] Not ready for release

---

**Next Steps:**
1. Address any issues found
2. Complete Task 12 (Safety Review)
3. Tag v1.2.0 if all tests pass
