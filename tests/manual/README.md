# Manual Tests - Human Verification

**Purpose:** Tests that require human observation and judgment.

**See `tests/README.md` for test type comparison and when to use which tests.**

---

## 📋 Available Test Files

### 1. General Feature Testing
**File:** `manual_test_plan.md`
**Time:** 15-20 minutes
**Tests:** All MairuCLI features (commands, warnings, achievements, etc.)

### 2. System Directory Protection
**File:** `system-protection-checklist.md`
**Time:** 10-15 minutes
**Tests:** System directory protection (Windows/Linux/macOS)

### 3. Quick Smoke Test
**File:** `manual_test_commands.txt`
**Time:** 5 minutes
**Tests:** Major features (copy-paste commands)

### 4. Timing Verification
**File:** `test_dramatic_timing.py`
**Time:** 2-3 minutes
**Tests:** Dramatic pauses and timing

### 5. Demo Preparation
**File:** `demo_session.py`
**Time:** 5 minutes
**Tests:** Demo flow practice

### 6. Additional Manual Tests
**Files:** Various `test_*.py` scripts
**Purpose:** Specific feature verification (variations, achievements, bypass testing, etc.)

---

## 🚀 Quick Start

### Step 1: Run Automated Tests First
```bash
# Ensure logic is correct before manual testing
pytest tests/unit/ -v
pytest tests/integration/ -v
```

### Step 2: Start MairuCLI
```bash
python -m src.main
```

### Step 3: Test Key Features
```
mairu> help
mairu> rm -rf /                    # Should block with warning
mairu> rm C:\Windows\test.txt      # Should block (Windows)
mairu> rm /etc/test.conf           # Should block (Linux)
mairu> stats
mairu> exit
```

### Step 4: Full Test (if needed)
- Open `manual_test_plan.md` or `SYSTEM_PROTECTION_CHECKLIST.md`
- Follow the checklist
- Check off items as you verify them

---

## 🎯 What to Verify

### Visual Quality
- [ ] ASCII art displays correctly
- [ ] Colors are visible
- [ ] Text is properly aligned
- [ ] No garbled characters

### Message Quality
- [ ] Messages are clear
- [ ] Language is age-appropriate
- [ ] Safe alternatives provided
- [ ] Educational value

### User Experience
- [ ] Feels responsive (no lag)
- [ ] Warnings are helpful
- [ ] Flow is smooth
- [ ] Halloween theme consistent

---

## 📝 Test Observation Points

Each manual test file focuses on specific observation points:

### `manual_test_plan.md`
- **Observes:** General feature functionality, visual quality, message clarity
- **Verifies:** Startup, builtins, dangerous commands, achievements, typos

### `system-protection-checklist.md`
- **Observes:** System protection accuracy, educational messages, performance
- **Verifies:** Windows/Linux/macOS protection, path resolution, edge cases

### `manual_test_commands.txt`
- **Observes:** Quick smoke test, major features work
- **Verifies:** No obvious regressions

### `test_dramatic_timing.py`
- **Observes:** Timing feels right, pauses are dramatic
- **Verifies:** ASCII art speed, pause durations

### `demo_session.py`
- **Observes:** Demo flow, presentation readiness
- **Verifies:** Commands work in demo order

### Additional Test Scripts
- `test_category_variations.py` - Verify category-based variation system
- `test_realtime_simulation.py` - Test educational timeline simulation
- `test_bypass_methods.py` - Verify security against bypass attempts
- `test_false_positives.py` - Check for incorrect dangerous pattern detection
- `test_false_negatives.py` - Check for missed dangerous patterns
- `test_achievements_live.txt` - Achievement unlock verification
- And more... (see directory for complete list)

---

## 🐛 If You Find Issues

1. **Note in checklist** - Record in "Issues Found" section
2. **Categorize severity:**
   - Critical: Blocks core functionality
   - Medium: Affects UX but has workaround
   - Minor: Polish issue
3. **Create issue** - Add to `docs/ISSUES.md`

---

## 💡 Tips

- **Test on your platform:** Windows users test Windows paths, Linux users test Linux paths
- **Test in different terminals:** CMD, PowerShell, GNOME Terminal, etc.
- **Test as a beginner:** Would a child understand the messages?
- **Note the "feel":** Does it feel responsive? Are pauses too long/short?

---

**For test type comparison and when to use which tests, see `tests/README.md`**
