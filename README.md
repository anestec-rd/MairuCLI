# MairuCLI (まいるCLI)

> 🎃 **An educational CLI wrapper that teaches command-line safety through Halloween-themed entertainment**

[![Hackathon](https://img.shields.io/badge/Hackathon-Kiroween%202025-orange)](https://kiroween.devpost.com/)
[![Category](https://img.shields.io/badge/Category-Frankenstein-purple)](https://kiroween.devpost.com/)
[![Status](https://img.shields.io/badge/Status-In%20Development-yellow)](https://github.com/yourusername/mairu-cli)

## 🚧 Work in Progress

This project is currently under active development for the [Kiroween Hackathon](https://kiroween.devpost.com/) (Submission deadline: December 5, 2025).

**Current Phase:** Specification Complete → Implementation Starting

## What is MairuCLI?

MairuCLI (参る = "to be troubled" + wordplay on "Kiro") is an educational CLI wrapper that:

- 🔥 **Intercepts dangerous commands** before they execute (e.g., `rm -rf /`)
- 🎃 **Displays Halloween-themed warnings** with ASCII art and educational messages
- 🚂 **Entertains with typo responses** (e.g., `sl` shows a steam locomotive)
- 📚 **Teaches CLI safety** through real-world incident examples
- ✅ **Passes safe commands** to your system shell normally

### Example

```bash
$ mairu
🎃 Welcome to MairuCLI 🎃

mairu> ls
file1.txt  file2.txt  folder/

mairu> rm -rf /
🔥 YOU'RE FIRED! 🔥
(And so is your entire filesystem!)

[ASCII art of burning figure]

This command deletes EVERYTHING on your system.
No undo button. No trash bin. Just... gone.

💡 Safe alternative: Use 'rm -i' for confirmation prompts.

mairu> ls
file1.txt  file2.txt  folder/  # Still works!
```

## Project Goals

1. **Educational Value:** Teach engineers about CLI dangers in a memorable way
2. **Entertainment:** Halloween party aesthetic (comedic, not scary)
3. **Kiro Showcase:** Demonstrate effective use of Kiro's Spec-Driven Development workflow

## Development Approach

This project is built using **Kiro's Spec-Driven Development** methodology:

- ✅ **Requirements** → Defined user stories and acceptance criteria
- ✅ **Design** → Architecture and implementation strategy
- ✅ **Tasks** → Detailed implementation checklist
- 🔄 **Implementation** → Currently starting (Phase 1)

### Kiro Features Demonstrated

- **Spec-Driven Development:** Complete requirements → design → tasks workflow
- **Steering:** AI-guided code generation following project standards
- **Meeting Logs:** Documented decision-making process
- **Chat Context:** Natural use of project references

## Technology Stack

- **Language:** Python 3.8+ (standard library only)
- **Platform:** Linux, macOS (Windows via WSL)
- **Development Tool:** Kiro IDE
- **Version Control:** Git

## Project Structure

```
mairu-cli/
├── .kiro/
│   ├── specs/mairu-cli/      # Specification documents
│   │   ├── requirements.md
│   │   ├── design.md
│   │   ├── tasks.md
│   │   └── meetings/          # Development logs
│   └── steering/              # Kiro steering files
├── src/                       # Source code (coming soon)
├── ascii_art/                 # ASCII art files (coming soon)
├── tests/                     # Test files (coming soon)
└── README.md
```

## ⚠️ Important Disclaimer

**MairuCLI is an educational tool, NOT a production security solution.**

This tool is designed for:
- Learning about CLI safety
- Demonstrating common mistakes
- Entertainment and engagement

This tool is NOT designed for:
- Production environments
- Actual security enforcement
- Replacing proper access controls

See [LIMITATIONS.md](LIMITATIONS.md) (coming soon) for detailed information.

## Development Timeline

- **November 16, 2025:** Specification phase complete
- **November 22-24, 2025:** Implementation phase
- **November 29, 2025:** Quality Improvement
- **November 30, 2025:** Demo video and submission
- **December 5, 2025:** Hackathon submission deadline

## Contributing

This is a hackathon project with a tight deadline. Contributions are not currently being accepted, but feel free to:
- ⭐ Star the repository
- 👀 Watch for updates
- 💬 Open issues for suggestions (after hackathon submission)

## License

[MIT License](LICENSE)

## Acknowledgments

- **Kiroween Hackathon:** Organized by AWS and Devpost
- **Kiro IDE:** AI-powered development tool that made this project possible
- **CLI_Troubled.md:** Reference material for common CLI mistakes
- **Community:** Thanks to all who provided feedback and testing

## Contact

- **Hackathon Submission:** [Devpost Link](https://kiroween.devpost.com/) (coming soon)
- **Demo Video:** [YouTube Link](https://youtube.com) (coming soon)
- **Developer:** [Your Name/Handle]

---

**Built with ❤️ and 🎃 using Kiro**

*Last Updated: November 16, 2025*
