# Day 13 Plan - Demo Preparation & macOS Testing

**Date:** 2025-11-29 (Planned)
**Estimated Time:** 5-7 hours
**Focus:** Demo script creation, video recording, macOS verification, and enhancements

---

## 🎯 Goals

1. **Create demo script** - Showcase all key features
2. **Record demo video** - 3-minute target
3. **macOS testing** - Verify cross-platform compatibility
4. **Video editing** - Polish final video
5. **Timeline enhancement** - Real-time simulation for dramatic effect
6. **Windows command translation** - Address Unix/Windows command differences
7. **Personarrative reflection** - Document AI agent collaboration insights

---

## 📋 Task List

### Morning Session (3-4 hours)

#### 1. macOS Testing Guide & Verification (1-1.5 hours)

**Background:**
- MairuCLI developed on Windows
- Tested on Linux
- macOS not yet tested (no hardware access)
- Team member has macOS - can verify!

**Create Testing Guide for macOS User:**

**File:** `docs/MACOS_TESTING_GUIDE.md`

```markdown
# macOS Testing Guide for MairuCLI

## Setup Instructions

### 1. Prerequisites
- macOS 10.15 (Catalina) or later
- Python 3.8 or later
- Terminal app

### 2. Installation
```bash
# Clone repository
git clone [repository-url]
cd MairuCLI

# Verify Python version
python3 --version  # Should be 3.8+

# Install dependencies (if any)
pip3 install -r requirements.txt  # If requirements.txt exists
```

### 3. Running MairuCLI
```bash
python3 -m src.main
```

## Testing Checklist

### Basic Functionality (15 minutes)
- [ ] Welcome banner displays correctly
- [ ] Colors display properly (orange, purple, green, red)
- [ ] ASCII art renders correctly
- [ ] Help command works
- [ ] Exit command works

### Builtin Commands (20 minutes)
Test these commands:
- [ ] `pwd` - Shows current directory
- [ ] `ls` - Lists files
- [ ] `cd <dir>` - Changes directory
- [ ] `echo <text>` - Prints text
- [ ] `cat <file>` - Shows file contents
- [ ] `whoami` - Shows username
- [ ] `date` - Shows current date/time
- [ ] `hostname` - Shows computer name
- [ ] `tree` - Shows directory tree
- [ ] `stats` - Shows statistics
- [ ] `breakdown` - Lists available breakdowns

### Dangerous Pattern Detection (30 minutes)
Test these dangerous commands (they should be BLOCKED):

**Critical Patterns:**
- [ ] `rm -rf /` - Should show "YOU'RE FIRED" warning
- [ ] `chmod 777 file.txt` - Should show permission warning
- [ ] `chmod 000 file.txt` - Should show lockout warning
- [ ] `dd if=/dev/zero of=/dev/sda` - Should show disk wipe warning
- [ ] `:(){ :|:& };:` - Should show fork bomb warning

**Expected Behavior:**
- Warning displays with ASCII art
- Command is BLOCKED (not executed)
- Educational prompt appears: "Want to learn more?"

### Educational Breakdown System (20 minutes)
- [ ] Type `breakdown` - Shows available patterns
- [ ] Type `breakdown rm_dangerous` - Shows full breakdown
- [ ] Verify slow printing works (line-by-line display)
- [ ] Check timeline simulation displays
- [ ] Verify GitLab 2017 incident story shows

After dangerous command warning:
- [ ] Prompt appears: "Type 'breakdown' to learn more"
- [ ] Type `breakdown` - Shows educational content
- [ ] Press Enter - Skips educational content

### System Directory Protection (30 minutes)

**macOS-Specific Protected Directories:**
Test these commands (should be BLOCKED):

**Critical (Should Block Immediately):**
- [ ] `rm -rf /System` - macOS system directory
- [ ] `rm -rf /Library` - System library
- [ ] `rm -rf /bin` - Essential binaries
- [ ] `rm -rf /sbin` - System binaries
- [ ] `rm -rf /etc` - System configuration
- [ ] `rm -rf /var` - System variables
- [ ] `chmod 777 /System` - System permission change
- [ ] `mv /bin /tmp/bin` - Moving system directory

**Expected Behavior:**
- Shows system protection warning
- Explains why directory is protected
- Command is BLOCKED
- Educational message about safe zones

**Safe Commands (Should Work Normally):**
- [ ] `rm -rf ~/Documents/test` - User directory (safe)
- [ ] `mkdir ~/test` - User directory (safe)
- [ ] `chmod 755 ~/script.sh` - User file (safe)

### Achievement System (10 minutes)
- [ ] Trigger dangerous command - Check for "First Blood" achievement
- [ ] Trigger 3 dangerous commands - Check for achievements
- [ ] Use 5 safe commands - Check for "Explorer" achievement
- [ ] Type `stats` - Verify achievements display

### Typo Detection (10 minutes)
- [ ] `sl` - Should show steam locomotive
- [ ] `cd..` - Should suggest `cd ..`
- [ ] `grpe` - Should suggest `grep`

## Issues to Report

### If You Find Issues:

**1. Display Issues**
- Colors not showing correctly
- ASCII art rendering problems
- Text alignment issues
- Emoji not displaying

**2. Functional Issues**
- Commands not being blocked
- Wrong warnings displayed
- System protection not working
- Educational breakdown errors

**3. macOS-Specific Issues**
- Protected directories not detected
- Path resolution problems
- Permission issues
- Terminal compatibility

### How to Report

**Create Issue Report:**
```markdown
## macOS Testing Issue

**Environment:**
- macOS Version: [e.g., macOS 14.0 Sonoma]
- Python Version: [e.g., 3.11.5]
- Terminal: [e.g., Terminal.app, iTerm2]

**Issue:**
[Describe what went wrong]

**Expected:**
[What should have happened]

**Actual:**
[What actually happened]

**Steps to Reproduce:**
1. [Step 1]
2. [Step 2]
3. [Step 3]

**Screenshots:**
[If possible]
```

**Send to:** [Your contact method]

## Success Criteria

**macOS Testing Complete When:**
- ✅ All basic functionality works
- ✅ All builtin commands work
- ✅ Dangerous patterns are detected and blocked
- ✅ System directory protection works for macOS paths
- ✅ Educational breakdown displays correctly
- ✅ No critical bugs found
- ✅ Any issues documented

## Expected Results

**Best Case:**
- Everything works perfectly
- No macOS-specific issues
- Can confidently claim "macOS support"

**Likely Case:**
- Minor display issues (easily fixable)
- Some macOS paths need adjustment
- Overall functionality works

**Worst Case:**
- Major compatibility issues
- Need to mark macOS as "experimental"
- Document known limitations

## Notes for Tester

**This is an educational tool:**
- It's designed to teach CLI safety
- It blocks dangerous commands
- It's NOT a production security tool
- Have fun exploring!

**Time Commitment:**
- Full testing: ~2 hours
- Quick smoke test: ~30 minutes
- Your feedback is valuable!

**Thank you for helping test MairuCLI on macOS!** 🎃
```

**Tasks:**
1. Create `docs/MACOS_TESTING_GUIDE.md`
2. Send to team member with macOS
3. Schedule testing session (Day 13)
4. Collect feedback
5. Fix any critical issues
6. Update README.md with results

**Outcomes:**
- **If all tests pass:** Update README to "Tested on macOS ✅"
- **If minor issues:** Document as "Known Issues" and fix if time permits
- **If major issues:** Mark as "Experimental" and document limitations

**Time Estimate:** 1-1.5 hours (guide creation + coordination)

#### 2. Timeline Simulation Enhancement (30-45 minutes)

**Current Issue:**
Timeline simulation shows "+1s", "+2s" instantly, which doesn't convey the real-time horror of watching a disaster unfold.

**Enhancement Idea:**
Make timeline events display in **real-time** to create dramatic tension.

**Example - Fork Bomb Timeline:**
```
Current (Instant):
+0s: First process spawns
+1s: 2 processes running
+2s: 4 processes running
+3s: 8 processes running

Proposed (Real-time):
+0s: First process spawns
[wait 1 second]
+1s: 2 processes running
[wait 1 second]
+2s: 4 processes running
[wait 1 second]
+3s: 8 processes running
```

**Implementation:**
```python
def _display_timeline_realtime(timeline: List[str]) -> None:
    """Display timeline events in real-time for dramatic effect."""
    for event in timeline:
        print(f"    {event}")

        # Extract time from event (e.g., "+1s:", "+2s:")
        if match := re.match(r'\+(\d+)s:', event):
            seconds = int(match.group(1))
            # Wait until next event
            if seconds < len(timeline) - 1:
                time.sleep(1.0)  # Real 1-second delay
```

**Benefits:**
- ✅ Creates real tension and horror
- ✅ User experiences the escalation
- ✅ More memorable and impactful
- ✅ Better educational value (feels the danger)

**Patterns to Apply:**
- Fork bomb (exponential growth)
- rm -rf / (progressive deletion)
- dd disk wipe (percentage progress)

**Considerations:**
- Total time: ~5-10 seconds per breakdown
- Add "Press Enter to skip" option
- Only for timeline sections, not all content

**Time Estimate:** 30-45 minutes

---

#### 3. Windows Command Translation Issue (1-2 hours)

**Critical Discovery:**
Windows doesn't have `rm`, `chmod`, `dd`, etc. - these are Unix commands!

**Current Problem:**
```bash
# On Windows, these don't exist:
rm -rf /          # Should be: del /s /q or rd /s /q
chmod 777 file    # Should be: icacls or attrib
dd if=/dev/zero   # No direct equivalent
```

**Existing Translation:**
- `ls` ↔ `dir` (already implemented)

**Commands Needing Translation:**

| Unix Command | Windows Equivalent | Priority |
|--------------|-------------------|----------|
| `rm -rf` | `del /s /q`, `rd /s /q` | High |
| `chmod` | `icacls`, `attrib` | High |
| `mv` | `move`, `ren` | Medium |
| `cp` | `copy`, `xcopy` | Medium |
| `cat` | `type` | Medium |
| `grep` | `findstr` | Low |
| `dd` | No equivalent | Low |

**Solution Options:**

**Option A: Detect Both Patterns (Recommended)**
```python
DANGEROUS_PATTERNS = {
    "rm_dangerous": {
        "unix": r"rm\s+(-rf|-fr)\s+(/|~)",
        "windows": r"(del|rd)\s+(/s\s+)?(/q\s+)?[A-Z]:\\",
    },
    "chmod_777": {
        "unix": r"chmod\s+(-R\s+)?777",
        "windows": r"icacls\s+.*\s+/grant\s+.*:\(F\)",
    }
}
```

**Option B: Show Educational Message**
```python
# When user types Unix command on Windows
if platform.system() == "Windows" and is_unix_command(cmd):
    print("🎃 Trying Unix commands on Windows?")
    print(f"💡 On Windows, use: {get_windows_equivalent(cmd)}")
    print("🎓 MairuCLI teaches both Unix and Windows commands!")
```

**Option C: Defer to Post-Contest**
- Document as known limitation
- Focus on demo (use WSL or Linux VM)
- Add in v1.6.0

**Recommendation:** Option A + B
- Detect both patterns (safety)
- Educate about differences (learning)
- Time: 1-2 hours

**Decision Point:** Discuss with user before implementing

---

#### 4. PowerShell vs CMD Consideration (Discussion)

**Question:** Should MairuCLI support PowerShell commands?

**PowerShell Dangerous Commands:**
```powershell
Remove-Item -Recurse -Force C:\
Get-ChildItem C:\ -Recurse | Remove-Item -Force
Format-Volume -DriveLetter C -FileSystem NTFS
```

**Pros:**
- ✅ More relevant for modern Windows users
- ✅ PowerShell is default on Windows 10+
- ✅ More powerful (and dangerous) than CMD

**Cons:**
- ❌ Significant scope increase
- ❌ Different syntax patterns
- ❌ Time-constrained (contest deadline)

**Recommendation:** Defer to v1.6.0
- Document as future enhancement
- Focus on Unix commands for demo
- Add PowerShell support post-contest

**Time if implemented:** 3-4 hours (too much for Day 12-13)

---

#### 5. Personarrative Reflection Document (30 minutes)

**Concept:** Personal + Narrative = Personarrative

**Key Insight:**
Kiro's strength is **pair programming**, not just outsourcing.

**Create:** `docs/lessons/personarrative-reflection.md`

```markdown
# Personarrative: AI Agent UI/UX Reflection

**Date:** 2025-11-28
**Context:** Day 12 of MairuCLI development with Kiro

---

## The Concept

**Personarrative** = Personal (個人) + Narrative (文脈)

The UI/UX of AI agents is determined by two factors:
1. **Personal settings** - Individual preferences and context
2. **Narrative context** - The ongoing conversation and shared understanding

---

## Two Types of AI Agents

### Type 1: Outsourcing Agent (分業)
- **Role:** Separate worker, task executor
- **Interaction:** Assign tasks, receive results
- **Benefit:** Fast iteration, parallel work
- **Example:** "Generate 10 test cases for this function"

### Type 2: Collaboration Agent (同業)
- **Role:** Pair programmer, thought partner
- **Interaction:** Discuss, iterate, build together
- **Benefit:** Deeper understanding, no loneliness
- **Example:** Kiro's spec-driven development

---

## Kiro's Strength: Collaboration

**What makes Kiro different:**
- Spec-driven workflow (shared understanding)
- Iterative refinement (not one-shot generation)
- Context preservation (remembers decisions)
- Steering files (personal preferences)

**Personal Experience (2 weeks with Kiro):**
- ✅ Never felt lonely
- ✅ Felt like working with a teammate
- ✅ Could discuss trade-offs and decisions
- ✅ Learned while building

---

## Implications for AI Agent Design

### For Outsourcing Agents
- Optimize for: Speed, parallelization, task completion
- UI/UX: Clear task definition, result delivery
- Context: Minimal (task-focused)

### For Collaboration Agents
- Optimize for: Understanding, iteration, learning
- UI/UX: Conversation, shared artifacts (specs)
- Context: Rich (project history, decisions)

---

## The Personarrative Framework

**Personal Layer:**
- Steering files (coding standards, preferences)
- Project context (goals, constraints)
- Individual style (communication, workflow)

**Narrative Layer:**
- Conversation history
- Shared decisions and rationale
- Evolving understanding

**Together:** Creates unique AI agent experience

---

## Future Research Questions

1. Can we quantify "loneliness" in AI-assisted development?
2. What's the optimal balance between outsourcing and collaboration?
3. How do we preserve narrative context across sessions?
4. Can personarrative be transferred between developers?

---

## Conclusion

Kiro demonstrates that AI agents can be **thought partners**, not just **task executors**.

The key is **Personarrative**: combining personal context with narrative continuity.

This may be the future of AI-assisted development.

---

**Note:** This reflection emerged naturally during MairuCLI development.
The best insights come from doing, not just planning.
```

**Time Estimate:** 30 minutes

---

#### 6. Demo Script Creation (1-1.5 hours)

**Script Structure:**

**Introduction (30 seconds)**
- What is MairuCLI?
- Educational CLI wrapper with Halloween theme
- Built 100% with Kiro

**Feature Showcase (2 minutes)**
1. **Dangerous Command Detection** (30s)
   - Show `rm -rf /` being blocked
   - Show ASCII art and warning

2. **Educational Breakdown** (30s)
   - Type `breakdown` after warning
   - Show slow-printed educational content
   - Highlight GitLab 2017 incident

3. **System Directory Protection** (30s)
   - Try to delete system directory
   - Show protection warning
   - Explain safe zones

4. **Achievement System** (30s)
   - Show stats command
   - Display unlocked achievements
   - Show progression

**Closing (30 seconds)**
- Built with Kiro's Spec-Driven Development
- Educational value
- Call to action

**Script Format:**
```markdown
# MairuCLI Demo Script

## Setup
- Terminal: Full screen, dark theme
- Font size: Large enough for video
- MairuCLI: Already started

## Scene 1: Introduction (0:00-0:30)
[Narration]
"Meet MairuCLI - an educational CLI wrapper that teaches command line safety
through Halloween-themed warnings and interactive learning."

[Action]
- Show welcome banner
- Type `help` briefly

## Scene 2: Dangerous Command Detection (0:30-1:00)
[Narration]
"Watch what happens when I try to delete everything..."

[Action]
- Type: `rm -rf /`
- Show warning with ASCII art
- Highlight "YOU'RE FIRED" message

## Scene 3: Educational Breakdown (1:00-1:30)
[Narration]
"But MairuCLI doesn't just block commands - it teaches you why they're dangerous."

[Action]
- Type: `breakdown`
- Show slow-printed educational content
- Highlight GitLab 2017 incident
- Show timeline simulation

## Scene 4: System Protection (1:30-2:00)
[Narration]
"MairuCLI also protects critical system directories..."

[Action]
- Type: `rm -rf /etc` (or Windows equivalent)
- Show system protection warning
- Explain safe zones concept

## Scene 5: Achievement System (2:00-2:30)
[Narration]
"And it gamifies learning with achievements..."

[Action]
- Type: `stats`
- Show unlocked achievements
- Highlight progression

## Scene 6: Closing (2:30-3:00)
[Narration]
"MairuCLI was built entirely with Kiro using Spec-Driven Development.
It combines education, entertainment, and safety in one Halloween-themed package."

[Action]
- Show final stats
- Type `exit`
- Show goodbye message
```

**Preparation:**
- Write full script with timing
- Practice multiple times
- Adjust timing as needed
- Prepare any props (if needed)

#### 11. Create v1.5.0 Release (15 minutes)

---


## 📊 Updated Time Estimates

| Task | Estimated Time |
|------|----------------|
| macOS Testing Guide | 1-1.5 hours |
| Timeline Enhancement | 30-45 minutes |
| Windows Command Translation | 1-2 hours |
| PowerShell Discussion | 15 minutes |
| Personarrative Reflection | 30 minutes |
| Demo Script Creation | 1-1.5 hours |
| Demo Video Recording | 1-2 hours |
| Video Editing | 30-60 minutes |
| **Total** | **5-7 hours** |

---

## 🎯 Deliverables

### Enhancements
1. **Real-time Timeline Simulation** - Dramatic effect for educational content
2. **Windows Command Support** - Cross-platform command detection
3. **Personarrative Document** - AI collaboration insights

### Demo Materials
1. **Demo Script** - Complete with timing and narration
2. **Demo Video** - 3-minute polished video
3. **macOS Compatibility Report** - Testing results

### Documentation
1. **Platform Support Update** - Windows/Linux/macOS status
2. **Known Limitations** - Windows command differences
3. **Future Enhancements** - PowerShell support roadmap

---

## 📝 Key Decisions

### Timeline Enhancement
**Decision:** Implement real-time simulation
**Rationale:** Creates dramatic tension, better educational impact
**Time:** 30-45 minutes

### Windows Commands
**Decision:** Detect both Unix and Windows patterns + educate
**Rationale:** Safety + learning, manageable scope
**Time:** 1-2 hours

### PowerShell Support
**Decision:** Defer to v1.6.0
**Rationale:** Too large for contest deadline
**Documentation:** Add to TODO.md as future enhancement

### Personarrative Reflection
**Decision:** Document insights now
**Rationale:** Fresh perspective, valuable for contest narrative
**Time:** 30 minutes

---

## 💡 Insights from Day 12 Start

### Technical Insights
1. **Timeline Simulation:** Real-time display creates horror/tension
2. **Cross-platform:** Windows/Unix command differences are significant
3. **PowerShell:** Modern Windows users need different patterns

### Philosophical Insights
4. **Personarrative:** AI agents can be collaborators, not just tools
5. **Kiro's Strength:** Pair programming > outsourcing
6. **No Loneliness:** 2 weeks of development felt like teamwork

---

## 🔄 Day 14 Preview

**Next Day Focus:**
- Final polish and bug fixes
- Contest submission preparation
- Documentation finalization
- Celebration! 🎉

**Prerequisites from Day 13:**
- Demo video complete
- macOS testing done
- All enhancements implemented
- Documentation updated

---

**End of Day 13 Plan**

**Goal:** Complete demo materials and enhancements
**Next:** Day 14 - Final submission preparation
