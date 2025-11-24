# Dangerous Command Patterns Reference

This document provides detailed information about all dangerous patterns that MairuCLI detects and blocks.

---

## Overview

MairuCLI protects you from commands that could cause:
- �  System directory damage (Windows, Linux, macOS)
- � SData loss (deletion, overwriting)
- � Syecurity vulnerabilities (permission issues)
- � SDystem crashes (kernel panic, fork bombs)
- 🗄️ Database destruction

Each pattern below includes:
- What commands are detected
- Why they're dangerous
- Real-world incidents
- Safe alternatives

---

## System Directory Protection

**Protection Level:** CRITICAL / CAUTION (platform-specific)

**What It Protects:**

**Windows:**
- `C:\Windows\` - Windows system directory (CRITICAL)
- `C:\Windows\System32\` - Core system files (CRITICAL)
- `C:\Program Files\` - Installed programs (CAUTION)
- `C:\Program Files (x86)\` - 32-bit programs (CAUTION)
- `C:\ProgramData\` - Application data (CAUTION)

**Linux/Unix:**
- `/bin/`, `/sbin/` - Essential system binaries (CRITICAL)
- `/boot/` - Boot loader files (CRITICAL)
- `/etc/` - System configuration (CRITICAL)
- `/lib/`, `/lib64/` - System libraries (CRITICAL)
- `/proc/`, `/sys/` - Kernel interfaces (CRITICAL)
- `/root/` - Root user home (CRITICAL)
- `/usr/bin/`, `/usr/sbin/` - System binaries (CAUTION)
- `/var/log/` - System logs (CAUTION)

**macOS:**
- `/System/` - macOS system files (CRITICAL)
- `/bin/`, `/sbin/` - System binaries (CRITICAL)
- `/Library/` - System libraries (CAUTION)
- `/Applications/` - Installed applications (CAUTION)

**Why It's Dangerous:**
System directories contain critical files that the operating system needs to function. Modifying or deleting these files can:
- Make the system unbootable
- Break essential system services
- Require OS reinstallation
- Cause data loss

**Detection Features:**
- Resolves relative paths (e.g., `../../Windows`)
- Expands environment variables (e.g., `$WINDIR`, `$HOME`)
- Handles path shortcuts (e.g., `~`)
- Detects wildcards in system directories
- Works with all file operations (rm, mv, chmod, dd, redirects)

**Educational Message Example:**
```
🛑 STOP RIGHT THERE!

You're trying to modify: C:\Windows\System32\kernel32.dll

💡 What you should know:
  - System32 contains essential Windows components
  - Deleting files here can make Windows unbootable
  - Even with admin rights, this is extremely dangerous

🎃 Safe alternative:
  - Work in your user directory: C:\Users\YourName\
  - Use Documents, Downloads, or Desktop folders
  - Ask an experienced user if you need to modify system files

Command blocked for your safety.
```

**Safe Alternatives:**
- Work in user directories: `C:\Users\<username>\` (Windows) or `/home/<username>/` (Linux)
- Use Documents, Downloads, or Desktop folders
- Create project directories in safe locations
- Ask for help before modifying system files

**Implementation:**
- Path resolution module (`src/path_resolver.py`)
- Command parser module (`src/command_parser.py`)
- System directory checker (`src/interceptor.py`)
- Educational warnings (`src/display/system_protection_warning.py`)

---

## Dangerous Command Patterns

---

## 1. Recursive Deletion (`rm_dangerous`)

**Patterns Detected:**
- `rm -rf /` - Delete root directory
- `rm -rf ~` - Delete home directory
- `rm -rf *` - Delete everything in current directory
- `rm -rf $VAR` - Delete with variable expansion

**Why It's Dangerous:**
Recursively deletes files without confirmation. Can wipe entire filesystems in seconds.

**Real-World Incident:**
GitLab.com lost 300GB of production data in 2017 due to accidental `rm -rf` execution during a recovery attempt.

**Safe Alternative:**
- Use `rm -i` for interactive confirmation
- Use `trash-cli` to move files to trash instead
- Always specify exact file names
- Never use wildcards with `rm -rf`

---

## 2. Permission Chaos (`chmod_777`)

**Patterns Detected:**
- `chmod 777 file` - Give everyone full access
- `chmod -R 777 /path` - Recursively open permissions

**Why It's Dangerous:**
Makes files readable, writable, and executable by everyone on the system. This is a major security vulnerability that can lead to:
- Unauthorized file modification
- Malware execution
- Data theft
- System compromise

**Real-World Impact:**
Compromised servers often show `chmod 777` as the first sign of breach. Attackers use it to maintain access.

**Safe Alternative:**
- Use `chmod 644` for regular files (owner: rw, others: r)
- Use `chmod 755` for executables (owner: rwx, others: rx)
- Use `chmod 600` for sensitive files (owner only)
- Only give write access when absolutely necessary

---

## 3. Disk Destroyer (`dd_zero`)

**Patterns Detected:**
- `dd if=/dev/zero of=/dev/sda` - Overwrite disk with zeros
- `dd if=/dev/zero` - Incomplete but still dangerous

**Why It's Dangerous:**
The `dd` command directly writes to disk devices, bypassing the filesystem. Writing zeros overwrites all data, making recovery impossible.

**Real-World Use:**
Legitimately used for secure disk wiping, but catastrophic if:
- Wrong device is specified
- Command is run on production system
- No backup exists

**Safe Alternative:**
- Triple-check device names with `lsblk` before running
- Use disk management tools with confirmation dialogs
- Always backup before disk operations
- Test on non-critical systems first

---

## 4. Database Annihilation (`drop_database`)

**Patterns Detected:**
- `DROP DATABASE production` - Delete entire database
- `DROP DATABASE *` - Delete all databases (if supported)

**Why It's Dangerous:**
Permanently deletes entire databases including:
- All tables and data
- Relationships and constraints
- Stored procedures
- User permissions

**Real-World Incident:**
Numerous startups have lost everything due to accidental database drops. Some never recovered.

**Safe Alternative:**
- Always backup before destructive operations
- Use database management tools with confirmation
- Test on development databases first
- Implement database access controls
- Use read-only connections when possible

---

## 5. Fork Bomb (`fork_bomb`)

**Patterns Detected:**
- `:(){ :|:& };:` - Classic bash fork bomb

**Why It's Dangerous:**
Creates a function that calls itself twice, creating exponentially multiplying processes:
- 1 → 2 → 4 → 8 → 16 → 32 → 64 → 128...
- System runs out of process slots
- Everything freezes
- Requires hard reboot

**Real-World Impact:**
This is a Denial of Service (DoS) attack. Can crash systems in seconds.

**Safe Alternative:**
- Never run code you don't understand
- This is malicious, not a mistake
- Set process limits with `ulimit -u`
- Use systemd resource controls

---

## 6. Direct Disk Write (`redirect_to_disk`)

**Patterns Detected:**
- `echo data > /dev/sda` - Write directly to disk device
- `cat file > /dev/sdb` - Redirect output to disk

**Why It's Dangerous:**
Bypasses the filesystem and writes raw data directly to disk:
- Corrupts filesystem structures
- Makes disk unreadable
- Data loss is immediate
- System may become unbootable

**Real-World Impact:**
Even a small write can corrupt critical filesystem metadata, making the entire disk unusable.

**Safe Alternative:**
- Never redirect to `/dev/sd*` devices
- Use proper disk tools (`dd`, `parted`, etc.)
- Understand block devices vs filesystems
- Mount filesystems and write to files instead

---

## 7. Filesystem Formatting (`mkfs_disk`)

**Patterns Detected:**
- `mkfs.ext4 /dev/sda` - Format disk as ext4
- `mkfs.xfs /dev/sdb` - Format disk as XFS
- `mkfs.* /dev/sd*` - Any filesystem format

**Why It's Dangerous:**
Creates a new filesystem, which:
- Erases all existing data
- Destroys partition table
- Makes recovery extremely difficult
- Cannot be undone

**Real-World Incident:**
Wrong device selection (e.g., `/dev/sda` instead of `/dev/sdb`) has destroyed production data countless times.

**Safe Alternative:**
- Verify device with `lsblk` multiple times
- Check mounted filesystems with `df -h`
- Unmount device first
- Backup everything before formatting
- Use partition labels to avoid confusion

---

## 8. Dev Null Deletion (`mv_to_null`)

**Patterns Detected:**
- `mv important.txt /dev/null` - Move file to void
- `mv * /dev/null` - Move everything to void

**Why It's Dangerous:**
`/dev/null` is a black hole - anything written to it disappears forever:
- No trash bin
- No recovery possible
- Looks like moving files, but actually deletes them
- Silent data loss

**Real-World Impact:**
Sneaky way to delete files that looks innocent. Often used in scripts that go wrong.

**Safe Alternative:**
- Use `rm` if you want to delete (at least it's explicit)
- Use trash utilities (`trash-cli`, `gio trash`) for safety
- Never use `/dev/null` as a destination
- Use `/tmp` for temporary storage instead

---

## 9. File Overwrite (`overwrite_file`)

**Patterns Detected:**
- `> /etc/passwd` - Overwrite system file with nothing
- `> important.txt` - Create zero-byte file

**Why It's Dangerous:**
The `>` operator truncates the file to zero bytes before writing:
- Original content is lost immediately
- Even if you Ctrl+C, file is already empty
- System files can be corrupted
- No undo

**Real-World Impact:**
Common mistake when you meant to use `>>` (append) instead of `>` (overwrite).

**Safe Alternative:**
- Use `>>` to append instead of `>`
- Use text editors to modify files
- Backup before modifying system files
- Use `tee -a` for appending with sudo
- Test with non-critical files first

---

## 10. Random Data Overwrite (`dd_random`)

**Patterns Detected:**
- `dd if=/dev/random of=/dev/sda` - Fill disk with random data
- `dd if=/dev/urandom of=/dev/sdb` - Fill with pseudo-random data

**Why It's Dangerous:**
Overwrites every byte on the disk with random data:
- Makes data recovery impossible
- Even professional recovery services can't help
- Destroys all partitions and data
- Takes hours to complete

**Real-World Use:**
Legitimate use for secure disk wiping before disposal, but catastrophic if:
- Wrong device specified
- Run on production system
- No backup exists

**Safe Alternative:**
- Use dedicated secure erase tools (`shred`, `hdparm --security-erase`)
- Verify device name multiple times
- Physically label disks to avoid confusion
- Use disk serial numbers to confirm
- Understand the consequences before running

---

## 11. Kernel Panic Trigger (`kernel_panic`)

**Patterns Detected:**
- `echo c > /proc/sysrq-trigger` - Trigger kernel crash

**Why It's Dangerous:**
Immediately crashes the Linux kernel:
- System goes down hard
- No graceful shutdown
- Potential data loss
- Requires reboot

**Real-World Use:**
This is a debugging tool for kernel developers to:
- Test crash dump mechanisms
- Debug kernel issues
- Force system into specific states

**Safe Alternative:**
- Never write to `/proc/sysrq-trigger` unless debugging
- This is a system debugging feature, not for normal use
- Use proper shutdown commands (`shutdown`, `reboot`)
- Understand SysRq keys before using

---

## Caution-Level Patterns

MairuCLI also detects **4 caution-level patterns** that are risky but have legitimate uses. You'll be asked to confirm before proceeding.

### 1. Root Shell Access (`sudo_shell`)
**Commands:** `sudo su`, `sudo bash`, `sudo sh`, `sudo -i`

**Risk:** Disables all safety checks. One mistake in root shell can damage the entire system.

**When to use:** Only when you need to run multiple commands as root. Prefer `sudo command` for single commands.

---

### 2. Permissive Permissions (`chmod_permissive`)
**Commands:** `chmod 666`, `chmod 755`, `chmod 775`

**Risk:** Makes files accessible to other users. Potential security vulnerability or data exposure.

**When to use:** When you need to share files with other users. Consider if read-only (`644`) is sufficient.

---

### 3. Firewall Disable (`firewall_disable`)
**Commands:** `ufw disable`, `iptables -F`, `systemctl stop firewalld`

**Risk:** Exposes system to network attacks. All ports become accessible.

**When to use:** Temporary debugging on trusted networks only. Always re-enable afterward.

---

### 4. SELinux Disable (`selinux_disable`)
**Commands:** `setenforce 0`

**Risk:** Disables mandatory access control. Significantly weakens system security.

**When to use:** Debugging SELinux policy issues. Fix the policy instead of disabling SELinux.

---

## Summary

| Pattern | Severity | Impact | Recovery |
|---------|----------|--------|----------|
| rm_dangerous | Critical | Data loss | Impossible without backup |
| chmod_777 | High | Security breach | Fix permissions |
| dd_zero | Critical | Disk destruction | Impossible |
| drop_database | Critical | Data loss | Impossible without backup |
| fork_bomb | High | System crash | Reboot required |
| redirect_to_disk | Critical | Disk corruption | Impossible |
| mkfs_disk | Critical | Data loss | Impossible |
| mv_to_null | High | Data loss | Impossible |
| overwrite_file | Medium | File loss | Impossible |
| dd_random | Critical | Data loss | Impossible |
| kernel_panic | High | System crash | Reboot required |

---

## Educational Purpose

MairuCLI is designed to teach CLI safety through:
- **Prevention:** Blocks dangerous commands before execution
- **Education:** Explains why commands are dangerous
- **Alternatives:** Suggests safe ways to accomplish goals
- **Entertainment:** Makes learning fun with Halloween theme

**Remember:** This is an educational tool. Always be careful with real systems, even with MairuCLI running.

---

## References

- [CLI_Troubled.md](reference/cli-dangers.md) - Comprehensive CLI dangers reference
- Real-world incidents documented in industry reports
- Security best practices from OWASP and NIST

---

**Want to try MairuCLI?** See [QUICKSTART.md](../QUICKSTART.md) for a guided tour!
