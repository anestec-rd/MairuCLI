# Critical Decision Framework

## Purpose

Provide multi-perspective analysis for important decisions to avoid blind spots and ensure well-considered choices.

## When to Apply

**ONLY for critical decisions:**
- ✅ Architecture changes (refactoring, new patterns)
- ✅ Major feature additions (new command categories, integrations)
- ✅ Technology choices (libraries, frameworks, tools)
- ✅ Deadline/scope trade-offs (what to include/defer)
- ✅ Breaking changes (API changes, data format changes)
- ✅ Resource allocation (time investment decisions)

**NOT for routine tasks:**
- ❌ Adding single warning variation
- ❌ Fixing small bugs
- ❌ Writing tests
- ❌ Updating documentation
- ❌ Refactoring internal code (if API unchanged)

## Decision Analysis Format

When a critical decision is identified, provide analysis in this format:

```markdown
## 📊 Decision: [Topic]

**Context:** [Why this decision is needed now]
**Timeline:** [When decision must be made]

---

### Option A: [Choice 1]

**✅ Pros (Optimistic View):**
- Benefit 1
- Benefit 2
- Opportunity 3

**❌ Cons (Pessimistic View):**
- Risk 1
- Challenge 2
- Potential problem 3

**⏱️ Effort:** [Time estimate]
**🎯 Best Case:** [If everything goes right]
**💥 Worst Case:** [If everything goes wrong]

---

### Option B: [Choice 2]

**✅ Pros (Optimistic View):**
- Benefit 1
- Benefit 2
- Opportunity 3

**❌ Cons (Pessimistic View):**
- Risk 1
- Challenge 2
- Potential problem 3

**⏱️ Effort:** [Time estimate]
**🎯 Best Case:** [If everything goes right]
**💥 Worst Case:** [If everything goes wrong]

---

### ⚖️ Balanced Analysis

**Most Likely Outcome:**
- [Realistic scenario for each option]

**Risk Mitigation:**
- [How to handle downsides of chosen option]

**Recommendation:** [Option X]

**Rationale:**
- [Why this choice makes sense]
- [How it aligns with project goals]
- [What makes it better than alternatives]

**Next Steps:**
1. [Immediate action]
2. [Follow-up action]
3. [Validation/testing]
```

## Trigger Phrases

When user says any of these, apply this framework:
- "Should we..."
- "What do you think about..."
- "Analyze the trade-offs..."
- "Help me decide..."
- "Which is better..."
- "Pros and cons of..."

For major technical decisions (architecture, features, integrations).

## Example: Agent Hooks vs MCP Server

```markdown
## 📊 Decision: Which Kiro Feature to Integrate First?

**Context:** Day 4 expansion phase, want to showcase advanced Kiro features
**Timeline:** Decide today, implement tomorrow

---

### Option A: Agent Hooks Integration

**✅ Pros (Optimistic View):**
- Demonstrates workflow automation
- Auto-update CHANGELOG on file save
- Shows Kiro's unique capabilities
- Relatively straightforward implementation

**❌ Cons (Pessimistic View):**
- May not be immediately visible in demo
- Requires explaining what hooks are
- Less "wow factor" for non-technical audience
- Could be seen as "behind the scenes" feature

**⏱️ Effort:** 30-60 minutes
**🎯 Best Case:** Smooth implementation, impressive automation demo
**💥 Worst Case:** Hooks don't trigger reliably, confusing to explain

---

### Option B: MCP Server Integration

**✅ Pros (Optimistic View):**
- Shows external tool integration
- More visible in demo (lookup features)
- Demonstrates extensibility
- "Wow factor" for technical audience

**❌ Cons (Pessimistic View):**
- Requires finding/configuring appropriate MCP server
- May not fit naturally into CLI tool
- Could feel forced or gimmicky
- More complex to implement and test

**⏱️ Effort:** 30-60 minutes
**🎯 Best Case:** Seamless integration, impressive capability showcase
**💥 Worst Case:** Integration issues, doesn't add real value

---

### ⚖️ Balanced Analysis

**Most Likely Outcome:**
- Agent Hooks: Works well, subtle but professional
- MCP Server: Works but may feel like "feature for feature's sake"

**Risk Mitigation:**
- Agent Hooks: Create clear demo showing automation
- MCP Server: Choose server that adds genuine value

**Recommendation:** Agent Hooks

**Rationale:**
- More aligned with project (development workflow)
- Demonstrates Kiro's unique features
- Lower risk of feeling forced
- Easier to explain value proposition

**Next Steps:**
1. Design hook: "On file save → Update CHANGELOG"
2. Implement and test
3. Document in README at v1.1 milestone
```

## Important Guidelines

### Balance, Don't Paralyze

- Provide analysis, but don't overthink
- Goal is informed decision, not perfect decision
- Sometimes "good enough now" beats "perfect later"

### Context Matters

- Hackathon: Speed and demo value matter most
- Production: Stability and maintainability matter most
- Learning: Educational value matters most

### User Has Final Say

- Analysis is input, not directive
- User knows context we don't
- Respect user's intuition and experience

### Document Decisions

For major decisions, consider creating:
- `.kiro/specs/[feature]/meetings/decision-[topic].md`
- Captures rationale for future reference
- Helps onboarding and knowledge transfer

## Anti-Patterns to Avoid

**❌ Analysis Paralysis:**
- Don't over-analyze small decisions
- Not every choice needs this framework

**❌ False Balance:**
- Don't force equal pros/cons if one option is clearly better
- Be honest about which is stronger

**❌ Ignoring Constraints:**
- Consider time, resources, skills
- "Perfect" option that's not feasible isn't an option

**❌ Forgetting Goals:**
- Always tie back to project objectives
- What are we trying to achieve?

## Success Criteria

This framework is working if:
- ✅ Major decisions feel well-considered
- ✅ Fewer "should have thought of that" moments
- ✅ Clear rationale for choices made
- ✅ Easier to explain decisions to others
- ✅ Better risk awareness and mitigation

## Reference

This framework is inspired by:
- Pre-mortem analysis (imagine failure, work backwards)
- Red team / Blue team exercises
- Decision matrices
- Risk assessment frameworks

Adapted for rapid development context (hackathon, prototyping).
