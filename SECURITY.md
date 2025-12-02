# Security Policy

## Important Disclaimer

**MairuCLI is an educational tool, NOT a production security solution.**

This project is designed for:
- ✅ Learning about CLI safety
- ✅ Demonstrating common mistakes
- ✅ Educational workshops and demonstrations
- ✅ Entertainment and engagement

This project is NOT designed for:
- ❌ Production environments
- ❌ Actual security enforcement
- ❌ Replacing proper access controls
- ❌ Mission-critical systems

## Known Limitations

### Pattern Matching Can Be Bypassed

MairuCLI uses regex pattern matching to detect dangerous commands. This approach has inherent limitations:

- **Obfuscation**: Commands can be obfuscated to bypass detection
- **Encoding**: Alternative encodings may not be detected
- **Shell features**: Command substitution, aliases, and functions can bypass detection
- **New patterns**: Unknown dangerous patterns are not detected

**Example bypasses:**
```bash
# These may bypass detection:
r""m -rf /
$(echo rm) -rf /
alias safe='rm -rf' && safe /
```

### Not Comprehensive

MairuCLI detects common dangerous patterns but cannot catch all possible dangerous commands. It is a learning tool, not a security barrier.

### Safe Commands Pass Through

By design, MairuCLI passes safe commands directly to your system shell. This means:
- Unknown commands will show system error messages
- Safe commands execute normally
- No sandboxing or isolation is provided

## Reporting Security Issues

If you discover a security vulnerability in MairuCLI itself (not bypasses of pattern detection, which are expected), please report it by:

1. **Opening a GitHub Issue** with the `security` label
2. **Describing the vulnerability** clearly
3. **Providing reproduction steps** if applicable

We will respond as quickly as possible.

## What to Report

**DO report:**
- ✅ Code execution vulnerabilities in MairuCLI itself
- ✅ Path traversal issues
- ✅ Injection vulnerabilities in the wrapper
- ✅ Privilege escalation issues

**DON'T report:**
- ❌ Pattern detection bypasses (these are expected limitations)
- ❌ Missing dangerous patterns (open a feature request instead)
- ❌ False positives (open a bug report instead)

## Security Best Practices

If using MairuCLI for educational purposes:

1. **Use in isolated environments**: VMs, containers, or sandboxes
2. **Don't rely on it for security**: It's educational, not protective
3. **Supervise learners**: Monitor usage in educational settings
4. **Explain limitations**: Make sure users understand it's not foolproof
5. **Use proper backups**: Always have backups before demonstrations

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.5.x   | ✅ Yes             |
| < 1.5   | ❌ No              |

## Updates

Security-related updates will be documented in [CHANGELOG.md](CHANGELOG.md) and tagged with `[SECURITY]`.

---

**Remember: MairuCLI is a teaching tool. For production security, use proper access controls, permissions, and security policies.**
