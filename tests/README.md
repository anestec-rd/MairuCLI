# MairuCLI Test Suite

## Test Organization

This test suite is organized by test type for maintainability and clarity.

### Directory Structure

```
tests/
├── unit/                    # Unit tests (component-level)
│   ├── display/            # Display module unit tests
│   └── ...                 # Other component tests
├── integration/            # Integration tests (feature-level)
│   ├── test_dangerous.py   # Dangerous command detection
│   ├── test_repeat_warning.py # Repeat warning flow
│   └── ...                 # Other feature tests
├── manual/                 # Manual tests (human verification)
│   ├── manual_test_plan.md # Testing checklist
│   ├── demo_session.py     # Demo script
│   └── test_dramatic_timing.py # Timing verification
└── TEST_STRUCTURE.md       # Detailed test organization design
```

## Running Tests

### All Tests
```bash
pytest tests/
```

### Unit Tests Only
```bash
pytest tests/unit/
```

### Integration Tests Only
```bash
pytest tests/integration/
```

### Specific Test File
```bash
pytest tests/integration/test_dangerous.py
```

## Test Types

### Unit Tests (`tests/unit/`)
- Test individual components in isolation
- Fast execution
- Mocked dependencies
- One test file per source module

### Integration Tests (`tests/integration/`)
- Test multiple components working together
- Realistic scenarios
- Minimal mocking
- One test file per feature

### Manual Tests (`tests/manual/`)
- Require human observation
- Visual/timing verification
- Demo scenarios
- Not automated

## Adding New Tests

### When Adding New Component
1. Create corresponding unit test: `tests/unit/test_<component>.py`
2. Follow template in `TEST_STRUCTURE.md`

### When Adding New Feature
1. Create integration test: `tests/integration/test_<feature>.py`
2. Test end-to-end flow

### When Modifying Component
1. Update corresponding unit test
2. Run integration tests to verify no breakage

## Documentation

See `TEST_STRUCTURE.md` for:
- Detailed test organization philosophy
- Test coverage map
- Migration plan
- Test templates
- Best practices

## Quick Test Execution

### Pattern Detection Test (Day 5 - Automated)
```bash
python tests/unit/test_interceptor.py
```

**What it tests:**
- All 11 dangerous patterns
- All 4 caution patterns
- All 2 typo patterns
- Safe command pass-through
- Bug fix verification (Issue #2)

**Expected:** 35 tests, 100% pass rate, <5 seconds

**Report:** See [docs/reports/DAY5_TEST_REPORT.md](../docs/reports/DAY5_TEST_REPORT.md)

## Current Status

**Day 5 (2025-11-21):**
- ✅ Automated pattern detection test (`test_interceptor.py`)
- ✅ 35 test cases, 100% pass rate
- ✅ Bug fix verified (Issue #2)
- ✅ Test structure compliance

**Day 3 (2025-11-18):**
- ✅ Test structure designed
- ✅ Directories created
- ✅ Existing tests organized

**Next Steps (Future):**
- Create unit tests for display components (if time permits)
- Add missing integration tests
- Continuous maintenance as project grows

