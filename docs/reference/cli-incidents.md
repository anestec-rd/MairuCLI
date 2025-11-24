# Famous CLI Incidents & Disasters

## Purpose
Document real-world CLI disasters to inform MairuCLI's educational content. Each incident provides lessons for dangerous command patterns to detect and warn about.

---

## Major Incidents

### 1. GitLab.com Database Deletion (2017)
**Date:** January 31, 2017
**Command:** `rm -rf /var/opt/gitlab/git-data/repositories`
**Impact:** 300GB of production data lost, 6 hours of downtime

**What Happened:**
- Engineer was trying to stop a runaway replication process
- Accidentally ran deletion command on PRIMARY database instead of secondary
- Backup system had been failing silently for months
- Had to restore from 6-hour-old backup

**Lessons:**
- Always verify which server you're on before destructive commands
- Test backup restoration regularly
- Use confirmation prompts for critical operations
- Implement "read-only" modes for production systems

**MairuCLI Application:**
- ✅ Already detects: `rm -rf` patterns
- 🔴 Could add: Server/environment awareness warnings
- 🔴 Could add: "Are you on the right machine?" prompt

**Educational Message:**
"Even experienced engineers at major companies make this mistake. Always double-check which server you're on!"

---

### 2. Pixar's Toy Story 2 Deletion (1998)
**Date:** 1998 (during production)
**Command:** `rm -rf *` in wrong directory
**Impact:** 90% of Toy Story 2 assets deleted, nearly lost entire film

**What Happened:**
- Someone ran `rm -rf *` in the wrong directory
- Deleted months of animation work
- Backup system was also failing
- Film was saved because one employee had a copy at home (working remotely during maternity leave)

**Lessons:**
- Backups are critical
- Test backup systems regularly
- Remote work can be a lifesaver (literally)
- Always verify current directory before `rm -rf`

**MairuCLI Application:**
- ✅ Already detects: `rm -rf` patterns
- 🟡 Could improve: Show current directory in warning
- 🔴 Could add: "Last backup was X days ago" reminder

**Educational Message:**
"Pixar almost lost Toy Story 2 to this command. Even movie studios aren't immune to CLI mistakes!"

---

### 3. AWS S3 Outage (2017)
**Date:** February 28, 2017
**Command:** Typo in S3 subsystem removal command
**Impact:** Major internet outage, millions of websites affected, 4 hours downtime

**What Happened:**
- Engineer was debugging S3 billing system
- Intended to remove a few servers
- Typo caused removal of much larger set of servers
- Cascading failure took down major portion of internet
- Many websites showed broken images (S3-hosted)

**Lessons:**
- Typos in production commands can have massive impact
- Always use dry-run mode first
- Implement rate limiting on destructive operations
- Have rollback procedures ready

**MairuCLI Application:**
- ✅ Already has: Typo detection (sl, cd..)
- 🔴 Could add: "Dry run" mode suggestions
- 🔴 Could add: Warnings for commands affecting multiple targets

**Educational Message:**
"One typo took down a large portion of the internet. This is why we double-check commands!"

---

### 4. Bumblebee npm Package Incident (2018)
**Date:** 2018
**Command:** `npm install` (malicious package)
**Impact:** Cryptocurrency stolen from developers' machines

**What Happened:**
- Popular npm package "event-stream" was transferred to malicious actor
- Malicious code added to steal cryptocurrency wallet credentials
- Installed by thousands of developers via `npm install`
- Went undetected for months

**Lessons:**
- Supply chain attacks are real
- Verify package sources
- Review dependency changes
- Use package lock files

**MairuCLI Application:**
- 🔴 New pattern: `npm install` without verification
- 🔴 New pattern: `pip install` from untrusted sources
- 🔴 Educational: Teach about supply chain security

**Educational Message:**
"Not all dangers come from obvious commands. Even 'npm install' can be dangerous if you don't verify the package!"

---

### 5. Steam on Linux Bug (2015)
**Date:** January 2015
**Command:** `rm -rf "$STEAMROOT/"*` (with empty variable)
**Impact:** Users' home directories deleted

**What Happened:**
- Steam installer script had a bug
- `$STEAMROOT` variable was empty
- Command expanded to `rm -rf /*`
- Deleted users' entire home directories
- Affected Linux users who ran installer

**Lessons:**
- Always validate variables before using in destructive commands
- Use `${VAR:?}` syntax to fail if variable is unset
- Test scripts with empty/invalid variables
- Implement safety checks in installers

**MairuCLI Application:**
- ✅ Already detects: `rm -rf /` patterns
- 🔴 Could add: Variable expansion warnings
- 🔴 Could add: "Check your variables!" message

**Educational Message:**
"Even professional software can have bugs. This Steam installer deleted users' files because of an empty variable!"

---

### 6. Ansible Playbook Disaster (Various)
**Date:** Ongoing
**Command:** `ansible-playbook` with wrong inventory
**Impact:** Production servers wiped, wrong servers configured

**What Happened:**
- Engineers run Ansible playbooks on wrong environment
- Development playbook runs on production
- Production servers get wiped/reconfigured
- Common mistake in DevOps

**Lessons:**
- Always verify inventory file
- Use different credentials for dev/prod
- Implement approval workflows for production
- Color-code terminal prompts by environment

**MairuCLI Application:**
- 🔴 New pattern: Ansible/automation tool warnings
- 🔴 Educational: Environment awareness
- 🟡 Could add: "Which environment?" prompt

---

### 7. `curl | bash` Attacks (Ongoing)
**Date:** Ongoing threat
**Command:** `curl https://example.com/install.sh | bash`
**Impact:** Arbitrary code execution, malware installation

**What Happened:**
- Many installation instructions use this pattern
- Convenient but extremely dangerous
- Executes code without inspection
- Attacker can serve different content to different IPs
- No way to verify what's being executed

**Lessons:**
- Never pipe untrusted scripts to bash
- Download first, inspect, then execute
- Verify checksums/signatures
- Use package managers when possible

**MairuCLI Application:**
- 🔴 New pattern: `curl | bash`, `wget | sh`
- 🔴 High priority: Very common, very dangerous
- 🔴 Educational: Teach safe installation practices

**Educational Message:**
"This is like inviting a stranger into your house and giving them the keys. Download and inspect scripts before running them!"

---

### 8. `chmod -R 777` on Production (Various)
**Date:** Ongoing
**Command:** `chmod -R 777 /var/www` or similar
**Impact:** Security vulnerabilities, unauthorized access

**What Happened:**
- Developers get permission errors
- Quick "fix": Make everything world-writable
- Creates massive security hole
- Attackers can modify files, inject code
- Common in web hosting environments

**Lessons:**
- Understand Unix permissions
- Use proper user/group ownership
- Never use 777 in production
- Fix the root cause, not the symptom

**MairuCLI Application:**
- ✅ Already detects: `chmod 777` pattern
- 🟡 Could improve: Explain why 777 is dangerous
- 🟡 Could add: Suggest proper permissions (644, 755)

---

### 9. Git Force Push Disasters (Ongoing)
**Date:** Ongoing
**Command:** `git push --force` to main branch
**Impact:** Lost commits, team conflicts, code loss

**What Happened:**
- Developer force-pushes to shared branch
- Overwrites other developers' work
- Commits lost from history
- Team has to recover from backups
- Common in teams without branch protection

**Lessons:**
- Never force-push to shared branches
- Use branch protection rules
- Communicate before force-pushing
- Use `--force-with-lease` instead

**MairuCLI Application:**
- 🔴 New pattern: `git push --force` to main/master
- 🔴 Educational: Version control best practices
- 🟡 Could add: "Are you sure?" with explanation

---

### 10. Docker Volume Deletion (Ongoing)
**Date:** Ongoing
**Command:** `docker volume prune -f` or `docker system prune -a`
**Impact:** Database data loss, persistent data deleted

**What Happened:**
- Developers clean up Docker to save space
- Accidentally delete volumes with database data
- No easy recovery
- Common with Docker beginners

**Lessons:**
- Understand Docker volume persistence
- Backup before pruning
- Use named volumes for important data
- Be careful with `-f` (force) flag

**MairuCLI Application:**
- 🔴 New pattern: Docker destructive commands
- 🔴 Educational: Container data persistence
- 🟡 Could add: Docker-specific warnings

---

## Patterns Identified

### High Priority (Implement Soon)
1. **`curl | bash` pattern** - Extremely dangerous, very common
2. **`npm install` warnings** - Supply chain security
3. **`git push --force`** - Team collaboration disasters
4. **Variable expansion in rm** - Empty variable dangers

### Medium Priority
5. **Docker destructive commands** - Container data loss
6. **Ansible/automation warnings** - Wrong environment
7. **`tar` extraction** - Tar bombs, path traversal

### Low Priority (Future)
8. **SSH credential exposure** - Security best practices
9. **Package manager as root** - Privilege escalation
10. **Compression bombs** - Resource exhaustion

---

## Educational Themes

### Common Threads
1. **"Even experts make mistakes"** - GitLab, AWS, Pixar
2. **"Backups save lives"** - Pixar, GitLab
3. **"Test in safe environment first"** - AWS, Ansible
4. **"Verify before executing"** - All incidents
5. **"One typo can be catastrophic"** - AWS, Steam

### Halloween Metaphors
- `curl | bash` = "Inviting vampires in"
- `chmod 777` = "Leaving all doors unlocked"
- `git push --force` = "Erasing memories"
- `npm install` = "Trick or treat? (Could be either!)"
- `rm -rf` = "Summoning the data destroyer"

---

## Next Steps

1. **Prioritize Patterns**
   - Start with `curl | bash` (highest impact)
   - Add npm/pip warnings (supply chain)
   - Implement git warnings (team collaboration)

2. **Create Specs**
   - One spec per pattern category
   - Include real incident examples
   - Design educational messages

3. **Test with Users**
   - Show real incident stories
   - Measure educational impact
   - Iterate based on feedback

---

## Sources
- GitLab Incident Report: https://about.gitlab.com/blog/2017/02/01/gitlab-dot-com-database-incident/
- AWS S3 Outage: https://aws.amazon.com/message/41926/
- Pixar Story: Various interviews and articles
- npm event-stream: Security advisories
- Steam Bug: GitHub issues and user reports

---

**Last Updated:** 2025-11-24 17:15
**Next Review:** When adding new patterns
