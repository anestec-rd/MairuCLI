# Caution-Level Warnings Design

**Date:** 2025-11-19
**Status:** Planned (Not Yet Implemented)
**Priority:** High (Educational Value)

---

## Overview

Implement a second tier of warnings for commands that are risky but not immediately catastrophic. These commands require careful consideration but have legitimate uses.

## Motivation

**Educational Gap:**
- Current system: Binary (BLOCK or ALLOW)
- Reality: Many commands are "use with caution"
- Need: Teach users to think critically about command usage

**Examples:**
- `sudo su` - Legitimate for admin work, but risky if misused
- `chmod 666` - Sometimes needed, but often a security mistake
- `ufw disable` - Necessary for debugging, dangerous in production

## Design

### Three-Tier Warning System

```
🔥 CRITICAL (Current)
├─ Immediate data loss/system destruction
├─ Always blocked with ASCII art
└─ Examples: rm -rf /, dd, DROP DATABASE

⚠️  CAUTION (New)
├─ Security/stability risks
├─ Light warning + educational message
├─ User can proceed after confirmation
└─ Examples: sudo su, chmod 666, firewall disable

✅ SAFE (Current)
├─ Normal commands
└─ No warning
```

### User Experience

#### Critical Warning (Current)
```
🔥 YOU'RE FIRED! 🔥
[ASCII ART]
This command deletes EVERYTHING!
[BLOCKED - Cannot proceed]
```

#### Caution Warning (New)
```
⚠️  Heads Up! Think Carefully.

Command: sudo su
Risk: Entering root shell - all safety checks disabled
Impact: One mistake could damage the entire system

💡 What to consider:
  • Do you really need full root access?
  • Could you use 'sudo command' instead?
  • Are you in the right directory?

Continue anyway? (y/n): _
```

## Implementation Plan

### 1. Add CAUTION_PATTERNS to interceptor.py

```python
CAUTION_PATTERNS: Dict[str, Dict[str, str]] = {
    "sudo_shell": {
        "pattern": r"sudo\s+(su|bash|sh|-i)(?:\s|$)",
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
    "chmod_permissive": {
        "pattern": r"chmod\s+(-R\s+)?(666|755|775)",
        "category": "permissions",
        "severity": "medium",
        "risk": "Making files readable/writable by others",
        "impact": "Potential security vulnerability or data exposure",
        "considerations": [
            "Who needs access to this file?",
            "Is 644 (read-only for others) sufficient?",
            "Are you setting permissions on sensitive data?"
        ]
    },
    "firewall_disable": {
        "pattern": r"(iptables\s+-F|ufw\s+disable|systemctl\s+stop\s+firewalld)",
        "category": "security",
        "severity": "high",
        "risk": "Disabling firewall protection",
        "impact": "System exposed to network attacks",
        "considerations": [
            "Is this a temporary debugging step?",
            "Will you re-enable the firewall?",
            "Are you on a trusted network?"
        ]
    },
    "selinux_disable": {
        "pattern": r"setenforce\s+0",
        "category": "security",
        "severity": "high",
        "risk": "Disabling SELinux mandatory access control",
        "impact": "Weakens system security significantly",
        "considerations": [
            "Could you fix the SELinux policy instead?",
            "Is this permanent or temporary?",
            "Do you understand the security implications?"
        ]
    }
}
```

### 2. Update check_command() in interceptor.py

```python
def check_command(command: str) -> Tuple[str, str]:
    """
    Returns: (level, pattern_name)
    level: "critical", "caution", or "safe"
    """
    # Check critical patterns first
    for pattern_name, pattern_data in DANGEROUS_PATTERNS.items():
        if re.search(pattern_data["pattern"], command, re.IGNORECASE):
            return "critical", pattern_name

    # Check caution patterns
    for pattern_name, pattern_data in CAUTION_PATTERNS.items():
        if re.search(pattern_data["pattern"], command, re.IGNORECASE):
            return "caution", pattern_name

    # Check typo patterns
    for pattern_name, pattern_data in TYPO_PATTERNS.items():
        if re.search(pattern_data["pattern"], command, re.IGNORECASE):
            return "critical", f"typo_{pattern_name}"

    return "safe", ""
```

### 3. Add CautionWarning component

Create `src/display/caution_warning.py`:

```python
class CautionWarning:
    """Display caution-level warnings with user confirmation."""

    def display(self, pattern_name: str, command: str) -> bool:
        """
        Display caution warning and get user confirmation.

        Returns:
            True if user wants to proceed, False to cancel
        """
        pattern = CAUTION_PATTERNS[pattern_name]

        print()
        print("=" * 60)
        print(f"⚠️  {colorize('Heads Up! Think Carefully.', 'orange')}")
        print("=" * 60)
        print()
        print(f"Command: {colorize(command, 'purple')}")
        print(f"Risk: {pattern['risk']}")
        print(f"Impact: {pattern['impact']}")
        print()
        print(colorize("💡 What to consider:", "chocolate"))
        for consideration in pattern['considerations']:
            print(f"  • {consideration}")
        print()

        # Get user confirmation
        response = input(colorize("Continue anyway? (y/n): ", "orange"))
        return response.lower() in ['y', 'yes']
```

### 4. Update main.py process_command()

```python
def process_command(command: str) -> str:
    # ... existing code ...

    # Check if dangerous or caution command
    level, pattern_name = check_command(command)

    if level == "critical":
        show_warning(pattern_name, command)
        return ""
    elif level == "caution":
        if not show_caution_warning(pattern_name, command):
            print("Command cancelled.")
            return ""
        # User confirmed - proceed to execute

    # Execute in system shell (safe or confirmed caution command)
    execute_in_system_shell(command)
    return ""
```

## Educational Value

### What Users Learn

1. **Critical Thinking**: Not all commands are black/white
2. **Context Matters**: Same command can be safe or risky depending on situation
3. **Security Awareness**: Understanding implications before acting
4. **Best Practices**: Learning safer alternatives

### Example Learning Moments

**Scenario 1: sudo su**
- User types: `sudo su`
- System asks: "Do you really need full root access?"
- User thinks: "Actually, I just need to edit one file"
- User learns: `sudo nano /etc/config` is safer

**Scenario 2: chmod 666**
- User types: `chmod 666 config.txt`
- System asks: "Who needs access to this file?"
- User thinks: "Only me, actually"
- User learns: `chmod 600` is more secure

## Statistics Tracking

Add to Statistics class:
```python
self._stats["caution_warnings_shown"] = 0
self._stats["caution_warnings_proceeded"] = 0
self._stats["caution_warnings_cancelled"] = 0
```

## Achievements

New achievements:
- **Thoughtful User**: Cancelled a caution command 3 times
- **Risk Taker**: Proceeded with 5 caution commands
- **Learning Curve**: Saw all caution warning types

## Testing

### Test Cases

1. **sudo su** → Show caution, allow proceed
2. **sudo ls** → No warning (safe sudo usage)
3. **chmod 666 file** → Show caution
4. **chmod 644 file** → No warning (safe permission)
5. **ufw disable** → Show caution
6. **User cancels** → Command not executed
7. **User proceeds** → Command executed

## Future Enhancements

### Phase 2: Context-Aware Warnings
- Check current directory (warning if in /)
- Check file ownership (warning if system file)
- Check network status (warning if public network)

### Phase 3: Learning Mode
- Track which warnings user ignores
- Adjust warning frequency based on user expertise
- Suggest safer alternatives automatically

## Implementation Checklist

- [ ] Add CAUTION_PATTERNS to interceptor.py
- [ ] Update check_command() to return warning level
- [ ] Create CautionWarning component
- [ ] Update main.py to handle caution warnings
- [ ] Add user confirmation prompt
- [ ] Update statistics tracking
- [ ] Add new achievements
- [ ] Test all caution patterns
- [ ] Update help command to mention caution warnings
- [ ] Document in README.md

## Estimated Time

- Implementation: 30-45 minutes
- Testing: 15 minutes
- Documentation: 10 minutes
- **Total: ~1 hour**

---

**This feature significantly enhances the educational value of MairuCLI by teaching nuanced decision-making rather than just blocking dangerous commands.**
