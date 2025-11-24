# File Naming Conventions

## Purpose

Enforce consistent file naming across the MairuCLI project to improve maintainability and reduce confusion.

---

## Naming Rules by Directory

### Root Directory

**Rule:** `SCREAMING_SNAKE_CASE` for important files only

**Allowed:**
- `README.md` - Project overview
- `LICENSE` - Legal document
- `CHANGELOG.md` - Version history
- `TODO.md` - Task tracking
- `QUICKSTART.md` - Quick start guide
- `LESSONS_LEARNED.md` - Project retrospective

**Examples:**
```
✅ README.md
✅ CHANGELOG.md
✅ LICENSE
❌ Project_Overview.md
❌ project-overview.md
```

---

### src/ (Python Source Code)

**Rule:** `snake_case` (PEP 8 standard)

**Pattern:** `module_name.py`, `class_name.py`

**Examples:**
```
✅ src/interceptor.py
✅ src/command_parser.py
✅ src/display/warning_components.py
✅ src/builtins/file_operations.py
❌ src/CommandParser.py
❌ src/command-parser.py
❌ src/INTERCEPTOR.py
```

---

### tests/ (Python Test Files)

**Rule:** `snake_case` with `test_` prefix

**Pattern:** `test_module_name.py`

**Examples:**
```
✅ tests/unit/test_interceptor.py
✅ tests/integration/test_dangerous_commands.py
✅ tests/unit/display/test_achievements.py
❌ tests/unit/TestInterceptor.py
❌ tests/unit/test-interceptor.py
❌ tests/unit/TEST_INTERCEPTOR.py
```

---

### docs/ (Documentation)

**Rule:** `kebab-case` for all Markdown files

**Pattern:** `descriptive-name.md`

**Examples:**
```
✅ docs/design-review.md
✅ docs/initial-brainstorm.md
✅ docs/hooks-guide.md
✅ docs/category-based-variations-design.md
❌ docs/DesignReview.md
❌ docs/design_review.md
❌ docs/DESIGN_REVIEW.md
```

**Subdirectories:**
```
✅ docs/reports/day7-summary.md
✅ docs/reference/cli-incidents.md
✅ docs/lessons/full-archive.md
❌ docs/reports/DAY7_SUMMARY.md
❌ docs/reference/CLI_INCIDENTS.md
```

---

### data/ (Data Files)

**Rule:** `snake_case` for JSON and text files

**Pattern:** `data_name.json`, `file_name.txt`

**Examples:**
```
✅ data/warnings/warning_catalog.json
✅ data/warnings/danger_variations.json
✅ data/ascii_art/fired.txt
✅ data/ascii_art/permission_denied.txt
❌ data/warnings/WarningCatalog.json
❌ data/warnings/warning-catalog.json
❌ data/ascii_art/FIRED.txt
```

---

### .kiro/ (Kiro Configuration)

**Rule:** `kebab-case` for all files

**Pattern:** `feature-name.md`, `config-name.json`

**Examples:**
```
✅ .kiro/steering/naming-conventions.md
✅ .kiro/steering/magic-numbers.md
✅ .kiro/specs/display-refactoring/design.md
❌ .kiro/steering/NamingConventions.md
❌ .kiro/steering/naming_conventions.md
```

---

## Quick Reference Table

| Directory | Rule | Example |
|-----------|------|---------|
| `/` (root) | `SCREAMING_SNAKE_CASE` | `README.md`, `CHANGELOG.md` |
| `src/` | `snake_case` | `interceptor.py`, `warning_components.py` |
| `tests/` | `snake_case` | `test_interceptor.py`, `test_achievements.py` |
| `docs/` | `kebab-case` | `design-review.md`, `hooks-guide.md` |
| `data/` | `snake_case` | `warning_catalog.json`, `fired.txt` |
| `.kiro/` | `kebab-case` | `naming-conventions.md`, `design.md` |

---

## Rationale

### Why Different Rules?

1. **Root files (`SCREAMING_SNAKE_CASE`)**
   - High visibility and importance
   - Industry standard (README, LICENSE, CHANGELOG)
   - Immediately recognizable

2. **Python code (`snake_case`)**
   - PEP 8 standard
   - Consistency with Python naming conventions
   - Import-friendly (no hyphens in module names)

3. **Documentation (`kebab-case`)**
   - URL-friendly (for web hosting)
   - Easy to read
   - Common in web/documentation contexts

4. **Data files (`snake_case`)**
   - Consistency with Python code
   - Easy to reference from code
   - JSON keys typically use snake_case

---

## When Creating New Files

### Checklist

Before creating a new file, ask:

1. **What directory is it in?**
   - Root → `SCREAMING_SNAKE_CASE`
   - src/tests → `snake_case`
   - docs/.kiro → `kebab-case`
   - data → `snake_case`

2. **Does it follow the pattern?**
   - Check the examples above
   - Verify with Quick Reference Table

3. **Is it consistent with existing files?**
   - Look at similar files in the same directory
   - Follow the established pattern

### Examples

**Creating a new design document:**
```bash
# ✅ Correct
docs/authentication-design.md

# ❌ Wrong
docs/Authentication_Design.md
docs/authentication_design.md
docs/AUTHENTICATION_DESIGN.md
```

**Creating a new Python module:**
```bash
# ✅ Correct
src/authentication.py

# ❌ Wrong
src/Authentication.py
src/authentication-module.py
src/AUTHENTICATION.py
```

**Creating a new test:**
```bash
# ✅ Correct
tests/unit/test_authentication.py

# ❌ Wrong
tests/unit/TestAuthentication.py
tests/unit/test-authentication.py
tests/unit/TEST_AUTHENTICATION.py
```

---

## Migration from Old Naming

If you encounter files with inconsistent naming:

1. **Identify the correct name** using the rules above
2. **Rename the file** using git mv (preserves history)
3. **Update all references** in code and documentation
4. **Test** to ensure nothing broke

**Example:**
```bash
# Rename file
git mv docs/HOOKS_GUIDE.md docs/hooks-guide.md

# Update references (if any)
grep -r "HOOKS_GUIDE.md" .
# Update found references

# Test
python -m pytest
```

---

## Enforcement

### For Developers

- **Before committing:** Review file names against this guide
- **During code review:** Check for naming consistency
- **When in doubt:** Refer to Quick Reference Table

### For AI Assistants (Kiro)

- **ALWAYS check this steering file** before creating new files
- **NEVER create files** with inconsistent naming
- **SUGGEST renaming** if encountering inconsistent files
- **FOLLOW the rules strictly** - no exceptions

---

## Common Mistakes to Avoid

### ❌ Mixing Cases in Same Directory

**Bad:**
```
docs/
├── HOOKS_GUIDE.md        # SCREAMING
├── hooks-benefits.md     # kebab-case
└── design_review.md      # snake_case
```

**Good:**
```
docs/
├── hooks-guide.md        # kebab-case
├── hooks-benefits.md     # kebab-case
└── design-review.md      # kebab-case
```

### ❌ Using Hyphens in Python Files

**Bad:**
```python
# ❌ Cannot import
from src import command-parser  # SyntaxError!
```

**Good:**
```python
# ✅ Can import
from src import command_parser
```

### ❌ Using Underscores in Documentation

**Bad:**
```
docs/design_review.md     # Harder to read in URLs
```

**Good:**
```
docs/design-review.md     # Clean URLs: /docs/design-review
```

---

## Summary

**Golden Rule:** Follow the directory-specific naming convention consistently.

**Quick Decision Tree:**
```
Is it in root directory?
├─ Yes → SCREAMING_SNAKE_CASE
└─ No → Is it Python code/test?
    ├─ Yes → snake_case
    └─ No → Is it documentation?
        ├─ Yes → kebab-case
        └─ No → Is it data?
            ├─ Yes → snake_case
            └─ No → Check this guide
```

**When in doubt:** Look at existing files in the same directory and follow their pattern.

---

**This steering file ensures consistent naming as MairuCLI grows.**
