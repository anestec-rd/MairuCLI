# Requirements Document: Data-Driven Pattern Configuration

## Introduction

This specification addresses the duplication between pattern detection logic in `src/interceptor.py` and pattern metadata in `data/warnings/warning_catalog.json`. Currently, pattern information (regex, category, severity, ASCII art) is defined in both places, creating a maintenance burden and potential for inconsistency. This refactoring will establish JSON files as the single source of truth for all pattern configuration.

## Glossary

- **Pattern Detection**: The process of matching user commands against dangerous command patterns using regular expressions
- **Pattern Metadata**: Information about a pattern including category, severity, ASCII art file, explanations, and advice
- **Interceptor**: The module (`src/interceptor.py`) responsible for detecting dangerous commands and typos
- **Warning Catalog**: The JSON file (`data/warnings/warning_catalog.json`) containing pattern metadata for display
- **Single Source of Truth**: A design principle where each piece of data is stored in exactly one authoritative location
- **Data-Driven Configuration**: An approach where behavior is controlled by external data files rather than hardcoded in source code

## Requirements

### Requirement 1: Unified Pattern Configuration

**User Story:** As a developer, I want all pattern information defined in JSON files, so that I don't have to update multiple files when adding or modifying patterns.

#### Acceptance Criteria

1. THE Interceptor SHALL load all pattern definitions (regex, category, severity) from JSON files at startup
2. WHEN a new dangerous pattern is added, THE System SHALL require changes to only JSON files, not Python code
3. THE Interceptor SHALL validate JSON pattern definitions on load and report errors clearly
4. WHERE pattern definitions are invalid or missing, THE Interceptor SHALL log errors and continue with valid patterns
5. THE System SHALL maintain a single authoritative source for each pattern attribute (regex, category, severity, ASCII art)

### Requirement 2: Pattern Detection from JSON

**User Story:** As a developer, I want the interceptor to read regex patterns from JSON, so that pattern matching logic is data-driven.

#### Acceptance Criteria

1. THE Interceptor SHALL load regex patterns from `data/warnings/warning_catalog.json`
2. WHEN checking commands, THE Interceptor SHALL use regex patterns loaded from JSON
3. THE Interceptor SHALL compile regex patterns once at startup for performance
4. THE Interceptor SHALL support all regex features currently used (groups, flags, etc.)
5. WHERE regex compilation fails, THE Interceptor SHALL log the error and skip that pattern

### Requirement 3: Caution Pattern Configuration

**User Story:** As a developer, I want caution patterns defined in JSON files, so that they follow the same data-driven approach as dangerous patterns.

#### Acceptance Criteria

1. THE System SHALL provide a JSON file for caution pattern definitions
2. THE Interceptor SHALL load caution patterns from JSON at startup
3. WHEN a caution pattern is matched, THE Interceptor SHALL retrieve all metadata from JSON
4. THE System SHALL support all caution pattern attributes (risk, impact, considerations)
5. WHERE caution patterns are missing from JSON, THE Interceptor SHALL use fallback behavior

### Requirement 4: Typo Pattern Configuration

**User Story:** As a developer, I want typo patterns defined in JSON files, so that adding new typo detection doesn't require code changes.

#### Acceptance Criteria

1. THE System SHALL maintain typo patterns in `data/warnings/typo_messages.json`
2. THE Interceptor SHALL load typo patterns from JSON at startup
3. WHEN a typo is detected, THE Interceptor SHALL retrieve correction suggestions from JSON
4. THE System SHALL support both specific typo patterns and generic typo detection
5. WHERE typo patterns are missing, THE Interceptor SHALL fall back to generic detection

### Requirement 5: Backward Compatibility

**User Story:** As a user, I want the refactored system to detect the same patterns as before, so that my protection level is not reduced.

#### Acceptance Criteria

1. THE Interceptor SHALL detect all patterns that were previously detected
2. WHEN commands are checked, THE Interceptor SHALL return the same results as before refactoring
3. THE System SHALL maintain the same performance characteristics (< 50ms per check)
4. THE Interceptor SHALL maintain the same API (function signatures unchanged)
5. WHERE existing tests exist, THE System SHALL pass all tests without modification

### Requirement 6: JSON Schema Validation

**User Story:** As a developer, I want JSON pattern files validated on load, so that configuration errors are caught early.

#### Acceptance Criteria

1. THE System SHALL define a schema for pattern configuration JSON files
2. WHEN loading JSON files, THE System SHALL validate structure against the schema
3. THE System SHALL report specific validation errors (missing fields, wrong types, etc.)
4. WHERE validation fails, THE System SHALL log errors and use fallback patterns
5. THE System SHALL provide clear error messages indicating which file and field has issues

### Requirement 7: Hot Reload Support (Future)

**User Story:** As a developer, I want the ability to reload patterns without restarting, so that I can test pattern changes quickly.

#### Acceptance Criteria

1. THE System SHALL provide a mechanism to reload pattern definitions from JSON
2. WHEN patterns are reloaded, THE System SHALL recompile regex patterns
3. THE System SHALL validate reloaded patterns before replacing current patterns
4. WHERE reload fails, THE System SHALL keep current patterns and log errors
5. THE System SHALL support reload through a command or signal (implementation deferred)

### Requirement 8: Help Command Auto-Generation

**User Story:** As a developer, I want the help command to automatically display patterns from JSON, so that I don't have to maintain the dangerous command list in two places.

#### Acceptance Criteria

1. THE Help Command SHALL load dangerous patterns from warning_catalog.json
2. THE Help Command SHALL load caution patterns from caution_catalog.json
3. WHEN displaying dangerous commands, THE Help Command SHALL show pattern name, emoji, and brief description
4. WHEN displaying caution commands, THE Help Command SHALL show pattern name, emoji, and brief description
5. THE Help Command SHALL group patterns by category (deletion, permission, disk, database, system)
6. WHERE a pattern has a help_description field, THE Help Command SHALL use it; otherwise use explanation field
7. THE Help Command SHALL maintain consistent formatting and color scheme
8. WHEN new patterns are added to JSON, THE Help Command SHALL automatically include them without code changes

### Requirement 9: Migration Path

**User Story:** As a developer, I want a clear migration path from hardcoded patterns to JSON, so that the transition is smooth and safe.

#### Acceptance Criteria

1. THE System SHALL provide a migration script or tool to extract patterns from Python to JSON
2. WHEN migrating, THE System SHALL preserve all pattern attributes exactly
3. THE System SHALL validate that migrated JSON produces identical detection results
4. THE System SHALL provide documentation for the migration process
5. WHERE migration is incomplete, THE System SHALL support a hybrid mode (Python + JSON)

