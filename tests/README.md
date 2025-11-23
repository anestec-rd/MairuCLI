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

## Test Types - When to Use Which

### Unit Tests (`tests/unit/`)

**What they test:**
- Individual functions and classes
- Pattern matching logic
- Path resolution algorithms
- Command parsing
- Data validation

**What they DON'T test:**
- Visual appearance
- User experience
- Component interactions
- Timing and "feel"

**When to run:**
- After every code change
- Before committing
- Automatically via hooks
- Fast feedback (< 10 seconds)

**Example:**
```bash
pytest tests/unit/test_interceptor.py -v
```

---

### Integration Tests (`tests/integration/`)

**What they test:**
- Complete feature flows
- Component interactions
- End-to-end scenarios
- System protection logic
- Multi-step processes

**What they DON'T test:**
- Visual quality
- Message clarity
- User experience
- Performance perception

**When to run:**
- After feature completion
- Before releases
- When modifying core components
- Moderate speed (< 60 seconds)

**Example:**
```bash
pytest tests/integration/test_system_protection.py -v
```

---

### Manual Tests (`tests/manual/`)

**What they test:**
- ✅ Visual appearance (ASCII art, colors, formatting)
- ✅ User experience (message clarity, helpfulness)
- ✅ Timing and "feel" (dramatic pauses, flow)
- ✅ Educational value (are messages understandable?)
- ✅ Real user scenarios (how it feels to use)

**What they DON'T test:**
- Logic correctness (that's unit tests)
- Code coverage (that's automated tests)

**When to run:**
- Before demo/presentation
- After visual changes
- Before releases
- After refactoring display code

**How to run:**
See `tests/manual/README.md` for detailed instructions.

---

## Test Coverage Comparison

| Test Aspect | Unit | Integration | Manual |
|-------------|------|-------------|--------|
| Pattern detection | ✅ | ✅ | ❌ |
| Path resolution | ✅ | ✅ | ❌ |
| Command parsing | ✅ | ✅ | ❌ |
| Feature flows | ❌ | ✅ | ✅ |
| Visual quality | ❌ | ❌ | ✅ |
| Message clarity | ❌ | ❌ | ✅ |
| User experience | ❌ | ❌ | ✅ |
| Timing/feel | ❌ | ❌ | ✅ |
| Performance | ✅ | ✅ | ✅ |

**Key Insight:** All three test types are necessary for comprehensive quality assurance.

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

