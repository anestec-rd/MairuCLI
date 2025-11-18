# Documentation Update Guidelines

## When to Update Documentation

### README.md - Update at Milestones Only

**DO update README.md when:**
- ✅ Releasing a new version (v1.0, v1.1, etc.)
- ✅ Adding major features (new command categories, etc.)
- ✅ Changing installation/usage instructions
- ✅ Completing major refactoring
- ✅ Before demo/submission

**DON'T update README.md when:**
- ❌ Adding single warning variation
- ❌ Fixing small bugs
- ❌ Refactoring internal code (if API unchanged)
- ❌ Adding tests
- ❌ During exploratory development

**Rationale:**
- Avoid cluttering git history
- README is user-facing, not developer-facing
- Frequent updates suggest instability
- Save updates for meaningful milestones

### CHANGELOG.md - Update Frequently

**ALWAYS update CHANGELOG.md when:**
- Adding new features
- Fixing bugs
- Making breaking changes
- Refactoring (note in "Changed" section)
- Releasing versions

**Format:**
```markdown
## [Unreleased]

### Added
- New feature description

### Changed
- Modified behavior description

### Fixed
- Bug fix description
```

### TODO.md - Update as Needed

**Update TODO.md when:**
- Completing tasks (mark as done)
- Discovering new tasks
- Changing priorities
- Planning next steps

**Don't overthink it** - TODO.md is a working document.

### docs/ISSUES.md - Update Immediately

**ALWAYS update when:**
- Discovering bugs
- Identifying limitations
- Deferring features
- Resolving issues

See `issue-tracking.md` steering file for format.

### Code Comments - Update with Code

**ALWAYS update when:**
- Modifying function behavior
- Changing parameters
- Fixing bugs that affect documented behavior

**Keep docstrings in sync with code.**

## Documentation Hierarchy

### User-Facing (Update Carefully)
1. **README.md** - Main project documentation
   - Update at milestones
   - Review before committing
   - Keep concise and accurate

2. **LICENSE** - Legal document
   - Never change without reason
   - Already set to Apache 2.0

### Developer-Facing (Update Freely)
1. **CHANGELOG.md** - Version history
   - Update with every significant change
   - Keep chronological

2. **TODO.md** - Task tracking
   - Update as tasks evolve
   - Working document

3. **docs/ISSUES.md** - Issue tracking
   - Update immediately when issues found
   - Keep current

4. **docs/DAY*_SUMMARY.md** - Development logs
   - Create at end of each day
   - Historical record

5. **tests/TEST_STRUCTURE.md** - Test design
   - Update when test strategy changes
   - Reference document

### Internal (Update with Code)
1. **Code comments** - Inline documentation
   - Update with code changes
   - Keep in sync

2. **Docstrings** - Function documentation
   - Update with function changes
   - Required for public APIs

## Commit Message Guidelines

### When Documentation Changes

**Good commit messages:**
```
docs: update README.md for v1.1 release
docs(changelog): add v1.0 release notes
docs(issues): document echo variable expansion limitation
```

**Avoid:**
```
update readme
fix typo
docs
```

### Batching Documentation Updates

**Prefer:**
- One commit with multiple doc updates at milestone
- Example: "docs: prepare v1.0 release documentation"

**Over:**
- Multiple small commits for each doc file
- Cluttered history

## Special Cases

### README.md During Development

**If you must update README.md during development:**
1. Batch changes (don't commit after each edit)
2. Use `git commit --amend` if not pushed yet
3. Consider if it can wait until next milestone

### Experimental Features

**When adding experimental features:**
1. Update CHANGELOG.md (mark as experimental)
2. Update TODO.md (track completion)
3. DON'T update README.md until stable
4. Document in code comments

### Breaking Changes

**When making breaking changes:**
1. Update CHANGELOG.md immediately (Breaking Changes section)
2. Update README.md if user-facing
3. Update affected code documentation
4. Consider version bump

## Summary

**Golden Rule:**
> User-facing docs (README) = Milestone updates
> Developer-facing docs (CHANGELOG, TODO, ISSUES) = Frequent updates
> Code docs (comments, docstrings) = Update with code

**When in doubt:**
- Will users see this? → Wait for milestone
- Will developers need this? → Update now
- Is this code-level? → Update with code
