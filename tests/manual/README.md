# Manual Tests

This directory contains resources for manual testing of MairuCLI.

## Files

### manual_test_plan.md
Comprehensive checklist for manual testing. Use this before releases or after major changes.

### manual_test_commands.txt
Quick list of commands to test all major features. Copy-paste these into MairuCLI REPL.

**Usage:**
```bash
python -m src.main
# Then paste commands from manual_test_commands.txt
```

### test_session.txt
Sample test session for quick smoke testing.

## When to Use Manual Tests

- **Before demo/presentation** - Ensure everything looks good
- **After visual changes** - Verify ASCII art, colors, timing
- **Before release** - Final quality check
- **After refactoring** - Verify backward compatibility

## Automated vs Manual

**Automated tests** (`tests/unit/test_interceptor.py`):
- ✅ Pattern detection logic
- ✅ Fast (< 5 seconds)
- ✅ Run on every commit

**Manual tests** (this directory):
- ✅ Visual appearance
- ✅ User experience
- ✅ Timing and "feel"
- ✅ Run before releases

Both are important! Automated tests catch logic bugs, manual tests catch UX issues.

---

**For end users:** See [QUICKSTART.md](../../QUICKSTART.md) in the root directory for a fun guided tour!
