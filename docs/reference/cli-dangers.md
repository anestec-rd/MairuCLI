# CLI Dangers: Common Command-Line Mistakes

## Overview

This document catalogs common and dangerous CLI mistakes that engineers make. These patterns informed the design of MairuCLI's warning system.

**Source:** Compiled from real-world incidents, Stack Overflow discussions, and engineering war stories.

---

## 1. Destructive Deletion Commands

### rm -rf Nightmares

**`sudo rm -rf /`** - The Ultimate Disaster
- Deletes the entire system
- No trash bin, no undo
- Unrecoverable without backups

**`rm -rf *` Misfires**
- Executed in wrong directory
- Deletes all important files instantly

**Empty Variable Trap**
```bash
DIR=""
rm -rf $DIR/*  # Expands to: rm -rf /*
```

**Typo Hell**
```bash
# Intended: rm -rf /home/user/tmp
# Typed: rm -rf /home/user /tmp
# Result: Deletes /home/user AND /tmp (space matters!)
```

**Real Incident:** GitLab lost 300GB of production data in 2017 due to accidental `rm -rf` execution.

---

### dd Command (Data Destroyer)

**`dd if=/dev/zero of=/dev/sda`**
- Overwrites entire disk with zeros
- Wrong drive specification = total data loss
- No confirmation, no warning
- Executes silently and completely

**Common Mistakes:**
- Swapping `if` and `of` parameters
- Targeting wrong device (`sda` vs `sdb`)

---

## 2. Permission Setting Mistakes

### chmod 777 - Security Nightmare

**The Problem:**
- Frustrated by "Permission denied"
- Mindlessly types `chmod 777`
- Opens massive security hole

**Impact:**
```bash
chmod 777 file.txt        # Anyone can read/write/execute
chmod -R 777 /            # Entire system permissions destroyed
```

**Why It's Dangerous:**
- Anyone can read sensitive files
- Anyone can modify system files
- Anyone can execute malicious code

**Real Incident:** Multiple security breaches traced to `chmod 777` on production servers.

---

### chown Disasters

**`sudo chown -R root: /`**
- Changes ownership of entire root directory
- Users lose access to their own files
- System becomes unusable
- Recovery extremely difficult

**Sudo Becomes Unusable:**
```bash
chown user:user /usr/bin/sudo
# Now sudo doesn't work - you're locked out!
```

---

## 3. sudo Misuse and Abuse

### Mindless sudo Usage

**`sudo cd /root`**
- Common misconception
- `cd` is a shell builtin, sudo has no effect
- Shows lack of understanding

**sudo Habit:**
- Adding sudo without thinking
- Missing critical errors
- Executing dangerous commands with elevated privileges

**`sudo !!` Trap:**
```bash
$ rm -rf /  # Oops, permission denied
$ sudo !!   # Executes: sudo rm -rf /
# System destroyed!
```

---

## 4. Pipe and Redirect Accidents

### /dev/null Disasters

**`cat important.log > /dev/null`**
- Sends critical logs to black hole
- Data lost forever
- No recovery possible

**`>` vs `>>` Confusion:**
```bash
echo "new" > config.txt   # Overwrites entire file
echo "new" >> config.txt  # Appends to file
```

### Destructive Pipe Chains

**`cat /etc/passwd | rm -rf`**
- Chaining dangerous commands
- Unexpected interactions
- Difficult to debug

**File Overwrite:**
```bash
echo "test" > /etc/hosts  # Destroys network configuration
```

---

## 5. Environment Confusion

### Production vs Development Mix-up

**The Scenario:**
- Multiple SSH tabs open
- Similar-looking prompts
- Execute test command on production server
- Catastrophic data loss

**Prevention:**
- Color-code prompts (production = red, dev = green)
- Use different terminal themes
- Add clear environment indicators

**tmux/screen Pane Mistakes:**
- Wrong pane selected
- Command executed on wrong server

---

## 6. Git Command Horrors

### Force Push Disasters

**`git push -f origin master`**
- Overwrites remote history
- Deletes teammates' commits
- Causes merge conflicts
- Team productivity destroyed

**`git reset --hard HEAD~10`**
- Deletes 10 commits locally
- Unrecoverable without reflog knowledge

**`git clean -fdx`**
- Deletes all untracked files
- No recovery possible
- Build artifacts, configs gone

---

## 7. Database Command Tragedies

### DROP Commands

**`DROP DATABASE production;`**
- Deletes entire production database
- All user data lost
- Business impact: catastrophic

**`TRUNCATE TABLE users;`**
- Deletes all user data
- Cannot ROLLBACK (unlike DELETE)
- Instant and permanent

**Missing WHERE Clause:**
```sql
DELETE FROM orders;  -- Intended: WHERE id = 123
-- Result: All orders deleted
```

**Real Incident:** Junior developer dropped production database, company lost $1M+ in recovery costs.

---

## 8. Network Command Accidents

### iptables Disasters

**`iptables -F`** (Flush all rules)
- Executed on remote server via SSH
- SSH connection drops
- Locked out permanently
- Requires physical access to recover

**Self-Lockout:**
- Modifying firewall rules while connected
- Blocking own SSH port
- No way back in

---

## 9. Process Management Mistakes

### kill Command Misfires

**`kill -9 -1`**
- Kills ALL processes
- System crashes immediately
- Data corruption likely

**PID Confusion:**
```bash
kill -9 1234  # Intended: kill process 1234
# Actually: Killed critical system process
```

### Shutdown Accidents

**`sudo reboot`** on production during peak hours
- All users disconnected
- Services down
- Revenue loss

**`shutdown now`**
- Immediate shutdown
- No graceful termination
- Data loss risk

---

## 10. Alias and History Traps

### Dangerous Aliases

**`alias rm='rm -rf'`**
- Every deletion becomes recursive force delete
- Muscle memory becomes dangerous

**Malicious Aliases:**
```bash
alias cd='cd .. && rm -rf *'  # Prank that destroys data
```

### Command History Accidents

**`Ctrl+R` Search Gone Wrong:**
- Searching for command
- Accidentally selects dangerous command from history
- Executes before realizing

**`!!` and `!$` Surprises:**
- Repeats last command (might be dangerous)
- Uses last argument (might be wrong file)

---

## 11. Typos and Spelling Mistakes

### Common Typos

**`cd /usr/lcoal`** (typo: lcoal)
- Directory doesn't exist
- Next command executes in wrong location
- Unexpected results

**`rm -rf ./tmp`** intended, typed **`rm -rf . /tmp`**
- Space before `/tmp`
- Deletes current directory AND /tmp

**`chmod 644`** intended, typed **`chmod 664`**
- Wrong permissions set
- Security implications

---

## 12. Ctrl+Key Accidents

### Ctrl+C / Ctrl+Z Mishaps

**Ctrl+C on Long-Running Process:**
- Hours of computation lost
- No checkpoint, must restart

**Ctrl+Z Accumulation:**
- Suspends process instead of killing
- Dozens of suspended processes
- Resource exhaustion

### Ctrl+S / Ctrl+Q

**Ctrl+S (XOFF):**
- Terminal appears frozen
- User panics, force-quits terminal
- Loses work

**Ctrl+Q (XON):**
- Unfreezes terminal
- Many users don't know this

---

## 13. Production Experimentation

### "Just Testing" Syndrome

**The Pattern:**
- "Let me just try this command..."
- Executes on production
- Unexpected behavior
- Disaster

**"Will This Work?" Mentality:**
- Testing without understanding
- No rollback plan
- No backup check

### Log Ignorance

**`2>/dev/null` Overuse:**
- Suppresses all errors
- Misses critical warnings
- Problems go unnoticed until catastrophic failure

---

## Prevention Strategies

### Basic Defenses

1. **Color-code prompts** - Visual warning for production
2. **Use `-i` flags** - Interactive confirmation (rm -i, mv -i, cp -i)
3. **Set aliases** - `alias rm='rm -i'`
4. **Always backup** - Before any destructive operation
5. **Check `pwd`** - Verify current directory before commands
6. **Use tmux/screen** - Protect against SSH disconnection
7. **Minimize sudo** - Only when truly necessary
8. **Review history** - Check before executing from history

### Advanced Defenses

1. **Use `saferm` tools** - Safer alternatives to rm
2. **Git-manage configs** - Version control for rollback
3. **Use `--dry-run`** - Test commands safely (rsync, etc.)
4. **Bastion hosts** - No direct production access
5. **Audit logging** - Record all command history
6. **Require approvals** - Two-person rule for critical operations

---

## Philosophy

> "In the CLI world, once you press Enter, there's no undo. One command mistake can affect an entire company. That's why caution and verification habits are more important than anything."

---

## References

- Stack Overflow: "Worst command-line mistakes"
- GitLab Incident Report (2017)
- Various engineering post-mortems
- Reddit r/sysadmin horror stories

---

**Note:** This document serves as reference material for MairuCLI's pattern database and educational messages. All incidents mentioned are real, though some details are anonymized.

**Last Updated:** November 16, 2025
