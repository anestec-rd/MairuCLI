# MairuCLI Implementation Tasks

## Document Information

**Version:** 1.0
**Date:** 2025-11-16
**Based on:** design.md (MVP Scope with Known Limitations)
**Total Time Budget:** 40 hours

---

## Task Overview

This document breaks down the implementation into concrete, actionable tasks. Each task includes:
- Clear objective
- Estimated time
- Dependencies
- Acceptance criteria
- References to requirements/design

### Task Status Legend
- `[ ]` Not started
- `[~]` In progress
- `[x]` Completed
- `[*]` Optional (implement if time permits)

---

## Phase 1: Core Infrastructure (12 hours)

**Goal:** Basic command interception and builtin commands working

### Task 1.1: Project Setup (1 hour)

- [ ] 1.1.1 Create project directory structure
  ```
  mairu-cli/
  ├── src/
  │   ├── __init__.py
  │   ├── main.py
  │   ├── builtins.py
  │   ├── interceptor.py
  │   ├── display.py
  │   └── config.py
  ├── ascii_art/
  ├── tests/
  ├── README.md
  └── requirements.txt (empty for MVP - stdlib only)
  ```
  - _Requirements: Requirement 10 (Installation)_
  - _Acceptance: Directory structure exists, all files created_

- [ ] 1.1.2 Set up Git repository
  - Initialize git
  - Create .gitignore (Python standard)
  - Initial commit with structure
  - _Acceptance: Git repo initialized, .gitignore present_

- [ ] 1.1.3 Create basic README.md skeleton
  - Project description
  - Installation instructions (placeholder)
  - Usage (placeholder)
  - Limitations section (from design.md)
  - _Acceptance: README.md exists with sections_

---

### Task 1.2: Builtin Commands Implementation (3 hours)

- [ ] 1.2.1 Implement `builtins.py` class structure (30 min)
  - Create `BuiltinCommands` class
  - Add class variables (`_history`, `_prev_dir`)
  - Implement `is_builtin()` method
  - Implement `execute_builtin()` dispatcher
  - _Requirements: Requirement 6 (Safe Mode Operation)_
  - _Acceptance: Class structure complete, methods defined_

- [ ] 1.2.2 Implement `cd` command (45 min)
  - Handle `cd` (go to home)
  - Handle `cd ~` (go to home)
  - Handle `cd -` (go to previous directory)
  - Handle `cd /path` (go to specific path)
  - Error handling (FileNotFoundError, PermissionError)
  - _Acceptance: All cd variations work, errors handled gracefully_

- [ ] 1.2.3 Implement `pwd` command (15 min)
  - Print current working directory
  - _Acceptance: pwd shows correct directory_

- [ ] 1.2.4 Implement `echo` command (15 min)
  - Print arguments separated by spaces
  - _Acceptance: echo prints text correctly_

- [ ] 1.2.5 Implement `export` command (30 min)
  - Handle `export VAR=value`
  - Handle `export` (show all env vars)
  - Error handling for invalid format
  - _Acceptance: Environment variables set correctly_

- [ ] 1.2.6 Implement `history` command (15 min)
  - Display command history with line numbers
  - _Acceptance: History shows all previous commands_

- [ ] 1.2.7 Implement `add_to_history()` method (15 min)
  - Append command to history list
  - _Acceptance: Commands added to history_

- [ ] 1.2.8 Test all builtin commands manually (15 min)
  - Test each command individually
  - Test error cases
  - _Acceptance: All builtins work as expected_

---

### Task 1.3: Main REPL Loop (2 hours)

- [ ] 1.3.1 Implement `main.py` entry point (30 min)
  - `main()` function
  - Call `display_welcome_banner()`
  - Call `repl_loop()`
  - _Requirements: Requirement 1 (Command Interception)_
  - _Acceptance: main() runs without errors_

- [ ] 1.3.2 Implement `repl_loop()` (45 min)
  - Display prompt with color
  - Read user input
  - Handle Ctrl+C / Ctrl+D gracefully
  - Call `process_command()`
  - Exit on "EXIT" return value
  - _Acceptance: REPL loop runs continuously, exits cleanly_

- [ ] 1.3.3 Implement `process_command()` (45 min)
  - Add command to history
  - Check for exit/quit
  - Parse command into parts
  - Check if builtin → execute
  - Check if dangerous → warn
  - Otherwise → execute in shell
  - Return "EXIT" or ""
  - _Acceptance: Command routing works correctly_

---

### Task 1.4: Command Interceptor (4 hours)

- [ ] 1.4.1 Create `interceptor.py` structure (30 min)
  - Import statements
  - Define `DANGEROUS_PATTERNS` dictionary
  - Define `TYPO_PATTERNS` dictionary (empty for now)
  - _Requirements: Requirement 1 (Command Interception), Requirement 7 (Pattern Recognition)_
  - _Acceptance: File structure complete_

- [ ] 1.4.2 Define 5 dangerous patterns (1 hour)
  - `rm_root`: `rm -rf /` and variations
  - `chmod_777`: `chmod 777` and variations
  - `dd_zero`: `dd if=/dev/zero`
  - `drop_database`: `DROP DATABASE`
  - `sudo_rm_var`: `sudo rm -rf $VAR`
  - Include metadata (category, severity, art_file)
  - _Reference: CLI_Troubled.md sections 1-2_
  - _Acceptance: All 5 patterns defined with metadata_

- [ ] 1.4.3 Implement `check_command()` function (1 hour)
  - Loop through DANGEROUS_PATTERNS
  - Use `re.search()` with IGNORECASE
  - Return (True, pattern_name) or (False, "")
  - _Acceptance: Function detects all 5 patterns_

- [ ] 1.4.4 Implement `get_pattern_info()` function (30 min)
  - Retrieve pattern metadata by name
  - Handle typo patterns (future)
  - _Acceptance: Returns correct pattern info_

- [ ] 1.4.5 Test pattern matching (1 hour)
  - Test each dangerous pattern
  - Test variations (spacing, case, sudo)
  - Test false positives (safe commands)
  - Document test results
  - _Acceptance: All patterns detected, no false positives_

---

### Task 1.5: Basic Display System (2 hours)

- [ ] 1.5.1 Create `display.py` structure (30 min)
  - Define `COLORS` dictionary (ANSI codes)
  - Define `EMOJI` dictionary
  - Import statements
  - _Requirements: Requirement 2 (Themed Warning Display), Requirement 4 (Visual Theme)_
  - _Acceptance: Constants defined_

- [ ] 1.5.2 Implement `colorize()` function (15 min)
  - Apply ANSI color code
  - Add reset code
  - _Acceptance: Text is colored correctly_

- [ ] 1.5.3 Implement `display_welcome_banner()` (30 min)
  - Halloween-themed banner
  - Use orange, red, purple colors
  - Include pumpkin emoji
  - Brief instructions
  - _Acceptance: Banner displays on startup_

- [ ] 1.5.4 Implement `display_goodbye_message()` (15 min)
  - Friendly goodbye message
  - Halloween theme
  - _Acceptance: Message displays on exit_

- [ ] 1.5.5 Implement `show_warning()` dispatcher (30 min)
  - Check if dangerous or typo pattern
  - Call appropriate display function
  - _Acceptance: Routes to correct display function_

---

## Phase 2: Visual Enhancement (8 hours)

**Goal:** Halloween theme and ASCII art fully implemented

### Task 2.1: ASCII Art Creation (2 hours)

- [ ] 2.1.1 Create `fired.txt` ASCII art (45 min)
  - Design "YOU'RE FIRED" theme
  - Fire emoji and flames
  - Burning figure
  - Max 80 characters wide
  - Test rendering in terminal
  - _Requirements: Requirement 2.1 (ASCII Art Response)_
  - _Acceptance: Art renders correctly, fits in 80 chars_

- [ ] 2.1.2 Create `permission_denied.txt` ASCII art (45 min)
  - Design permission/security theme
  - Skull or lock imagery
  - Max 80 characters wide
  - _Acceptance: Art renders correctly_

- [ ] 2.1.3 Create `data_destroyer.txt` ASCII art (30 min)
  - Design disk/data destruction theme
  - Explosion or broken disk imagery
  - Max 80 characters wide
  - _Acceptance: Art renders correctly_

---

### Task 2.2: Warning Display Implementation (3 hours)

- [ ] 2.2.1 Implement `load_ascii_art()` function (30 min)
  - Read ASCII art from file
  - Handle FileNotFoundError gracefully
  - Return art as string
  - _Acceptance: Loads art files correctly, handles errors_

- [ ] 2.2.2 Implement `show_danger_warning()` for deletion (45 min)
  - Load "fired.txt" art
  - Colorize art in red
  - Display "YOU'RE FIRED!" headline
  - Show explanation
  - Show safe alternative
  - _Requirements: Requirement 2 (Themed Warning Display), Requirement 5 (Educational Feedback)_
  - _Reference: halloween-theme.md message templates_
  - _Acceptance: Warning displays with art, colors, education_

- [ ] 2.2.3 Implement warning for permission patterns (45 min)
  - Load "permission_denied.txt" art
  - Display "PERMISSION DENIED!" headline
  - Explain chmod 777 risks
  - Show safe alternative
  - _Acceptance: Warning displays correctly_

- [ ] 2.2.4 Implement warning for dd/database patterns (45 min)
  - Load "data_destroyer.txt" art
  - Display appropriate headline
  - Explain risks
  - Show safe alternative
  - _Acceptance: Warnings display correctly_

- [ ] 2.2.5 Test all warnings visually (15 min)
  - Test on dark terminal background
  - Verify colors are readable
  - Verify ASCII art renders correctly
  - _Acceptance: All warnings look good_

---

### Task 2.3: Educational Messages (1 hour)

- [ ] 2.3.1 Add real-world incident examples (30 min)
  - GitLab data loss (rm -rf)
  - Security breaches (chmod 777)
  - Reference CLI_Troubled.md
  - _Requirements: Requirement 5.5 (Real-world incidents)_
  - _Acceptance: Incidents mentioned in warnings_

- [ ] 2.3.2 Add safe alternatives to all warnings (30 min)
  - rm -i for deletion
  - Specific permissions for chmod
  - Backup strategies
  - _Acceptance: All warnings include safe alternatives_

---

### Task 2.4: System Shell Integration (2 hours)

- [ ] 2.4.1 Implement `execute_in_system_shell()` (1 hour)
  - Use `subprocess.run(command, shell=True)`
  - Handle exceptions gracefully
  - Preserve stdout/stderr
  - _Requirements: Requirement 6 (Safe Mode Operation)_
  - _Acceptance: Safe commands execute correctly_

- [ ] 2.4.2 Test system shell integration (1 hour)
  - Test `ls`, `grep`, `git status`
  - Test pipes: `ls | grep .txt`
  - Test redirects: `echo "test" > file.txt`
  - Test globs: `ls *.py`
  - Document what works
  - _Acceptance: Common commands work as expected_

---

## Phase 3: Typo Entertainment (4 hours)

**Goal:** Add typo detection and fun responses

### Task 3.1: Typo Pattern Implementation (2 hours)

- [ ] 3.1.1 Define typo patterns in `interceptor.py` (30 min)
  - `sl` → "Choo choo! Typo train!"
  - `cd..` → "Stuck together?"
  - _Requirements: Requirement 3 (Typo Entertainment)_
  - _Acceptance: Patterns defined_

- [ ] 3.1.2 Update `check_command()` to check typos (30 min)
  - Check typo patterns after dangerous patterns
  - Return pattern name with "typo_" prefix
  - _Acceptance: Typos detected_

- [ ] 3.1.3 Implement `show_typo_warning()` (1 hour)
  - Display fun message
  - Show correct command
  - Use Halloween colors
  - _Reference: halloween-theme.md typo template_
  - _Acceptance: Typo warnings display correctly_

---

### Task 3.2: Typo Testing (1 hour)

- [ ] 3.2.1 Test sl typo (30 min)
  - Verify detection
  - Verify message display
  - _Acceptance: sl shows train message_

- [ ] 3.2.2 Test cd.. typo (30 min)
  - Verify detection
  - Verify message display
  - _Acceptance: cd.. shows stuck message_

---

### Task 3.3: Documentation Update (1 hour)

- [ ] 3.3.1 Update README.md with features (30 min)
  - List dangerous patterns detected
  - List typo patterns
  - Add screenshots (if possible)
  - _Acceptance: README complete_

- [ ] 3.3.2 Add usage examples to README (30 min)
  - Show example session
  - Show warnings
  - Show typo entertainment
  - _Acceptance: Examples clear and helpful_

---

## Phase 4: Polish & Testing (6 hours)

**Goal:** Code quality, bug fixes, stability

### Task 4.1: Code Quality (2 hours)

- [ ] 4.1.1 Add docstrings to all functions (1 hour)
  - Follow mairu-cli-standards.md format
  - Include type hints
  - Explain parameters and returns
  - _Reference: mairu-cli-standards.md_
  - _Acceptance: All functions documented_

- [ ] 4.1.2 Add inline comments (30 min)
  - Explain complex regex patterns
  - Explain design decisions
  - Reference CLI_Troubled.md where relevant
  - _Acceptance: Code is well-commented_

- [ ] 4.1.3 Code cleanup (30 min)
  - Remove debug prints
  - Fix formatting
  - Ensure consistent style
  - _Acceptance: Code is clean and consistent_

---

### Task 4.2: Testing (2 hours)

- [ ] 4.2.1 Manual end-to-end testing (1 hour)
  - Run through all test scenarios
  - Test builtin commands
  - Test dangerous patterns
  - Test typos
  - Test safe commands
  - Document any bugs found
  - _Acceptance: All features work_

- [ ] 4.2.2 Bug fixes (1 hour)
  - Fix any bugs found in testing
  - Retest after fixes
  - _Acceptance: No critical bugs remain_

---

### Task 4.3: Limitations Documentation (1 hour)

- [ ] 4.3.1 Create LIMITATIONS.md (30 min)
  - Copy from design.md
  - Add examples
  - Explain why limitations exist
  - _Reference: design.md Known Limitations section_
  - _Acceptance: LIMITATIONS.md complete_

- [ ] 4.3.2 Update README.md with limitations (15 min)
  - Add prominent warning section
  - Link to LIMITATIONS.md
  - Emphasize educational purpose
  - _Acceptance: README warns about limitations_

- [ ] 4.3.3 Add disclaimer to welcome banner (15 min)
  - Brief note about educational purpose
  - Not a security tool
  - _Acceptance: Banner includes disclaimer_

---

### Task 4.4: Final Polish (1 hour)

- [ ] 4.4.1 Test on different terminals (30 min)
  - Test on macOS Terminal (dark theme)
  - Test on iTerm2 (if available)
  - Verify colors work
  - Verify ASCII art renders
  - _Acceptance: Works on tested terminals_

- [ ] 4.4.2 Create demo script (30 min)
  - Write script of commands to demonstrate
  - Include dangerous commands
  - Include typos
  - Include safe commands
  - _Acceptance: Demo script ready for video_

---

## Phase 5: Demo & Submission (10 hours)

**Goal:** Create demo video and submit to hackathon

### Task 5.1: Demo Video Preparation (3 hours)

- [ ] 5.1.1 Write video script (1 hour)
  - Introduction (30 sec)
  - Problem statement (30 sec)
  - Demo of features (90 sec)
  - Kiro workflow showcase (30 sec)
  - Conclusion (30 sec)
  - Total: ~3 minutes
  - _Acceptance: Script complete, timed_

- [ ] 5.1.2 Prepare demo environment (1 hour)
  - Clean terminal
  - Set up screen recording
  - Test audio
  - Prepare slides (if needed)
  - _Acceptance: Ready to record_

- [ ] 5.1.3 Practice demo (1 hour)
  - Run through script multiple times
  - Time each section
  - Smooth out rough spots
  - _Acceptance: Demo runs smoothly_

---

### Task 5.2: Video Recording & Editing (4 hours)

- [ ] 5.2.1 Record demo video (2 hours)
  - Record multiple takes
  - Capture terminal session
  - Record voiceover (or use text)
  - _Acceptance: Raw footage captured_

- [ ] 5.2.2 Edit video (2 hours)
  - Cut best takes together
  - Add titles/captions
  - Add background music (optional)
  - Export final video
  - _Acceptance: 3-minute video complete_

---

### Task 5.3: Submission Materials (2 hours)

- [ ] 5.3.1 Finalize README.md (30 min)
  - Ensure all sections complete
  - Add screenshots
  - Proofread
  - _Acceptance: README polished_

- [ ] 5.3.2 Create submission description (30 min)
  - Write project description for Devpost
  - Highlight Kiro usage
  - Mention limitations honestly
  - _Acceptance: Description ready_

- [ ] 5.3.3 Prepare Kiro workflow documentation (30 min)
  - Screenshots of Steering files
  - Screenshots of meeting logs
  - Highlight Spec-Driven Development
  - _Acceptance: Kiro usage documented_

- [ ] 5.3.4 Submit to Devpost (30 min)
  - Upload video
  - Fill out submission form
  - Add links to GitHub
  - Submit
  - _Acceptance: Submission complete!_

---

### Task 5.4: Bonus Content (1 hour)

- [ ] 5.4.1 Write blog post for dev.to (optional)
  - Title: "Building MairuCLI: How Kiro Helped Me Overcome Language Barriers"
  - Describe learning journey
  - Show Steering effectiveness
  - Include code examples
  - Use #kiro hashtag
  - _Prize: $100 for first 50 posts_
  - _Acceptance: Blog post published_

- [ ] 5.4.2 Social media post (optional)
  - Post on X/LinkedIn/BlueSky
  - Tag @kirodotdev
  - Use #hookedonkiro
  - Describe favorite Kiro feature
  - _Prize: $100 for 5 selected posts_
  - _Acceptance: Post published_

---

## Optional Enhancements (If Time Permits)

### [*] Task 6.1: Command Chaining Detection (2-3 hours)

**Only implement if >5 hours remain after Phase 4**

- [*] 6.1.1 Implement enhanced `check_command_with_chaining()` (1.5 hours)
  - Detect `|`, `;`, `&&`, `||` in command
  - Warn user about chaining
  - Block command for safety
  - _Reference: design.md Known Limitations, Priority 1_
  - _Acceptance: Chaining detected and warned_

- [*] 6.1.2 Test chaining detection (1 hour)
  - Test `rm -rf / | grep`
  - Test `rm -rf / && ls`
  - Test `rm -rf / ; ls`
  - _Acceptance: All chaining attempts caught_

- [*] 6.1.3 Update documentation (30 min)
  - Update LIMITATIONS.md
  - Note that chaining is now detected
  - _Acceptance: Docs updated_

---

### [*] Task 6.2: Additional Patterns (2 hours)

**Only implement if >7 hours remain after Phase 4**

- [*] 6.2.1 Add 3 more dangerous patterns (1 hour)
  - `git push -f`
  - `iptables -F`
  - `kill -9 -1`
  - _Acceptance: Patterns added and tested_

- [*] 6.2.2 Add 1 more typo pattern (30 min)
  - `grpe` → grep typo
  - _Acceptance: Pattern added and tested_

- [*] 6.2.3 Update documentation (30 min)
  - Update README with new patterns
  - _Acceptance: Docs updated_

---

## Time Tracking

| Phase | Planned Hours | Actual Hours | Status |
|-------|---------------|--------------|--------|
| Phase 1: Core Infrastructure | 12h | - | Not Started |
| Phase 2: Visual Enhancement | 8h | - | Not Started |
| Phase 3: Typo Entertainment | 4h | - | Not Started |
| Phase 4: Polish & Testing | 6h | - | Not Started |
| Phase 5: Demo & Submission | 10h | - | Not Started |
| **Total** | **40h** | **-** | **-** |
| Optional: Chaining Detection | 3h | - | Optional |
| Optional: Additional Patterns | 2h | - | Optional |

---

## Daily Schedule (Suggested)

### Day 1 (8 hours)
- Morning: Phase 1.1-1.2 (Project setup, builtins)
- Afternoon: Phase 1.3-1.4 (REPL, interceptor)
- **End of Day Goal:** Basic interception working

### Day 2 (8 hours)
- Morning: Phase 1.5, 2.1 (Display system, ASCII art)
- Afternoon: Phase 2.2-2.3 (Warnings, education)
- **End of Day Goal:** Full warnings with ASCII art

### Day 3 (8 hours)
- Morning: Phase 2.4, 3.1 (Shell integration, typos)
- Afternoon: Phase 3.2-3.3, 4.1 (Testing, code quality)
- **End of Day Goal:** All features complete

### Day 4 (8 hours)
- Morning: Phase 4.2-4.4 (Testing, polish, limitations)
- Afternoon: Phase 5.1 (Demo prep)
- **End of Day Goal:** Ready to record

### Day 5 (8 hours)
- Morning: Phase 5.2 (Record and edit video)
- Afternoon: Phase 5.3-5.4 (Submission, bonus)
- **End of Day Goal:** Submitted!

---

## Success Criteria

### Minimum Viable Product (Must Have)
- [x] Detects 5 dangerous command patterns
- [x] Displays 3 ASCII art warnings
- [x] Shows 2 typo entertainments
- [x] Implements 6 builtin commands (cd, pwd, exit, echo, export, history)
- [x] Uses Halloween color scheme
- [x] Includes educational messages
- [x] Documents known limitations
- [x] 3-minute demo video
- [x] Submitted to Devpost

### Stretch Goals (Nice to Have)
- [ ] Command chaining detection
- [ ] 8+ dangerous patterns
- [ ] 3+ typo patterns
- [ ] Blog post on dev.to
- [ ] Social media post

---

## Notes

- **Prioritize ruthlessly:** If running behind, cut optional features
- **Test early, test often:** Don't wait until Phase 4 to test
- **Document as you go:** Update meeting logs daily
- **Be honest about limitations:** Transparency is valued
- **Focus on demo quality:** A polished 3-minute video is worth more than extra features

---

**Tasks Document Created By:** Kiro AI Assistant
**Date:** 2025-11-16
**Status:** Ready for implementation
**Next Step:** Begin Phase 1.1 (Project Setup)
