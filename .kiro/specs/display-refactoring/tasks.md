# Implementation Plan: Display Module Refactoring

- [x] 1. Set up project structure and data files
  - Create display/ subdirectory under src/
  - Create data/warnings/ and data/ascii_art/ directories
  - Create __init__.py for display module
  - Move existing ASCII art files to data/ascii_art/
  - _Requirements: 5.1, 5.3, 5.4_

- [ ] 2. Implement content loader component
  - [x] 2.1 Create ContentLoader class with JSON loading
    - Implement load_catalog() method for warning_catalog.json
    - Implement get_warning_content() for pattern lookup
    - Implement get_variations() for variation sets
    - Add error handling for missing/invalid files
    - _Requirements: 6.1, 6.2, 6.3, 6.6_

  - [x] 2.2 Create warning content data files
    - Create warning_catalog.json with rm_root and chmod_777 entries
    - Create danger_variations.json with existing variations
    - Create typo_messages.json with sl and cd_stuck entries
    - Create repeat_warnings.json with escalating messages
    - _Requirements: 6.2, 6.7_

  - [ ]* 2.3 Write unit tests for ContentLoader
    - Test valid JSON loading
    - Test missing file handling
    - Test invalid JSON handling
    - Test content validation
    - _Requirements: 6.4, 6.6_

- [ ] 3. Implement ASCII renderer component
  - [x] 3.1 Create AsciiRenderer class
    - Implement load_art() with file loading and error handling
    - Implement display_art() with color application
    - Implement display_art_slowly() with line-by-line timing
    - Add fallback for missing ASCII art files
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5_

  - [ ]* 3.2 Write unit tests for AsciiRenderer
    - Test file loading with valid paths
    - Test file loading with invalid paths
    - Test color application
    - Test timing effects
    - _Requirements: 2.5_

- [ ] 4. Implement message formatter component
  - [x] 4.1 Create MessageTemplate class
    - Implement template initialization with required fields
    - Implement format() method with placeholder replacement
    - Implement validate() method for field checking
    - _Requirements: 3.1, 3.2, 3.4_

  - [x] 4.2 Create MessageFormatter class
    - Implement format_danger_warning() method
    - Implement format_typo_warning() method
    - Implement format_repeat_warning() method
    - Add color code and emoji placeholder support
    - _Requirements: 3.2, 3.3, 3.5_

  - [ ]* 4.3 Write unit tests for message formatting
    - Test template population
    - Test field validation
    - Test color code insertion
    - Test missing field handling
    - _Requirements: 3.4_

- [ ] 5. Implement statistics and achievements components
  - [x] 5.1 Create Statistics class
    - Implement counter initialization
    - Implement increment_dangerous_blocked() method
    - Implement increment_typos_caught() method
    - Implement track_repeat_command() method
    - Implement get_stats() method
    - _Requirements: 4.4_

  - [x] 5.2 Create AchievementTracker class
    - Implement achievement checking logic
    - Implement show_achievement() method with timing
    - Track unlocked achievements to prevent duplicates
    - _Requirements: 4.4_

  - [ ]* 5.3 Write unit tests for statistics and achievements
    - Test counter increments
    - Test achievement triggers
    - Test repeat command tracking
    - Test achievement deduplication
    - _Requirements: 4.4_

- [ ] 6. Implement warning component base and implementations
  - [x] 6.1 Create WarningComponent base class
    - Define abstract display() method
    - Set up dependency injection for renderer and formatter
    - _Requirements: 1.2, 4.1, 4.2_

  - [x] 6.2 Create DangerWarning component
    - Implement display() method with content loading
    - Implement random variation selection
    - Integrate ASCII art rendering with timing
    - Integrate message formatting
    - Display safe alternatives from catalog
    - _Requirements: 1.1, 1.4, 2.1, 2.2, 3.2_

  - [x] 6.3 Create TypoWarning component
    - Implement display() method for typo warnings
    - Load typo messages from content loader
    - Display suggestion with color formatting
    - _Requirements: 1.1, 3.2_

  - [x] 6.4 Create RepeatWarning component
    - Implement display() method with escalating messages
    - Load repeat messages from content loader
    - Handle different repeat counts (2, 3, 4, 5+)
    - _Requirements: 1.1, 3.2_

  - [ ]* 6.5 Write unit tests for warning components
    - Test DangerWarning display flow
    - Test TypoWarning display flow
    - Test RepeatWarning escalation
    - Test variation selection
    - _Requirements: 1.4_

- [ ] 7. Refactor display.py to use new components
  - [x] 7.1 Initialize components in display.py
    - Create module-level instances of all components
    - Set up dependency injection
    - Load content at module initialization
    - _Requirements: 4.1, 7.1, 7.2_

  - [x] 7.2 Update show_warning() to delegate to components
    - Route to DangerWarning for dangerous patterns
    - Route to TypoWarning for typo patterns
    - Route to RepeatWarning for repeat commands
    - Update statistics tracking
    - Maintain existing function signature
    - _Requirements: 1.3, 7.2, 7.3_

  - [x] 7.3 Update helper functions to use new components
    - Update show_danger_warning() to use DangerWarning
    - Update show_typo_warning() to use TypoWarning
    - Update show_repeat_warning() to use RepeatWarning
    - Update check_achievements() to use AchievementTracker
    - _Requirements: 7.2, 7.3_

  - [x] 7.4 Clean up old code from display.py
    - Remove WARNING_VARIATIONS constant
    - Remove hardcoded message logic
    - Remove duplicate ASCII art loading code
    - Keep only public API functions
    - _Requirements: 5.2, 7.4_

- [ ] 8. Verify backward compatibility and integration
  - [x] 8.1 Run existing tests
    - Execute all existing display tests
    - Verify no test failures
    - _Requirements: 7.5_

  - [x] 8.2 Manual testing of warning displays
    - Test rm -rf / warning displays correctly
    - Test chmod 777 warning displays correctly
    - Test typo warnings display correctly
    - Test repeat warnings escalate correctly
    - Test achievements display correctly
    - Verify timing effects work as before
    - _Requirements: 7.1, 7.3, 7.4_

  - [x] 8.3 Test error handling
    - Test with missing warning_catalog.json
    - Test with invalid JSON in data files
    - Test with missing ASCII art files
    - Verify graceful degradation in all cases
    - _Requirements: 6.6_

- [ ] 9. Documentation and cleanup
  - [x] 9.1 Update documentation
    - Add architecture diagram to README.md
    - Document content file formats
    - Add guide for adding new warnings
    - Update CHANGELOG.md with refactoring notes
    - _Requirements: 8.1, 8.2, 8.3_

  - [x] 9.2 Add inline documentation
    - Add docstrings to all new classes and methods
    - Add type hints to all functions
    - Add comments explaining complex logic
    - _Requirements: 8.4_

  - [ ]* 9.3 Create developer guide
    - Write guide for adding new warning types
    - Document content file structure
    - Provide examples of custom variations
    - _Requirements: 8.5_
