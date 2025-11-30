# Changelog

All notable changes to MairuCLI will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [Unreleased]

---

## [1.5.0] - 2025-11-30 (Day 14 - Contest Submission Release)

### Added
- **Timeline Real-Time Display** - Enhanced educational experience
  - Simulation steps now display in real-time with dramatic pauses
  - Color-coded results (green for success, red for failure)
  - Slow printing effect for each step (0.05s per character)
  - Pauses between steps for dramatic effect (0.8s)
  - Makes timeline simulations more engaging and memorable
  - Implemented in `breakdown_formatter.py`
  - All existing tests pass (321/321)

- **Lie Command File Inversion** - Educational misinformation awareness
  - `lie <filename>` displays inverted file content
  - Word replacement using opposites dictionary (good→bad, up→down, etc.)
  - Number randomization (preserves format, changes values)
  - Original file remains unchanged (read-only operation)
  - Educational warnings about verifying information
  - Opposites dictionary in `data/builtins/lie_opposites.json`
  - Teaches critical thinking about information sources
  - Fun Easter egg feature for exploration

### Changed
- **Documentation Updates for Contest Submission**
  - Updated README.md to v1.5.0
  - Added Platform Support section (Windows/Linux/macOS verified)
  - Added Test Coverage section (321 tests, 100% pass rate)
  - Added Quick Verification guide with step-by-step commands
  - Updated feature list to include Educational Breakdown and System Protection
  - Emphasized "Built 100% with Kiro AI" at top of README
  - Updated version badges and added test/platform badges
  - Added `lie` command to builtin commands list (21 total)

- **Test Coverage Milestone**
  - 321 total tests (274 unit + 47 integration)
  - 100% pass rate on all platforms
  - Cross-platform verification (Windows, Linux, macOS)
  - Comprehensive coverage of all features

### Documentation
- Updated README.md for v1.5.0 release
- Added comprehensive platform support documentation
- Added test coverage details and running instructions
- Updated version number throughout documentation

### Quality Metrics
- **Total Tests**: 321 (274 unit + 47 integration)
- **Pass Rate**: 100%
- **Platforms**: Windows, Linux, macOS (all verified)
- **Features**: 21 builtin commands, 11 dangerous patterns, 4 caution patterns
- **Educational Content**: 5 patterns with full breakdown/simulation/incident
- **Code Quality**: Zero breaking changes, backward compatible

### Contest Submission Highlights
- ✅ Built 100% exclusively with Kiro AI
- ✅ Demonstrates Spec-Driven Development methodology
- ✅ 7.5-9x productivity gain (20-minute refactoring)
- ✅ Complete documentation and audit trail
- ✅ Educational value + entertainment fusion
- ✅ Clean, maintainable architecture
- ✅ Cross-platform support verified
- ✅ Comprehensive test coverage

---

## [1.4.0] - 2025-11-29 (Day 13)

### Added
- **Educational Breakdown Mode** - Interactive learning system
  - Three-level learning: Quick (5s), Full (breakdown + simulation + incident), Skip
  - Command breakdowns explain each part of dangerous commands
  - Timeline simulations show step-by-step consequences
  - Real-world incident stories with verified sources
  - 5 patterns with full educational content: rm -rf, chmod 777/000, dd, fork bomb
  - JSON-based content system for easy expansion
  - Components: EducationalBreakdown, EducationalLoader, BreakdownFormatter
  - Graceful fallback for missing content
  - Halloween-themed presentation maintains fun learning atmosphere
  - Integration tests verify complete user flows
  - Unit tests for all components (loader, formatter, breakdown)

- **Complete Data-Driven Architecture** - Day 11
  - All patterns now loaded from JSON files (no hardcoded patterns)
  - Builtin commands defined in `data/builtins/builtin_commands.json`
  - COMMON_COMMANDS loaded from JSON (no duplication)
  - Help command auto-generated from JSON data
  - Pattern-specific emojis (chmod 000 = 🔒, chmod 777 = 🔓)
  - Easy to add new patterns without touching code
  - Single source of truth for all command information
- **Complete ASCII Art Overhaul - Intense & Distinctive** - Day 7
  - **Enhanced existing (3):** fired.txt, permission_denied.txt, data_destroyer.txt
    - Added burning faces, screaming, flames, destruction effects
    - More intense visuals with 💀💀💀 and 🔥💥⚡
  - **Created new (8):**
    - database_drop.txt - Database apocalypse with DELETED markers
    - fork_bomb.txt - Process explosion with CPU meltdown
    - kernel_panic.txt - Glitch text (K̴E̷R̶N̸E̵L̴), system death
    - disk_destroyer.txt - Physical disk obliteration
    - data_void.txt - /dev/null void consumption
    - zero_wipe.txt - Zero byte flood attack
    - file_eraser.txt - File content wipeout
    - system_glitch.txt - System corruption with glitch effects
  - **35 new warning variations** across all patterns
  - **All 11 danger patterns** now have unique, intense ASCII art
  - **Improved intensity:** More 💀, 🔥, 💥, ⚡, block noise (▓▓▓), glitch text
  - **Better educational impact:** Visual severity matches danger level

- **Category-Based Warning Variations System with Merge Strategy** - Day 7
  - **Merge strategy:** Category (8) + Pattern-specific (4) = 12 total variations
  - **Scalability:** 11 patterns with 87 entries → 50+ patterns with ~45 entries
  - **New files:**
    - `category_variations.json` - 5 categories × 8 variations = 40 shared entries
    - `pattern_variations.json` - 9 patterns × 4 unique variations = 36 entries
  - **Result:** Each pattern gets 8-13 variations (category + pattern-specific)
  - **Benefits:**
    - Rich variety (12 variations per pattern vs 8)
    - Reduced duplication (45 entries vs 300 for 50 patterns)
    - Balanced approach (category consistency + pattern uniqueness)
    - Easy to extend (just add 4 pattern-specific if needed)
  - **Backward compatible:** Legacy danger_variations.json still supported
  - **Documentation:**
    - Design doc: `docs/CATEGORY_BASED_VARIATIONS_DESIGN.md`
    - Steering guide: `.kiro/steering/warning-variations.md`

- **Echo Command Variable Expansion** - Day 7
  - Unix-style variable expansion: $VAR and ${VAR}
  - Windows-style variable expansion: %VAR%
  - Undefined variables remain as literal text (safe fallback)
  - Cross-platform support for environment variable access
  - 11 unit tests added, all passing
  - Educational value: teaches environment variable concepts

- **Achievement Categorization System** - Day 7
  - ACHIEVEMENT_METADATA dictionary with category information
  - Four categories: danger, safe, exploration, system_protection
  - get_achievements_by_category() method for filtered retrieval
  - get_all_categories() method for dynamic category listing
  - Stats command now displays achievements grouped by category
  - Custom icons for each category (💀 danger, 🏆 safe, 🚂 exploration, 🛡️ system_protection)
  - Removed hardcoded achievement lists from stats command
  - Single source of truth for achievement properties
  - Easier to add new achievements without code changes

### Changed
- **Magic Number Refactoring Phase 2 & 3 Complete** - Day 7
  - Added achievement threshold constants to achievements.py:
    - ACHIEVEMENT_FIRST_BLOOD = 1
    - ACHIEVEMENT_THRESHOLD_LOW = 3
    - ACHIEVEMENT_THRESHOLD_MEDIUM = 5
    - ACHIEVEMENT_THRESHOLD_HIGH = 8
    - ACHIEVEMENT_THRESHOLD_EXPERT = 10
  - Added display formatting constants to config.py:
    - DISPLAY_SEPARATOR_WIDTH = 60
    - DISPLAY_MIN_QUOTE_LENGTH = 2
  - Replaced 10+ magic numbers with named constants
  - Benefits:
    - Single source of truth for thresholds
    - Easy to adjust achievement difficulty
    - Self-documenting code
    - Improved maintainability
  - All 94 tests passing
  - No functional changes

- **Builtin Commands Refactoring** - Day 7
  - Split monolithic builtins.py (719 lines) into modular package
  - Created src/builtins/ package with 7 specialized modules:
    - navigation.py - cd, pwd commands
    - file_operations.py - ls, cat, touch, mkdir commands
    - search.py - find, grep, which commands
    - system_info.py - whoami, date, hostname, env, export commands
    - display.py - tree command
    - shell_utils.py - echo, clear, history, alias commands
    - mairu_commands.py - help, stats commands (MairuCLI-specific)
  - Benefits:
    - Better code organization (100-150 lines per module)
    - Easier to maintain and extend
    - Clear separation of concerns
    - Improved testability
  - Backward compatibility maintained
  - All 20 unit tests passing
  - No functional changes to user interface

### Changed
- **Task Management Consolidation** - Day 7
  - Merged MairuCLI_StockTask.md into TODO.md
  - All active tasks now tracked in single location (TODO.md)
  - Stock task file updated with completion status and references
  - Verified "Achievement for Normal Commands" already implemented
  - Existing achievements: Explorer (5 commands), Command Master (10 commands), Balanced User

### Added
- **Extended Search and File Management Commands** - Day 7
  - File Management:
    - touch <file> - Create empty file or update timestamp
    - mkdir <dir> - Create directory
  - Search Commands:
    - find <pattern> - Find files by name (supports wildcards)
    - grep <pattern> <file> - Search text in files (with highlighting)
    - which <command> - Show command location in PATH
  - System Info:
    - whoami - Display current username
    - date - Display current date and time
    - hostname - Display computer name
    - tree [path] - Display directory tree structure (max 3 levels)
  - Educational Features:
    - All commands have Halloween-themed output
    - Usage help for each command
    - Error handling with friendly messages
    - Cross-platform compatibility (Windows/Unix)
  - Testing:
    - 20 unit tests added, all passing
    - Tests cover normal operation and edge cases
  - Updated help command to categorize commands by function

- **chmod -R 000 Pattern Detection** - Day 7
  - Detects chmod 000 and chmod -R 000 commands
  - Critical severity (blocks immediately)
  - Educational message explains total permission lockout
  - 5 warning variations with IT wordplay
  - Unit tests added

---

## [1.2.0] - 2025-11-23

### Added
- **System Directory Protection** - Critical safety feature (Day 6-7) ✅ COMPLETE
  - Protects critical system directories from accidental modification/deletion
  - Platform-specific protection: Windows (C:\Windows, System32, Program Files), Linux (/etc, /bin, /usr), macOS (/System, /Library)
  - Two-tier protection: Critical (immediate block) and Caution (confirmation prompt)
  - Path resolution: Handles relative paths (../../), environment variables ($WINDIR, $HOME), home expansion (~)
  - Command parsing: Extracts paths from rm, mv, chmod, dd, output redirection (>)
  - Educational warnings explain risks and provide safe alternatives
  - Comprehensive testing: 63 unit tests + 10 integration tests + manual test documentation
  - Performance: 0.02ms average (2500x faster than 50ms target)
  - Safety review: All fail-safe mechanisms verified, no bypass methods found
  - Cross-platform compatibility: Windows/Linux/macOS verified
  - Tasks 1-12 complete, approved for production
- **Achievement Display in Stats Command** - User testing feedback (Day 6)
  - Stats command now displays unlocked achievements
  - Achievements categorized into "Your Troublemaking History" (danger-related) and "Unlocked Achievements" (others)
  - Danger-related achievements: First Blood, Persistent Troublemaker, Danger Addict, Stubborn
  - Other achievements: Explorer, Command Master, Balanced User, Typo Master
  - Displays between statistics and final message for better visibility
- **Command Not Found Message Variations** - GitHub Issue #1 (Day 6)
  - 8 Halloween-themed variations for "command not found" messages
  - Randomly selected for variety and entertainment
  - Includes: candy store, ghost, pumpkin, bat, spider, wizard, skull, moon themes
  - Maintains educational value while adding personality

### Changed
- **Language Standards** - English-only CLI output
  - Added steering rule: All CLI output must be in English
  - Ensures consistency and international accessibility
  - Documentation can be multilingual, but user-facing text is English-only

### Fixed
- **Unicode Decode Error** - System command execution (Day 6)
  - Fixed crash when executing commands with non-UTF-8 output (e.g., sudo on Windows)
  - Added explicit UTF-8 encoding with error replacement
  - Handles cp932 (Japanese) and other encodings gracefully

### Planned
- Demo video recording
- Kiro workflow documentation
- Contest submission preparation
- Achievement categorization system (maintainability improvement - see TODO.md)

---

## [1.1.0] - 2025-11-21 (Day 5)

### Added
- **Automated Test Suite** - Production-ready testing
  - 35 automated tests for pattern detection
  - 100% pass rate, < 5 seconds execution
  - Tests for all 11 dangerous patterns, 4 caution patterns, 2 typo patterns
  - Safe command pass-through verification
  - Bug fix verification (Issue #2)
- **Test Strategy Framework** - Steering file for consistent testing
  - Decision tree for which tests to add
  - Templates for unit/integration/manual tests
  - Examples from MairuCLI history
  - Quick reference table
  - Integration with Kiro workflow
- **8 New Warning Variations** - Japanese-inspired messages
  - 5 new rm_root variations (total: 14)
  - 2 new chmod_777 variations (total: 9)
  - 2 new data_destroyer variations (total: 9)
  - Cultural context preservation ("spilt milk" = 覆水盆に返らず)
- **Comprehensive Pattern Reference** - docs/DANGEROUS_PATTERNS.md
  - Detailed explanation of all 11 dangerous patterns
  - Real-world incidents for each pattern
  - Why they're dangerous and safe alternatives
  - Caution-level patterns with guidance
  - Summary table with severity and recovery info
- **User-Friendly Quickstart Guide** - QUICKSTART.md
  - Exploratory approach with hints
  - Encourages discovery without spoiling
  - Fun, engaging tone
- **Documentation Organization**
  - Created docs/reports/ directory
  - Moved all daily summaries to reports/
  - Created reports/README.md with index
  - Clean separation: reports vs design docs
- **User Testing Guide** - docs/USER_TESTING_GUIDE.md
  - Complete guide for conducting user tests
  - Session structure and timing
  - Observation checklist
  - Feedback form template
  - Tips for effective testing

### Changed
- **Version numbering** - Corrected from v2.0 to v1.1
  - Refactoring doesn't warrant major version bump
  - Consistent versioning across all files
- **README.md** - Simplified and focused
  - Replaced long pattern list with concise summary
  - Added link to DANGEROUS_PATTERNS.md
  - Keeps README focused on project overview
- **Test Organization** - Proper structure
  - Moved test files to tests/unit/, tests/manual/
  - Created tests/manual/README.md
  - Clear separation: user guide vs developer tests
- **Root Directory** - Cleaned and organized
  - Deleted duplicate files (QUICK_TEST.md, ascii_art/)
  - Moved DEVELOPMENT_TIMELINE.md to docs/reports/
  - Professional, clean structure

### Fixed
- **dd Command Pattern Detection (Issue #2)** - Critical bug
  - Problem: `dd if=/dev/zero` without `of=` parameter was not detected
  - Root cause: Pattern required `of=` parameter
  - Solution: Made `of=` optional in regex pattern
  - Impact: Now catches both incomplete and complete dangerous dd commands
  - Verification: Automated tests confirm fix
- **Fork Bomb Pattern Detection** - Pattern bug
  - Problem: `:(){ :|:& };:` was not detected
  - Root cause: Regex too strict, didn't allow whitespace
  - Solution: Updated pattern to allow whitespace variations
  - Impact: Pattern now detects correctly
  - Discovery: Caught immediately by automated tests

### Documentation
- Added Day 5 summary (docs/reports/DAY5_SUMMARY.md)
- Updated docs/reports/README.md with Day 5 entry
- Created comprehensive test report (docs/reports/DAY5_TEST_REPORT.md)
- Added test strategy steering file (.kiro/steering/test-strategy.md)

---

## [1.0.0] - 2025-11-19 (Day 4)

### Added
- **Three-Tier Warning System** - Nuanced safety education
  - CRITICAL: Blocks immediately with ASCII art (11 patterns)
  - CAUTION: Warns and asks for confirmation (4 patterns)
  - SAFE: Passes through normally
- **4 Caution-Level Patterns** - Risky but legitimate commands
  - sudo_shell: Root shell access warnings
  - chmod_permissive: Permissive permission warnings
  - firewall_disable: Firewall disable warnings
  - selinux_disable: SELinux disable warnings
- **9 New Dangerous Patterns** - Expanded coverage
  - fork_bomb: DOS attack detection
  - redirect_to_disk: Direct disk write detection
  - mkfs_disk: Disk formatting detection
  - mv_to_null: /dev/null deletion detection
  - overwrite_file: Zero-byte overwrite detection
  - dd_random: Random data overwrite detection
  - kernel_panic: Kernel panic trigger detection
  - Consolidated rm patterns (rm_root, rm_star, rm_dot → rm_dangerous)
- **4 New Builtin Commands** - Cross-platform support
  - ls/dir: List directory contents (Windows/Unix compatible)
  - clear/cls: Clear terminal screen (Windows/Unix compatible)
  - env: Show environment variables
  - alias: Display available command aliases
- **3 New Achievements** - Safe command encouragement
  - Explorer: Used 5 different safe commands
  - Command Master: Used 10 different safe commands
  - Balanced User: Used 8 safe + 3 dangerous commands
- **IT Wordplay** - Technical humor integration
  - "Not today, SATA!" (Satan → Storage interface)
  - "RAM not found..." (Memory loss metaphor)
  - "Error 403: Forbidden" (HTTP status code)
  - "Ctrl+C won't save you!" (Process control)
- **Content Quality Review** - Systematic verification
  - Back-translation check
  - Native speaker perspective review
  - Offensive content check
  - IT wordplay implementation

### Changed
- **Statistics Tracking** - Enhanced metrics
  - Added safe command usage tracking
  - Added caution warning statistics (shown/proceeded/cancelled)
  - Updated stats display with new metrics
- **Documentation Structure** - Scalability improvements
  - Reorganized LESSONS_LEARNED.md into docs/lessons/
  - Created topic-based navigation
  - Moved original to FULL_ARCHIVE.md
  - Prevents future readability issues

### Documentation
- Added Day 4 summary (docs/reports/DAY4_SUMMARY.md)
- Created CAUTION_WARNINGS_DESIGN.md
- Created IT wordplay steering file (.kiro/steering/it-wordplay.md)
- Updated README.md for v1.1 features

---

## [0.2.0] - 2025-11-18 (Day 3)

### Added
- **Display Module Refactoring** - Major architectural improvement
  - Modular component-based architecture
  - Data-driven content management with JSON files
  - Separate components: AsciiRenderer, MessageFormatter, ContentLoader
  - Warning components: DangerWarning, TypoWarning, RepeatWarning, CautionWarning
  - Statistics and AchievementTracker as standalone classes
  - Content catalog system for managing warnings and variations
- **Test Structure Design** - Professional test organization
  - Created tests/TEST_STRUCTURE.md
  - Defined unit/integration/manual test categories
  - Test coverage map
  - Migration plan for future tests
- Creative warning message variations
- "I told you so" escalating sarcasm feature
- Comprehensive manual test plan
- Dramatic timing effects for warning displays

### Changed
- **Refactored display system** - From monolithic to modular
  - Reduced display.py from 400+ lines to clean component-based structure
  - Moved display.py to display/__init__.py for proper module organization
  - Extracted 200+ lines of old code into focused components
  - Maintained 100% backward compatibility with existing API
  - 7 new Python modules (900+ lines)
  - 4 JSON data files
  - Zero breaking changes
- Moved all test files to `tests/` directory
- Simplified welcome banner design to fix alignment issues
- Organized comment management system (Japanese source + English translations)
- Warning messages now loaded from JSON files instead of hardcoded
- ASCII art files moved to data/ascii_art/ directory

### Fixed
- Welcome banner border alignment issue (emoji width problem)
  - Issue: Box borders didn't align properly due to emoji display width
  - Solution: Replaced box design with simple separator lines
  - Impact: Banner now displays correctly on all terminals
- Content loader error handling when catalog file is missing
  - Added fallback catalog for graceful degradation

### Performance
- **Refactoring Speed**: 20 minutes (estimated 2.5-3 hours)
- **Productivity Gain**: 7.5-9x faster than estimated
- **Demonstrates**: Kiro + Spec-Driven Development effectiveness

### Documentation
- Added Day 3 summary (docs/reports/DAY3_SUMMARY.md)
- Created display refactoring spec (.kiro/specs/display-refactoring/)
- Added TEST_STRUCTURE.md

---

## [0.1.0] - 2025-11-16 (Day 1)

### Added
- Initial project structure
- Core REPL loop with three-layer command routing
- 8 builtin commands (cd, pwd, echo, export, history, help, stats, exit)
- 5 dangerous command patterns (rm -rf /, chmod 777, dd, DROP DATABASE, sudo rm)
- 2 typo patterns (sl, cd..)
- Halloween-themed display system
- ASCII art integration (3 variations)
- Colorized output with ANSI codes
- Educational warning messages with safe alternatives
- "I told you so" feature for repeated commands
- Achievement system
- Statistics tracking

### Documentation
- Comprehensive requirements (EARS format)
- Detailed design document
- Task breakdown (40+ tasks)
- Development timeline
- Lessons learned document
- Critical questions and concerns

---

## Quality Assurance Process

### Testing Approach
1. **Manual Testing**: Comprehensive test plan with 50+ test cases
2. **Visual Testing**: Terminal rendering verification
3. **Cross-platform Considerations**: Windows/Linux/Mac awareness
4. **User Experience Testing**: Real-world usage scenarios

### Bug Tracking
- Issues discovered during testing are documented here
- Each fix includes: problem description, solution, and impact
- Commits reference changelog entries

### Continuous Improvement
- User feedback incorporated iteratively
- Code quality maintained through diagnostics
- Documentation updated alongside code changes

---

## Development Metrics

### Summary (Day 1-5)
- **Total Time**: ~7 hours active development
- **Total Commits**: 58 commits
- **Total Files**: 35+ files
- **Total Lines**: ~3,500+ lines
- **Features**: 20+ features
- **Test Coverage**: 35 automated tests (100% pass)
- **Average Productivity**: 3-5x faster than traditional development

### Day 5 (2025-11-21)
- **Time**: 65 minutes
- **Focus**: Bug fixes, testing, documentation
- **Commits**: 9
- **Key Achievement**: Automated test suite (35 tests, 100% pass)
- **Efficiency**: 1.8x faster than estimated

### Day 4 (2025-11-19)
- **Time**: 65 minutes
- **Focus**: Content expansion, quality review
- **Commits**: 12
- **Key Achievement**: Three-tier warning system
- **Efficiency**: ~4x faster on average

### Day 3 (2025-11-18)
- **Time**: 20 minutes
- **Focus**: Display system refactoring
- **Commits**: 10+
- **Key Achievement**: Modular architecture (900+ lines)
- **Efficiency**: 7.5-9x faster than estimated (20 min vs 2.5-3 hours)

### Day 2 (2025-11-17)
- **Time**: ~1 hour
- **Focus**: Feature additions, spec creation
- **Commits**: 15+
- **Key Achievement**: Spec-Driven Development methodology

### Day 1 (2025-11-16)
- **Time**: ~4 hours (implementation) + 8 hours (specification)
- **Code**: ~2,000 lines
- **Features**: 20+
- **Efficiency**: 12x faster than estimated

---

## Notes

This changelog demonstrates:
- **Transparency**: All changes documented
- **Quality Focus**: Bug fixes tracked and explained
- **Iterative Development**: Continuous improvement
- **Professional Practice**: Industry-standard changelog format

For detailed development process, see:
- `DEVELOPMENT_TIMELINE.md` - Detailed timeline
- `LESSONS_LEARNED.md` - Key insights
- `tests/manual_test_plan.md` - Testing approach
