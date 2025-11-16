# Lessons Learned: Building MairuCLI with Kiro AI

## Developer's Insights

These are the key lessons learned during the development of MairuCLI using Kiro AI's Spec-Driven Development workflow.

---

## 1. 実際に動くものを見るからこそ分かること、浮かんでくるアイデアがある

### The Power of Working Prototypes

**Lesson:** Ideas emerge from seeing things work, not just from planning.

**What Happened:**
- Started with basic command interception
- Once we saw the warnings display, new ideas naturally emerged:
  - "What if we track repeated commands?"
  - "What if we add sarcastic responses?"
  - "What if we gamify it with achievements?"

**Key Insight:**
> だからこそモックを早めに開発することは大事である
> (That's why developing a working mock early is crucial)

**Practical Application:**
- Phase 1 took only 4 hours instead of planned 12 hours
- Working prototype enabled rapid iteration
- Visual feedback (ASCII art, colors) sparked creative ideas
- Each feature naturally led to the next

**Recommendation:**
- Build the simplest working version first
- Show it, test it, then iterate
- Don't wait for perfection before seeing results

---

## 2. 着手はたやすく、拡張はしやすいネタを考えておくと、後あと細かく動きやすくなる

### Design for Easy Start, Easy Extension

**Lesson:** Choose ideas that are easy to start and easy to extend.

**What Happened:**
- Started with 5 dangerous patterns → Easy to add more
- Basic warning display → Easy to add variations
- Simple statistics → Easy to add achievements
- Pattern matching → Easy to add new patterns

**Key Insight:**
> 着手はたやすく、拡張はしやすいネタを考えておくと、後あと細かく動きやすくなる
> (When you think of ideas that are easy to start and easy to extend, you can move more flexibly later)

**Examples from MairuCLI:**

1. **Pattern System:**
   ```python
   # Easy to start
   DANGEROUS_PATTERNS = {
       "rm_root": {"pattern": r"rm\s+-rf\s+/", ...}
   }

   # Easy to extend
   DANGEROUS_PATTERNS["new_pattern"] = {...}
   ```

2. **Warning Variations:**
   ```python
   # Started with one message
   print("YOU'RE FIRED!")

   # Extended to random variations
   messages = ["YOU'RE FIRED!", "GAME OVER!", "NOPE!"]
   print(random.choice(messages))
   ```

3. **Statistics:**
   ```python
   # Started simple
   _stats = {"dangerous_blocked": 0}

   # Extended easily
   _stats["typos_caught"] = 0
   _achievements = []
   ```

**Recommendation:**
- Use dictionaries for extensible data
- Use functions that can be easily wrapped/extended
- Keep core logic simple and modular
- Think "What if I want to add X later?"

---

## 3. AIとの会話は自分との対話でもある

### AI Conversation as Self-Dialogue

**Lesson:** Conversation with AI is also a dialogue with yourself. Your knowledge shapes AI's responses, which in turn shapes your questions.

**Key Insight:**
> 自分の知識量に応じてAIはより洗練された受け答えを行う。
> 洗練された答えがまた、洗練された問いを生む。
> そうやって良い開発体験が生まれる。
> (AI provides more refined responses based on your knowledge level.
> Refined answers generate refined questions.
> This creates a good development experience.)

**The Virtuous Cycle:**

```
Your Knowledge/Passion
        ↓
Better Questions to AI
        ↓
Better AI Responses
        ↓
New Insights/Ideas
        ↓
Deeper Knowledge
        ↓
(Cycle repeats)
```

**What Happened in This Project:**

1. **Initial Knowledge:**
   - Understood CLI dangers (from CLI_Troubled.md)
   - Had passion for Halloween theme
   - Knew what makes demos engaging

2. **This Led To:**
   - Specific questions about implementation
   - Clear requirements for Kiro
   - Concrete feature ideas

3. **AI Responded With:**
   - Detailed implementation plans
   - Code structure suggestions
   - Enhancement ideas

4. **Which Sparked:**
   - "What about 'I told you so' feature?"
   - "What about achievements?"
   - "What about random variations?"

**Important Distinction:**
> AIの開発をうまくやるのなら、自分の知識、熱量を高めておくこと。
> （それはコーディング／システムの知識というわけではなく、
> ＡＩに作ってもらいたい要件に関する知識・熱意ということ）
>
> (To work well with AI development, increase your knowledge and passion.
> This doesn't mean coding/system knowledge,
> but knowledge and enthusiasm about the requirements you want AI to build.)

**Examples:**

❌ **Vague Request:**
"Make a CLI tool that's safe"

✅ **Informed Request:**
"Create a Halloween-themed CLI wrapper that intercepts dangerous commands like 'rm -rf /', displays ASCII art warnings with educational messages, and uses a 'Don't try this!' reverse psychology approach in the help command"

**The Difference:**
- First request: Generic, unclear, leads to generic responses
- Second request: Specific, passionate, leads to creative solutions

---

## 4. Kiro's Spec-Driven Development Workflow

**What Worked Well:**

1. **Requirements Phase:**
   - EARS format forced clarity
   - INCOSE rules ensured quality
   - Glossary prevented ambiguity

2. **Design Phase:**
   - Clear architecture from the start
   - Known limitations documented early
   - Component boundaries well-defined

3. **Implementation Phase:**
   - Tasks were concrete and actionable
   - Each task built on previous ones
   - No orphaned code

**Time Savings:**
- No "What should I build?" confusion
- No architectural rework
- No scope creep (until we wanted it!)
- Clear stopping points

---

## 5. The Hackathon Mindset

**What Makes a Good Hackathon Project:**

1. **Demo-Friendly Features:**
   - Visual (ASCII art, colors)
   - Interactive (try commands, see results)
   - Funny (sarcasm, achievements)
   - Memorable (unique concept)

2. **Technical Completeness:**
   - Actually works
   - Handles errors gracefully
   - Clean code structure
   - Well-documented

3. **Story to Tell:**
   - Clear problem statement
   - Creative solution
   - Shows technical skill
   - Shows personality

**MairuCLI Hits All Three:**
- ✅ Visual and funny
- ✅ Fully functional
- ✅ Great story about CLI safety education

---

## 6. Practical Tips for AI-Assisted Development

### Do's:
- ✅ Start with clear requirements
- ✅ Build working prototypes early
- ✅ Test frequently
- ✅ Iterate based on what you see
- ✅ Bring your passion and knowledge
- ✅ Ask specific questions
- ✅ Embrace creative ideas that emerge

### Don'ts:
- ❌ Don't wait for perfect planning
- ❌ Don't ignore your instincts
- ❌ Don't be afraid to change direction
- ❌ Don't skip the fun features
- ❌ Don't forget to test in real environment

---

## 7. Time Management Insights

**Original Plan:** 40 hours
**Actual Phase 1:** 4 hours
**Reason:** Good planning + AI assistance + Clear vision

**Key Factors:**
1. Spec-Driven Development eliminated confusion
2. Clear requirements prevented rework
3. Working prototype enabled fast iteration
4. Passion for the project maintained momentum

**Lesson:**
> With AI assistance and good planning, you can move 3-5x faster than traditional development, but only if you bring clear vision and domain knowledge.

---

## 8. The Role of Humor and Personality

**Unexpected Benefit:**
Adding personality (sarcasm, achievements, "I told you so") made:
- Development more fun
- Features more memorable
- Demo more engaging
- Code more enjoyable to write

**Lesson:**
> Don't be afraid to inject personality into your projects. It makes them stand out and makes development more enjoyable.

---

## Conclusion

Building MairuCLI taught me that:

1. **Working prototypes unlock creativity**
2. **Extensible design enables rapid iteration**
3. **Your knowledge and passion amplify AI's effectiveness**
4. **Spec-Driven Development saves massive time**
5. **Personality makes projects memorable**

The best development experience comes from the synergy between:
- Your domain knowledge
- Your creative vision
- AI's implementation capability
- Rapid iteration on working prototypes

---

**Final Thought:**

> AIは道具ではなく、対話相手である。
> 良い対話には、良い質問と、良い聞き手が必要。
> あなたの知識と熱意が、AIを最高の開発パートナーにする。
>
> (AI is not a tool, but a conversation partner.
> Good dialogue requires good questions and a good listener.
> Your knowledge and passion make AI the best development partner.)

---

**Project:** MairuCLI
**Date:** 2025-11-16
**Developer:** [Your Name]
**AI Partner:** Kiro
**Time:** 4 hours (Phase 1 + Bonus Features)
**Result:** Fully functional, demo-ready, fun CLI safety wrapper
