# MairuCLI Documentation

**Last Updated:** 2025-11-30 (Day 14)

This directory contains all documentation for the MairuCLI project.

---

## 📁 Directory Structure

### 🎨 design/
**Design documents and technical specifications**

Contains architectural designs, system schemas, and design decisions.

- `category-based-variations-design.md` - Warning variation system design
- `caution-warnings-design.md` - Three-tier warning system
- `design-review.md` - Overall design review
- `educational-content-schema.md` - JSON schema for educational content

**Audience:** Developers, architects, technical reviewers

---

### 📖 guides/
**How-to guides and best practices**

Practical guides for using and extending MairuCLI features.

- `cross-platform-consistency.md` - Cross-platform development guide
- `hooks-benefits.md` - Benefits of using Kiro hooks
- `hooks-guide.md` - Kiro Agent Hooks configuration guide

**Audience:** Developers, contributors

---

### 💡 lessons/
**Lessons learned during development**

Insights and reflections from building MairuCLI with Kiro AI.

Contains lessons covering:
- Development philosophy
- AI collaboration
- Spec-Driven Development
- Quality and responsibility
- Practical challenges
- And more...

See [lessons/README.md](lessons/README.md) for full index.

**Audience:** Developers, AI tool users, project managers

**Value:** Demonstrates development process and Kiro's capabilities

---

### 📚 reference/
**Reference materials and background information**

- `cli-dangers.md` - Comprehensive list of dangerous CLI commands
- `cli-incidents.md` - Real-world CLI incident examples
- `judging-criteria.md` - Contest judging criteria

**Audience:** All users, researchers

---

### 📦 archive/
**Development process archive**

Historical records of the development process, including:

- `daily/` - Daily development summaries (Day 1-13)
- `planning/` - Planning documents and action plans
- `analysis/` - Analysis reports and reviews
- `testing/` - Test reports and verification results
- `development-timeline.md` - Complete development timeline
- `ideas-log.md` - Initial ideas and brainstorming
- `initial-brainstorm.md` - Project inception notes

**Audience:** Developers, process analysts, contest judges

**Value:** Demonstrates development transparency and Kiro workflow

---

### 💬 comments/
**Comment management system**

Internal system for managing code comments and translations.

- `comments_en.md` - English comments
- `comments_ja.txt` - Japanese source comments

**Audience:** Internal use

---

## 📄 Root-Level Documents

### dangerous-patterns.md
**Comprehensive dangerous command reference**

Detailed documentation of all 11 dangerous patterns detected by MairuCLI, including:
- Pattern descriptions
- Real-world incidents
- Why they're dangerous
- Safe alternatives

**Audience:** All users, security researchers

---

### issues.md
**Known issues and limitations**

Tracks known bugs, limitations, and deferred features.

**Audience:** Developers, users, contributors

---

## 🎯 Quick Navigation

### For New Users
1. Start with [../README.md](../README.md) - Project overview
2. Read [dangerous-patterns.md](dangerous-patterns.md) - Understand what MairuCLI protects against
3. Check [issues.md](issues.md) - Known limitations

### For Developers
1. Review [design/](design/) - Understand architecture
2. Read [guides/](guides/) - Learn best practices
3. Check [lessons/](lessons/) - Learn from development experience

### For Contest Judges
1. Read [lessons/](lessons/) - Development insights and Kiro usage
2. Review [archive/](archive/) - Development process transparency
3. Check [design/](design/) - Technical depth

### For Contributors
1. Read [guides/](guides/) - Development guidelines
2. Review [design/](design/) - System architecture
3. Check [issues.md](issues.md) - Known issues and TODOs

---

## 🔄 Maintenance

### Adding New Documents

**Design documents** → `design/`
- Architectural decisions
- System schemas
- Technical specifications

**Guides** → `guides/`
- How-to documents
- Best practices
- Usage instructions

**Lessons** → `lessons/`
- Development insights
- Reflections
- Learning experiences
- Update `lessons/README.md`

**Development records** → `archive/`
- Daily summaries
- Planning documents
- Analysis reports
- Test reports

**Reference materials** → `reference/`
- Background information
- External references
- Research materials

### Updating This README

When adding new directories or significantly changing structure:
1. Update the Directory Structure section
2. Update Quick Navigation if needed
3. Update Documentation Statistics
4. Update Last Updated date

---

## 🎓 Documentation Philosophy

### Transparency
All development process is documented and accessible.

### Organization
Clear separation between project docs and process records.

### Discoverability
Easy to find what you need through clear structure and this README.

### Maintainability
Consistent conventions make it easy to add new documents.

---

## 📞 Questions?

For questions about:
- **Project usage** → See [../README.md](../README.md)
- **Development process** → See [lessons/](lessons/)
- **Technical details** → See [design/](design/)
- **Known issues** → See [issues.md](issues.md)

---

**This documentation structure was established on Day 14 to improve organization and discoverability for the Kiroween 2025 contest submission.**

