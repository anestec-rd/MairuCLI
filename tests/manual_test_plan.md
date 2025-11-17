# Manual Test Plan for MairuCLI

**Date:** 2025-11-17
**Tester:** Developer
**Start Time:** ~9:40

---

## Test Environment
- OS: Windows
- Python: 3.x
- Shell: PowerShell/CMD

---

## Test Scenarios

### 1. Startup & Welcome Banner
**Command:** `python -m src.main`

**Expected:**
- [✓] Halloween-themed banner displays
- [✓] Orange/purple colors work
- [✓] Emoji display correctly (🎃👻🔥)
- [ ] Instructions are clear
- [✓] Prompt appears: `mairu>`

**Notes:**
```
[Record observations here]
```

---

### 2. Builtin Commands

#### 2.1 Help Command
**Command:** `help`

**Expected:**
- [ ] Shows all builtin commands
- [ ] Shows dangerous commands with warnings
- [ ] Shows typo patterns
- [ ] Halloween theme consistent
- [ ] "DON'T try these!" section visible

#### 2.2 PWD Command
**Command:** `pwd`

**Expected:**
- [ ] Shows current directory
- [ ] No errors

#### 2.3 Echo Command
**Command:** `echo Hello MairuCLI!`

**Expected:**
- [ ] Prints: Hello MairuCLI!
- [ ] No errors

#### 2.4 CD Command
**Commands:**
```
cd ..
pwd
cd -
pwd
```

**Expected:**
- [ ] Changes directory
- [ ] `cd -` returns to previous directory
- [ ] No errors

#### 2.5 History Command
**Command:** `history`

**Expected:**
- [ ] Shows all previous commands
- [ ] Line numbers displayed
- [ ] No errors

#### 2.6 Stats Command
**Command:** `stats`

**Expected:**
- [ ] Shows statistics (initially 0)
- [ ] Displays correctly
- [ ] No errors

---

### 3. Dangerous Command Detection

#### 3.1 rm -rf /
**Command:** `rm -rf /`

**Expected:**
- [ ] ASCII art displays (fired.txt)
- [ ] Warning message appears
- [ ] Random variation works
- [ ] Educational content shown
- [ ] Safe alternatives provided
- [ ] Command is blocked
- [ ] Stats increment

**Test variations:**
- [ ] `rm -rf /`
- [ ] `rm -fr /`
- [ ] `sudo rm -rf /`

#### 3.2 chmod 777
**Command:** `chmod 777 test.txt`

**Expected:**
- [ ] ASCII art displays (permission_denied.txt)
- [ ] Warning message appears
- [ ] Random variation works
- [ ] Educational content shown
- [ ] Command is blocked
- [ ] Stats increment

#### 3.3 DROP DATABASE
**Command:** `DROP DATABASE production`

**Expected:**
- [ ] ASCII art displays
- [ ] Warning message appears
- [ ] Command is blocked
- [ ] Stats increment

#### 3.4 dd command
**Command:** `dd if=/dev/zero of=/dev/sda`

**Expected:**
- [ ] ASCII art displays (data_destroyer.txt)
- [ ] Warning message appears
- [ ] Command is blocked
- [ ] Stats increment

---

### 4. "I Told You So" Feature

**Commands:** (Repeat same command multiple times)
```
rm -rf /
rm -rf /
rm -rf /
rm -rf /
rm -rf /
rm -rf /
```

**Expected:**
- [ ] 1st: Normal warning
- [ ] 2nd: "Wait... Haven't we been here before?"
- [ ] 3rd: "Seriously? I told you so..." + "How about trying something different?"
- [ ] 4th: "REALLY?! I give up."
- [ ] 5th: "Dracula is crying..."
- [ ] 6th+: "[No comment.]" with command log

---

### 5. Achievement System

**Test sequence:**
```
rm -rf /          # Achievement: First Blood
chmod 777 file
DROP DATABASE test
dd if=/dev/zero of=/dev/sda
rm -rf /          # Achievement: Persistent Troublemaker (5 dangerous)
rm -rf /
rm -rf /          # Achievement: Stubborn (3 repeats)
sl                # Typo
cd..              # Typo
sl                # Achievement: Typo Master (3 typos)
```

**Expected Achievements:**
- [ ] First Blood (1st dangerous command)
- [ ] Persistent Troublemaker (5 dangerous commands)
- [ ] Stubborn (same command 3 times)
- [ ] Typo Master (3 typos)

---

### 6. Typo Detection

#### 6.1 sl typo
**Command:** `sl`

**Expected:**
- [ ] "🚂 Choo choo! All aboard the typo train!"
- [ ] Suggests: ls
- [ ] Stats increment (typos)

#### 6.2 cd.. typo
**Command:** `cd..`

**Expected:**
- [ ] "🎃 Stuck together? Let me help you separate!"
- [ ] Suggests: cd ..
- [ ] Stats increment (typos)

---

### 7. New Creative Messages

#### 7.1 New Warning Variations
**Test:** Run dangerous commands multiple times to see variations

**Expected new messages:**
- [ ] "WHOA THERE..." (rm -rf /)
- [ ] "NEED A CHECKLIST?" (chmod 777)
- [ ] "TRICK AND TRIAGE!" (data destroyer)

#### 7.2 Unknown Command
**Command:** `nonexistentcommand`

**Expected:**
- [ ] "🍬 Sorry, we don't sell 'nonexistentcommand' at the candy store."
- [ ] "(Command not found)"

---

### 8. Stats Verification

**Command:** `stats`

**After all tests, expected:**
- [ ] Dangerous commands blocked: ~10+
- [ ] Typos caught: ~3+
- [ ] Sarcastic comment based on count
- [ ] Display is correct

---

### 9. Safe Command Execution

**Commands:**
```
dir
echo test
```

**Expected:**
- [ ] Commands execute normally
- [ ] Output displays correctly
- [ ] No warnings
- [ ] No errors

---

### 10. Exit

**Command:** `exit`

**Expected:**
- [ ] Goodbye message displays
- [ ] Halloween theme
- [ ] Clean exit
- [ ] No errors

---

## Issues Found

### Critical Issues
```
[List any critical bugs that prevent core functionality]
```

### Minor Issues
```
[List any minor bugs or polish items]
```

### Enhancement Ideas
```
[List any ideas that came up during testing]
```

---

## Test Summary

**Total Tests:** 50+
**Passed:** ___
**Failed:** ___
**Skipped:** ___

**Overall Status:** [ ] PASS / [ ] FAIL

**Time Completed:** ___
**Duration:** ___

---

## Next Steps

Based on test results:
1. [ ] Fix critical bugs
2. [ ] Fix minor bugs
3. [ ] Implement quick enhancements
4. [ ] Update README.md
5. [ ] Prepare for demo

---

**Notes:**
- Test on Windows (native environment)
- Colors may vary by terminal
- Some Unix commands won't execute (expected on Windows)
- Focus on warning system, not command execution
