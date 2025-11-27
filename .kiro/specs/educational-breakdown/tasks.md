# Implementation Plan - Educational Breakdown Mode

## Task List

- [x] 1. Set up project structure and data files
  - Create `data/educational/` directory structure
  - Create subdirectories: `command_breakdowns/`, `simulations/`, `incidents/`
  - Add `.gitkeep` files to ensure directories are tracked
  - _Requirements: 4.2, 4.3, 4.4_

- [x] 2. Implement EducationalLoader class
  - Create `src/display/educational_loader.py`
  - Implement `__init__` with base path and cache dictionaries
  - Implement `load_breakdown()` with file loading and caching
  - Implement `load_simulation()` with file loading and caching
  - Implement `load_incident()` with file loading and caching
  - Implement `get_related_incidents()` to find related incidents
  - Add error handling for FileNotFoundError and JSONDecodeError
  - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5, 8.4_

- [x] 3. Implement BreakdownFormatter class
  - Create `src/display/breakdown_formatter.py`
  - Implement `format_command_breakdown()` with Halloween theme
  - Implement `format_timeline_simulation()` with emoji and timing
  - Implement `format_incident_story()` with Halloween framing
  - Implement `format_quick_explanation()` for 5-second summary
  - Add helper methods for formatting sections and borders
  - _Requirements: 1.2, 1.3, 1.4, 1.5, 2.1, 2.2, 2.3, 2.4, 2.5, 3.2, 3.3, 3.4, 3.5, 9.1, 9.2, 9.3, 9.4, 9.5_

- [x] 4. Implement EducationalBreakdown class
  - Create `src/display/educational_breakdown.py`
  - Implement `__init__` with loader and formatter
  - Implement `show_breakdown_prompt()` to display options and get user choice
  - Implement `show_quick_explanation()` for quick mode
  - Implement `show_full_breakdown()` for full mode with all components
  - Add graceful fallback for missing content
  - _Requirements: 1.1, 5.1, 5.2, 5.3, 5.4, 5.5_

- [x] 5. Create educational content for rm_dangerous
  - Create `data/educational/command_breakdowns/rm_dangerous.json`
  - Define command parts: rm, -r, -f, /
  - Add emojis, meanings, danger levels
  - Add translation and Halloween analogy
  - Add safe alternatives
  - _Requirements: 1.2, 1.3, 1.4, 1.5, 7.1, 7.2, 7.3, 7.4, 7.5_

- [x] 6. Create simulation for rm_dangerous
  - Create `data/educational/simulations/rm_dangerous.json`
  - Define timeline events (T+0s to T+∞)
  - Add emojis and severity levels
  - Add final message with Halloween humor
  - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5_

- [x] 7. Create GitLab incident story
  - Create `data/educational/incidents/gitlab_2017.json`
  - Add incident details (date, company, summary)
  - Add timeline of events
  - Add source URL: https://about.gitlab.com/blog/2017/02/01/gitlab-dot-com-database-incident/
  - Add lesson and Halloween twist
  - Link to rm_dangerous pattern
  - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 10.1, 10.2, 10.3, 10.4, 10.5_

- [x] 8. Create educational content for chmod_777
  - Create `data/educational/command_breakdowns/chmod_777.json`
  - Define command parts: chmod, 777
  - Explain permission format (owner/group/others)
  - Explain numeric values (4=read, 2=write, 1=execute)
  - Add safe alternatives (chmod 644)
  - _Requirements: 6.1, 6.2, 6.3, 6.5_

- [x] 9. Create chmod_777 attack simulation
  - Create `data/educational/simulations/chmod_777_attack.json`
  - Implement story mode with 4 chapters
  - Chapter 1: The Careless Command (explain 777)
  - Chapter 2: The Midnight Visitor (🐺 hacker scenario)
  - Chapter 3: The Morning Horror (chmod 000 lockout)
  - Chapter 4: The Lesson (safe alternatives)
  - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 6.4_

- [x] 10. Integrate with main.py
  - Import EducationalBreakdown, EducationalLoader, BreakdownFormatter
  - Initialize components at startup
  - After dangerous command detection, call `show_breakdown_prompt()`
  - Handle user choice (quick/full/skip)
  - Ensure command remains blocked after breakdown
  - _Requirements: 1.1, 5.1, 5.2, 5.3, 5.4, 5.5_

- [x] 11. Create educational content for 3 more patterns
  - Create breakdowns for: dd_zero, fork_bomb, chmod_000
  - Create simulations for: dd_zero, fork_bomb, chmod_000
  - Follow same JSON schema as rm_dangerous
  - Add Halloween theme and safe alternatives
  - _Requirements: 8.1, 8.2, 8.3, 8.4, 8.5_

- [ ] 12. Add unit tests for EducationalLoader
  - Test successful file loading
  - Test caching behavior
  - Test missing file handling (returns None)
  - Test malformed JSON handling
  - Test get_related_incidents()
  - _Requirements: 4.5, 8.5_

- [ ] 13. Add unit tests for BreakdownFormatter
  - Test format_command_breakdown() output
  - Test format_timeline_simulation() output
  - Test format_incident_story() output
  - Test format_quick_explanation() output
  - Verify Halloween theme elements present
  - _Requirements: 9.1, 9.2, 9.3, 9.4, 9.5_

- [ ] 14. Add integration tests
  - Test full breakdown flow (prompt → full → display)
  - Test quick explanation flow
  - Test skip flow
  - Test graceful degradation with missing content
  - Test multiple patterns
  - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5_

- [ ] 15. Manual testing and polish
  - Test all patterns with breakdown mode
  - Verify timing feels natural (not too fast/slow)
  - Verify Halloween theme consistency
  - Verify source URLs are correct and accessible
  - Test on different terminal sizes
  - Adjust formatting if needed
  - _Requirements: All requirements_

- [ ] 16. Update documentation
  - Update README.md with breakdown mode feature
  - Add example screenshots/output
  - Document JSON schema in docs/
  - Update CHANGELOG.md
  - _Requirements: 8.1, 8.2, 8.3_

## Implementation Notes

### Priority Order
1. **Core Infrastructure** (Tasks 1-4): Foundation components
2. **Initial Content** (Tasks 5-7): rm_dangerous with full content
3. **chmod Content** (Tasks 8-9): Second pattern with story mode
4. **Integration** (Task 10): Connect to main system
5. **Additional Content** (Task 11): Expand to more patterns
6. **Testing** (Tasks 12-15): Ensure quality
7. **Documentation** (Task 16): User-facing docs

### Time Estimates
- Tasks 1-4 (Core): 30 minutes
- Tasks 5-7 (rm content): 15 minutes
- Tasks 8-9 (chmod content): 15 minutes
- Task 10 (Integration): 10 minutes
- Task 11 (More content): 15 minutes
- Tasks 12-14 (Testing): 20 minutes
- Task 15 (Manual testing): 15 minutes
- Task 16 (Documentation): 10 minutes

**Total: ~130 minutes (2 hours 10 minutes)**

### Content Creation Guidelines

**Command Breakdown:**
- Keep explanations concise (1 sentence per part)
- Use appropriate emojis for danger level
- Provide plain-language translation
- Include 2-3 safe alternatives

**Timeline Simulation:**
- Start with T+0s (beginning)
- Show progressive damage
- Use appropriate severity levels
- End with final summary message
- Keep total events to 6-10 for readability

**Incident Stories:**
- Verify all facts before adding
- Include official source URL
- Balance facts with Halloween theme
- Keep timeline to 8-12 key events
- Add lesson learned

### Testing Strategy

**Unit Tests:**
- Focus on individual component behavior
- Test error handling thoroughly
- Verify caching works correctly

**Integration Tests:**
- Test complete user flows
- Verify all components work together
- Test graceful degradation

**Manual Tests:**
- Verify visual appearance
- Check timing and pacing
- Ensure Halloween theme consistency
- Validate source URLs

### Scalability Considerations

**Adding New Patterns:**
1. Create breakdown JSON (5 minutes)
2. Create simulation JSON (5 minutes)
3. Find and add incident if available (10 minutes)
4. Test (5 minutes)

**Total per pattern: ~25 minutes**

**For 11 dangerous patterns:**
- Initial 2 patterns: Included in tasks
- Remaining 9 patterns: ~3.75 hours
- Can be done incrementally after MVP

### Success Criteria

**MVP Complete When:**
- ✅ Core components implemented and tested
- ✅ 2 patterns have full content (rm, chmod)
- ✅ Integration with main.py working
- ✅ Graceful fallback for missing content
- ✅ Unit and integration tests passing
- ✅ Manual testing confirms good UX

**Full Feature Complete When:**
- ✅ All 11 dangerous patterns have content
- ✅ All 4 caution patterns have content
- ✅ All incidents documented with sources
- ✅ Comprehensive test coverage
- ✅ Documentation updated

## Dependencies

**External:**
- None (uses Python standard library only)

**Internal:**
- Existing `ContentLoader` pattern (reference)
- Existing warning display system (integration point)
- Existing interceptor (provides pattern names)

## Risks and Mitigation

**Risk 1: Content creation takes longer than estimated**
- Mitigation: Start with 2 patterns for MVP, add more incrementally

**Risk 2: JSON schema changes needed during implementation**
- Mitigation: Keep schema flexible, add optional fields as needed

**Risk 3: Display formatting issues on different terminals**
- Mitigation: Test on multiple terminals early, use fallback formatting

**Risk 4: User finds breakdown mode disruptive**
- Mitigation: Make skip option prominent, remember user preference (future)

## Future Enhancements

**Post-MVP Features:**
1. Remember user preference (always skip, always full, etc.)
2. Achievement for viewing all breakdowns
3. Interactive quiz mode after breakdown
4. Community-contributed incidents
5. Localization (Japanese)
6. Export breakdown as text file
7. Breakdown history (what user has seen)

## Rollout Plan

**Phase 1: MVP (Tasks 1-10)**
- Core functionality
- 2 patterns with full content
- Basic integration

**Phase 2: Content Expansion (Task 11)**
- Add 3 more patterns
- Total 5 patterns covered

**Phase 3: Testing & Polish (Tasks 12-15)**
- Comprehensive testing
- UX refinement

**Phase 4: Documentation (Task 16)**
- User-facing docs
- Developer guides

**Phase 5: Full Coverage (Post-tasks)**
- Remaining 6 dangerous patterns
- 4 caution patterns
- Additional incidents
