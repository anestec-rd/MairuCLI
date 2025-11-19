# MairuCLI - TODO List

## High Priority (Before Demo)

### Bug Fixes
- [ ] **Fix dd command pattern detection (Issue #2)**
  - Current pattern: `r"dd\s+if=/dev/zero\s+of="` (requires `of=`)
  - Problem: `dd if=/dev/zero` without `of=` is not detected
  - Result: Falls through to system shell → "Command not found" on Windows
  - Fix: Change pattern to `r"dd\s+if=/dev/zero"` (make `of=` optional)
  - File: `src/interceptor.py` line 31
  - Priority: High (core functionality)
  - Discovered: 2025-11-19 (Day 4, user testing)
  - See: docs/ISSUES.md Issue #2

## High Priority (Before Demo)

### Documentation
- [ ] **Create final README.md for submission**
  - Project overview and purpose
  - Installation steps
  - How to run: `python -m src.main`
  - Feature showcase with examples
  - Screenshots/GIFs of warnings
  - Architecture overview (post-refactoring)
  - Known limitations section
  - Link to LESSONS_LEARNED.md
  - **Development methodology note**: Emphasize Kiro-only development

- [ ] **Document Kiro-exclusive development process**
  - **Important for contest**: This project was built EXCLUSIVELY with Kiro
  - No other AI tools used (no GitHub Copilot, no Claude, no ChatGPT)
  - Demonstrates Kiro's standalone capabilities
  - Include in README.md and submission description
  - Show Kiro's Spec-Driven Development workflow
  - Highlight steering files and context management
  - Document time savings and productivity gains

### Testing
- [ ] **Thorough manual testing in actual REPL**
  - Test all builtin commands
  - Test all dangerous patterns
  - Test typo detection
  - Test "I told you so" feature
  - Test achievements
  - Test stats command
  - Verify colors on different terminals

### Demo Preparation
- [ ] **Improve ASCII art** (if time permits)
  - Make them more elaborate
  - Add more variations
  - Test rendering on different terminals

- [ ] **Practice demo flow**
  - Follow DEMO_SCRIPT.md
  - Time each section
  - Ensure smooth transitions
  - Mention Kiro-exclusive development in intro/outro

## Medium Priority (Day 2-3)

### Video Production
- [ ] **Record demo video**
  - 3-minute target length
  - Show all key features
  - **Emphasize Kiro-exclusive development** (key differentiator)
  - Show Kiro workflow (specs, steering, context)
  - Include achievement unlocks
  - Show "I told you so" escalation
  - Mention no other AI tools were used

- [ ] **Edit demo video**
  - Add titles/captions
  - Highlight key moments
  - Add text overlay: "Built 100% with Kiro"
  - Add background music (optional)
  - Export final version

### Documentation Polish
- [ ] **Create comprehensive README.md**
  - Project overview
  - **"Built with Kiro" badge/section** (prominent placement)
  - Features list
  - Installation guide
  - Usage examples
  - Screenshots
  - Architecture overview (before/after refactoring)
  - Development methodology (Kiro-exclusive)
  - Contributing guidelines (if applicable)

- [ ] **Prepare Kiro workflow documentation**
  - Screenshots of Steering files
  - Spec-Driven Development process
  - Screenshots of spec creation workflow
  - Before/after comparisons
  - Time savings analysis
  - **Emphasize: No other AI tools used**
  - Show how Kiro's features enabled rapid development

## Low Priority (If Time Permits)

### Display Refactoring - Optional Tasks
- [ ] **Unit tests for display components** (Optional - core functionality tested manually)
  - ContentLoader unit tests (2.3)
  - AsciiRenderer unit tests (3.2)
  - MessageFormatter unit tests (4.3)
  - Statistics/Achievements unit tests (5.3)
  - WarningComponents unit tests (6.5)
  - Implementation: ~30-60 minutes
  - Value: Improved test coverage, easier future maintenance
  - Note: All components already tested manually and working correctly

- [ ] **Developer guide for display system** (Optional - for future contributors)
  - Guide for adding new warning types (9.3)
  - Document content file structure
  - Provide examples of custom variations
  - Implementation: ~20-30 minutes
  - Value: Easier onboarding for future contributors

### Project Organization
- [ ] **Reorganize folder structure** (Optional polish)

  **Current Issue:** Root directory has many documentation files

  **Proposed Structure:**
  ```
  Root (keep):
  - README.md (required)
  - LICENSE (required)
  - LESSONS_LEARNED.md (important - show to judges)
  - TODO.md (development management)

  Move to docs/hackathon/:
  - DAY1_SUMMARY.md
  - DEMO_SCRIPT.md
  - DEVELOPMENT_TIMELINE.md
  - PROGRESS.md
  - QUICK_TEST.md

  Move to tests/:
  - manual_test_commands.txt
  - test_session.txt
  ```

  **Rationale:**
  - Keep important docs visible in root (LESSONS_LEARNED.md)
  - Organize development docs in docs/hackathon/
  - Cleaner root directory
  - GitHub-friendly structure

  **Decision:** Deferred - focus on functionality first

### Code Improvements
- [ ] Add unit tests for core functionality
- [ ] Add integration tests
- [ ] Set up CI/CD pipeline
- [ ] Add code coverage reporting

### Feature Enhancements
- [ ] More dangerous command patterns
- [ ] More typo patterns
- [ ] Configuration file support
- [ ] Command logging to file
- [ ] Multi-language support (Japanese)
- [ ] **Echo command variable expansion** (Optional enhancement)
  - Current: Simple text display only (`echo Hello` → "Hello")
  - Enhancement: Add basic variable expansion (`echo $HOME` → actual path)
  - Implementation: ~5-10 minutes
  - Priority: Low (not essential for core functionality)
  - Note: Current simple implementation is sufficient for educational tool

### Visual Improvements
- [ ] More elaborate ASCII art
- [ ] Animation effects (if possible in terminal)
- [ ] Sound effects (terminal beep)
- [ ] Custom color schemes

### Kiro-Specific Features (Contest Showcase)
- [ ] **Agent Hooks integration** (Low priority - showcase Kiro features)
  - Hook: On file save → Auto-update CHANGELOG.md
  - Hook: On dangerous pattern added → Auto-update documentation
  - Hook: Manual "spell-check" hook for documentation files
  - Purpose: Demonstrate Kiro's Agent Hooks capability
  - Implementation: ~30-60 minutes
  - Value: Shows advanced Kiro workflow automation

- [ ] **MCP Server integration** (Low priority - showcase Kiro features)
  - Potential use: CLI command documentation lookup
  - Potential use: Security best practices database
  - Potential use: Real-world incident examples lookup
  - Purpose: Demonstrate Kiro's MCP integration
  - Implementation: ~30-60 minutes
  - Value: Shows Kiro's extensibility with external tools
  - Note: Only if natural fit exists, don't force it

## Submission Checklist

### Required Materials
- [ ] Demo video (3 minutes)
- [ ] GitHub repository link
- [ ] README.md complete
- [ ] **Project description for Devpost** (emphasize Kiro-exclusive development)
- [ ] Kiro workflow documentation
- [ ] **Clear statement**: "Built 100% with Kiro - no other AI tools used"

### Award Category Decision (To Be Determined)
**Status:** Pending final version review

**Candidates:**
1. **Costume Award** (Most likely)
   - Strong Halloween theme consistency
   - Visual impact
   - Concern: High competition

2. **Frankenstein Award** (Possible)
   - Fusion of different domains (security + entertainment + education)
   - Unexpected combination
   - Concern: "Tech mashup" interpretation unclear

3. **Best Entertainment** (Dark horse)
   - Pure fun factor
   - Interactive humor
   - Memorable experience

**Decision Process:**
- Day 2: Test thoroughly, identify strongest aspects
- Day 3: Review final version, watch demo video
- Day 3: Decide based on what shines most
- Day 3: Write tailored submission description

**Strategy:** Keep options open, decide after seeing complete project in action

### Optional (Bonus Prizes)
- [ ] Blog post on dev.to (#kiro hashtag)
- [ ] Social media post (@kirodotdev, #hookedonkiro)
- [ ] Additional documentation

## Notes

**Current Status:** Day 2 Complete (Spec Created)
**Next Session:** Display refactoring implementation (Day 3)
**Time Remaining:** ~34 hours

**Priority Order:**
1. Complete display refactoring (Day 3-5)
2. Manual testing (ensure everything works)
3. README.md with usage instructions + Kiro-exclusive emphasis
4. Demo video preparation (highlight Kiro workflow)
5. Kiro workflow documentation
6. Everything else (nice to have)

**Development Best Practices (Learned from Day 1-2):**
- ✅ Commit frequently (after each feature/fix)
- ✅ Use descriptive commit messages
- ✅ Include timestamps in documentation
- ✅ Take screenshots during development
- ✅ Document as you go
- ✅ Use Kiro's Spec-Driven Development for complex refactoring

**Key Differentiator for Contest:**
- 🎯 **100% Kiro-exclusive development**
- No GitHub Copilot, no Claude, no ChatGPT, no other AI tools
- Demonstrates Kiro's standalone capabilities
- Shows effectiveness of Kiro's Spec-Driven Development
- Highlights steering files, context management, and workflow features

---

**Last Updated:** 2025-11-17
**Status:** Active Development - Refactoring Phase
