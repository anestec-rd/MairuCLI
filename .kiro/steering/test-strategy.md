---
inclusion: always
---

# Test Strategy for MairuCLI

## Purpose

Guide developers (human or AI) to add appropriate tests when adding new features or modifying existing code.

---

## Decision Tree: Which Tests to Add?

### When Adding New Dangerous Pattern

**Example:** Adding `wget malicious-url` detection

**Required Tests:**

1. **Unit Test** (`tests/unit/test_interceptor.py`)
   ```python
   # Add to dangerous_commands list
   ("wget http://malicious.com/script.sh", "wget_malicious"),
   ```
   - ✅ Pattern detects the command
   - ✅ Existing patterns still work
   - ✅ Safe variations are not blocked

2. **Integration Test** (`tests/integration/test_dangerous.py`)
   - ⚠️ Optional if pattern follows existing flow
   - ✅ Required if pattern has unique behavior

3. **Manual Test** (`tests/manual/manual_test_plan.md`)
   - ✅ Add to checklist
   - ✅ Verify ASCII art displays correctly
   - ✅ Verify warning message is clear

**Time Investment:** 5-10 minutes

---

### When Adding New ASCII Art

**Example:** Creating `network_danger.txt` for network-related commands

**Required Tests:**

1. **Unit Test** - ❌ Not needed (no logic change)

2. **Integration Test** - ❌ Not needed (no logic change)

3. **Manual Test** (`tests/manual/manual_test_plan.md`)
   - ✅ Add to visual verification checklist
   - ✅ Test on different terminal sizes
   - ✅ Test on light/dark backgrounds
   - ✅ Verify timing feels natural

**Time Investment:** 2-5 minutes

---

### When Adding New Warning Variation

**Example:** Adding new subtitle to `rm_root` variations

**Required Tests:**

1. **Unit Test** (`tests/unit/test_interceptor.py`)
   - ✅ Verify pattern still detects correctly
   - ⚠️ Usually passes without modification

2. **Integration Test** - ❌ Not needed (display logic unchanged)

3. **Manual Test**
   - ✅ Run command multiple times
   - ✅ Verify new variation appears
   - ✅ Verify variation is appropriate/funny

**Time Investment:** 2-3 minutes

---

### When Adding New Caution Pattern

**Example:** Adding `systemctl stop sshd` detection

**Required Tests:**

1. **Unit Test** (`tests/unit/test_interceptor.py`)
   ```python
   # Add to caution_commands list
   ("systemctl stop sshd", "service_stop"),
   ```
   - ✅ Pattern detects as "caution" level
   - ✅ Existing patterns still work

2. **Integration Test** (`tests/integration/test_caution_flow.py`)
   - ✅ Verify confirmation prompt appears
   - ✅ Verify "y" proceeds, "n" cancels
   - ✅ Verify statistics update correctly

3. **Manual Test**
   - ✅ Test user interaction flow
   - ✅ Verify prompt is clear
   - ✅ Verify considerations are helpful

**Time Investment:** 10-15 minutes

---

### When Adding New Builtin Command

**Example:** Adding `whoami` builtin

**Required Tests:**

1. **Unit Test** (`tests/unit/test_builtins.py`)
   - ✅ Command executes correctly
   - ✅ Returns expected output
   - ✅ Handles errors gracefully

2. **Integration Test** (`tests/integration/test_builtin_commands.py`)
   - ⚠️ Optional if command is simple
   - ✅ Required if command interacts with other systems

3. **Manual Test**
   - ✅ Test in actual REPL
   - ✅ Verify output formatting
   - ✅ Verify help text updated

**Time Investment:** 10-15 minutes

---

### When Adding New Achievement

**Example:** Adding "Speed Demon" achievement (10 commands in 1 minute)

**Required Tests:**

1. **Unit Test** (`tests/unit/display/test_achievements.py`)
   - ✅ Achievement triggers correctly
   - ✅ Conditions are checked properly
   - ✅ No duplicate unlocks

2. **Integration Test** (`tests/integration/test_achievements_flow.py`)
   - ✅ Achievement displays correctly
   - ✅ Statistics update correctly
   - ✅ Multiple achievements don't conflict

3. **Manual Test**
   - ✅ Trigger achievement naturally
   - ✅ Verify message is satisfying
   - ✅ Verify timing feels right

**Time Investment:** 15-20 minutes

---

### When Refactoring Code

**Example:** Splitting a large module into smaller ones

**Required Tests:**

1. **Unit Test**
   - ✅ Create tests for new modules
   - ✅ Verify each module works independently
   - ✅ Run all existing unit tests

2. **Integration Test**
   - ✅ Run all integration tests
   - ✅ Verify module interactions still work
   - ✅ Add tests for new interaction patterns

3. **Manual Test**
   - ✅ Full smoke test
   - ✅ Verify no visual changes (backward compatibility)
   - ✅ Verify performance unchanged

**Time Investment:** 30-60 minutes

---

## Test Addition Checklist

When adding a feature, ask these questions:

### 1. Does it change logic/behavior?
- **Yes** → Add Unit Test
- **No** → Skip Unit Test

### 2. Does it involve multiple modules?
- **Yes** → Add Integration Test
- **No** → Skip Integration Test

### 3. Does it affect visual display or UX?
- **Yes** → Add Manual Test
- **No** → Skip Manual Test

### 4. Is it a critical feature?
- **Yes** → Add all three test types
- **No** → Add minimum required tests

---

## Test Templates

### Unit Test Template (Pattern Detection)

```python
# In tests/unit/test_interceptor.py

# Add to appropriate test section
def test_new_pattern():
    """Test new pattern detection."""
    # Test detection
    level, pattern = check_command("dangerous command")
    assert level == "critical"
    assert pattern == "pattern_name"

    # Test safe variation
    level, pattern = check_command("safe variation")
    assert level == "safe"
```

### Integration Test Template

```python
# In tests/integration/test_<feature>.py

def test_new_feature_flow():
    """Test complete flow for new feature."""
    # Arrange
    # Set up test environment

    # Act
    # Execute feature

    # Assert
    # Verify all components worked together
    pass
```

### Manual Test Template

```markdown
# In tests/manual/manual_test_plan.md

### Test: New Feature Name

**Steps:**
1. Start MairuCLI
2. Execute command: `<command>`
3. Observe behavior

**Expected:**
- [ ] Feature activates correctly
- [ ] Display is clear and readable
- [ ] User experience is smooth

**Notes:**
```

---

## Examples from MairuCLI History

### Example 1: Three-Tier Warning System (Day 4)

**What was added:** Caution-level warnings

**Tests added:**
- ✅ Unit: Added caution pattern tests to `test_interceptor.py`
- ✅ Integration: Created `test_caution_flow.py`
- ✅ Manual: Added caution testing to manual checklist

**Result:** Caught no bugs because tests were comprehensive

---

### Example 2: Display Refactoring (Day 3)

**What was changed:** Split display.py into 7 modules

**Tests added:**
- ✅ Unit: Tests for each new module (optional, deferred)
- ✅ Integration: Ran existing tests to verify no breakage
- ✅ Manual: Full smoke test to verify visual consistency

**Result:** 100% backward compatibility maintained

---

### Example 3: Fork Bomb Pattern (Day 5)

**What was added:** Fork bomb detection pattern

**Tests added:**
- ✅ Unit: Added to `test_interceptor.py`
- ❌ Integration: Not needed (follows existing flow)
- ❌ Manual: Not needed (no visual changes)

**Result:** Caught regex bug immediately (pattern too strict)

---

## Anti-Patterns to Avoid

### ❌ Don't: Add tests after finding bugs
**Why:** Reactive testing is inefficient

### ✅ Do: Add tests when adding features
**Why:** Prevents bugs from being introduced

---

### ❌ Don't: Skip tests because "it's simple"
**Why:** Simple code can still break

### ✅ Do: Add minimal tests even for simple changes
**Why:** 2 minutes now saves 20 minutes later

---

### ❌ Don't: Only add unit tests
**Why:** Integration bugs won't be caught

### ✅ Do: Follow the decision tree
**Why:** Right tests for the right changes

---

### ❌ Don't: Only add manual tests
**Why:** Manual tests are slow and error-prone

### ✅ Do: Automate what can be automated
**Why:** Fast feedback, repeatable, reliable

---

## Test Maintenance

### When to Update Tests

1. **Feature Addition** → Add new tests
2. **Feature Modification** → Update existing tests
3. **Bug Fix** → Add test that would have caught the bug
4. **Refactoring** → Ensure all tests still pass

### When to Remove Tests

1. **Feature Removal** → Remove corresponding tests
2. **Test Duplication** → Consolidate redundant tests
3. **Obsolete Tests** → Remove tests for removed features

---

## Success Metrics

### Good Test Coverage
- ✅ All critical patterns have unit tests
- ✅ All user flows have integration tests
- ✅ All visual features have manual test checklist

### Fast Feedback
- ✅ Unit tests run in <10 seconds
- ✅ Integration tests run in <60 seconds
- ✅ Manual tests have clear checklist

### Confidence
- ✅ Can add features without fear of breaking existing ones
- ✅ Can refactor with confidence
- ✅ Can release knowing tests passed

---

## Quick Reference

| Change Type | Unit | Integration | Manual | Time |
|-------------|------|-------------|--------|------|
| New dangerous pattern | ✅ | ⚠️ | ✅ | 5-10 min |
| New ASCII art | ❌ | ❌ | ✅ | 2-5 min |
| New variation | ⚠️ | ❌ | ✅ | 2-3 min |
| New caution pattern | ✅ | ✅ | ✅ | 10-15 min |
| New builtin command | ✅ | ⚠️ | ✅ | 10-15 min |
| New achievement | ✅ | ✅ | ✅ | 15-20 min |
| Refactoring | ✅ | ✅ | ✅ | 30-60 min |

**Legend:**
- ✅ Required
- ⚠️ Optional (depends on complexity)
- ❌ Not needed

---

## Integration with Kiro Workflow

### When Kiro Adds a Feature

1. **Kiro reads this steering file** (automatic)
2. **Kiro identifies change type** (from decision tree)
3. **Kiro adds appropriate tests** (following templates)
4. **Kiro runs tests** (verifies they pass)
5. **Kiro commits** (with test coverage)

### When Human Adds a Feature

1. **Read this steering file** (manual)
2. **Follow decision tree** (identify required tests)
3. **Use templates** (copy-paste and modify)
4. **Run tests** (verify they pass)
5. **Commit** (with test coverage)

---

## Summary

**Golden Rule:** Every feature change should include appropriate tests.

**Decision Process:**
1. What did I change? (logic, display, both)
2. Which tests are required? (use decision tree)
3. Add tests using templates
4. Run tests to verify
5. Commit with confidence

**Time Investment:** 2-60 minutes depending on change type

**Benefit:** Prevents bugs, enables confident refactoring, maintains quality

---

**This steering file ensures consistent test coverage as MairuCLI grows.**
