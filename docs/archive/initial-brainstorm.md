# Initial Brainstorming: From Horror CLI to MairuCLI

## Overview

This document captures the initial brainstorming session that led to MairuCLI's concept. It shows the evolution from a pure horror theme to an educational Halloween approach.

**Date:** November 16, 2025
**Status:** Historical record - Concept evolved significantly

---

## Original Concept: "Hanged-up CLI"

### Initial Idea
- **Name:** Hanged-up CLI
- **Theme:** Dark psychological horror
- **Concept:** CLI possessed by a malevolent spirit
- **Tone:** Genuinely frightening, unsettling

### Wordplay
- "hanged" (絞首刑 - execution by hanging)
- "hang-up" (不安の種 - psychological trauma)
- "hang up" (ハングアップ - system freeze)

**Triple meaning:** Death + trauma + system failure

### Planned Features
-絞首刑 (hanging) ASCII art on startup
- Red text on black background
- Gradually darkening text (black on black - hidden messages)
- User must drag to reveal hidden text
- Psychological horror elements
- Unpredictable behavior

---

## Pivot Point: Team Feedback

### The Problem
**Team members didn't like pure horror:**
- Too scary for daily use
- Not fun, just stressful
- Wanted something more lighthearted

### The Request
> "Can we make it more like Halloween? Fun and spooky, not genuinely frightening?"

---

## Evolved Concept: MairuCLI

### New Direction
- **Name:** MairuCLI (参る - "to be troubled" + Kiro wordplay)
- **Theme:** Halloween party aesthetic
- **Concept:** Educational tool with comedic horror
- **Tone:** Fun, memorable, slightly spooky

### Key Changes

**From:**
- Dark horror → Halloween party
- Psychological fear → Comedic warnings
- Hidden messages → Clear education
- Unpredictable → Consistent and helpful

**To:**
- 🎃 Pumpkins and candy
- 🔥 "YOU'RE FIRED" wordplay
- 💡 Educational messages
- 🚂 Typo entertainment (sl → steam locomotive)

---

## Design Philosophy Evolution

### Original: Pure Horror
```
Goal: Make users uncomfortable
Method: Psychological manipulation
Outcome: Memorable through fear
```

### Final: Educational Entertainment
```
Goal: Make learning fun
Method: Halloween-themed warnings
Outcome: Memorable through enjoyment
```

---

## Key Insights from Brainstorming

### 1. AI and Horror Compatibility

**Observation:**
> "AI is good at generating horror content because humans don't want to spend mental energy on disturbing ideas. AI can generate them without psychological cost."

**Application to MairuCLI:**
- AI helps generate creative warning messages
- AI suggests ASCII art ideas
- AI maintains consistent Halloween tone
- Human provides the "why it's scary" insight

**Example:**
- AI suggests: "Use jump scares"
- Human insight: "No, use active discovery (drag to reveal)"
- Result: User chooses to see scary content (more impactful)

### 2. Parody Requires Authenticity

**Observation:**
> "Parody only works if the original works well. CLI must function properly for the horror elements to be effective."

**Application to MairuCLI:**
- Must implement real CLI functionality
- Builtin commands (cd, pwd, echo) must work
- Safe commands must execute normally
- Only then can dangerous commands be parodied effectively

**This led to:** Builtin commands implementation (critical design decision)

### 3. CLI "Aru-Aru" (Common Experiences)

**Observation:**
> "Engineers have shared CLI horror stories. Tap into that collective experience."

**Application to MairuCLI:**
- Reference real incidents (GitLab data loss)
- Use familiar patterns (rm -rf /, chmod 777)
- Leverage shared trauma (we've all been there)
- Make it relatable, not abstract

**This led to:** CLI_Troubled.md research and pattern selection

---

## Rejected Ideas

### Too Scary
- ❌ Gradually darkening text (confusing, not fun)
- ❌ Random command failures (frustrating)
- ❌ Persistent "haunting" across sessions (annoying)
- ❌ Genuine jump scares (not educational)

### Too Complex
- ❌ AI-generated dynamic horror (40-hour limit)
- ❌ Learning user patterns to scare them (creepy, not fun)
- ❌ Psychological profiling (ethical concerns)

### Not Educational
- ❌ Pure entertainment with no learning value
- ❌ Jokes without explanations
- ❌ Scary without actionable advice

---

## Final Concept Validation

### What We Kept
- ✅ Halloween theme (not pure horror)
- ✅ ASCII art (visual impact)
- ✅ Wordplay ("YOU'RE FIRED")
- ✅ Color scheme (orange, red, purple)
- ✅ Educational value

### What We Added
- ✅ Real-world incident examples
- ✅ Safe alternatives in warnings
- ✅ Typo entertainment
- ✅ Builtin commands for authenticity
- ✅ Clear educational purpose

### What We Removed
- ❌ Psychological horror elements
- ❌ Hidden/darkening text
- ❌ Unpredictable behavior
- ❌ Genuine fear tactics

---

## Lessons for Future Projects

### 1. User Feedback is Critical
- Initial concept was too extreme
- Team feedback led to better product
- Compromise improved the design

### 2. Context Matters
- Horror for horror's sake → rejected
- Horror for education → accepted
- Purpose justifies the approach

### 3. Constraints Breed Creativity
- 40-hour limit forced focus
- Halloween theme provided clear direction
- Educational purpose gave structure

### 4. AI as Creative Partner
- AI generates ideas without mental cost
- Human provides insight and direction
- Collaboration produces better results

---

## Evolution Timeline

```
Day 1, Morning: "Hanged-up CLI" concept
              ↓
Day 1, Noon:  Team feedback - "too scary"
              ↓
Day 1, Afternoon: Pivot to "MairuCLI"
              ↓
Day 1, Evening: Halloween theme solidified
              ↓
Day 1, Night: Educational focus added
              ↓
Result: MairuCLI as we know it
```

---

## Conclusion

### From Horror to Halloween

The journey from "Hanged-up CLI" to "MairuCLI" shows the importance of:
- Listening to feedback
- Adapting to constraints
- Finding the right balance
- Maintaining core value (education)

### The Right Decision

**Original concept:** Technically interesting, but limited appeal
**Final concept:** Broadly useful, fun, and educational

**Outcome:** Better product, wider audience, clearer purpose

---

## Appendix: Original Japanese Notes

**Note:** The original brainstorming was conducted in Japanese. Key concepts:

- **参る (mairu):** To be troubled, to surrender, to be defeated
- **解雇 (kaiko):** To be fired (from a job)
- **ハロウィン (harowin):** Halloween
- **コミカル (komikaru):** Comedic, humorous

These linguistic elements influenced the final design, particularly the wordplay in warning messages.

---

**Status:** Historical document
**Current Project:** MairuCLI (evolved concept)
**Last Updated:** November 16, 2025
