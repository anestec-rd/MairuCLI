# Implementation Plan: Data-Driven Pattern Configuration

## Overview

This implementation plan converts the hardcoded pattern dictionaries in `interceptor.py` to a data-driven approach where all patterns are loaded from JSON files. The migration will be done incrementally to maintain backward compatibility.

---

## Tasks

- [x] 1. Add pattern field to existing JSON files
  - Add `"pattern"` field to all entries in `data/warnings/warning_catalog.json`
  - Migrate regex patterns from `interceptor.py` DANGEROUS_PATTERNS
  - Ensure proper escaping (double backslashes in JSON)
  - Validate JSON syntax
  - _Requirements: 1.1, 2.1_

- [x] 2. Create caution_catalog.json
  - Create new file `data/warnings/caution_catalog.json`
  - Migrate all CAUTION_PATTERNS from `interceptor.py`
  - Add `"pattern"` field to each entry
  - Include risk, impact, and considerations fields
  - Validate JSON structure
  - _Requirements: 3.1, 3.2_

- [x] 3. Update typo_messages.json with patterns
  - Add `"pattern"` field to all entries in `data/warnings/typo_messages.json`
  - Migrate regex patterns from `interceptor.py` TYPO_PATTERNS
  - Ensure proper escaping
  - _Requirements: 4.1, 4.2_

- [x] 4. Implement PatternLoader class
  - Create `PatternLoader` class in `interceptor.py`
  - Implement `load_all_patterns()` method
  - Implement `_load_dangerous_patterns()` method
  - Implement `_load_caution_patterns()` method
  - Implement `_load_typo_patterns()` method
  - Add error handling for missing files
  - Add error handling for invalid JSON
  - _Requirements: 1.2, 1.3_

- [x] 4.1 Write unit tests for PatternLoader
  - Test loading valid JSON files
  - Test handling missing files gracefully
  - Test handling invalid JSON syntax
  - Test handling missing pattern fields
  - _Requirements: 1.4_

- [x] 5. Implement PatternCompiler class
  - Create `PatternCompiler` class in `interceptor.py`
  - Implement `compile_patterns()` method
  - Implement `_compile_pattern_dict()` method
  - Add error handling for invalid regex patterns
  - Log compilation errors clearly
  - _Requirements: 2.2, 2.3_

- [x] 5.1 Write unit tests for PatternCompiler
  - Test compiling valid regex patterns
  - Test handling invalid regex gracefully
  - Test pattern matching with compiled patterns
  - _Requirements: 2.4_

- [x] 6. Create CommandInterceptor class
  - Implement `CommandInterceptor` class
  - Implement `__init__` with pattern loading
  - Implement `_load_and_compile_patterns()` method
  - Implement `check_command()` method using compiled patterns
  - Implement `get_pattern_info()` method
  - Maintain same logic as existing functions
  - _Requirements: 1.1, 2.1, 5.1_

- [x] 6.1 Write unit tests for CommandInterceptor
  - Test pattern detection with JSON-loaded patterns
  - Test all dangerous patterns are detected
  - Test all caution patterns are detected
  - Test all typo patterns are detected
  - _Requirements: 5.2_


- [x] 7. Add backward compatibility layer
  - Create module-level `_interceptor` singleton
  - Implement `_get_interceptor()` function
  - Update `check_command()` to use new class
  - Update `get_pattern_info()` to use new class
  - Ensure function signatures remain unchanged
  - _Requirements: 5.2, 5.3_

- [ ]* 7.1 Write integration tests for backward compatibility
  - Test that existing code using `check_command()` still works
  - Test that existing code using `get_pattern_info()` still works
  - Compare results with old implementation
  - _Requirements: 5.4_

- [x] 8. Remove hardcoded pattern dictionaries
  - Remove `DANGEROUS_PATTERNS` dictionary from `interceptor.py`
  - Remove `CAUTION_PATTERNS` dictionary from `interceptor.py`
  - Remove `TYPO_PATTERNS` dictionary from `interceptor.py`
  - Keep `PROTECTED_DIRECTORIES` (not part of this refactoring)
  - Keep `COMMON_COMMANDS` (used for generic typo detection)
  - _Requirements: 1.5_

- [x] 9. Checkpoint - Ensure all tests pass
  - Run all unit tests
  - Run all integration tests
  - Verify no regressions in pattern detection
  - Ask user if questions arise
  - _Requirements: 5.1, 5.2, 5.3, 5.4_

- [x] 10. Add help_example and help_description to JSON files
  - Add `help_example` field to all patterns in `warning_catalog.json`
  - Add `help_description` field to all patterns in `warning_catalog.json`
  - Add `help_example` field to all patterns in `caution_catalog.json`
  - Add `help_description` field to all patterns in `caution_catalog.json`
  - Ensure descriptions are concise (50 characters or less)
  - _Requirements: 8.1, 8.2, 8.3_

- [x] 11. Implement HelpGenerator class
  - Create `HelpGenerator` class in `src/builtins/mairu_commands.py`
  - Implement `generate_dangerous_commands_help()` method
  - Implement `generate_caution_commands_help()` method
  - Implement `_group_by_category()` helper method
  - Load patterns from JSON dynamically
  - _Requirements: 8.4, 8.5, 8.6_

- [x] 12. Update help command to use HelpGenerator
  - Replace hardcoded dangerous command list with `HelpGenerator`
  - Add caution commands section (currently missing)
  - Ensure formatting and colors are consistent
  - Verify all patterns appear in help output
  - _Requirements: 8.7, 8.8_

- [x] 12.1 Write tests for HelpGenerator
  - Test that all dangerous patterns appear in help
  - Test that all caution patterns appear in help
  - Test category grouping
  - Test missing fields are handled gracefully
  - _Requirements: 8.8_

- [x] 13. Add JSON schema validation (optional)
  - Create JSON schema for `warning_catalog.json`
  - Create JSON schema for `caution_catalog.json`
  - Create JSON schema for `typo_messages.json`
  - Implement schema validation in `PatternLoader`
  - _Requirements: 6.1, 6.2_

- [ ]* 13.1 Create validation tool script
  - Create `src/tools/validate_patterns.py`
  - Validate all JSON files against schemas
  - Report validation errors clearly
  - _Requirements: 6.3_

- [x] 14. Update documentation
  - Update README.md with new pattern addition process
  - Document JSON file structure (including help_example and help_description)
  - Add examples of adding new patterns
  - Update CHANGELOG.md with migration notes
  - _Requirements: 9.1, 9.2_

- [ ]* 14.1 Create pattern testing tool (optional)
  - Create `src/tools/test_pattern.py`
  - Allow testing pattern matching from command line
  - Display matched pattern information
  - _Requirements: 8.3_

---

## Notes

### Pattern Migration Reference

When migrating patterns from Python to JSON, remember:

**Python regex:**
```python
"pattern": r"rm\s+(-rf|-fr)"
```

**JSON regex (double-escape):**
```json
"pattern": "rm\\s+(-rf|-fr)"
```

### Testing Priority

1. **Critical**: Pattern detection still works (unit + integration tests)
2. **Important**: Error handling works (missing files, invalid JSON)
3. **Nice-to-have**: Validation tools and testing utilities

### Performance Target

- Startup time increase: < 30ms
- Runtime performance: No regression
- Memory usage: < 1MB additional

