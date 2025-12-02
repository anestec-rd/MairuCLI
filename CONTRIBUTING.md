# Contributing to MairuCLI

Thank you for your interest in contributing to MairuCLI! 🎃

## Current Status

This project was created for the **Kiroween 2025 Hackathon** and built 100% with Kiro AI. After the submission deadline (December 5, 2025), we will welcome contributions from the community!

## After December 5, 2025

### How to Contribute

We welcome contributions in several forms:

1. **🐛 Report Issues**: Found a bug or have a feature request? Open an issue!
2. **💻 Submit Pull Requests**: Fork the repo, make changes, and submit a PR
3. **🎨 Add Content**: New warning patterns, ASCII art, or educational content
4. **📚 Improve Documentation**: Help make the docs clearer and more comprehensive
5. **🧪 Add Tests**: Improve test coverage or add new test cases

### Adding New Warning Patterns

MairuCLI uses a data-driven architecture. To add new dangerous command patterns:

1. **Add pattern to `data/warnings/warning_catalog.json`**
2. **Add variations to `data/warnings/danger_variations.json`** (optional)
3. **Add ASCII art to `data/ascii_art/`** (optional)
4. **Add tests to `tests/unit/test_interceptor.py`**

See [docs/dangerous-patterns.md](docs/dangerous-patterns.md) for detailed instructions.

### Adding Educational Content

To add educational breakdowns for commands:

1. **Create breakdown in `data/educational/command_breakdowns/`**
2. **Create simulation in `data/educational/simulations/`**
3. **Add incident story in `data/educational/incidents/`** (optional)

See [docs/design/educational-content-schema.md](docs/design/educational-content-schema.md) for schema details.

### Code Style Guidelines

- **Python**: Follow PEP 8 standards
- **Line length**: 100 characters maximum
- **Type hints**: Use type hints for function parameters and return values
- **Docstrings**: Add docstrings to all public functions
- **Tests**: Add tests for new features (see `tests/TEST_STRUCTURE.md`)

### File Naming Conventions

- **Python files**: `snake_case.py`
- **Documentation**: `kebab-case.md`
- **Data files**: `snake_case.json`

See [.kiro/steering/naming-conventions.md](.kiro/steering/naming-conventions.md) for details.

### Testing

Before submitting a PR:

```bash
# Run all tests
python -m pytest tests/unit tests/integration -v

# Run specific test suite
python -m pytest tests/unit/ -v

# Run with coverage
python -m pytest tests/ --cov=src --cov-report=html
```

All tests must pass before merging.

### Pull Request Process

1. **Fork** the repository
2. **Create a branch** for your feature (`git checkout -b feature/amazing-feature`)
3. **Make your changes** and commit (`git commit -m 'feat: add amazing feature'`)
4. **Push** to your fork (`git push origin feature/amazing-feature`)
5. **Open a Pull Request** with a clear description of changes

### Commit Message Format

We follow conventional commits:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, no logic change)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Example:**
```
feat(interceptor): add wget malicious URL detection

Implements detection for wget commands downloading from suspicious URLs.
Includes variations with different protocols and domains.

Closes #42
```

## Development Setup

```bash
# Clone the repository
git clone https://github.com/anestec-rd/MairuCLI.git
cd MairuCLI

# Run MairuCLI
python -m src.main

# Run tests
python -m pytest tests/unit tests/integration -v
```

No external dependencies required - uses Python standard library only!

## Project Structure

```
mairu-cli/
├── src/                    # Source code
│   ├── builtins/          # Built-in commands
│   ├── display/           # Display system
│   ├── interceptor.py     # Pattern matching
│   └── main.py            # Entry point
├── data/                   # Data files (JSON, ASCII art)
├── tests/                  # Test files
├── docs/                   # Documentation
└── .kiro/                  # Kiro spec files
```

## Questions or Need Help?

- **Open an issue** for questions or discussions
- **Check existing issues** before creating new ones
- **Read the documentation** in the `docs/` directory

## Code of Conduct

Be respectful, inclusive, and constructive. We want MairuCLI to be a welcoming project for everyone.

## License

By contributing, you agree that your contributions will be licensed under the Apache License 2.0.

---

**Thank you for helping make CLI safety education fun and accessible! 🎃**
