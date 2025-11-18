# Test Organization Standards

## Test Structure Rules

When creating or modifying tests, ALWAYS follow this structure:

### Directory Organization

```
tests/
├── unit/              # Component-level tests
│   ├── test_<module>.py
│   └── display/
│       └── test_<component>.py
├── integration/       # Feature-level tests
│   └── test_<feature>.py
└── manual/           # Human verification tests
    └── <descriptive_name>.py
```

### Naming Convention

**Unit Tests:**
- Format: `test_<module_name>.py`
- Location: `tests/unit/` or `tests/unit/<submodule>/`
- Example: `src/display/ascii_renderer.py` → `tests/unit/display/test_ascii_renderer.py`

**Integration Tests:**
- Format: `test_<feature_name>.py`
- Location: `tests/integration/`
- Example: Dangerous command flow → `tests/integration/test_dangerous_commands.py`

**Manual Tests:**
- Format: `<descriptive_name>.py` or `.md`
- Location: `tests/manual/`
- Example: `manual_test_plan.md`, `demo_session.py`

### When to Create Tests

**When adding new source module:**
1. Create corresponding unit test file
2. Follow naming convention: `src/foo.py` → `tests/unit/test_foo.py`
3. Use template from TEST_STRUCTURE.md

**When adding new feature:**
1. Create integration test file
2. Test end-to-end flow
3. Minimal mocking

**When modifying existing code:**
1. Update corresponding unit test
2. Run integration tests to verify no breakage

### Test File Template

```python
"""
Unit tests for src/<path>/<module>.py
"""

import pytest
from src.<path>.<module> import <Class>


class Test<Class>:
    """Test suite for <Class>."""

    def test_<method>_<scenario>(self):
        """Test <method> when <scenario>."""
        # Arrange
        # Act
        # Assert
        pass
```

### Important Rules

1. **One test file per source module** (for unit tests)
2. **Clear mapping** between source and test files
3. **Use appropriate directory** (unit/integration/manual)
4. **Follow naming convention** strictly
5. **Include docstrings** explaining what is being tested

### Reference

See `tests/TEST_STRUCTURE.md` for detailed design and rationale.
