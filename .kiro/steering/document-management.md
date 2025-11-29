# Document Management Guidelines

## Purpose

Prevent document proliferation and duplication by establishing clear rules for when to create new documents vs updating existing ones.

---

## Core Principle

**"Update First, Create Last"**

Before creating a new document, ALWAYS ask:
1. Does a document with similar purpose already exist?
2. Can I update/extend an existing document instead?
3. Is this truly a new topic that needs its own document?

---

## Rules for Document Creation

### ❌ DON'T Create New Documents When:

1. **Similar content already exists**
   - Example: Don't create "final-sprint-plan.md" if "contest-submission-checklist.md" exists
   - Action: Update the existing document instead

2. **Information can be added to existing document**
   - Example: Don't create "platform-support.md" when it can be a section in README.md
   - Action: Add a new section to existing document

3. **Temporary information**
   - Example: Don't create "today-tasks.md" for daily work
   - Action: Use TODO.md or session notes

4. **Duplicate perspectives on same topic**
   - Example: Don't create multiple "testing strategy" documents
   - Action: Consolidate into single authoritative document

### ✅ DO Create New Documents When:

1. **Completely new topic**
   - Example: New feature spec, new design document
   - Criteria: No existing document covers this topic

2. **Different document type**
   - Example: Spec vs Steering file vs Lesson learned
   - Criteria: Different purpose and audience

3. **Historical record**
   - Example: Daily summaries (day01-summary.md, day02-summary.md)
   - Criteria: Time-stamped snapshots, not meant to be updated

4. **Reference material**
   - Example: API documentation, schema definitions
   - Criteria: Standalone reference that others will link to

---

## Document Lifecycle

### Before Creating

**Checklist:**
- [ ] Search for existing documents on this topic
- [ ] Check if existing document can be extended
- [ ] Verify this is truly a new topic
- [ ] Consider if this should be a section in existing doc

**Search locations:**
- `docs/` - All documentation
- `.kiro/specs/` - Spec documents
- `.kiro/steering/` - Guidelines and standards
- `docs/reports/` - Reports and summaries
- `docs/lessons/` - Lessons learned

### During Creation

**Guidelines:**
- Use clear, descriptive names
- Add creation date and purpose at top
- Link to related documents
- Indicate if this supersedes another document

**Template:**
```markdown
# Document Title

**Created:** YYYY-MM-DD
**Purpose:** [One sentence describing why this document exists]
**Related:** [Links to related documents]
**Supersedes:** [Link to old document if applicable]

---

[Content]
```

### After Creation

**Actions:**
- Update related documents with links
- Add to appropriate index/README
- Consider if old documents should be archived/deleted

---

## Document Organization

### Directory Structure

```
docs/
├── reports/
│   ├── daily/              # Daily summaries (historical)
│   ├── analysis/           # Analysis documents
│   └── planning/           # Planning documents (SINGLE source)
├── design/                 # Design documents
├── guides/                 # User guides
└── lessons/                # Lessons learned

.kiro/
├── specs/                  # Feature specs
│   └── [feature-name]/
│       ├── requirements.md
│       ├── design.md
│       └── tasks.md
└── steering/               # Development guidelines
```

### Naming Conventions

**Planning documents:**
- Use singular, authoritative names
- Example: `final-sprint-plan.md` (not `contest-submission-checklist.md` AND `final-sprint-plan.md`)

**Historical documents:**
- Use date-based names
- Example: `day01-summary.md`, `day02-summary.md`

**Reference documents:**
- Use descriptive, topic-based names
- Example: `dangerous-patterns.md`, `educational-content-schema.md`

---

## Common Scenarios

### Scenario 1: Planning Document

**Situation:** Need to plan contest submission

**Wrong approach:**
1. Create `contest-submission-checklist.md`
2. Later create `final-sprint-plan.md` with similar content
3. Now have two documents with overlapping information

**Right approach:**
1. Create `final-sprint-plan.md` (comprehensive)
2. If checklist is needed, add it as a section
3. Keep single source of truth

### Scenario 2: Feature Documentation

**Situation:** New feature needs documentation

**Wrong approach:**
1. Create `feature-overview.md`
2. Create `feature-guide.md`
3. Create `feature-examples.md`
4. Now have three documents to maintain

**Right approach:**
1. Add feature section to README.md
2. If complex, create single `docs/guides/feature-name.md`
3. Link from README.md

### Scenario 3: Development Notes

**Situation:** Daily development notes

**Wrong approach:**
1. Create `notes-nov-28.md`
2. Create `notes-nov-29.md`
3. Create `current-tasks.md`
4. Now have scattered information

**Right approach:**
1. Use TODO.md for tasks
2. Use daily summaries for historical record
3. Use single planning document for current plan

---

## Document Consolidation

### When to Consolidate

**Indicators:**
- Multiple documents on same topic
- Confusion about which document is current
- Duplicate information across documents
- Documents referencing each other circularly

**Process:**
1. Identify all related documents
2. Choose the most comprehensive as base
3. Merge content from others
4. Delete or archive old documents
5. Update all links

### Example: Contest Submission

**Before:**
- `contest-submission-checklist.md` (basic checklist)
- `final-sprint-plan.md` (comprehensive plan)
- Confusion about which to follow

**After:**
- `final-sprint-plan.md` (single source of truth)
- Includes checklist as section
- Clear, authoritative

---

## Spec Documents

### When to Use Specs

**Criteria:**
- Complex feature requiring structured approach
- Multiple phases (requirements → design → tasks)
- Needs formal documentation
- Will be implemented incrementally

**Structure:**
```
.kiro/specs/[feature-name]/
├── requirements.md    # User stories, acceptance criteria
├── design.md          # Architecture, components, design
└── tasks.md           # Implementation checklist
```

**Example: Contest Submission**

If contest submission is complex enough, create:
```
.kiro/specs/contest-submission/
├── requirements.md    # What needs to be submitted
├── design.md          # How to present the project
└── tasks.md           # Step-by-step submission tasks
```

**Benefits:**
- Structured approach
- Clear phases
- Trackable progress
- Reusable methodology

---

## Lessons Learned

### Document Proliferation Problem

**Problem:**
AI agents (including Kiro) tend to create new documents frequently, leading to:
- Duplicate information
- Confusion about which is current
- Maintenance burden
- Information fragmentation

**Root Cause:**
- Each interaction treated as fresh start
- No memory of existing documents
- Bias toward creation over update

**Solution:**
- Establish "Update First, Create Last" principle
- Add to steering files
- Check existing documents before creating
- Consolidate when duplication detected

### Best Practices

**For AI Agents:**
1. Search existing documents first
2. Propose updates to existing docs
3. Only create new when truly needed
4. Consolidate when duplication found

**For Developers:**
1. Review document structure regularly
2. Consolidate duplicate documents
3. Keep single source of truth
4. Archive historical documents

---

## Quick Reference

### Before Creating Document

**Ask:**
1. Does similar document exist?
2. Can I update existing instead?
3. Is this truly new topic?
4. Should this be a spec?

**Search:**
- `docs/` directory
- `.kiro/specs/` directory
- `.kiro/steering/` directory
- Related documents

### Document Types

| Type | When to Create | Example |
|------|----------------|---------|
| Planning | Single authoritative plan | `final-sprint-plan.md` |
| Historical | Time-stamped snapshot | `day01-summary.md` |
| Reference | Standalone reference | `dangerous-patterns.md` |
| Spec | Complex feature | `.kiro/specs/feature/` |
| Steering | Development guideline | `.kiro/steering/guideline.md` |
| Lesson | Insight or learning | `docs/lessons/topic.md` |

---

## Summary

**Golden Rule:** Update First, Create Last

**Process:**
1. Search for existing documents
2. Consider updating existing
3. Only create if truly new
4. Consolidate when duplication found

**Benefits:**
- Single source of truth
- Less confusion
- Easier maintenance
- Better organization

---

**This steering file prevents document proliferation and maintains clarity.**

**Related:**
- `documentation-updates.md` - When to update documentation
- `naming-conventions.md` - How to name documents

**Added:** 2025-11-29 (Day 13 - Document management lesson)
