---
inclusion: always
---

# IT Wordplay Guidelines for MairuCLI

## Purpose

MairuCLI uses IT-themed wordplay to make warnings more engaging for technical audiences while maintaining cultural sensitivity and international appeal.

## Core Principles

### 1. Technical Humor Over Cultural References

**Prefer:**
- IT terminology and concepts
- Technical puns and wordplay
- Industry-specific jokes

**Avoid:**
- Religious references
- Cultural-specific idioms
- Potentially offensive content

### 2. Wordplay Techniques

#### A. Sound-Alike Substitution
Replace potentially sensitive words with similar-sounding IT terms.

**Example:**
- "Satan" → "SATA" (storage interface)
  - Sound: Nearly identical pronunciation
  - Context: Disk destruction → Disk interface
  - Result: Double meaning that's both funny and appropriate

#### B. Technical Metaphors
Use IT concepts as metaphors for the warning message.

**Examples:**
- "Memory loss" → "RAM not found"
- "Permission denied" → "Error 403: Forbidden"
- "Abort" → "Ctrl+C won't save you"

#### C. Technical Accuracy with Humor
Combine accurate technical terms with humorous context.

**Examples:**
- "RAID 0 without the RAID... just 0" (no redundancy)
- "Disk I/O error: Your data not found"
- "SIGTERM sent! This is not a drill!"

## Wordplay Checklist

When creating new warning messages, ask:

### ✅ Does it work?
- [ ] Is the IT term widely known?
- [ ] Does it sound similar to the original?
- [ ] Does it fit the technical context?
- [ ] Is it funny to technical audiences?

### ✅ Is it appropriate?
- [ ] No religious references?
- [ ] No cultural insensitivity?
- [ ] No offensive content?
- [ ] Works internationally?

### ✅ Is it educational?
- [ ] Teaches an IT concept?
- [ ] Reinforces technical knowledge?
- [ ] Makes sense to beginners?

## IT Wordplay Examples

### Successful Wordplay

#### 1. "Not today, SATA!"
- **Original:** "Not today, Satan!"
- **IT Term:** SATA (Serial ATA storage interface)
- **Why it works:**
  - Nearly identical pronunciation
  - Disk destruction context (rm -rf)
  - Double meaning (storage + Satan parody)
  - Culturally neutral

#### 2. "RAM not found... Who are you again?"
- **Original:** "Who are you again? I don't remember you..."
- **IT Term:** RAM (Random Access Memory)
- **Why it works:**
  - Memory loss metaphor
  - Technical accuracy (RAM = memory)
  - Funny to technical audiences
  - Educational value

#### 3. "Error 403: Forbidden by your future self"
- **Original:** "By your future self"
- **IT Term:** HTTP 403 Forbidden error
- **Why it works:**
  - Permission context (chmod 777)
  - Accurate HTTP status code
  - Technical humor
  - Widely understood

#### 4. "Ctrl+C won't save you now!"
- **Original:** "This is not a drill!"
- **IT Term:** Ctrl+C (interrupt signal)
- **Why it works:**
  - Abort/cancel context
  - Universal keyboard shortcut
  - Implies urgency
  - Technical accuracy

## Common IT Terms for Wordplay

### Storage & Disk
- SATA, RAID, SSD, HDD
- Disk I/O, filesystem, partition
- Backup, snapshot, clone

### Memory
- RAM, ROM, cache, buffer
- Memory leak, segfault, core dump
- Heap, stack, pointer

### Networking
- HTTP status codes (403, 404, 500)
- TCP/IP, DNS, ping, packet loss
- Firewall, port, socket

### Process Control
- Ctrl+C, SIGTERM, SIGKILL
- Fork, exec, daemon, zombie process
- Thread, mutex, deadlock

### Errors & Debugging
- Segmentation fault, null pointer
- Stack overflow, buffer overflow
- Exception, panic, crash

### Security
- Permission denied, access violation
- Encryption, hash, salt
- Vulnerability, exploit, patch

## Anti-Patterns to Avoid

### ❌ Forced Wordplay
Don't force IT terms where they don't fit naturally.

**Bad Example:**
```
"Not today, TCP!" (doesn't relate to the command)
```

### ❌ Obscure Terms
Avoid overly technical or obscure terms.

**Bad Example:**
```
"Not today, SCSI!" (outdated, less known than SATA)
```

### ❌ Breaking the Joke
Don't over-explain the wordplay.

**Bad Example:**
```
"Not today, SATA! (Get it? Like Satan but it's a disk interface!)"
```

## Process for New Content

### When Adding New Warnings

1. **Write the message naturally**
   - Focus on the warning content first
   - Make it clear and educational

2. **Identify wordplay opportunities**
   - Look for common words/phrases
   - Check if IT terms could substitute
   - Consider sound-alike possibilities

3. **Apply the checklist**
   - Does it work? (technical fit)
   - Is it appropriate? (cultural sensitivity)
   - Is it educational? (learning value)

4. **Test with examples**
   - Read it aloud
   - Show to technical colleagues
   - Check international understanding

5. **Document the wordplay**
   - Add to this steering file
   - Explain why it works
   - Provide context

## Examples in Context

### rm -rf / Warning
```json
{
  "title": "NOPE. JUST NOPE.",
  "subtitle": "(Not today, SATA!)"
}
```
**Wordplay:** Satan → SATA (disk interface)
**Context:** Disk destruction command
**Why:** Perfect technical and contextual fit

### chmod 777 Warning
```json
{
  "title": "PERMISSION DENIED!",
  "subtitle": "(Error 403: Forbidden by your future self)"
}
```
**Wordplay:** HTTP 403 error code
**Context:** Permission modification
**Why:** Accurate technical metaphor

### Memory/Filesystem Warning
```json
{
  "title": "MEMORY LOSS!",
  "subtitle": "(RAM not found... Who are you again?)"
}
```
**Wordplay:** Memory → RAM
**Context:** Filesystem deletion
**Why:** Technical accuracy + humor

## Maintenance

### Regular Review
- Review all wordplay quarterly
- Check for outdated terms (e.g., floppy disk references)
- Update based on user feedback
- Ensure continued cultural appropriateness

### Community Contributions
When accepting community-contributed wordplay:
- Apply the same checklist
- Verify technical accuracy
- Check cultural sensitivity
- Test with diverse audiences

## Success Metrics

Good IT wordplay should:
- ✅ Make technical users smile
- ✅ Teach or reinforce IT concepts
- ✅ Work across cultures
- ✅ Enhance the Halloween theme
- ✅ Maintain educational value

---

**Remember:** The goal is to make warnings memorable and engaging for technical audiences while remaining appropriate and educational for all users.

**When in doubt:** Choose clarity and appropriateness over cleverness.
