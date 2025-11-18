# MairuCLI (まいるCLI)

> 🎃 **An educational CLI wrapper that teaches command-line safety through Halloween-themed entertainment**

[![Hackathon](https://img.shields.io/badge/Hackathon-Kiroween%202025-orange)](https://kiroween.devpost.com/)
[![Built with Kiro](https://img.shields.io/badge/Built%20with-Kiro%20AI-blue)](https://kiro.dev/)
[![Version](https://img.shields.io/badge/Version-1.0-green)](https://github.com/yourusername/mairu-cli)

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
========================================================
  🎃 Welcome to MairuCLI 🎃
  Your friendly CLI safety wrapper with a spooky twist!
========================================================

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
- **8 Built-in Commands:** cd, pwd, echo, export, history, help, stats, exit
- **5 Dangerous Pattern Detection:** rm -rf /, chmod 777, dd, DROP DATABASE, sudo rm
- **2 Typo Entertainment:** sl → ls, cd.. → cd ..
- **Achievement System:** 5 unlockable achievements
- **Statistics Tracking:** Track dangerous commands blocked and typos caught
- **Repeat Detection:** Escalating sarcasm for repeated dangerous commands

### Display System (v2.0 - Refactored Architecture)
- **Modular Components:** Separated concerns for maintainability
- **Data-Driven Content:** JSON-based warning messages and variations
- **ASCII Art Rendering:** Dramatic timing effects for impact
- **Template-Based Messages:** Consistent formatting across warning types
- **Graceful Error Handling:** Fallbacks for missing content

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- Linux, macOS, or Windows (via WSL)

### Quick Start

```bash
# Clone the repository
git clone https://github.com/yourusername/mairu-cli.git
cd mairu-cli

# Run MairuCLI
python -m src.main

# Or make it executable (Linux/macOS)
chmod +x run.sh
./run.sh
```

No external dependencies required - uses Python standard library only!

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

- **First Blood:** Block your first dangerous command
- **Persistent Troublemaker:** Try 5 dangerous commands
- **Typo Master:** Make 3 typos
- **Danger Addict:** Block 10 dangerous commands
- **Stubborn:** Try the same command 3 times

## 🏗️ Architecture

### Project Structure

```
mairu-cli/
├── src/
│   ├── main.py                    # Entry point and REPL loop
│   ├── builtins.py                # Built-in command implementations
│   ├── interceptor.py             # Pattern matching for dangerous commands
│   └── display/                   # Modular display system (v2.0)
│       ├── __init__.py            # Public API
│       ├── ascii_renderer.py      # ASCII art loading and rendering
│       ├── message_formatter.py   # Template-based message formatting
│       ├── warning_components.py  # Warning display components
│       ├── achievements.py        # Achievement tracking
│       ├── statistics.py          # Statistics tracking
│       └── content_loader.py      # JSON content management
├── data/
│   ├── warnings/                  # Warning content (JSON)
│   │   ├── warning_catalog.json   # Master catalog
│   │   ├── danger_variations.json # Message variations
│   │   ├── typo_messages.json     # Typo messages
│   │   └── repeat_warnings.json   # Repeat warnings
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

### Display System Architecture (v2.0)

The display system was refactored from a monolithic 400-line file into a modular architecture:

**Before:** Single `display.py` with hardcoded messages
**After:** 7 focused components with data-driven content

**Key Components:**
- `AsciiRenderer`: Handles ASCII art loading and dramatic timing
- `MessageFormatter`: Template-based message formatting
- `WarningComponents`: Modular warning displays (Danger, Typo, Repeat)
- `ContentLoader`: JSON-based content management
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
- `.kiro/steering/` - Development standards and guidelines

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

## 🧪 Testing

### Manual Testing

```bash
# Run test script
python tests/test_dangerous.py

# Run manual test plan
# See tests/manual_test_plan.md
```

### Test Coverage

- ✅ All dangerous patterns detected correctly
- ✅ All typo patterns work
- ✅ Achievements trigger correctly
- ✅ Statistics track accurately
- ✅ Repeat warnings escalate properly
- ✅ Error handling with missing files
- ✅ Backward compatibility maintained

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

**Known Limitations:**
- Pattern matching can be bypassed
- Not a comprehensive security solution
- Educational purpose only
- See `docs/ISSUES.md` for details

## 📚 Documentation

- **[LESSONS_LEARNED.md](LESSONS_LEARNED.md)** - Development insights and philosophy
- **[CHANGELOG.md](CHANGELOG.md)** - Version history and changes
- **[TODO.md](TODO.md)** - Planned features and improvements
- **[docs/DAY1_SUMMARY.md](docs/DAY1_SUMMARY.md)** - Day 1 development summary
- **[docs/DAY2-1_SUMMARY.md](docs/DAY2-1_SUMMARY.md)** - Day 2 Session 1 summary
- **[docs/DAY2-2_SUMMARY.md](docs/DAY2-2_SUMMARY.md)** - Day 2 Session 2 summary (spec creation)
- **[docs/DAY3_SUMMARY.md](docs/DAY3_SUMMARY.md)** - Day 3 summary (20-minute refactoring)

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

## 🤝 Contributing

This is a hackathon project. After the submission deadline, contributions will be welcome!

For now:
- ⭐ Star the repository
- 👀 Watch for updates
- 💬 Open issues for suggestions (after December 5)

## 📄 License

[MIT License](LICENSE)

## 🙏 Acknowledgments

- **Kiro IDE:** Made this rapid development possible
- **Kiroween Hackathon:** Organized by AWS and Devpost
- **CLI_Troubled.md:** Reference material for CLI dangers
- **Halloween Theme Guidelines:** Design inspiration

## 📞 Contact

- **GitHub:** [Your GitHub Profile]
- **Devpost:** [Submission Link - Coming Soon]
- **Demo Video:** [YouTube Link - Coming Soon]

---

**Built with ❤️ and 🎃 using Kiro AI**

*Version 1.0 - November 18, 2025*

