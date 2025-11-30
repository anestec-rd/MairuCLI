# MairuCLI (まいるCLI)

> 🎃 **An educational CLI wrapper that teaches command-line safety through Halloween-themed entertainment**
>
> **✨ Built 100% with Kiro AI** - No GitHub Copilot, No Claude, No ChatGPT

[![Hackathon](https://img.shields.io/badge/Hackathon-Kiroween%202025-orange)](https://kiroween.devpost.com/)
[![Built with Kiro](https://img.shields.io/badge/Built%20100%25%20with-Kiro%20AI-blue)](https://kiro.dev/)
![Version](https://img.shields.io/badge/Version-1.5.0-green)
![Tests](https://img.shields.io/badge/Tests-322%20passing-brightgreen)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)

## 🎉 What is MairuCLI?

MairuCLI (参る = "to be troubled" + wordplay on "Kiro") is an educational CLI wrapper that combines **security education** with **Halloween entertainment**:

- 🔥 **Intercepts dangerous commands** before they execute (e.g., `rm -rf /`, `chmod 777`)
- 🎃 **Displays Halloween-themed warnings** with ASCII art and educational messages
- 🚂 **Entertains with typo responses** (e.g., `sl` shows a steam locomotive)
- 🏆 **Gamifies learning** with achievements and statistics
- 📚 **Teaches CLI safety** through real-world incident examples
- ✅ **Passes safe commands** to your system shell normally

### Example Session

```bash
$ python -m src.main

          ███╗   ███╗ █████╗ ██╗██████╗ ██╗   ██╗
          ████╗ ████║██╔══██╗██║██╔══██╗██║   ██║
          ██╔████╔██║███████║██║██████╔╝██║   ██║
          ██║╚██╔╝██║██╔══██║██║██╔══██╗██║   ██║
          ██║ ╚═╝ ██║██║  ██║██║██║  ██║╚██████╔╝
          ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝╚═╝  ╚═╝ ╚═════╝

           ██████╗██╗     ██╗    __../＾\.._
          ██╔════╝██║     ██║   / / / || \ \ \
          ██║     ██║     ██║  | (🔥)/ \(🔥)||
          ██║     ██║     ██║  | |\/\/\/\/\/| |
          ╚██████╗███████╗██║   \ \/\/\/\/\/ /
           ╚═════╝╚══════╝╚═╝    '.|_|,.|_|,/

 　 Your friendly CLI safety wrapper with a spooky twist!

mairu> ls
file1.txt  file2.txt  folder/

mairu> rm -rf /
============================================================
    🔥🔥🔥 YOU'RE FIRED! 🔥🔥🔥

         .-""""""-.
       .'          '.
      /   O      O   \
     :                :
     |                |
     :    .-----.    :
      \  '       '  /
       '.          .'
         '-......-'

🔥 YOU'RE FIRED! 🔥
(And so is your entire filesystem!)

The command 'rm -rf /' attempts to delete EVERYTHING.
This is unrecoverable without backups.

💡 Safe alternative:
  - Use 'rm -i' for interactive confirmation
  - Use 'trash-cli' instead of rm

Blocked command: rm -rf /
============================================================

============================================================
🏆 ACHIEVEMENT UNLOCKED! 🏆

  First Blood
  Blocked your first dangerous command!
============================================================

mairu> help
Available commands:
  cd <dir>    - Change directory
  pwd         - Print working directory
  ls          - List files (passes to system)
  help        - Show this help message
  stats       - Show your safety statistics
  exit        - Exit MairuCLI

🎃 DON'T try these dangerous commands:
  rm -rf /           - Deletes everything
  chmod 777 file     - Opens security holes
  dd if=/dev/zero    - Destroys disk data
  DROP DATABASE      - Deletes entire database
  sudo rm -rf $VAR   - Dangerous with variables

(But if you do, I'll stop you! 😈)
```

## ✨ Features

### Core Functionality
- **21 Built-in Commands:**
  - Navigation: cd, pwd
  - File Operations: ls/dir, cat, touch, mkdir
  - Search: find, grep, which
  - System Info: whoami, date, hostname, env, export
  - Display: tree
  - Utilities: echo, clear/cls, history, alias
  - MairuCLI: help, stats, lie, exit
- **System Directory Protection:** Prevents accidental modification of critical system directories (Windows, Linux, macOS) with educational warnings
- **11 Dangerous Pattern Detection:** rm -rf variants, chmod 777/000, dd, DROP DATABASE, fork bomb, disk operations, kernel panic
- **4 Caution-Level Warnings:** sudo su, chmod 666/755, firewall disable, SELinux disable
- **2 Typo Entertainment:** sl → ls, cd.. → cd ..
- **Educational Breakdown Mode:** Interactive learning with command breakdowns, timeline simulations, and real-world incident stories (5 patterns covered)
- **Achievement System:** Multiple unlockable achievements to discover (danger-related, safe exploration, system protection, and more...)
- **Statistics Tracking:** Dangerous blocks, typos, caution warnings, safe commands, system protection
- **Repeat Detection:** Escalating sarcasm for repeated dangerous commands
- **IT Wordplay:** Technical humor with terms like SATA, RAM, HTTP 403, Ctrl+C
- **Modular Architecture:** Clean separation with 15+ modules, 322 passing tests

### Display System (Refactored Architecture)
- **Modular Components:** Separated concerns for maintainability
- **Data-Driven Content:** JSON-based warning messages and variations
- **ASCII Art Rendering:** Dramatic timing effects for impact
- **Template-Based Messages:** Consistent formatting across warning types
- **Graceful Error Handling:** Fallbacks for missing content

### Educational Breakdown Mode
- **Interactive Learning:** Choose your detail level (quick/full/skip)
- **Command Breakdowns:** Understand what each part of a dangerous command means
- **Timeline Simulations:** See step-by-step what would happen if executed
- **Real-World Incidents:** Learn from actual production disasters (e.g., GitLab 2017)
- **5 Patterns Covered:** rm -rf, chmod 777/000, dd, fork bomb
- **JSON-Based Content:** Easy to add new educational content without code changes

### Dangerous Patterns

MairuCLI detects **11 dangerous command patterns** including:
- `rm -rf /` - Recursive deletion
- `chmod 777` - Permission chaos
- `dd if=/dev/zero` - Disk destruction
- `DROP DATABASE` - Database annihilation
- `:(){ :|:& };:` - Fork bomb
- And 6 more...

**See full details:** [docs/dangerous-patterns.md](docs/dangerous-patterns.md)

Each pattern includes real-world incidents, why it's dangerous, and safe alternatives.

## 🚀 Try It Out

### Option 1: GitHub Codespaces (Recommended - No Installation!)

**Method A: Direct Link (Easiest)**

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/anestec-rd/MairuCLI?quickstart=1)

**Method B: From Repository**

1. Go to [MairuCLI Repository](https://github.com/anestec-rd/MairuCLI)
2. Click the green **"Code"** button
3. Select **"Codespaces"** tab
4. Click **"Create codespace on main"**

**Click the button above to try MairuCLI in your browser - no installation required!**

**Steps:**
1. Click the "Open in GitHub Codespaces" button above
2. If prompted, select **"anestec-rd/MairuCLI"** repository (should be pre-selected)
3. Click **"Create codespace"** (green button)
4. Wait ~30 seconds for environment to load
5. Terminal will open automatically with welcome message
6. Run: `python -m src.main`
7. Try dangerous commands safely:
   - `rm -rf /` - See the 🔥 YOU'RE FIRED! warning
   - `chmod 777 file` - Permission chaos warning
   - `sl` - Typo entertainment (steam locomotive!)
   - `stats` - Check your safety statistics
8. Type `exit` to quit

**Perfect for judges and reviewers!** 🎃

### Option 2: Local Installation

**Prerequisites:**
- Python 3.8 or higher
- Linux, macOS, or Windows

**Quick Start:**

```bash
# Clone the repository
git clone https://github.com/anestec-rd/MairuCLI.git
cd MairuCLI

# Run MairuCLI
python -m src.main

# Or make it executable (Linux/macOS)
chmod +x run.sh
./run.sh
```

No external dependencies required - uses Python standard library only!

**Want a guided tour?** See [QUICKSTART.md](QUICKSTART.md) for a fun walkthrough! 🎃

## 🖥️ Platform Support

MairuCLI has been **verified and tested** on:

| Platform | Status | Notes |
|----------|--------|-------|
| **Windows** | ✅ Verified | Full support via native Python or WSL |
| **Linux** | ✅ Verified | Tested on Ubuntu, Debian, Fedora |
| **macOS** | ✅ Verified | Tested on macOS 12+ (Intel & Apple Silicon) |

### Cross-Platform Features
- ✅ **System Directory Protection** works on all platforms
  - Windows: `C:\Windows`, `C:\Program Files`, etc.
  - Linux/macOS: `/bin`, `/usr`, `/etc`, etc.
- ✅ **All dangerous patterns** detected consistently
- ✅ **All tests pass** on all platforms (322 tests)
- ✅ **ASCII art** renders correctly on all terminals

### Quick Verification

Verify MairuCLI works on your system:

```bash
# 1. Run the test suite
python -m pytest tests/unit tests/integration -v

# Expected: 322 passed, 8 skipped

# 2. Try a safe command
python -m src.main
mairu> ls
# Should list files normally

# 3. Try a dangerous command (safely!)
mairu> rm -rf /
# Should show warning and block

# 4. Check statistics
mairu> stats
# Should show your activity

# 5. Exit
mairu> exit
```

**All working?** You're ready to go! 🎃

## 🧪 Test Coverage

MairuCLI has **comprehensive test coverage** to ensure reliability:

| Test Type | Count | Status |
|-----------|-------|--------|
| **Unit Tests** | ~275 | ✅ All Passing |
| **Integration Tests** | ~47 | ✅ All Passing |
| **Total** | **322** | ✅ **All Passing** |

**Note:** Test counts are approximate. Run `pytest tests/unit tests/integration -v` for exact count.

### Test Categories

**Unit Tests** (`tests/unit/`):
- ✅ Command parsing and validation
- ✅ Pattern detection (dangerous, caution, typo)
- ✅ Path resolution and system protection
- ✅ Display components (ASCII, messages, formatting)
- ✅ Achievement and statistics tracking
- ✅ Educational content loading
- ✅ Builtin command functionality

**Integration Tests** (`tests/integration/`):
- ✅ End-to-end dangerous command flow
- ✅ Caution warning confirmation flow
- ✅ Educational breakdown interaction
- ✅ System protection across platforms
- ✅ Repeat warning escalation
- ✅ Achievement unlock triggers
- ✅ Builtin command redirection

### Running Tests

```bash
# Run all tests (unit + integration)
python -m pytest tests/unit tests/integration -v

# Run specific test category
python -m pytest tests/unit/ -v
python -m pytest tests/integration/ -v

# Run with coverage report
python -m pytest tests/ --cov=src --cov-report=html
```

**Test Philosophy:**
- Every dangerous pattern has tests
- Every feature has integration tests
- No mocks for core functionality (tests real behavior)
- Cross-platform compatibility verified

## 📖 Usage

### Basic Commands

```bash
mairu> cd /tmp          # Change directory
mairu> pwd              # Show current directory
mairu> ls -la           # List files (passed to system)
mairu> echo Hello       # Print text
mairu> history          # Show command history
mairu> stats            # Show your statistics
mairu> help             # Show help message
mairu> exit             # Exit MairuCLI
```

### Try Dangerous Commands (Safely!)

```bash
mairu> rm -rf /         # Blocked with warning
mairu> chmod 777 file   # Blocked with warning
mairu> sl               # Typo entertainment
```

### Unlock Achievements

**Multiple achievements to discover:**

🔥 **Danger-Related**
- Unlock by trying dangerous commands
- Some require persistence...
- Try the same command multiple times!

✅ **Safe Explorer**
- Unlock by using safe commands
- Try different commands!
- Balance is key...

🚂 **Typo Master**
- Unlock by making typos
- We all make mistakes!

**Hint:** Use `stats` to see your progress and unlocked achievements!

## 🏗️ Architecture

### Project Structure

```
mairu-cli/
├── src/
│   ├── main.py                    # Entry point and REPL loop
│   ├── config.py                  # Configuration and constants
│   ├── builtins/                  # Modular builtin commands (refactored Day 7)
│   │   ├── __init__.py            # Main interface
│   │   ├── navigation.py          # cd, pwd
│   │   ├── file_operations.py    # ls, cat, touch, mkdir
│   │   ├── search.py              # find, grep, which
│   │   ├── system_info.py        # whoami, date, hostname, env
│   │   ├── display.py             # tree
│   │   ├── shell_utils.py        # echo, clear, history, alias
│   │   └── mairu_commands.py     # help, stats
│   ├── interceptor.py             # Pattern matching for dangerous commands
│   ├── command_parser.py          # Command parsing and path extraction
│   ├── path_resolver.py           # Path resolution for system protection
│   └── display/                   # Modular display system
│       ├── __init__.py            # Public API
│       ├── ascii_renderer.py      # ASCII art loading and rendering
│       ├── message_formatter.py   # Template-based message formatting
│       ├── warning_components.py  # Warning display components
│       ├── system_protection_warning.py # System directory warnings
│       ├── caution_warning.py     # Caution-level warnings
│       ├── educational_breakdown.py # Educational breakdown mode
│       ├── educational_loader.py  # Educational content loader
│       ├── breakdown_formatter.py # Educational content formatter
│       ├── achievements.py        # Achievement tracking
│       ├── statistics.py          # Statistics tracking
│       └── content_loader.py      # JSON content management
├── data/
│   ├── warnings/                  # Warning content (JSON)
│   │   ├── warning_catalog.json   # Master catalog
│   │   ├── danger_variations.json # Message variations
│   │   ├── typo_messages.json     # Typo messages
│   │   └── repeat_warnings.json   # Repeat warnings
│   ├── educational/               # Educational content (JSON)
│   │   ├── command_breakdowns/    # Command part explanations
│   │   ├── simulations/           # Timeline simulations
│   │   └── incidents/             # Real-world incident stories
│   └── ascii_art/                 # ASCII art files
│       ├── fired.txt
│       ├── permission_denied.txt
│       └── data_destroyer.txt
├── tests/                         # Test files
├── docs/                          # Documentation
└── .kiro/                         # Kiro spec files
    ├── specs/
    │   ├── mairu-cli/             # Original spec
    │   └── display-refactoring/   # Refactoring spec
    └── steering/                  # Development standards
```

### Display System Architecture

The display system was refactored from a monolithic 400-line file into a modular architecture:

**Before:** Single `display.py` with hardcoded messages
**After:** 7 focused components with data-driven content

**Key Components:**
- `AsciiRenderer`: Handles ASCII art loading and dramatic timing
- `MessageFormatter`: Template-based message formatting
- `WarningComponents`: Modular warning displays (Danger, Typo, Repeat)
- `ContentLoader`: JSON-based content management
- `EducationalBreakdown`: Interactive learning mode orchestration
- `EducationalLoader`: Loads educational content from JSON
- `BreakdownFormatter`: Formats educational displays
- `Statistics` & `Achievements`: Separated tracking logic

**Benefits:**
- Easy to add new warnings (just edit JSON)
- Easy to add new variations (no code changes)
- Testable components
- Maintainable codebase

## 🎯 Development Methodology

### Built Exclusively with Kiro AI

This project was built **100% with Kiro** - no other AI tools were used:
- ❌ No GitHub Copilot
- ❌ No Claude
- ❌ No ChatGPT
- ✅ **Only Kiro**

This demonstrates Kiro's standalone capabilities for complete project development.

### Spec-Driven Development

Kiro's Spec-Driven Development methodology was used throughout:

1. **Requirements Phase:** User stories with EARS-compliant acceptance criteria
2. **Design Phase:** Architecture, components, and data models
3. **Tasks Phase:** Detailed implementation checklist
4. **Implementation:** Incremental execution with testing

**Key Artifacts:**
- `.kiro/specs/mairu-cli/` - Original project spec
- `.kiro/specs/display-refactoring/` - Refactoring spec
- `.kiro/steering/` - Development standards and guidelines (15 files)

### Productivity Gains

**Display Module Refactoring:**
- **Original Estimate:** 2.5-3 hours
- **Actual Time:** 20 minutes
- **Speed Improvement:** 7.5-9x faster

**Tasks Completed in 20 Minutes:**
- Created 6 new Python modules (900+ lines)
- Created 4 JSON data files
- Refactored 400-line monolithic file
- Maintained 100% backward compatibility
- Zero breaking changes
- Complete documentation

This demonstrates the power of Kiro + Spec-Driven Development.

### Learn More About Kiro Workflow

**Want to see how Kiro made this possible?**

📖 **[Read the Complete Kiro Workflow Documentation](docs/kiro-workflow.md)**

This comprehensive guide covers:
- **Spec-Driven Development:** Requirements → Design → Tasks → Implementation
- **15 Steering Files:** Development standards that ensure consistency
- **Productivity Metrics:** How we achieved 7.5-9x speed improvements
- **Real Examples:** Detailed case studies from MairuCLI development
- **Best Practices:** How to leverage Kiro for your own projects

**Key Features Documented:**
- ✅ How specs structure complex features
- ✅ How steering files provide persistent guidance
- ✅ How incremental task execution enables validation
- ✅ How context awareness eliminates repetition
- ✅ Real productivity metrics with time tracking

## 🧪 Testing & Quality Assurance

### Automated Testing

```bash
# Run all tests (322 tests)
python -m pytest tests/unit tests/integration -v

# Run specific test suites
python -m pytest tests/unit/ -v           # 275 unit tests
python -m pytest tests/integration/ -v    # 47 integration tests

# Run with coverage report
python -m pytest tests/ --cov=src --cov-report=html
```

### Manual Testing

```bash
# Run manual test plan
# See tests/manual/manual_test_plan.md

# Test specific features
python tests/manual/test_dangerous_commands.py
python tests/manual/test_educational_messages.py
python tests/manual/test_system_protection_manual.py
```

### Quality Metrics

- ✅ **322 automated tests** (unit + integration)
- ✅ **All tests passing** on all platforms
- ✅ **Zero breaking changes** during refactoring
- ✅ **Backward compatibility** maintained
- ✅ **Cross-platform verified** (Windows, Linux, macOS)
- ✅ **All dangerous patterns** tested
- ✅ **All achievements** verified
- ✅ **Error handling** comprehensive

## ⚠️ Important Disclaimer

**MairuCLI is an educational tool, NOT a production security solution.**

**Designed for:**
- Learning about CLI safety
- Demonstrating common mistakes
- Entertainment and engagement
- Educational workshops

**NOT designed for:**
- Production environments
- Actual security enforcement
- Replacing proper access controls
- Mission-critical systems

**How It Works:**
- ✅ **Dangerous commands** are blocked with warnings
- ✅ **Safe commands** are passed to your system shell
- ℹ️ **Unknown/invalid commands** will show system error messages

This is intentional! Learning includes seeing what happens with invalid commands.

**Known Limitations:**
- Pattern matching can be bypassed
- Not a comprehensive security solution
- Educational purpose only
- Unknown commands pass through to system (by design)
- See `docs/ISSUES.md` for details

## 📚 Documentation

### Core Documentation
- **[LESSONS_LEARNED.md](LESSONS_LEARNED.md)** - Development insights, AI collaboration, and philosophy
- **[CHANGELOG.md](CHANGELOG.md)** - Version history and changes
- **[Kiro Workflow Documentation](docs/kiro-workflow.md)** - How Kiro enabled rapid development

### Development Archive
- **[docs/archive/](docs/archive/)** - Complete development process archive
  - Daily summaries (Day 1-13)
  - Planning documents
  - Analysis reports
  - Test reports
  - Development timeline
  - See [docs/README.md](docs/README.md) for full documentation structure

### Design Documents
- **[docs/design/caution-warnings-design.md](docs/design/caution-warnings-design.md)** - Three-tier warning system design
- **[docs/design/educational-content-schema.md](docs/design/educational-content-schema.md)** - Educational content JSON schema
- **[docs/issues.md](docs/issues.md)** - Known issues and limitations

### Kiro Steering Files
- **[.kiro/steering/it-wordplay.md](.kiro/steering/it-wordplay.md)** - IT wordplay guidelines
- **[.kiro/steering/halloween-theme.md](.kiro/steering/halloween-theme.md)** - Halloween theme design
- **[.kiro/steering/test-organization.md](.kiro/steering/test-organization.md)** - Test structure standards
- **[.kiro/steering/data-driven-content.md](.kiro/steering/data-driven-content.md)** - Content management approach

## 🎬 Demo

**Demo Video:** [Coming Soon]

**Live Demo:** Run `python -m src.main` and try these commands:
1. `help` - See available commands
2. `rm -rf /` - See a danger warning
3. `sl` - See typo entertainment
4. `stats` - Check your statistics

## 🏆 Hackathon Submission

**Event:** Kiroween Hackathon 2025
**Category:** Frankenstein Award (Fusion of security + entertainment + education)
**Submission Deadline:** December 5, 2025

**Key Highlights:**
- ✅ Built exclusively with Kiro (no other AI tools)
- ✅ Demonstrates Spec-Driven Development
- ✅ 20-minute major refactoring (7.5-9x productivity gain)
- ✅ Complete documentation and audit trail
- ✅ Educational value + entertainment
- ✅ Clean, maintainable architecture

## 🔧 Adding New Patterns

MairuCLI uses a **data-driven architecture** - all patterns are stored in JSON files, not hardcoded in Python!

### Adding a Dangerous Pattern

1. **Add to `data/warnings/warning_catalog.json`:**

```json
{
  "your_pattern_name": {
    "category": "deletion",
    "severity": "critical",
    "variation_set": "your_pattern",
    "ascii_art": "your_art.txt",
    "color": "red",
    "emoji": "fire",
    "pattern": "your\\s+regex\\s+pattern",
    "explanation": "What this command does",
    "consequence": "Why it's dangerous",
    "advice": ["Safe alternative 1", "Safe alternative 2"],
    "help_example": "your command",
    "help_description": "Short description (under 50 chars)",
    "timing": {
      "art_delay": 0.05,
      "pause_after_art": 0.3,
      "pause_before_explanation": 0.5,
      "pause_before_achievement": 0.3
    }
  }
}
```

2. **Add variations to `data/warnings/category_variations.json`** (if needed)
3. **Add ASCII art to `data/ascii_art/`** (if needed)
4. **Test:** Run `python -m src.main` and try your pattern

**Important:** Use double backslashes in JSON regex patterns! (`\\s+` not `\s+`)

### Adding a Caution Pattern

Add to `data/warnings/caution_catalog.json`:

```json
{
  "your_caution": {
    "pattern": "your\\s+pattern",
    "category": "security",
    "severity": "medium",
    "risk": "What could go wrong",
    "impact": "Potential consequences",
    "considerations": [
      "Question 1 to make user think",
      "Question 2 about alternatives",
      "Question 3 about context"
    ],
    "help_example": "your command",
    "help_description": "Short description"
  }
}
```

### Adding a Typo Pattern

Add to `data/warnings/typo_messages.json`:

```json
{
  "your_typo": {
    "pattern": "^typo\\b",
    "correct": "correct_command",
    "message": "🎃 Fun message about the typo!",
    "ascii_art": null
  }
}
```

### Adding Educational Content (Optional)

To add educational breakdown content for your pattern:

1. **Create command breakdown** in `data/educational/command_breakdowns/{pattern_name}.json`
2. **Create timeline simulation** in `data/educational/simulations/{pattern_name}.json`
3. **Add incident story** (optional) in `data/educational/incidents/{incident_id}.json`

See [Educational Content Schema](docs/educational-content-schema.md) for detailed format.

### No Code Changes Needed!

The pattern loader automatically picks up new patterns from JSON files. Just restart MairuCLI and your new pattern will work!

---

## 🤝 Contributing

This is a hackathon project. After the submission deadline, contributions will be welcome!

For now:
- ⭐ Star the repository
- 👀 Watch for updates
- 💬 Open issues for suggestions (after December 5)

## 📄 License

[Apache License 2.0](LICENSE)

## 🙏 Acknowledgments

- **Kiro IDE:** Made this rapid development possible
- **Kiroween Hackathon:** Organized by AWS and Devpost
- **CLI_Troubled.md:** Reference material for CLI dangers
- **Halloween Theme Guidelines:** Design inspiration

## 📞 Contact

- **Devpost:** [Submission Link - Coming Soon]
- **Demo Video:** [YouTube Link - Coming Soon]

---

## 🎨 Special Features

### Three-Tier Warning System

**CRITICAL (Blocks immediately):**
- Dangerous commands that cause immediate data loss
- ASCII art + dramatic warnings
- Examples: `rm -rf /`, `dd`, `DROP DATABASE`

**CAUTION (Asks for confirmation):**
- Risky commands with legitimate uses
- Educational considerations
- User choice to proceed or cancel
- Examples: `sudo su`, `chmod 666`, `ufw disable`

**SAFE (No warning):**
- Normal commands pass through
- Tracked for achievement system

### IT Wordplay

MairuCLI uses technical humor to make warnings engaging:
- **"Not today, SATA!"** - Storage interface pun (Satan → SATA)
- **"RAM not found..."** - Memory loss metaphor
- **"Error 403: Forbidden"** - HTTP status code humor
- **"Ctrl+C won't save you!"** - Process control reference

See [IT Wordplay Guidelines](.kiro/steering/it-wordplay.md) for more examples.

---

**Built with ❤️ and 🎃 using Kiro AI**

*Version 1.5.0 - November 30, 2025*

