# Test Structure Design for MairuCLI

**Purpose:** Maintainable test organization that clearly maps tests to components

**Last Updated:** 2025-11-18

---

## Test Organization Philosophy

### Problems with Current Structure
- Multiple test files with unclear purposes
- No clear mapping between test files and source modules
- Difficult to know which tests to run when modifying specific components
- Risk of duplicate or missing test coverage

### Solution: Component-Based Test Organization

Each source module should have a corresponding test file with clear naming:

```
src/module.py → tests/test_module.py
```

---

## Proposed Test Structure

### Unit Tests (Component-Level)

```
tests/
├── unit/
│   ├── __init__.py
│   ├── test_interceptor.py          # Tests for src/interceptor.py
│   ├── test_builtins.py             # Tests for src/builtins.py
│   └── display/
│       ├── __init__.py
│       ├── test_ascii_renderer.py   # Tests for src/display/ascii_renderer.py
│       ├── test_content_loader.py   # Tests for src/display/content_loader.py
│       ├── test_message_formatter.py # Tests for src/display/message_formatter.py
│       ├── test_statistics.py       # Tests for src/display/statistics.py
│       ├── test_achievements.py     # Tests for src/display/achievements.py
│       └── test_warning_components.py # Tests for src/display/warning_components.py
```

### Integration Tests (Feature-Level)

```
tests/
├── integration/
│   ├── __init__.py
│   ├── test_dangerous_commands.py   # End-to-end dangerous command flow
│   ├── test_typo_detection.py       # End-to-end typo detection flow
│   ├── test_achievements_flow.py    # Achievement unlock scenarios
│   └── test_repeat_warnings.py      # Repeat command detection flow
```

### Manual Tests (Human Verification)

```
tests/
├── manual/
│   ├── manual_test_plan.md          # Checklist for manual testing
│   ├── demo_session.py              # Demo script for presentations
│   └── test_dramatic_timing.py      # Visual timing verification
```

---

## Test File Naming Convention

### Unit Tests
**Format:** `test_<module_name>.py`

**Examples:**
- `test_interceptor.py` → Tests `src/interceptor.py`
- `test_ascii_renderer.py` → Tests `src/display/ascii_renderer.py`

**Content:**
- Test individual functions/methods
- Mock dependencies
- Fast execution
- No external dependencies

### Integration Tests
**Format:** `test_<feature_name>.py`

**Examples:**
- `test_dangerous_commands.py` → Tests complete dangerous command flow
- `test_typo_detection.py` → Tests complete typo detection flow

**Content:**
- Test multiple components working together
- Minimal mocking
- Test realistic scenarios
- May have external dependencies (files, etc.)

### Manual Tests
**Format:** `<descriptive_name>.py` or `.md`

**Examples:**
- `manual_test_plan.md` → Human-readable checklist
- `demo_session.py` → Interactive demonstration

**Content:**
- Require human observation
- Visual/timing verification
- Demo scenarios

---

## Test Coverage Map

### Current Components → Test Files

| Source Module | Unit Test | Integration Test | Status |
|---------------|-----------|------------------|--------|
| `src/main.py` | N/A (entry point) | `test_all_features.py` | ✅ Complete |
| `src/interceptor.py` | `test_interceptor.py` | `test_all_features.py` | ✅ Complete |
| `src/command_parser.py` | `test_command_parser.py` | `test_all_features.py` | ✅ Complete |
| `src/path_resolver.py` | `test_path_resolver.py` | `test_system_protection.py` | ✅ Complete |
| `src/builtins/*` | `test_builtins_*.py` | `test_builtin_redirection.py` | ✅ Complete |
| `src/display/achievements.py` | `display/test_achievements.py` | `test_all_features.py` | ✅ Complete |
| `src/display/statistics.py` | `display/test_statistics.py` | `test_all_features.py` | ✅ Complete |
| `src/display/educational_breakdown.py` | `display/test_educational_breakdown.py` | `test_educational_breakdown_flow.py` | ✅ Complete |
| `src/display/breakdown_formatter.py` | `display/test_breakdown_formatter.py` | `test_educational_breakdown_flow.py` | ✅ Complete |
| `src/display/content_loader.py` | `test_content_loader_variations.py` | N/A | ✅ Complete |

---

## Migration Plan

### Phase 1: Organize Existing Tests ✅ **COMPLETE** (Day 3)
1. ✅ Created this design document
2. ✅ Created directory structure (`unit/`, `integration/`, `manual/`)
3. ✅ Moved existing tests to appropriate directories
4. ✅ Updated imports in moved files

### Phase 2: Fill Gaps ✅ **COMPLETE** (Day 4-11)
1. ✅ Created unit tests for all components (274 tests)
2. ✅ Created integration tests for all features (47 tests)
3. ✅ Ensured each component has corresponding test
4. ✅ Achieved 100% test pass rate

### Phase 3: Continuous Maintenance ✅ **ONGOING**
1. ✅ When adding new component → Add corresponding test file
2. ✅ When modifying component → Update corresponding test file
3. ✅ Keep TEST_STRUCTURE.md updated
4. ✅ Maintain 100% pass rate

---

## Running Tests

### Run All Tests
```bash
pytest tests/
```

### Run Unit Tests Only
```bash
pytest tests/unit/
```

### Run Integration Tests Only
```bash
pytest tests/integration/
```

### Run Specific Component Tests
```bash
pytest tests/unit/test_interceptor.py
pytest tests/unit/display/test_ascii_renderer.py
```

### Run Tests for Modified Component
```bash
# Modified src/display/ascii_renderer.py
pytest tests/unit/display/test_ascii_renderer.py
pytest tests/integration/  # Run integration tests to verify no breakage
```

---

## Test Template

### Unit Test Template

```python
"""
Unit tests for src/<module_path>/<module_name>.py

Tests individual functions/methods in isolation with mocked dependencies.
"""

import pytest
from unittest.mock import Mock, patch
from src.<module_path>.<module_name> import <ClassName>


class Test<ClassName>:
    """Test suite for <ClassName>."""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        # Initialize test objects
        pass

    def test_<method_name>_<scenario>(self):
        """Test <method_name> when <scenario>."""
        # Arrange
        # Act
        # Assert
        pass

    def test_<method_name>_error_handling(self):
        """Test <method_name> handles errors gracefully."""
        # Arrange
        # Act
        # Assert
        pass
```

### Integration Test Template

```python
"""
Integration tests for <feature_name> feature.

Tests multiple components working together in realistic scenarios.
"""

import pytest
from src.main import <relevant_functions>


class Test<FeatureName>Flow:
    """Test suite for <feature_name> end-to-end flow."""

    def setup_method(self):
        """Set up test environment before each test."""
        # Initialize components
        pass

    def test_<scenario>_flow(self):
        """Test complete flow for <scenario>."""
        # Arrange
        # Act
        # Assert
        pass
```

---

## Benefits of This Structure

### 1. Clear Mapping
- Easy to find tests for specific component
- Easy to know which tests to run when modifying code

### 2. Maintainability
- New components automatically get corresponding test file
- No confusion about where to add new tests

### 3. Scalability
- Structure supports project growth
- Easy to add new test categories

### 4. Discoverability
- New team members can quickly understand test organization
- Clear separation of unit vs integration vs manual tests

### 5. CI/CD Friendly
- Easy to run different test suites in different stages
- Fast unit tests in pre-commit hooks
- Slower integration tests in CI pipeline

---

## Notes

### Current State (Day 14)
- ✅ Test structure fully implemented
- ✅ 322 automated tests, 100% pass rate
- ✅ Comprehensive coverage across all components
- ✅ Cross-platform verified (Windows/Linux/macOS)

### Achievements
- **Day 3:** Test structure designed
- **Day 4-11:** Tests implemented incrementally
- **Day 11:** System protection tests added (73 tests)
- **Day 14:** Test documentation updated

### Related Documents
- `tests/README.md` - Test suite overview and usage
- `tests/manual/README.md` - Manual testing guide
- `tests/manual/manual_test_plan.md` - Complete testing checklist
- `.kiro/specs/*/tasks.md` - Spec-driven test implementation

---

**Status:** ✅ **COMPLETE** - Fully Implemented and Maintained
**Test Coverage:** 322 tests, 100% pass rate
**Last Updated:** 2025-11-30 (Day 14)

