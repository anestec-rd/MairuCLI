# MairuCLI - Kiro Agent Hooks Guide

**Last Updated:** 2025-11-23 (Day 7)

---

## Overview

This document describes the Kiro Agent Hooks configured for MairuCLI. Hooks automate testing workflows by triggering agent actions when specific files are edited.

**Location:** `.kiro/hooks/`

---

## Registered Hooks

### 1. Test System Protection

**File:** `.kiro/hooks/test-system-protection.kiro.hook`

**Purpose:** Run system directory protection integration tests when related source files are modified.

**Current Status:** ⚠️ **NEEDS FIX** - Currently triggers on ALL file edits (empty pattern)

**Current Configuration:**
```json
{
  "enabled": true,
  "name": "Test System Protection",
  "description": "Run system directory protection tests only",
  "when": {
    "type": "fileEdited",
    "patterns": [""]  // ⚠️ PROBLEM: Empty pattern = triggers on everything
  },
  "then": {
    "type": "askAgent",
    "prompt": "Execute: python tests/integration/test_system_protection.py"
  }
}
```

**Problem:**
- Empty pattern `[""]` matches ALL file edits
- Hook executes on every file change (docs, tests, source, etc.)
- Causes unnecessary test runs

**Recommended Fix:**
```json
{
  "enabled": true,
  "name": "Test System Protection",
  "description": "Run system protection tests when related source files are modified",
  "when": {
    "type": "fileEdited",
    "patterns": [
      "src/path_resolver.py",
      "src/command_parser.py",
      "src/interceptor.py",
      "src/display/system_protection_warning.py",
      "src/main.py"
    ]
  },
  "then": {
    "type": "askAgent",
    "prompt": "Execute the following command and report the results: python tests/integration/test_system_protection.py. If all tests pass, respond with \"✅ System protection tests passed!\". If any tests fail, respond with \"❌ System protection tests failed. Check the output above.\" and include details about which tests failed."
  }
}
```

**Trigger Conditions (After Fix):**
- ✅ `src/path_resolver.py` edited → Run test
- ✅ `src/command_parser.py` edited → Run test
- ✅ `src/interceptor.py` edited → Run test
- ✅ `src/display/system_protection_warning.py` edited → Run test
- ✅ `src/main.py` edited → Run test
- ❌ Documentation files edited → No test
- ❌ Other source files edited → No test

**Related Files:**
- Implementation: `src/path_resolver.py`, `src/command_parser.py`, `src/interceptor.py`, `src/display/system_protection_warning.py`, `src/main.py`
- Tests: `tests/integration/test_system_protection.py`

---

### 2. Run Unit Tests

**File:** `.kiro/hooks/run-unit-tests.kiro.hook`

**Purpose:** Run all unit tests when unit test files are modified.

**Status:** ✅ Working correctly

**Configuration:**
```json
{
  "enabled": true,
  "name": "Run Unit Tests",
  "description": "Run all unit tests with pytest and report the results",
  "when": {
    "type": "fileEdited",
    "patterns": [
      "tests/unit/**/*.py"
    ]
  },
  "then": {
    "type": "askAgent",
    "prompt": "Execute: python -m pytest tests/unit/ -v"
  }
}
```

**Trigger Conditions:**
- ✅ Any file in `tests/unit/` edited → Run all unit tests
- ✅ `tests/unit/test_interceptor.py` edited → Run all unit tests
- ✅ `tests/unit/display/test_achievements.py` edited → Run all unit tests
- ❌ Source files edited → No test (by design)
- ❌ Integration tests edited → No test

**Behavior:**
- Runs ALL unit tests (not just the edited file)
- Reports pass/fail status
- Shows detailed output on failure

**Use Case:**
- Verify unit test changes don't break other tests
- Quick feedback when writing/modifying unit tests

---

### 3. Run Integration Tests

**File:** `.kiro/hooks/run-integration-tests.kiro.hook`

**Purpose:** Run specific integration tests when those test files are modified.

**Status:** ✅ Working correctly

**Configuration:**
```json
{
  "enabled": true,
  "name": "Run Integration Tests",
  "description": "Run all integration tests including system protection",
  "when": {
    "type": "fileEdited",
    "patterns": [
      "tests/integration/test_system_protection.py",
      "tests/integration/test_all_features.py"
    ]
  },
  "then": {
    "type": "askAgent",
    "prompt": "Execute: python tests/integration/test_system_protection.py && python tests/integration/test_all_features.py"
  }
}
```

**Trigger Conditions:**
- ✅ `tests/integration/test_system_protection.py` edited → Run both tests
- ✅ `tests/integration/test_all_features.py` edited → Run both tests
- ❌ Other integration tests edited → No test
- ❌ Source files edited → No test (by design)

**Behavior:**
- Runs BOTH specified integration tests
- Reports pass/fail status
- Shows detailed output on failure

**Use Case:**
- Verify integration test changes work correctly
- Ensure test modifications don't break related tests

---

### 4. Auto-test on Save

**File:** `.kiro/hooks/auto-test-on-save.kiro.hook`

**Purpose:** Automatically run unit tests when source files in `src/` are modified.

**Status:** ✅ Working correctly

**Configuration:**
```json
{
  "enabled": true,
  "name": "Auto-test on Save",
  "description": "Automatically run unit tests when saving Python files in src/ directory",
  "when": {
    "type": "fileEdited",
    "patterns": [
      "src/**/*.py"
    ]
  },
  "then": {
    "type": "askAgent",
    "prompt": "Execute: python -m pytest tests/unit/ -v --tb=short. Only report if tests fail. If all tests pass, just say \"✅ Tests passed\"."
  }
}
```

**Trigger Conditions:**
- ✅ Any Python file in `src/` edited → Run unit tests
- ✅ `src/main.py` edited → Run unit tests
- ✅ `src/display/achievements.py` edited → Run unit tests
- ❌ Test files edited → No test
- ❌ Documentation edited → No test

**Behavior:**
- Runs ALL unit tests
- Brief output if tests pass (just "✅ Tests passed")
- Detailed output if tests fail
- Uses `--tb=short` for concise error messages

**Use Case:**
- Continuous feedback during development
- Catch regressions immediately after code changes
- TDD (Test-Driven Development) workflow

---

## Hook Interaction Matrix

| File Edited | Test System Protection | Run Unit Tests | Run Integration Tests | Auto-test on Save |
|-------------|------------------------|----------------|----------------------|-------------------|
| `src/path_resolver.py` | ✅ (after fix) | ❌ | ❌ | ✅ |
| `src/interceptor.py` | ✅ (after fix) | ❌ | ❌ | ✅ |
| `src/display/achievements.py` | ❌ | ❌ | ❌ | ✅ |
| `tests/unit/test_interceptor.py` | ❌ | ✅ | ❌ | ❌ |
| `tests/integration/test_system_protection.py` | ❌ | ❌ | ✅ | ❌ |
| `docs/README.md` | ⚠️ (currently yes, should be no) | ❌ | ❌ | ❌ |
| `TODO.md` | ⚠️ (currently yes, should be no) | ❌ | ❌ | ❌ |

**Legend:**
- ✅ Hook triggers
- ❌ Hook does not trigger
- ⚠️ Unintended behavior (needs fix)

---

## Current Issues

### Issue 1: Test System Protection Triggers on Everything

**Problem:**
- Empty pattern `[""]` in `test-system-protection.kiro.hook`
- Triggers on ALL file edits (docs, tests, source, everything)
- Causes unnecessary test runs

**Impact:**
- Every file edit triggers system protection tests
- Slows down workflow
- Confusing behavior

**Solution:**
- Update pattern to specific source files (see recommended fix above)
- Or disable the hook if manual execution is preferred

**Priority:** High (affects user experience)

---

## Best Practices

### 1. Specific Patterns

✅ **Good:**
```json
"patterns": [
  "src/path_resolver.py",
  "src/command_parser.py"
]
```

❌ **Bad:**
```json
"patterns": [""]  // Matches everything!
```

### 2. Related Files Only

Trigger tests only for files that affect the test:
- System protection tests → System protection source files
- Unit tests → Unit test files
- Integration tests → Integration test files

### 3. Avoid Overlap

Be careful with overlapping patterns:
- `src/**/*.py` (Auto-test on Save) already covers most source files
- Don't add redundant hooks for the same files

### 4. Test Scope

- **Unit test hooks:** Run all unit tests (fast, comprehensive)
- **Integration test hooks:** Run specific integration tests (slower, targeted)
- **Feature-specific hooks:** Run tests for that feature only

---

## Disabling Hooks

To disable a hook without deleting it:

1. Open the hook file (e.g., `.kiro/hooks/test-system-protection.kiro.hook`)
2. Change `"enabled": true` to `"enabled": false`
3. Save the file

The hook will remain registered but won't trigger.

---

## Manual Execution

Even with hooks disabled, you can manually trigger them:
1. Open Kiro UI
2. Navigate to Agent Hooks panel
3. Click the hook you want to run
4. Hook executes immediately

---

## Recommended Actions

### Immediate (Day 7)

1. **Fix Test System Protection Hook**
   - Update pattern to specific source files
   - Test that it only triggers on relevant files
   - Verify it doesn't trigger on docs/tests

2. **Document Hook Behavior**
   - ✅ This document created
   - Share with team/users
   - Update as hooks evolve

### Future Enhancements

1. **Add More Granular Hooks**
   - Hook for display module tests when display files change
   - Hook for interceptor tests when interceptor changes
   - Hook for achievement tests when achievement code changes

2. **Optimize Test Execution**
   - Run only affected tests (not all tests)
   - Use pytest markers to run specific test categories
   - Add timeout limits for long-running tests

3. **Add Notification Hooks**
   - Hook to update CHANGELOG.md when features added
   - Hook to run linter when Python files change
   - Hook to check for magic numbers when code changes

---

## Testing Hooks

To test if a hook works correctly:

1. **Edit a file that should trigger the hook**
   - Example: Edit `src/path_resolver.py` for system protection hook

2. **Observe Kiro's response**
   - Hook should trigger automatically
   - Agent should execute the specified command
   - Results should be reported

3. **Edit a file that should NOT trigger the hook**
   - Example: Edit `README.md` for system protection hook
   - Hook should NOT trigger
   - No test execution

4. **Check the interaction matrix** (see above)
   - Verify behavior matches expected triggers

---

## Troubleshooting

### Hook Triggers Too Often

**Symptom:** Hook runs on every file edit

**Cause:** Pattern is too broad (e.g., `[""]` or `["**/*"]`)

**Fix:** Make pattern more specific

### Hook Never Triggers

**Symptom:** Hook doesn't run even when expected files are edited

**Cause:** Pattern doesn't match the file path

**Fix:** Check pattern syntax, verify file path matches

### Hook Triggers on Wrong Files

**Symptom:** Hook runs on unexpected files

**Cause:** Pattern is too broad or uses wildcards incorrectly

**Fix:** Test pattern with specific file paths

---

## Summary

**Current Status:**
- ✅ 3 hooks working correctly
- ⚠️ 1 hook needs fix (Test System Protection)

**Next Steps:**
1. Fix Test System Protection hook pattern
2. Test all hooks with various file edits
3. Document any additional hooks added in future

**Benefits:**
- Automated testing on relevant changes
- Faster feedback during development
- Reduced manual test execution

---

**For questions or issues with hooks, refer to Kiro documentation or this guide.**
