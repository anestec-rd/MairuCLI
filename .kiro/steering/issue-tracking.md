# Issue Tracking Standards

## Issue Documentation Rules

When encountering bugs, limitations, or deferred features, ALWAYS document them in `docs/ISSUES.md`.

### Issue Format

```markdown
## [Category] Issue Title

**Status:** Open/Deferred/Fixed
**Priority:** High/Medium/Low
**Discovered:** YYYY-MM-DD

### Description
[Clear description of the issue]

### Impact
[Who/what is affected]

### Reproduction Steps (if applicable)
1. Step 1
2. Step 2
3. Expected vs Actual

### Workaround (if available)
[Temporary solution]

### Resolution Plan
[How to fix, or why deferred]

### Related
- Files: [list of affected files]
- Issues: [related issue numbers]
```

### When to Document

**ALWAYS document:**
- Known bugs
- Limitations of current implementation
- Deferred features (with reason)
- Technical debt
- Breaking changes needed
- Security considerations

**Document immediately when:**
- Discovering a bug during development
- Deciding to defer a feature
- Identifying a limitation
- Making a temporary workaround

### Categories

- `[BUG]` - Something that doesn't work as intended
- `[LIMITATION]` - Known constraint or boundary
- `[DEFERRED]` - Feature postponed for later
- `[TECH-DEBT]` - Code that needs refactoring
- `[SECURITY]` - Security-related concern
- `[PERFORMANCE]` - Performance issue

### Priority Levels

- **High:** Blocks core functionality or causes data loss
- **Medium:** Affects user experience but has workaround
- **Low:** Minor inconvenience or edge case

### Example

```markdown
## [LIMITATION] Echo Command Variable Expansion

**Status:** Deferred
**Priority:** Low
**Discovered:** 2025-11-17

### Description
The `echo` command does not expand environment variables.
`echo $HOME` prints literal "$HOME" instead of the actual path.

### Impact
Users expecting shell-like variable expansion will be surprised.
However, this is an educational tool, not a production shell.

### Workaround
Use actual values instead of variables, or use system shell.

### Resolution Plan
Deferred to post-hackathon. Would require implementing variable
expansion logic (~30 minutes). Not critical for educational purpose.

### Related
- Files: `src/builtins.py` (echo_command function)
- Priority: Low (nice-to-have, not essential)
```

### Important Rules

1. **Document immediately** - Don't wait
2. **Be specific** - Include reproduction steps
3. **Assess impact** - Who/what is affected
4. **Provide workaround** - If available
5. **Update status** - When resolved or deferred
6. **Link related items** - Files, issues, PRs

### Reference

See `docs/ISSUES.md` for current issues and examples.
