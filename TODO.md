# MairuCLI - TODO List

## High Priority (Before Demo)

### Documentation
- [ ] **Update README.md with usage instructions**
  - Installation steps
  - How to run: `python -m src.main`
  - Basic usage examples
  - Feature highlights
  - Screenshots/GIFs of warnings
  - Known limitations section
  - Link to LESSONS_LEARNED.md

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

## Medium Priority (Day 2-3)

### Video Production
- [ ] **Record demo video**
  - 3-minute target length
  - Show all key features
  - Emphasize Kiro workflow
  - Include achievement unlocks
  - Show "I told you so" escalation

- [ ] **Edit demo video**
  - Add titles/captions
  - Highlight key moments
  - Add background music (optional)
  - Export final version

### Documentation Polish
- [ ] **Create comprehensive README.md**
  - Project overview
  - Features list
  - Installation guide
  - Usage examples
  - Screenshots
  - Architecture overview
  - Contributing guidelines (if applicable)

- [ ] **Prepare Kiro workflow documentation**
  - Screenshots of Steering files
  - Spec-Driven Development process
  - Before/after comparisons
  - Time savings analysis

## Low Priority (If Time Permits)

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

### Visual Improvements
- [ ] More elaborate ASCII art
- [ ] Animation effects (if possible in terminal)
- [ ] Sound effects (terminal beep)
- [ ] Custom color schemes

## Submission Checklist

### Required Materials
- [ ] Demo video (3 minutes)
- [ ] GitHub repository link
- [ ] README.md complete
- [ ] Project description for Devpost
- [ ] Kiro workflow documentation

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

**Current Status:** Day 1 Complete
**Next Session:** Focus on testing and README.md
**Time Remaining:** ~36 hours

**Priority Order:**
1. Manual testing (ensure everything works)
2. README.md with usage instructions
3. Demo video preparation
4. Kiro workflow documentation
5. Everything else (nice to have)

**Development Best Practices (Learned from Day 1):**
- ✅ Commit frequently (after each feature/fix)
- ✅ Use descriptive commit messages
- ✅ Include timestamps in documentation
- ✅ Take screenshots during development
- ✅ Document as you go

---

**Last Updated:** 2025-11-16
**Status:** Active Development
