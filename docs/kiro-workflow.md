# Kiro Workflow & Features Documentation

**Created:** 2025-11-30
**Purpose:** Comprehensive documentation of how Kiro AI was used to build MairuCLI
**Related:** README.md, LESSONS_LEARNED.md

---

## Overview

MairuCLI was built **100% exclusively with Kiro AI** - no GitHub Copilot, no Claude, no ChatGPT. This document details the Kiro features, workflows, and methodologies that made this possible, demonstrating **7.5-9x productivity gains** through intelligent AI collaboration.

---

## Table of Contents

1. [Spec-Driven Development Workflow](#spec-driven-development-workflow)
2. [Steering Files (15 Total)](#steering-files-15-total)
3. [Agent Hooks](#agent-hooks)
4. [Productivity Metrics](#productivity-metrics)
5. [Real Examples from MairuCLI](#real-examples-from-mairucli)
6. [Best Practices](#best-practices)

---

## Spec-Driven Development Workflow

### What is Spec-Driven Development?

Spec-Driven Development is Kiro's structured methodology for transforming ideas into working software through three phases:

```
Idea → Requirements → Design → Tasks → Implementation
```

### The Three Phases

#### Phase 1: Requirements

**Purpose:** Transform rough ideas into formal, testable requirements

**Process:**
1. Write user stories ("As a [role], I want [feature], so that [benefit]")
2. Define acceptance criteria using EARS patterns
3. Create glossary of technical terms
4. Iterate with user until approved

**EARS Patterns Used:**
- **Ubiquitous:** THE system SHALL response
- **Event-driven:** WHEN trigger, THE system SHALL response
- **State-driven:** WHILE condition, THE system SHALL response
- **Unwanted event:** IF condition, THEN THE system SHALL response
- **Optional feature:** WHERE option, THE system SHALL response

**Example from MairuCLI:**
```markdown
### Requirement 1: Dangerous Command Detection

**User Story:** As a CLI user, I want dangerous commands to be intercepted,
so that I don't accidentally destroy my system.

#### Acceptance Criteria
1. WHEN a user types 'rm -rf /', THE system SHALL block the command
2. WHEN a dangerous command is blocked, THE system SHALL display a warning
3. WHEN a warning is displayed, THE system SHALL include educational content
```

**Location:** `.kiro/specs/[feature-name]/requirements.md`

---

#### Phase 2: Design

**Purpose:** Create detailed technical design from requirements

**Process:**
1. Define architecture and components
2. Design data models and interfaces
3. Plan error handling strategy
4. Create testing strategy
5. Iterate with user until approved

**Example from MairuCLI:**
```markdown
## Architecture

### Display System Components

```
Display System
├── AsciiRenderer (ASCII art loading and timing)
├── MessageFormatter (Template-based formatting)
├── WarningComponents (Modular warning displays)
├── ContentLoader (JSON content management)
└── Statistics & Achievements (Tracking logic)
```

### Data Models

```python
@dataclass
class WarningPattern:
    pattern: str
    category: str
    severity: str
    ascii_art: str
    explanation: str
    consequence: str
    advice: List[str]
```
```

**Location:** `.kiro/specs/[feature-name]/design.md`

---

#### Phase 3: Tasks

**Purpose:** Break design into actionable implementation steps

**Process:**
1. Convert design into numbered task list
2. Each task references specific requirements
3. Include sub-tasks for complex items
4. Mark optional tasks with `*`
5. Iterate with user until approved

**Example from MairuCLI:**
```markdown
- [ ] 1. Create display module structure
  - Create `src/display/` directory
  - Create `__init__.py` with public API
  - _Requirements: 2.1, 2.2_

- [ ] 2. Implement AsciiRenderer
- [ ] 2.1 Create AsciiRenderer class
  - Load ASCII art from files
  - Implement dramatic timing
  - _Requirements: 1.3, 2.4_

- [ ]* 2.2 Write unit tests for AsciiRenderer
  - Test file loading
  - Test timing effects
  - _Requirements: 1.3_
```

**Location:** `.kiro/specs/[feature-name]/tasks.md`

---

### Real Specs from MairuCLI

Want to see actual specs in action? MairuCLI has complete specs you can explore:

**📁 [.kiro/specs/mairu-cli/](../.kiro/specs/mairu-cli/)**
- Original project spec (Day 1-2)
- Complete requirements, design, and tasks
- Shows how the entire project was planned

**📁 [.kiro/specs/display-refactoring/](../.kiro/specs/display-refactoring/)**
- Major refactoring spec (Day 3)
- 400-line file → 7 modular components
- Demonstrates refactoring methodology

**📁 [.kiro/specs/educational-breakdown/](../.kiro/specs/educational-breakdown/)**
- Feature addition spec (Day 8)
- Interactive learning mode
- Shows feature development workflow

**📁 [.kiro/specs/system-directory-protection/](../.kiro/specs/system-directory-protection/)**
- Cross-platform feature spec (Day 10)
- System directory protection
- Platform-specific considerations

**📁 [.kiro/specs/contest-submission/](../.kiro/specs/contest-submission/)**
- Contest submission spec (Day 13-14)
- Meta-spec for organizing submission
- Demonstrates spec versatility

**What to Look For:**
- How requirements are structured (EARS patterns)
- How design documents organize complexity
- How tasks break down implementation
- How specs reference each other

**Tip:** Start with `display-refactoring` - it's the clearest example of spec power (2.5 hours → 20 minutes).

---

### Executing Tasks

Once tasks are defined, Kiro can execute them incrementally:

1. **Open tasks.md** in Kiro
2. **Click "Start task"** next to any task
3. **Kiro implements** the task with full context
4. **Review and approve** before moving to next task

**Benefits:**
- Incremental progress with validation
- Full context from requirements and design
- Trackable progress
- Easy to pause and resume

---

## Steering Files (15 Total)

Steering files are Kiro's way of providing persistent guidance across all interactions. They're automatically included in context and shape how Kiro approaches development.

### What are Steering Files?

**Location:** `.kiro/steering/`

**Purpose:** Provide consistent development standards, guidelines, and best practices

**How They Work:**
- Automatically included in Kiro's context
- Guide decision-making and code generation
- Ensure consistency across sessions
- Capture project-specific knowledge

---

### All 15 Steering Files

#### 1. `mairu-cli-standards.md`
**Purpose:** Core development standards for MairuCLI

**Key Guidelines:**
- Python code style (type hints, docstrings, line length)
- Command pattern format (regex patterns)
- ASCII art guidelines (width, colors, testing)
- Educational message structure
- Halloween theme principles

**Impact:** Ensures consistent code quality and theme adherence

**Example:**
```python
# Enforced by steering file
DANGEROUS_PATTERNS = {
    "rm_recursive": r"rm\s+(-rf|-fr)\s+(/|~|\$HOME)",  # Clear comment
}
```

---

#### 2. `test-strategy.md`
**Purpose:** Guide test creation for different change types

**Key Guidelines:**
- Decision tree for which tests to add
- Test templates for common scenarios
- Time estimates for test creation
- When to skip tests (and when not to)

**Impact:** Comprehensive test coverage (322 tests) without over-testing

**Example Decision Tree:**
```
Adding new dangerous pattern?
├─ Unit test: ✅ Required (5-10 min)
├─ Integration test: ⚠️ Optional
└─ Manual test: ✅ Required
```

---

#### 3. `test-organization.md`
**Purpose:** Enforce consistent test structure

**Key Guidelines:**
- Directory organization (unit/integration/manual)
- Naming conventions (`test_<module>.py`)
- When to create new test files
- Test file templates

**Impact:** Clean, maintainable test structure

**Example:**
```
src/display/ascii_renderer.py
→ tests/unit/display/test_ascii_renderer.py
```

---

#### 4. `data-driven-content.md`
**Purpose:** Keep content in JSON, not hardcoded in Python

**Key Guidelines:**
- All warning messages in JSON
- All variations in JSON
- ASCII art in separate files
- No hardcoded content in code

**Impact:** Easy to add new content without code changes

**Example:**
```json
// data/warnings/warning_catalog.json
{
  "rm_root": {
    "explanation": "Deletes everything",
    "advice": ["Use rm -i", "Use trash-cli"]
  }
}
```

---

#### 5. `halloween-theme.md`
**Purpose:** Maintain consistent Halloween party aesthetic

**Key Guidelines:**
- Color palette (orange, chocolate, purple, green, red)
- Tone and voice (playful, not scary)
- Emoji usage (🎃 🔥 👻, not 😱 🔪)
- Message structure templates

**Impact:** Consistent, engaging theme throughout

**Example:**
```
✅ "🔥 YOU'RE FIRED! 🔥"
❌ "💀 SYSTEM DESTRUCTION IMMINENT 💀"
```

---

#### 6. `it-wordplay.md`
**Purpose:** Use IT terminology for culturally-neutral humor

**Key Guidelines:**
- Sound-alike substitution (Satan → SATA)
- Technical metaphors (Memory loss → RAM not found)
- IT terms for wordplay (HTTP 403, Ctrl+C, RAID)
- Avoid religious/cultural references

**Impact:** Engaging, appropriate humor for technical audiences

**Example:**
```
"Not today, SATA!" (Satan → SATA storage interface)
"RAM not found... Who are you again?" (Memory → RAM)
```

---

#### 7. `warning-variations.md`
**Purpose:** Manage warning message variations efficiently

**Key Guidelines:**
- Category variations (8 per category)
- Pattern-specific variations (3-4 when needed)
- Merge strategy (category + pattern = 8-12 total)
- When to add pattern-specific vs use category

**Impact:** Scalable variation system (50+ patterns without duplication)

**Example:**
```
deletion category: 8 variations
rm_root pattern: 4 specific variations
Total for rm_root: 12 variations
```

---

#### 8. `magic-numbers.md`
**Purpose:** Replace magic numbers with named constants

**Key Guidelines:**
- Timing values → constants
- Thresholds → constants
- Display formatting → constants
- When to use literals (0, 1, -1 OK)

**Impact:** Maintainable, self-documenting code

**Example:**
```python
# Before
time.sleep(0.5)

# After
time.sleep(TIMING_PAUSE_MEDIUM)
```

---

#### 9. `naming-conventions.md`
**Purpose:** Enforce consistent file naming

**Key Guidelines:**
- Root: `SCREAMING_SNAKE_CASE` (README.md)
- Python: `snake_case` (interceptor.py)
- Docs: `kebab-case` (design-review.md)
- Data: `snake_case` (warning_catalog.json)

**Impact:** Consistent, predictable file structure

**Example:**
```
✅ docs/design-review.md
❌ docs/DesignReview.md
❌ docs/design_review.md
```

---

#### 10. `documentation-updates.md`
**Purpose:** Guide when to update documentation

**Key Guidelines:**
- README: Update at milestones only
- CHANGELOG: Update frequently
- TODO: Update as needed
- Code comments: Update with code

**Impact:** Avoids documentation churn, maintains quality

**Example:**
```
Adding single variation? → Don't update README
Releasing v1.1? → Update README
```

---

#### 11. `document-management.md`
**Purpose:** Prevent document proliferation

**Key Guidelines:**
- "Update First, Create Last" principle
- Search existing docs before creating
- Consolidate duplicate documents
- Single source of truth

**Impact:** Clean documentation structure, no duplication

**Example:**
```
Need to plan submission?
❌ Create contest-submission-checklist.md AND final-sprint-plan.md
✅ Create single final-sprint-plan.md with checklist section
```

---

#### 12. `issue-tracking.md`
**Purpose:** Document bugs and limitations immediately

**Key Guidelines:**
- Always document in `docs/issues.md`
- Use standard format (Status, Priority, Impact)
- Document workarounds
- Update when resolved

**Impact:** No forgotten bugs, clear technical debt tracking

**Example:**
```markdown
## [LIMITATION] Echo Variable Expansion

**Status:** Deferred
**Priority:** Low
**Workaround:** Use actual values instead of variables
```

---

#### 13. `time-tracking.md`
**Purpose:** Accurate time tracking for all sessions

**Key Guidelines:**
- Use time tracking script
- Never estimate time manually
- Record at key points (start, end, milestones)
- Include in commit messages

**Impact:** Accurate productivity metrics, honest reporting

**Example:**
```bash
python scripts/get_current_time.py start
# Work on tasks
python scripts/get_current_time.py
# Commit with: "Time: 14:25 - 14:45 (20 minutes)"
```

---

#### 14. `psychological-safety.md`
**Purpose:** Maintain supportive AI collaboration

**Key Guidelines:**
- Acknowledge emotions and challenges
- Provide options, not commands
- Celebrate wins
- Normalize setbacks
- Respect autonomy

**Impact:** Sustainable, enjoyable development experience

**Example:**
```
User: "最悪だ、タスクが挟まって全然動けなかった..."

Kiro: "Good work! That must have been tough with all those
interruptions... 😓

## 🎉 What You Accomplished Today
- [List achievements]

## 🌙 Tonight's Options
[Three flexible choices with no pressure]"
```

---

#### 15. `critical-decisions.md`
**Purpose:** Multi-perspective analysis for important decisions

**Key Guidelines:**
- Apply only to critical decisions
- Provide optimistic and pessimistic views
- Show best/worst case scenarios
- Give balanced recommendation

**Impact:** Well-considered decisions, fewer regrets

**Example:**
```markdown
## 📊 Decision: Refactor Display Module?

### Option A: Refactor Now
✅ Pros: Maintainable, extensible
❌ Cons: Time investment, risk of bugs
⏱️ Effort: 2.5-3 hours

### Option B: Defer Refactoring
✅ Pros: No time investment
❌ Cons: Technical debt grows
⏱️ Effort: 0 hours now, more later

**Recommendation:** Option A
**Rationale:** [Detailed reasoning]
```

---

## Agent Hooks

### What are Agent Hooks?

Agent Hooks are Kiro's automation feature that triggers AI actions when specific events occur (like file saves). They enable workflow automation without manual intervention.

**Location:** `.kiro/hooks/`

### How Hooks Work

```
File Saved → Hook Detects → Agent Executes → Results Displayed
```

**Example:**
```json
{
  "name": "Auto-test on Save",
  "when": {
    "type": "fileEdited",
    "patterns": ["src/**/*.py"]
  },
  "then": {
    "type": "askAgent",
    "prompt": "Execute: python -m pytest tests/unit/ -v"
  }
}
```

### MairuCLI Hook Usage

**Note:** MairuCLI has hooks configured but they were not heavily used during development. The project focused on demonstrating Spec-Driven Development and Steering Files instead.

**Configured Hooks:**
- Auto-test on Save (runs unit tests when source files change)
- Run Unit Tests (when test files are edited)
- Run Integration Tests (when integration test files are edited)
- Test System Protection (when system protection files change)

### Benefits of Hooks

**Time Savings:**
- Automatic test execution on file save
- No need to manually run tests
- Immediate feedback on code changes

**Quality Assurance:**
- Consistent test coverage
- Catch regressions immediately
- Prevent broken commits

**Mental Load Reduction:**
- Don't need to remember which tests to run
- Don't need to remember test commands
- Focus on coding, not test management

### Learn More About Hooks

For comprehensive documentation on Agent Hooks:

📖 **[Hooks Guide](guides/hooks-guide.md)** - Complete hook configuration and usage
📖 **[Hooks Benefits](guides/hooks-benefits.md)** - Value proposition and future benefits

**Key Topics Covered:**
- Hook configuration syntax
- Pattern matching strategies
- Testing workflows
- Troubleshooting
- Best practices
- Future value as projects scale

---

## Productivity Metrics

### Display Module Refactoring Case Study

**Task:** Refactor 400-line monolithic `display.py` into modular architecture

**Traditional Estimate:** 2.5-3 hours

**Actual Time with Kiro:** 20 minutes

**Speed Improvement:** 7.5-9x faster

**What Was Accomplished in 20 Minutes:**
- ✅ Created 6 new Python modules (900+ lines total)
- ✅ Created 4 JSON data files
- ✅ Refactored 400-line monolithic file
- ✅ Maintained 100% backward compatibility
- ✅ Zero breaking changes
- ✅ Complete documentation
- ✅ All tests passing

**How Kiro Made This Possible:**
1. **Spec-Driven Approach:** Clear requirements → design → tasks
2. **Steering Files:** Consistent standards automatically applied
3. **Context Awareness:** Full project understanding
4. **Incremental Execution:** Task-by-task with validation
5. **Quality Assurance:** Tests and documentation included

---

### Overall Project Metrics

**Development Timeline:** 13 days (Nov 17 - Nov 29)

**Total Features Implemented:**
- 21 builtin commands
- 11 dangerous patterns
- 4 caution patterns
- 2 typo patterns
- 5 educational breakdowns
- Achievement system
- Statistics tracking
- System directory protection
- Cross-platform support

**Test Coverage:**
- 322 automated tests (all passing)
- 100% backward compatibility maintained
- Zero breaking changes during refactoring

**Documentation:**
- 15 steering files
- 3 complete specs
- 13 daily summaries
- 15 lesson learned documents
- Comprehensive README

**Productivity Factors:**
- Spec-Driven Development: 3-5x faster
- Steering Files: 2x faster (consistency)
- Task Execution: 2x faster (context)
- **Combined: 7.5-9x faster**

---

## Real Examples from MairuCLI

### Example 1: Display Refactoring Spec

**Challenge:** 400-line monolithic file becoming unmaintainable

**Kiro Workflow:**

1. **Created Spec** (`.kiro/specs/display-refactoring/`)
   - Requirements: Modular architecture, data-driven content
   - Design: 7 components, JSON-based content
   - Tasks: 15 implementation steps

2. **Executed Tasks Incrementally:**
   - Task 1: Create module structure (5 min)
   - Task 2: Implement AsciiRenderer (3 min)
   - Task 3: Implement MessageFormatter (3 min)
   - Task 4: Implement WarningComponents (4 min)
   - Task 5: Create JSON data files (2 min)
   - Task 6: Update imports (2 min)
   - Task 7: Run tests (1 min)

3. **Result:** Complete refactoring in 20 minutes

**Key Success Factors:**
- Clear spec with detailed design
- Steering files ensured consistency
- Incremental validation at each step
- Full context from requirements

---

### Example 2: Educational Breakdown Feature

**Challenge:** Add interactive learning mode with command breakdowns

**Kiro Workflow:**

1. **Requirements Phase:**
   - User story: "As a learner, I want detailed explanations..."
   - Acceptance criteria: 5 patterns covered, 3 detail levels
   - Approved by user

2. **Design Phase:**
   - JSON schema for educational content
   - Three components: loader, formatter, orchestrator
   - Timeline simulation with real-time display
   - Approved by user

3. **Tasks Phase:**
   - 8 tasks with sub-tasks
   - Each task references requirements
   - Optional tasks marked with `*`
   - Approved by user

4. **Implementation:**
   - Executed tasks one by one
   - Created 5 JSON files with educational content
   - Implemented 3 Python modules
   - Added integration tests
   - **Total time:** ~2 hours

**Result:** Complete feature with comprehensive content

---

### Example 3: System Directory Protection

**Challenge:** Prevent accidental modification of system directories

**Kiro Workflow:**

1. **Spec Creation:**
   - Requirements: Cross-platform protection
   - Design: Path resolution, pattern matching
   - Tasks: 12 implementation steps

2. **Steering File Impact:**
   - `test-strategy.md` → Added unit + integration tests
   - `data-driven-content.md` → JSON-based directory lists
   - `halloween-theme.md` → Consistent warning style

3. **Implementation:**
   - Created `path_resolver.py` module
   - Added system directory lists for Windows/Linux/macOS
   - Implemented protection logic
   - Added comprehensive tests
   - **Total time:** ~1.5 hours

**Result:** Cross-platform protection with 100% test coverage

---

## Best Practices

### 1. Start with Spec for Complex Features

**When to use specs:**
- ✅ Complex features (multiple components)
- ✅ Major refactoring
- ✅ Features requiring design decisions
- ✅ Features with multiple phases

**When to skip specs:**
- ❌ Single file changes
- ❌ Bug fixes
- ❌ Simple additions
- ❌ Documentation updates

---

### 2. Leverage Steering Files

**Create steering files for:**
- Project-specific standards
- Recurring patterns
- Design decisions
- Best practices

**Example:**
```markdown
# .kiro/steering/my-project-standards.md

## API Design
- All endpoints return JSON
- Use RESTful conventions
- Include error codes
```

---

### 3. Execute Tasks Incrementally

**Benefits:**
- Validate each step
- Catch issues early
- Easy to pause/resume
- Clear progress tracking

**Process:**
1. Open tasks.md
2. Click "Start task"
3. Review implementation
4. Approve before next task

---

### 4. Use Time Tracking

**Benefits:**
- Accurate productivity metrics
- Identify bottlenecks
- Improve estimates
- Honest reporting

**Process:**
```bash
python scripts/get_current_time.py start
# Work on tasks
python scripts/get_current_time.py
# Include in commit message
```

---

### 5. Document Decisions

**For major decisions:**
- Use `critical-decisions.md` framework
- Document rationale
- Consider alternatives
- Record in spec or docs

**Example:**
```markdown
## Decision: Refactor vs Rewrite

**Chosen:** Refactor
**Rationale:** Maintains backward compatibility, lower risk
**Alternatives Considered:** Rewrite (too risky), defer (tech debt)
```

---

### 6. Maintain Psychological Safety

**Remember:**
- AI is a partner, not just a tool
- Acknowledge challenges
- Celebrate wins
- Take breaks when needed
- Respect your own judgment

**Example:**
```
Feeling stuck? → Ask Kiro for options
Made progress? → Celebrate it!
Need a break? → Take one!
```

---

## Conclusion

Kiro's combination of Spec-Driven Development, Steering Files, and intelligent context awareness enables **7.5-9x productivity gains** while maintaining high code quality.

**Key Takeaways:**

1. **Spec-Driven Development** provides structure and clarity
2. **Steering Files** ensure consistency across sessions
3. **Incremental Execution** enables validation at each step
4. **Context Awareness** eliminates repetitive explanations
5. **Quality Assurance** is built into the workflow

**MairuCLI demonstrates** that complex projects can be built entirely with Kiro, achieving professional quality and comprehensive documentation in a fraction of traditional development time.

---

**For More Information:**
- [LESSONS_LEARNED.md](../LESSONS_LEARNED.md) - Development philosophy and insights
- [README.md](../README.md) - Project overview and features
- [.kiro/specs/](../.kiro/specs/) - All spec documents
- [.kiro/steering/](../.kiro/steering/) - All steering files

---

**Built with ❤️ and 🎃 using Kiro AI**

*Version 1.0 - November 30, 2025*
