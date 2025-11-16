# MairuCLI Development Standards

## Project Context
MairuCLI is an educational CLI wrapper that intercepts dangerous commands and displays Halloween-themed warnings. The goal is to combine security education with entertainment.

## Code Style Guidelines

### Python Code Standards
- Use type hints for all function parameters and return values
- Maximum line length: 100 characters
- Use descriptive variable names (no single letters except loop counters)
- Add docstrings to all functions explaining purpose and parameters

### Command Pattern Format
```python
# Good example:
DANGEROUS_PATTERNS = {
    "rm_recursive": r"rm\s+(-rf|-fr)\s+(/|~|\$HOME)",  # Catches rm -rf /
    "chmod_777": r"chmod\s+(-R\s+)?777",  # Catches chmod 777 or chmod -R 777
}
```

- Use raw strings (r"...") for regex patterns
- Include inline comments explaining what each pattern catches
- Group related patterns by category (deletion, permission, database, etc.)
- Test patterns against variations (spacing, argument order)

### ASCII Art Guidelines
- Maximum width: 80 characters for terminal compatibility
- Use ANSI color codes from our Halloween palette
- Store in separate files under `ascii_art/` directory
- Include both colored and plain text versions
- Test rendering on both light and dark terminal backgrounds

### Educational Message Structure
When creating warning messages:
1. **Hook**: Start with humor or wordplay (e.g., "YOU'RE FIRED" for rm -rf /)
2. **Explanation**: Explain what the command does and why it's dangerous
3. **Consequence**: Describe real-world impact (reference CLI_Troubled.md)
4. **Advice**: Provide the safe alternative or best practice

Example:
```
🔥 YOU'RE FIRED! 🔥
(And so is your entire filesystem)

The command 'rm -rf /' attempts to delete EVERYTHING on your system.
This is unrecoverable without backups.

Real incident: GitLab.com lost 300GB of production data in 2017 due to
accidental rm -rf execution.

Safe alternative: Always use 'rm -i' for interactive confirmation, or
use a trash utility like 'trash-cli' instead of rm.
```

## Halloween Theme Guidelines

### Color Palette (ANSI Codes)
- Orange: `\033[38;5;208m` - Primary accent
- Chocolate: `\033[38;5;130m` - Secondary text
- Purple: `\033[38;5;141m` - Highlights
- Green: `\033[38;5;46m` - Success/safe actions
- Red: `\033[38;5;196m` - Danger warnings
- Reset: `\033[0m` - Always reset after colored text

### Design Principles
- **Comedic, not scary**: Think Halloween party, not horror movie
- **Educational, not preachy**: Make learning fun and memorable
- **Pop aesthetic**: Bright colors, friendly tone
- **Accessible**: Provide option to disable colors for accessibility

## Testing Requirements

### Pattern Testing
- Every dangerous pattern must have at least 3 test cases
- Test variations: spacing, argument order, with/without sudo
- Test false positives: ensure safe commands aren't flagged

### ASCII Art Testing
- Verify rendering in 80-character width
- Test on both light and dark terminal themes
- Ensure colors display correctly

### Educational Content Testing
- Verify all incident references are accurate
- Check that advice is actionable and correct
- Ensure tone is appropriate (comedic but informative)

## Documentation Standards

### Language Requirements
- **All documentation files (*.md) must be written in English**
- Exception: `private_talk.md` can contain any language
- When quoting user input in Japanese, translate it to English before including in documentation
- Code comments should be in English
- Commit messages should be in English

### README.md
- Include installation instructions for multiple platforms
- Provide usage examples with screenshots
- List all supported dangerous command patterns
- Credit sources (CLI_Troubled.md, incident reports)

### Code Comments
- Explain WHY, not just WHAT
- Reference CLI_Troubled.md sections for context
- Include links to incident reports when relevant
- All comments must be in English

## File Organization
```
mairu-cli/
├── src/
│   ├── interceptor.py      # Command pattern matching
│   ├── display.py           # ASCII art and color rendering
│   ├── education.py         # Educational message generation
│   └── config.py            # Configuration management
├── ascii_art/
│   ├── fired.txt            # "YOU'RE FIRED" art
│   ├── steam_locomotive.txt # SL typo art
│   └── ...
├── patterns/
│   ├── dangerous_commands.json  # Pattern database
│   └── typo_patterns.json       # Common typos
├── tests/
│   ├── test_interceptor.py
│   ├── test_display.py
│   └── ...
└── docs/
    ├── CLI_Troubled.md      # Reference material
    └── incident_examples.md # Real-world cases
```

## Commit Message Format
```
<type>(<scope>): <subject>

<body>

<footer>
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, no logic change)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

Example:
```
feat(interceptor): add chmod 777 pattern detection

Implements detection for chmod 777 and chmod -R 777 patterns.
Includes variations with different spacing and argument order.

Refs: CLI_Troubled.md section 2 (Permission Setting Mistakes)
```

## Priority Guidelines

### Must Have (Phase 1)
- rm -rf / detection
- chmod 777 detection
- Basic ASCII art (3 variations)
- Halloween color scheme
- Educational messages for top 5 dangerous commands

### Should Have (Phase 2)
- Typo entertainment (sl, cd.., etc.)
- More ASCII art variations
- Configuration file support
- Command history logging

### Nice to Have (Phase 3)
- Multi-language support (Japanese)
- Custom pattern addition by users
- Statistics dashboard
- Integration with shell history

## References
- CLI_Troubled.md: Comprehensive list of CLI dangers
- Real-world incidents: GitLab data loss, AWS S3 outage, etc.
- Halloween design inspiration: Friendly, pop aesthetic
