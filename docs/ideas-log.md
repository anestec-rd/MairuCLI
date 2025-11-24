# MairuCLI - Ideas Log

## Purpose
This document tracks feature ideas, inspirations, and potential improvements for MairuCLI. Ideas are logged with dates and can be marked as implemented, deferred, or rejected.

---

## 2025-11-24 (Day 8) - Initial Brainstorm

### Current State Analysis
**What we have:**
- 11 dangerous command patterns
- 20 builtin commands
- Achievement system
- Category-based variation system (scalable to 50+ patterns)
- System directory protection
- Halloween theme throughout

**What's working well:**
- Educational approach
- Halloween party aesthetic (not horror)
- Variation system is scalable
- Test coverage is comprehensive

**Potential gaps:**
- Limited to command-line dangers
- No network-related dangers yet
- No package manager dangers (npm, pip)
- No git-related dangers
- Limited interactive features

---

## Ideas by Category

### 🔴 Dangerous Command Patterns (High Priority)

#### Network & Remote Operations
- [ ] **`curl | bash` pattern** - Piping untrusted scripts directly to bash
  - Educational value: Teaches about script execution risks
  - Real-world relevance: Common attack vector
  - Halloween theme: "Inviting vampires into your home"

- [ ] **`wget` malicious URLs** - Downloading from suspicious sources
  - Educational value: URL safety awareness
  - Real-world relevance: Malware distribution

- [ ] **`ssh` with password in command** - Exposing credentials
  - Educational value: Security best practices
  - Real-world relevance: Credential leaks

#### Package Manager Dangers
- [ ] **`npm install` without verification** - Installing unverified packages
  - Educational value: Supply chain security
  - Real-world relevance: npm package attacks

- [ ] **`pip install` from untrusted sources**
  - Educational value: Python package security

- [ ] **`sudo npm install -g` as root**
  - Educational value: Privilege escalation risks

#### Git Operations
- [ ] **`git push --force` to main/master**
  - Educational value: Version control best practices
  - Real-world relevance: Team collaboration disasters

- [ ] **`git reset --hard` without backup**
  - Educational value: Data loss prevention

- [ ] **`git clean -fdx`** - Deleting untracked files
  - Educational value: Working directory management

#### Compression & Archives
- [ ] **`tar` extraction without inspection** - `tar xzf unknown.tar.gz`
  - Educational value: Archive safety
  - Real-world relevance: Tar bombs, malicious archives

- [ ] **`unzip` with path traversal** - Archives with `../` paths
  - Educational value: Path traversal attacks

---

### 🟡 Interactive Features (Medium Priority)

#### Learning Modes
- [ ] **Tutorial Mode** - Step-by-step CLI learning
  - Guided lessons on safe commands
  - Progressive difficulty
  - Achievement rewards

- [ ] **Challenge Mode** - "Can you spot the danger?"
  - Present commands, user identifies risks
  - Educational quiz format

- [ ] **Story Mode** - Narrative-driven learning
  - Halloween-themed story
  - Commands unlock story progression

#### Social Features
- [ ] **Leaderboard** - Compare achievements with friends
  - Local file-based (no server needed)
  - Export/import achievement data

- [ ] **Share Warnings** - Export funny warning screenshots
  - ASCII art + message as text file
  - Social media friendly format

---

### 🟢 Quality of Life (Low Priority)

#### Customization
- [ ] **Theme Selection** - Multiple holiday themes
  - Halloween (current)
  - Christmas
  - Cyberpunk
  - Minimal (for serious use)

- [ ] **Difficulty Levels**
  - Beginner: More warnings, more help
  - Expert: Fewer warnings, assume knowledge

- [ ] **Language Support** - Japanese localization
  - All messages in Japanese
  - Cultural adaptation of humor

#### Convenience
- [ ] **Command Suggestions** - "Did you mean...?"
  - Typo correction beyond current patterns
  - Context-aware suggestions

- [ ] **Bookmark Commands** - Save frequently used commands
  - Quick access to safe commands
  - Personal command library

---

## Ideas from External Sources

### To Research
- [ ] Famous CLI disasters (GitLab, Pixar, AWS)
- [ ] Stack Overflow "dangerous command" questions
- [ ] Reddit r/sysadmin horror stories
- [ ] XKCD comics about CLI dangers
- [ ] Security vulnerability databases (CVE)

---

## Rejected Ideas (With Reasons)

### `lie` command - Inverts true/false in files
**Reason:** Questionable educational value, could be confusing rather than helpful
**Date:** 2025-11-23
**Status:** Deferred indefinitely

---

## Implemented Ideas

### ✅ System Directory Protection
**Implemented:** 2025-11-22 (Day 6)
**Impact:** Prevents catastrophic system damage
**User Feedback:** Positive, requested by testers

### ✅ Category-Based Variation System
**Implemented:** 2025-11-23 (Day 7)
**Impact:** Scalable to 50+ patterns with minimal duplication
**User Feedback:** N/A (internal improvement)

### ✅ Achievement Categorization
**Implemented:** 2025-11-23 (Day 7)
**Impact:** Better stats display, easier to extend
**User Feedback:** N/A (internal improvement)

---

## Next Steps

1. **Research Phase** (Today)
   - Investigate CLI disasters
   - Identify top 10 new dangerous patterns
   - Prioritize by educational value

2. **Design Phase** (Tomorrow)
   - Create specs for top 3 patterns
   - Design new interactive features
   - Plan implementation

3. **Implementation Phase** (Day 10+)
   - Implement highest priority patterns
   - Test with users
   - Iterate based on feedback

---

## Notes

- Keep Halloween theme consistent
- Prioritize educational value over entertainment
- Every feature should teach something
- Test with actual beginners (children, CLI novices)
- Document real-world incidents for credibility

---

**Last Updated:** 2025-11-24 17:10
**Next Review:** Daily during active development
