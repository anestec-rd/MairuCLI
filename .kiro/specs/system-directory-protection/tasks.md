# Implementation Plan - System Directory Protection

## Overview

This implementation plan breaks down the system directory protection feature into discrete, testable tasks. Each task is designed to be implemented incrementally with immediate testing to ensure safety and correctness.

**Critical Safety Note:** This feature protects users from system damage. Every component must be thoroughly tested before integration.

---

## Task List

- [x] 1. Create Path Resolution Module
  - Create `src/path_resolver.py` with PathResolver class
  - Implement path resolution logic (relative → absolute)
  - Implement environment variable expansion
  - Implement user home directory expansion (~)
  - Implement path normalization (separators, case)
  - Add error handling for invalid paths
  - _Requirements: 2.1, 2.2, 2.3, 8.2, 8.3_

- [x] 1.1 Write unit tests for PathResolver
  - Test relative path resolution
  - Test environment variable expansion ($WINDIR, $HOME)
  - Test home directory expansion (~)
  - Test path normalization
  - Test error handling (permission denied, invalid paths)
  - Test edge cases (empty string, None, special characters)
  - _Requirements: 10.1, 10.4_

- [x] 2. Create Command Parser Module
  - Create `src/command_parser.py` with CommandParser class
  - Implement command parsing to extract file paths
  - Handle different command types (rm, mv, chmod, dd, etc.)
  - Detect output redirection (>)
  - Handle quoted paths and spaces
  - Add support for command options/flags
  - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5_

- [x] 2.1 Write unit tests for CommandParser
  - Test path extraction from rm commands
  - Test path extraction from mv commands (source and dest)
  - Test path extraction from chmod/chown commands
  - Test dd command parsing (if=/of=)
  - Test output redirection detection
  - Test quoted paths with spaces
  - _Requirements: 10.1, 10.4_

- [x] 3. Add Protected Directory Database
  - Add PROTECTED_DIRECTORIES dict to `src/interceptor.py`
  - Define Windows critical directories (Windows, System32, etc.)
  - Define Windows caution directories (Program Files, etc.)
  - Define Linux critical directories (/etc, /bin, etc.)
  - Define Linux caution directories (/usr, /var/log)
  - Define macOS critical directories (/System, etc.)
  - Define macOS caution directories (/Library, /Applications)
  - _Requirements: 1.4, 1.5, 6.2, 6.3, 6.4_

- [x] 4. Implement System Directory Check Function
  - Add `check_system_directory()` function to `src/interceptor.py`
  - Integrate PathResolver for path resolution
  - Integrate CommandParser for path extraction
  - Implement platform detection (sys.platform)
  - Implement critical directory matching
  - Implement caution directory matching
  - Add performance optimization (caching, early exit)
  - Add comprehensive error handling (fail-safe)
  - _Requirements: 1.1, 1.2, 1.3, 2.4, 5.1, 5.2, 5.3, 6.1, 7.1, 8.5_

- [x] 4.1 Write unit tests for check_system_directory
  - Test Windows System32 detection
  - Test Windows Program Files detection
  - Test Linux /etc detection
  - Test Linux /usr detection
  - Test macOS /System detection
  - Test relative path detection (../../Windows)
  - Test environment variable paths ($WINDIR)
  - Test wildcard detection (C:\Windows\*.dll)
  - Test safe paths (user directories)
  - Test error handling (invalid paths)
  - _Requirements: 10.2, 10.4_

- [x] 5. Create Directory Information Database
  - Add DIRECTORY_INFO dict to `src/display/system_protection_warning.py`
  - Add Windows directory descriptions and risks
  - Add Linux directory descriptions and risks
  - Add macOS directory descriptions and risks
  - Add safe alternatives for each directory
  - Use age-appropriate, educational language
  - Maintain Halloween theme in messages
  - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5_

- [x] 6. Create System Protection Warning Component
  - Create `src/display/system_protection_warning.py`
  - Implement SystemProtectionWarning class
  - Implement critical warning display
  - Implement caution warning display (with confirmation)
  - Integrate with existing AsciiRenderer
  - Add Halloween-themed formatting
  - Add educational message formatting
  - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5_

- [x] 7. Integrate into Command Processing Flow
  - Modify `process_command()` in `src/main.py`
  - Add system directory check before dangerous pattern check
  - Handle critical level (block immediately)
  - Handle caution level (warn with confirmation)
  - Update statistics tracking for blocked commands
  - Maintain backward compatibility
  - _Requirements: 5.4, 5.5, 9.1, 9.4_

- [x] 8. Update Display Module Public API
  - Add `show_system_protection_warning()` to `src/display/__init__.py`
  - Initialize SystemProtectionWarning component
  - Export public interface
  - Maintain consistency with existing warning functions
  - _Requirements: 9.2, 9.3_

- [x] 9. Write integration tests
  - Test complete flow: command → check → block → warning
  - Test Windows system directory protection
  - Test Linux system directory protection
  - Test caution level confirmation flow
  - Test statistics update on block
  - Test interaction with existing dangerous pattern checks
  - _Requirements: 10.3_

- [ ] 10. Manual testing and validation
  - Test on actual Windows system (safe commands only!)
  - Test on actual Linux system (safe commands only!)
  - Test all edge cases (symlinks, relative paths, wildcards)
  - Verify educational messages are clear and helpful
  - Verify performance (< 50ms per check)
  - Test with real user scenarios
  - _Requirements: 7.1, 10.4_

- [x] 11. Update documentation
  - Update CHANGELOG.md with new feature
  - Update README.md with system protection description
  - Add to docs/DANGEROUS_PATTERNS.md
  - Update TODO.md (mark as complete)
  - Add examples to DEMO_SCRIPT.md
  - _Requirements: N/A (documentation)_

- [ ] 12. Final safety review
  - Review all fail-safe mechanisms
  - Verify no bypass methods exist
  - Confirm error handling is comprehensive
  - Test with malicious input attempts
  - Verify cross-platform compatibility
  - Get peer review if possible
  - _Requirements: 8.1, 8.2, 8.3, 8.4, 8.5_

---

## Implementation Notes

### Safety-First Approach

1. **Test Each Component Independently**
   - PathResolver → Unit tests first
   - CommandParser → Unit tests first
   - check_system_directory → Unit tests first
   - Only integrate after all tests pass

2. **Fail-Safe Design**
   - If path resolution fails → Block command
   - If parsing fails → Block command
   - If platform unknown → Block command
   - When in doubt → Block command

3. **Incremental Integration**
   - Implement in development branch
   - Test thoroughly before merging
   - Use safe test commands only
   - Never test with actual dangerous commands on real systems

### Testing Strategy

**Unit Tests (Required):**
- PathResolver: 10+ test cases
- CommandParser: 10+ test cases
- check_system_directory: 15+ test cases
- Total: 35+ unit tests minimum

**Integration Tests (Required):**
- Complete flow tests: 5+ test cases
- Cross-component interaction: 5+ test cases
- Total: 10+ integration tests minimum

**Manual Tests (Required):**
- Real system testing (Windows): 10+ scenarios
- Real system testing (Linux): 10+ scenarios
- Edge case verification: 10+ scenarios
- Total: 30+ manual test scenarios

### Performance Targets

- Path resolution: < 10ms
- Command parsing: < 10ms
- Directory check: < 20ms
- Total overhead: < 50ms
- Cache hit: < 1ms

### Edge Cases to Test

1. **Path Manipulation**
   - `../../Windows/System32`
   - `C:\Windows\..\Windows\System32`
   - `C:/Windows/System32` (forward slashes on Windows)
   - `c:\windows\system32` (case variations)

2. **Environment Variables**
   - `$WINDIR\System32`
   - `%SYSTEMROOT%\System32`
   - `$HOME/../../../etc`

3. **Wildcards**
   - `C:\Windows\*.dll`
   - `/etc/*.conf`
   - `C:\Windows\System32\*`

4. **Symbolic Links**
   - Links pointing to system directories
   - Circular links
   - Broken links

5. **Special Characters**
   - Spaces in paths
   - Unicode characters
   - Special shell characters

### Development Workflow

1. **Create feature branch**
   ```bash
   git checkout -b feature/system-directory-protection
   ```

2. **Implement task by task**
   - Complete task
   - Write tests
   - Run tests
   - Commit
   - Repeat

3. **Integration testing**
   - Merge to development branch
   - Run full test suite
   - Manual testing

4. **Final review**
   - Code review
   - Safety review
   - Documentation review
   - Merge to main

### Rollback Plan

If critical issues are discovered:
1. Revert commits immediately
2. Document the issue
3. Fix in feature branch
4. Re-test thoroughly
5. Re-deploy

---

## Estimated Time Breakdown

| Task | Estimated Time | Priority |
|------|---------------|----------|
| 1. PathResolver | 15 min | High |
| 1.1 PathResolver tests | 10 min | High |
| 2. CommandParser | 20 min | High |
| 2.1 CommandParser tests | 10 min | High |
| 3. Protected directories | 5 min | High |
| 4. check_system_directory | 15 min | High |
| 4.1 System check tests | 15 min | High |
| 5. Directory info | 10 min | Medium |
| 6. Warning component | 15 min | Medium |
| 7. Integration | 10 min | High |
| 8. Public API | 5 min | Medium |
| 9. Integration tests | 15 min | High |
| 10. Manual testing | 20 min | High |
| 11. Documentation | 10 min | Low |
| 12. Safety review | 10 min | Critical |
| **Total** | **175 min** | **(~3 hours)** |

**Note:** Original estimate was 90-130 minutes. Increased to 175 minutes due to comprehensive testing requirements for safety-critical feature.

---

## Success Criteria

- [ ] All unit tests pass (35+ tests)
- [ ] All integration tests pass (10+ tests)
- [ ] Manual testing completed on Windows and Linux
- [ ] No bypass methods discovered
- [ ] Performance targets met (< 50ms)
- [ ] Educational messages are clear and helpful
- [ ] Documentation is complete
- [ ] Peer review completed (if available)
- [ ] Zero false negatives (all dangerous operations blocked)
- [ ] Acceptable false positives (< 1% of safe operations)

---

**Ready to begin implementation with safety as top priority.**
