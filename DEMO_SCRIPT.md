# MairuCLI Demo Script

This script demonstrates all the fun features of MairuCLI for the hackathon demo video.

## Demo Flow (3 minutes)

### 1. Introduction (30 seconds)
```
"Hi! I'm demonstrating MairuCLI - a Halloween-themed CLI safety wrapper
that I built using Kiro AI. It catches dangerous commands before they
destroy your system, with a spooky twist!"
```

### 2. Startup & Help (30 seconds)
```bash
python -m src.main
help
```

**Show:**
- Halloween-themed welcome banner
- Help command listing safe and dangerous commands
- "DON'T try these!" section (reverse psychology)

### 3. Safe Commands (20 seconds)
```bash
pwd
echo Hello from MairuCLI!
cd ..
pwd
```

**Show:** Normal commands work fine

### 4. System Directory Protection (40 seconds)
```bash
rm C:\Windows\System32\test.dll    # Windows
# or
rm /etc/passwd                      # Linux
```
**Show:**
- 🛑 "STOP RIGHT THERE!" warning
- Explanation of what the directory contains
- Why it's dangerous to modify
- Safe alternatives (user directories)

**Narration:**
"MairuCLI protects system directories across Windows, Linux, and macOS.
It teaches beginners which directories are safe to work in!"

### 5. Dangerous Command Detection (60 seconds)
```bash
rm -rf /
```
**Show:**
- ASCII art warning
- "YOU'RE FIRED!" message
- Educational explanation
- Safe alternatives

```bash
chmod 777 secret.txt
```
**Show:** Different warning for permission issues

```bash
DROP DATABASE production
```
**Show:** Database destruction warning

### 6. "I Told You So" Feature (40 seconds)
```bash
rm -rf /
```
**Show:** "Wait... Haven't we been here before?"

```bash
rm -rf /
```
**Show:** "Seriously? I told you so..."

```bash
rm -rf /
```
**Show:** "REALLY?! Okay, I give up."

**Narration:** "The more you try, the more sarcastic it gets!"

### 7. Typo Entertainment (20 seconds)
```bash
sl
cd..
```

**Show:** Fun typo corrections with emoji

### 8. Statistics (20 seconds)
```bash
stats
```

**Show:**
- Total saves count
- Breakdown of dangerous vs typos
- Sarcastic comment based on count

### 9. Kiro Workflow Showcase (20 seconds)

**Screen recording of:**
- Steering files (.kiro/steering/)
- Spec files (.kiro/specs/mairu-cli/)
- Show how Kiro helped with:
  - Requirements gathering
  - Design decisions
  - Implementation guidance

**Narration:**
"I built this entire project using Kiro's Spec-Driven Development workflow.
Kiro helped me go from idea to implementation in just a few hours!"

### 10. Conclusion (20 seconds)
```bash
exit
```

**Show:** Goodbye message

**Narration:**
"MairuCLI: Making CLI mistakes fun and educational!
Check out the code on GitHub, and remember - stay curious, stay safe!"

---

## Key Points to Emphasize

1. **Educational Value**: Not just blocking commands, but teaching why they're dangerous
2. **Humor**: Halloween theme, escalating sarcasm, "I told you so"
3. **Kiro Integration**: Built using Kiro's AI-assisted development
4. **Demo-Friendly**: Visual ASCII art, colorful output, emoji
5. **Complete**: Fully functional CLI wrapper with real command execution

---

## Technical Highlights for Judges

- **Pattern Recognition**: Regex-based dangerous command detection
- **State Management**: Tracks warned commands and statistics
- **Builtin Commands**: Implements shell builtins (cd, pwd, etc.)
- **System Integration**: Safely passes commands to system shell
- **Error Handling**: Graceful handling of edge cases
- **Code Quality**: Type hints, docstrings, clean architecture

---

## Bonus: Live Interaction

If time permits, take questions and demonstrate:
- Adding new dangerous patterns
- Customizing warning messages
- Showing the code structure
