# JSON Schema Validation

## Overview

MairuCLI uses JSON schema validation to ensure pattern configuration files are correctly formatted. This helps catch errors early and provides clear error messages when patterns are misconfigured.

## Schema Files

Schema files are located in `data/warnings/schemas/`:

- `warning_catalog_schema.json` - Schema for dangerous command patterns
- `caution_catalog_schema.json` - Schema for caution-level patterns
- `typo_messages_schema.json` - Schema for typo patterns

## Validation Features

### Automatic Validation

Pattern files are automatically validated when MairuCLI starts:

```python
from src.interceptor import PatternLoader

# Validation enabled by default
loader = PatternLoader(validate_schema=True)
dangerous, caution, typo = loader.load_all_patterns()
```

### Validation Tool

Use the validation script to check all pattern files:

```bash
python scripts/validate_patterns.py
```

Output:
```
============================================================
MairuCLI Pattern Validation Tool
============================================================

Loading and validating patterns...

============================================================
Validation Results
============================================================

✅ warning_catalog.json: 14 patterns loaded
✅ caution_catalog.json: 7 patterns loaded
✅ typo_messages.json: 6 patterns loaded

✅ All required pattern files validated successfully!
```

## Schema Requirements

### Warning Catalog Schema

Required fields for each pattern:
- `pattern` (string) - Regular expression pattern
- `category` (enum) - One of: deletion, permission, disk, database, system
- `severity` (enum) - One of: critical, high, medium, low

Optional fields:
- `variation_set` (string)
- `ascii_art` (string)
- `color` (string)
- `emoji` (string)
- `explanation` (string)
- `consequence` (string)
- `advice` (array of strings)
- `timing` (object)
- `help_example` (string)
- `help_description` (string, max 50 chars)

### Caution Catalog Schema

Required fields for each pattern:
- `pattern` (string) - Regular expression pattern
- `category` (string)
- `severity` (enum) - One of: high, medium, low
- `risk` (string)
- `impact` (string)
- `considerations` (array of strings, min 1 item)

Optional fields:
- `help_example` (string)
- `help_description` (string, max 50 chars)

### Typo Messages Schema

Required fields for each pattern:
- `pattern` (string) - Regular expression pattern
- `correct` (string) - Correct command
- `message` (string) - Friendly message

Optional fields:
- `ascii_art` (string or null)

## Error Handling

### Validation Errors

When validation fails, MairuCLI:
1. Prints detailed error message with path and issue
2. Continues loading patterns (fail-safe behavior)
3. Allows system to function with available patterns

Example error:
```
Validation error in data/warnings/warning_catalog.json:
  Path: warnings -> rm_dangerous
  Error: 'pattern' is a required property
Warning: Validation failed for data/warnings/warning_catalog.json. Using patterns anyway.
```

### Missing Schema Files

If schema files are missing:
- Validation is skipped with a warning
- Patterns load normally
- System continues to function

### Missing jsonschema Library

If `jsonschema` is not installed:
- Validation is automatically disabled
- Warning message suggests installation
- System continues to function

Install jsonschema:
```bash
pip install jsonschema
```

## Disabling Validation

Validation can be disabled if needed:

```python
# Disable validation
loader = PatternLoader(validate_schema=False)
```

## Adding New Patterns

When adding new patterns:

1. **Add pattern to JSON file** (e.g., `warning_catalog.json`)
2. **Run validation tool** to check for errors:
   ```bash
   python scripts/validate_patterns.py
   ```
3. **Fix any validation errors** reported
4. **Test the pattern** in MairuCLI

## Schema Validation Benefits

✅ **Early error detection** - Catch configuration errors before runtime
✅ **Clear error messages** - Know exactly what's wrong and where
✅ **Type safety** - Ensure fields have correct types
✅ **Required fields** - Never miss critical configuration
✅ **Enum validation** - Ensure values are from allowed set
✅ **Documentation** - Schema serves as documentation

## Troubleshooting

### Pattern not loading

1. Run validation tool: `python scripts/validate_patterns.py`
2. Check for validation errors in output
3. Fix reported issues in JSON file
4. Verify pattern field is present and correct

### Validation always fails

1. Check schema file exists: `data/warnings/schemas/*.json`
2. Verify jsonschema is installed: `pip list | grep jsonschema`
3. Check JSON syntax is valid
4. Ensure pattern names match `^[a-z0-9_]+$` (lowercase, numbers, underscores)

### Schema too strict

If schema rejects valid patterns:
1. Review schema requirements
2. Update schema if needed (with caution)
3. Ensure changes don't break existing patterns
4. Run full test suite after schema changes

## Related Documentation

- [Data-Driven Content Management](../.kiro/steering/data-driven-content.md)
- [Pattern Configuration Design](design/educational-content-schema.md)
- [Testing Strategy](../.kiro/steering/test-strategy.md)
