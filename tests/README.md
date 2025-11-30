# MairuCLI Test Suite

## Overview

MairuCLI has **comprehensive test coverage** with **322 automated tests** across unit and integration testing.

| Test Type | Count | Purpose |
|-----------|-------|---------|
| **Unit Tests** | ~275 | Component-level testing |
| **Integration Tests** | ~47 | Feature-level testing |
| **Manual Tests** | N/A | Human verification |
| **Total Automated** | **322** | ✅ **All Passing** |

**Note:** Test counts are approximate and may vary as tests are added or modified. Run `pytest tests/unit tests/integration -v` for exact count.

---

## Test Organization

### Directory Structure

```
tests/
├── unit/                    # Unit tests (component-level)
│   ├── display/            # Display module unit tests
│   │   ├── test_achievements.py
│   │   ├── test_breakdown_formatter.py
│   │   ├── test_educational_breakdown.py
│   │   └── test_statistics.py
│   ├── test_builtins_echo.py
│   ├── test_builtins_search.py
│   ├── test_command_interceptor.py
│   ├── test_command_parser.py
│   ├── test_command_parser_redirection.py
│   ├── test_content_loader_variations.py
│   ├── test_help_generator.py
│   ├── test_interceptor.py
│   ├── test_mkfs_patterns.py
│   ├── test_path_resolver.py
│   ├── test_pattern_compiler.py
│   ├── test_pattern_loader.py
│   └── test_system_directory_check.py
├── integration/            # Integration tests (feature-level)
│   ├── test_all_features.py
│   ├── test_builtin_redirection.py
│   ├── test_educational_breakdown_flow.py
│   ├── test_help.py
│   ├── test_repeat_warning.py
│   └── test_system_protection.py
├── manual/                 # Manual tests (human verification)
│   ├── README.md           # Manual testing guide
│   ├── manual_test_plan.md # Complete testing checklist
│   ├── system-protection-checklist.md
│   ├── demo_session.py     # Demo script
│   └── test_*.py           # Various manual test scripts
├── README.md               # This file
└── TEST_STRUCTURE.md       # Test organization design
```

---

## Running Tests

### Quick Start

```bash
# Run all automated tests (unit + integration)
python -m pytest tests/unit tests/integration -v

# Expected output:
# ======================== 322 passed, 8 skipped in X.XXs ========================
```

**Note:** We exclude `tests/manual/` from automated runs as those require human verification.

### By Test Type

```bash
# Unit tests only (~275 tests, fast: <10 seconds)
python -m pytest tests/unit/ -v

# Integration tests only (~47 tests, moderate: <60 seconds)
python -m pytest tests/integration/ -v

# Specific test file
python -m pytest tests/unit/test_interceptor.py -v
```

### With Coverage Report (Optional)

```bash
# Install pytest-cov if not already installed
pip install pytest-cov

# Generate HTML coverage report
python -m pytest tests/unit tests/integration --cov=src --cov-report=html

# View report: open htmlcov/index.html
```

**Note:** Coverage measurement is optional. We focus on functional correctness rather than coverage metrics.

---

## Test Types Explained

### Unit Tests (`tests/unit/`)

**What they test:**
- ✅ Individual functions and classes
- ✅ Pattern matching logic
- ✅ Path resolution algorithms
- ✅ Command parsing
- ✅ Data validation
- ✅ Component behavior in isolation

**What they DON'T test:**
- ❌ Visual appearance
- ❌ User experience
- ❌ Component interactions (that's integration tests)
- ❌ Timing and "feel" (that's manual tests)

**When to run:**
- After every code change
- Before committing
- Automatically via hooks
- **Speed:** Fast (<10 seconds)

**Example:**
```bash
# Test dangerous command pattern detection
python -m pytest tests/unit/test_interceptor.py -v

# Test path resolution for system protection
python -m pytest tests/unit/test_path_resolver.py -v

# Test educational breakdown formatting
python -m pytest tests/unit/display/test_breakdown_formatter.py -v
```

---

### Integration Tests (`tests/integration/`)

**What they test:**
- ✅ Complete feature flows
- ✅ Component interactions
- ✅ End-to-end scenarios
- ✅ System protection logic
- ✅ Multi-step processes
- ✅ Real-world usage patterns

**What they DON'T test:**
- ❌ Visual quality (that's manual tests)
- ❌ Message clarity (that's manual tests)
- ❌ User experience perception
- ❌ Performance perception

**When to run:**
- After feature completion
- Before releases
- When modifying core components
- **Speed:** Moderate (<60 seconds)

**Example:**
```bash
# Test complete dangerous command flow
python -m pytest tests/integration/test_all_features.py -v

# Test system directory protection across platforms
python -m pytest tests/integration/test_system_protection.py -v

# Test educational breakdown interaction
python -m pytest tests/integration/test_educational_breakdown_flow.py -v
```

---

### Manual Tests (`tests/manual/`)

**What they test:**
- ✅ Visual appearance (ASCII art, colors, formatting)
- ✅ User experience (message clarity, helpfulness)
- ✅ Timing and "feel" (dramatic pauses, flow)
- ✅ Educational value (are messages understandable?)
- ✅ Real user scenarios (how it feels to use)
- ✅ Cross-platform visual consistency

**What they DON'T test:**
- ❌ Logic correctness (that's unit tests)
- ❌ Code coverage (that's automated tests)

**When to run:**
- Before demo/presentation
- After visual changes
- Before releases
- After refactoring display code

**How to run:**
See `tests/manual/README.md` for detailed instructions.

**Quick manual test:**
```bash
# Start MairuCLI
python -m src.main

# Try these commands:
mairu> help
mairu> rm -rf /                    # Should block with warning
mairu> rm C:\Windows\test.txt      # Should block (Windows)
mairu> rm /etc/test.conf           # Should block (Linux)
mairu> stats
mairu> exit
```

---

## Test Coverage Map

### What Each Test File Tests

#### Unit Tests

| Test File | Tests | Component |
|-----------|-------|-----------|
| `test_interceptor.py` | Pattern detection (dangerous, caution, typo) | `src/interceptor.py` |
| `test_command_parser.py` | Command parsing, argument extraction | `src/command_parser.py` |
| `test_command_parser_redirection.py` | Redirection target extraction | `src/command_parser.py` |
| `test_path_resolver.py` | Path resolution, expansion, normalization | `src/path_resolver.py` |
| `test_system_directory_check.py` | System directory protection logic | `src/interceptor.py` |
| `test_mkfs_patterns.py` | mkfs command pattern detection | `src/interceptor.py` |
| `test_pattern_compiler.py` | Pattern compilation and matching | `src/interceptor.py` |
| `test_pattern_loader.py` | Pattern loading from JSON | `src/interceptor.py` |
| `test_builtins_echo.py` | Echo command with variable expansion | `src/builtins/shell_utils.py` |
| `test_builtins_search.py` | Search commands (find, grep, which) | `src/builtins/search.py` |
| `test_content_loader_variations.py` | Warning variation loading | `src/display/content_loader.py` |
| `test_help_generator.py` | Help message generation | `src/builtins/mairu_commands.py` |
| `display/test_achievements.py` | Achievement tracking and unlocking | `src/display/achievements.py` |
| `display/test_statistics.py` | Statistics tracking | `src/display/statistics.py` |
| `display/test_educational_breakdown.py` | Educational breakdown orchestration | `src/display/educational_breakdown.py` |
| `display/test_breakdown_formatter.py` | Educational content formatting | `src/display/breakdown_formatter.py` |

#### Integration Tests

| Test File | Tests | Features |
|-----------|-------|----------|
| `test_all_features.py` | Complete feature flows | All major features |
| `test_builtin_redirection.py` | Builtin command redirection blocking | Issue #4 fix |
| `test_educational_breakdown_flow.py` | Educational breakdown interaction | Educational system |
| `test_help.py` | Help command display | Help system |
| `test_repeat_warning.py` | Repeat warning escalation | Repeat detection |
| `test_system_protection.py` | System directory protection | Cross-platform protection |

---

## Test Coverage Comparison

| Test Aspect | Unit | Integration | Manual |
|-------------|------|-------------|--------|
| Pattern detection | ✅ | ✅ | ❌ |
| Path resolution | ✅ | ✅ | ❌ |
| Command parsing | ✅ | ✅ | ❌ |
| System protection | ✅ | ✅ | ✅ |
| Feature flows | ❌ | ✅ | ✅ |
| Visual quality | ❌ | ❌ | ✅ |
| Message clarity | ❌ | ❌ | ✅ |
| User experience | ❌ | ❌ | ✅ |
| Timing/feel | ❌ | ❌ | ✅ |
| Educational value | ❌ | ❌ | ✅ |

**Key Insight:** All three test types are necessary for comprehensive quality assurance.

---

## Adding New Tests

### When Adding New Component

1. **Create unit test:** `tests/unit/test_<component>.py`
2. **Follow naming convention:** Match source file name
3. **Use template:** See `TEST_STRUCTURE.md`

**Example:**
```python
# New component: src/new_feature.py
# Create test: tests/unit/test_new_feature.py

"""Unit tests for src/new_feature.py"""

import pytest
from src.new_feature import NewFeature

class TestNewFeature:
    def test_basic_functionality(self):
        # Test implementation
        pass
```

### When Adding New Feature

1. **Create integration test:** `tests/integration/test_<feature>.py`
2. **Test end-to-end flow**
3. **Minimal mocking**

**Example:**
```python
# New feature: User profiles
# Create test: tests/integration/test_user_profiles.py

"""Integration tests for user profile feature"""

def test_profile_creation_flow():
    # Test complete flow
    pass
```

### When Modifying Component

1. **Update corresponding unit test**
2. **Run integration tests** to verify no breakage
3. **Run manual tests** if visual changes

---

## Test Execution Tips

### Fast Feedback Loop

```bash
# Run only tests for modified component
python -m pytest tests/unit/test_interceptor.py -v

# Run with fail-fast (stop on first failure)
python -m pytest tests/ -x

# Run last failed tests only
python -m pytest tests/ --lf
```

### Debugging Failed Tests

```bash
# Show print statements
python -m pytest tests/ -v -s

# Show full error traceback
python -m pytest tests/ -v --tb=long

# Run specific test function
python -m pytest tests/unit/test_interceptor.py::test_rm_dangerous -v
```

### Performance Testing

```bash
# Show slowest 10 tests
python -m pytest tests/ --durations=10

# Profile test execution
python -m pytest tests/ --profile
```

---

## Current Test Status

**Last Updated:** 2025-11-30 (Day 14)

**Test Statistics:**
- ✅ 322 automated tests (unit + integration)
- ✅ All tests passing
- ✅ 8 tests skipped (platform-specific)
- ✅ Cross-platform verified (Windows/Linux/macOS)

**Recent Additions:**
- Day 11: System directory protection tests (~73 tests)
- Day 11: Builtin redirection tests (~14 tests)
- Day 10: Educational breakdown tests (~12 tests)
- Day 9: Educational content tests (~8 tests)
- Day 7: Builtin command tests (~20 tests)

**Test Coverage:**
- Pattern detection: Comprehensive
- Path resolution: Comprehensive
- System protection: Comprehensive
- Educational system: Comprehensive
- Builtin commands: Comprehensive

**Note:** We focus on functional correctness and real-world scenarios rather than coverage metrics.

---

## Documentation

- **TEST_STRUCTURE.md** - Test organization design and philosophy
- **manual/README.md** - Manual testing guide
- **manual/manual_test_plan.md** - Complete manual testing checklist
- **manual/system-protection-checklist.md** - System protection testing

---

## Quick Reference

### Run All Tests
```bash
python -m pytest tests/ -v
```

### Run Fast Tests Only (Unit)
```bash
python -m pytest tests/unit/ -v
```

### Run Before Commit
```bash
python -m pytest tests/ -x  # Stop on first failure
```

### Run Before Release
```bash
python -m pytest tests/ -v --cov=src --cov-report=html
```

### Manual Testing
```bash
python -m src.main
# Follow tests/manual/manual_test_plan.md
```

---

**For detailed test organization design, see `TEST_STRUCTURE.md`**

**For manual testing instructions, see `manual/README.md`**
