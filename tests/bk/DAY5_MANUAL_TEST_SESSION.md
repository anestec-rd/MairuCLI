# Day 5 Manual Test Session

**Date:** 2025-11-21
**Time:** 11:30-12:15
**Tester:** User + Kiro
**Version:** 1.1

## Test Objectives
1. Verify dd command bug fix (Issue #2)
2. Test all 11 dangerous patterns
3. Test all 4 caution patterns
4. Test all 12 builtin commands
5. Test 2 typo patterns
6. Test 8 achievements
7. Test stats command
8. Verify new warning variations

---

## Test Results

### 1. Bug Fix Verification (Issue #2)

#### Test 1.1: dd if=/dev/zero (without of=)
- **Command:** `dd if=/dev/zero`
- **Expected:** Should be blocked with warning
- **Result:** ⬜ PENDING
- **Notes:**

#### Test 1.2: dd if=/dev/zero of=/dev/sda (with of=)
- **Command:** `dd if=/dev/zero of=/dev/sda`
- **Expected:** Should be blocked with warning
- **Result:** ⬜ PENDING
- **Notes:**

#### Test 1.3: dd if=file of=file2 (safe dd)
- **Command:** `dd if=test.txt of=test2.txt`
- **Expected:** Should pass through to system
- **Result:** ⬜ PENDING
- **Notes:**

---

### 2. Dangerous Pattern Detection (11 patterns)

#### Test 2.1: rm_dangerous
- **Command:** `rm -rf /`
- **Expected:** Blocked with ASCII art + warning
- **Result:** ⬜ PENDING
- **Variation shown:**
- **Notes:**

#### Test 2.2: chmod_777
- **Command:** `chmod 777 file.txt`
- **Expected:** Blocked with ASCII art + warning
- **Result:** ⬜ PENDING
- **Variation shown:**
- **Notes:**

#### Test 2.3: dd_zero
- **Command:** `dd if=/dev/zero of=/dev/sda`
- **Expected:** Blocked with ASCII art + warning
- **Result:** ⬜ PENDING
- **Variation shown:**
- **Notes:**

#### Test 2.4: drop_database
- **Command:** `DROP DATABASE production`
- **Expected:** Blocked with ASCII art + warning
- **Result:** ⬜ PENDING
- **Variation shown:**
- **Notes:**

#### Test 2.5: fork_bomb
- **Command:** `:(){ :|:& };:`
- **Expected:** Blocked with ASCII art + warning
- **Result:** ⬜ PENDING
- **Variation shown:**
- **Notes:**

#### Test 2.6: redirect_to_disk
- **Command:** `echo test > /dev/sda`
- **Expected:** Blocked with ASCII art + warning
- **Result:** ⬜ PENDING
- **Variation shown:**
- **Notes:**

#### Test 2.7: mkfs_disk
- **Command:** `mkfs.ext4 /dev/sda`
- **Expected:** Blocked with ASCII art + warning
- **Result:** ⬜ PENDING
- **Variation shown:**
- **Notes:**

#### Test 2.8: mv_to_null
- **Command:** `mv important.txt /dev/null`
- **Expected:** Blocked with ASCII art + warning
- **Result:** ⬜ PENDING
- **Variation shown:**
- **Notes:**

#### Test 2.9: overwrite_file
- **Command:** `> /etc/passwd`
- **Expected:** Blocked with ASCII art + warning
- **Result:** ⬜ PENDING
- **Variation shown:**
- **Notes:**

#### Test 2.10: dd_random
- **Command:** `dd if=/dev/random of=/dev/sda`
- **Expected:** Blocked with ASCII art + warning
- **Result:** ⬜ PENDING
- **Variation shown:**
- **Notes:**

#### Test 2.11: kernel_panic
- **Command:** `echo c > /proc/sysrq-trigger`
- **Expected:** Blocked with ASCII art + warning
- **Result:** ⬜ PENDING
- **Variation shown:**
- **Notes:**

---

### 3. Caution Pattern Detection (4 patterns)

#### Test 3.1: sudo_shell
- **Command:** `sudo su`
- **Expected:** Caution warning + confirmation prompt
- **Result:** ⬜ PENDING
- **User choice:**
- **Notes:**

#### Test 3.2: chmod_permissive
- **Command:** `chmod 666 file.txt`
- **Expected:** Caution warning + confirmation prompt
- **Result:** ⬜ PENDING
- **User choice:**
- **Notes:**

#### Test 3.3: firewall_disable
- **Command:** `ufw disable`
- **Expected:** Caution warning + confirmation prompt
- **Result:** ⬜ PENDING
- **User choice:**
- **Notes:**

#### Test 3.4: selinux_disable
- **Command:** `setenforce 0`
- **Expected:** Caution warning + confirmation prompt
- **Result:** ⬜ PENDING
- **User choice:**
- **Notes:**

---

### 4. Builtin Commands (12 commands)

#### Test 4.1: cd
- **Command:** `cd /tmp`
- **Expected:** Change directory
- **Result:** ⬜ PENDING
- **Notes:**

#### Test 4.2: pwd
- **Command:** `pwd`
- **Expected:** Show current directory
- **Result:** ⬜ PENDING
- **Notes:**

#### Test 4.3: ls
- **Command:** `ls`
- **Expected:** List files (pass to system)
- **Result:** ⬜ PENDING
- **Notes:**

#### Test 4.4: dir (Windows)
- **Command:** `dir`
- **Expected:** List files (pass to system)
- **Result:** ⬜ PENDING
- **Notes:**

#### Test 4.5: clear
- **Command:** `clear`
- **Expected:** Clear screen
- **Result:** ⬜ PENDING
- **Notes:**

#### Test 4.6: cls (Windows)
- **Command:** `cls`
- **Expected:** Clear screen
- **Result:** ⬜ PENDING
- **Notes:**

#### Test 4.7: echo
- **Command:** `echo Hello World`
- **Expected:** Print "Hello World"
- **Result:** ⬜ PENDING
- **Notes:**

#### Test 4.8: export
- **Command:** `export TEST=value`
- **Expected:** Set environment variable
- **Result:** ⬜ PENDING
- **Notes:**

#### Test 4.9: env
- **Command:** `env`
- **Expected:** Show environment variables
- **Result:** ⬜ PENDING
- **Notes:**

#### Test 4.10: alias
- **Command:** `alias`
- **Expected:** Show available aliases
- **Result:** ⬜ PENDING
- **Notes:**

#### Test 4.11: history
- **Command:** `history`
- **Expected:** Show command history
- **Result:** ⬜ PENDING
- **Notes:**

#### Test 4.12: help
- **Command:** `help`
- **Expected:** Show help message
- **Result:** ⬜ PENDING
- **Notes:**

#### Test 4.13: stats
- **Command:** `stats`
- **Expected:** Show statistics
- **Result:** ⬜ PENDING
- **Notes:**

#### Test 4.14: exit
- **Command:** `exit`
- **Expected:** Exit MairuCLI
- **Result:** ⬜ PENDING
- **Notes:**

---

### 5. Typo Detection (2 patterns)

#### Test 5.1: sl typo
- **Command:** `sl`
- **Expected:** Typo message + offer correction
- **Result:** ⬜ PENDING
- **Notes:**

#### Test 5.2: cd.. typo
- **Command:** `cd..`
- **Expected:** Typo message + offer correction
- **Result:** ⬜ PENDING
- **Notes:**

---

### 6. Achievement System (8 achievements)

#### Test 6.1: First Blood
- **Trigger:** Block first dangerous command
- **Expected:** Achievement unlocked message
- **Result:** ⬜ PENDING
- **Notes:**

#### Test 6.2: Persistent Troublemaker
- **Trigger:** Try 5 dangerous commands
- **Expected:** Achievement unlocked message
- **Result:** ⬜ PENDING
- **Notes:**

#### Test 6.3: Danger Addict
- **Trigger:** Block 10 dangerous commands
- **Expected:** Achievement unlocked message
- **Result:** ⬜ PENDING
- **Notes:**

#### Test 6.4: Stubborn
- **Trigger:** Try same command 3 times
- **Expected:** Achievement unlocked message
- **Result:** ⬜ PENDING
- **Notes:**

#### Test 6.5: Explorer
- **Trigger:** Use 5 different safe commands
- **Expected:** Achievement unlocked message
- **Result:** ⬜ PENDING
- **Notes:**

#### Test 6.6: Command Master
- **Trigger:** Use 10 different safe commands
- **Expected:** Achievement unlocked message
- **Result:** ⬜ PENDING
- **Notes:**

#### Test 6.7: Balanced User
- **Trigger:** Use 8 safe + 3 dangerous commands
- **Expected:** Achievement unlocked message
- **Result:** ⬜ PENDING
- **Notes:**

#### Test 6.8: Typo Master
- **Trigger:** Make 3 typos
- **Expected:** Achievement unlocked message
- **Result:** ⬜ PENDING
- **Notes:**

---

### 7. Repeat Warning System

#### Test 7.1: Same command 2nd time
- **Command:** `rm -rf /` (2nd time)
- **Expected:** Different variation or escalated message
- **Result:** ⬜ PENDING
- **Notes:**

#### Test 7.2: Same command 3rd time
- **Command:** `rm -rf /` (3rd time)
- **Expected:** "I told you so" message
- **Result:** ⬜ PENDING
- **Notes:**

---

### 8. New Variations Verification

#### Test 8.1: New rm_root variations
- **Commands to try:** Multiple `rm -rf /` attempts
- **Expected variations to see:**
  - "WATCH OUT! (Your precious files are about to elope!)"
  - "OOPS! (Not the trash bin... the ocean voyage!)"
  - "NO NO NO! (The system will cry, so let's not do this)"
  - "THAT'S A GOOD ERASER! (It erases really well... too well)"
  - "NO USE CRYING! (It's no use crying over spilt milk)"
- **Result:** ⬜ PENDING
- **Variations seen:**

#### Test 8.2: New chmod_777 variations
- **Commands to try:** Multiple `chmod 777 file` attempts
- **Expected variations to see:**
  - "A BIT TOO TIDY! (Maybe a little too clean?)"
  - "PARTY TIME? (Did you throw a party? There's a wolf at the door)"
- **Result:** ⬜ PENDING
- **Variations seen:**

#### Test 8.3: New data_destroyer variations
- **Commands to try:** Multiple dangerous disk commands
- **Expected variations to see:**
  - "BBQ DATA! (The taste of barbecued data is terrible)"
  - "NO USE CRYING! (It's no use crying over spilt milk)"
- **Result:** ⬜ PENDING
- **Variations seen:**

---

## Summary

### Pass/Fail Count
- **Total Tests:** 0/0
- **Passed:** 0
- **Failed:** 0
- **Pending:** 0

### Critical Issues Found
- None yet

### Minor Issues Found
- None yet

### Notes
- Test session in progress

---

**Test Status:** 🟡 IN PROGRESS
**Next Steps:** Execute tests systematically
