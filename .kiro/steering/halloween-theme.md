---
inclusion: always
---

# Halloween Theme Design Guidelines for MairuCLI

## Core Aesthetic Philosophy

MairuCLI embraces a **"Halloween Party"** aesthetic rather than genuine horror. Think:
- 🎃 Trick-or-treating with friends
- 🍬 Candy and costumes
- 🎉 Fun and festive
- NOT: 😱 Jump scares or psychological horror

## Color Palette

### Primary Colors
```
Orange (#FF8C00 / ANSI 208)
- Use for: Primary warnings, headers, emphasis
- Represents: Pumpkins, autumn, warmth
- ANSI code: \033[38;5;208m

Chocolate Brown (#D2691E / ANSI 130)
- Use for: Body text, secondary information
- Represents: Chocolate candy, earth tones
- ANSI code: \033[38;5;130m
```

### Accent Colors
```
Purple (#9370DB / ANSI 141)
- Use for: Highlights, special effects
- Represents: Mystery, magic, twilight
- ANSI code: \033[38;5;141m

Green (#32CD32 / ANSI 46)
- Use for: Success messages, safe alternatives
- Represents: Slime, glow-in-the-dark, monsters
- ANSI code: \033[38;5;46m

Red (#DC143C / ANSI 196)
- Use for: Danger warnings, critical alerts
- Represents: Blood (comedic), urgency
- ANSI code: \033[38;5;196m
```

### Usage Rules
1. **Never use more than 3 colors in a single message**
2. **Always reset color after use**: `\033[0m`
3. **Provide monochrome fallback** for accessibility
4. **Test on both light and dark terminals**

## Typography & Symbols

### Emoji Usage
Appropriate emojis that fit the Halloween party theme:
- 🎃 Pumpkin - For general Halloween vibes
- 🔥 Fire - For "YOU'RE FIRED" and deletion warnings
- 💀 Skull - For serious warnings (use sparingly)
- 👻 Ghost - For mysterious or unexpected behavior
- 🍬 Candy - For rewards or positive feedback
- 🦇 Bat - For night/dark theme elements
- 🕷️ Spider - For bugs or errors
- 🧙 Wizard - For magic/automation features

**Avoid:**
- 😱 Genuine fear emojis
- 🔪 Violence-related emojis
- 🩸 Gore-related emojis

### ASCII Art Style
- **Width**: 60-80 characters maximum
- **Style**: Blocky, retro, terminal-friendly
- **Tone**: Cartoonish, not realistic
- **Examples**:
  - Friendly jack-o'-lantern faces
  - Cute ghosts
  - Silly monsters
  - Steam locomotive (for sl typo)

## Tone & Voice

### Writing Style
- **Playful**: Use puns and wordplay
- **Educational**: Always include learning value
- **Encouraging**: Never shame the user
- **Memorable**: Make mistakes fun to encounter

### Example Tone Comparisons

❌ **Too Scary:**
```
FATAL ERROR: Your system is about to be destroyed.
All your data will be lost forever.
There is no escape.
```

❌ **Too Boring:**
```
Error: The command 'rm -rf /' is dangerous.
Please do not execute this command.
```

✅ **Just Right:**
```
🔥 YOU'RE FIRED! 🔥
(And so is your entire filesystem!)

Whoa there! That command would delete EVERYTHING.
Let's not turn this into a real horror story, okay?

💡 Try this instead: Use 'rm -i' for interactive mode,
or 'trash-cli' to safely move files to trash.
```

## Message Structure Templates

### Danger Warning Template
```
[EMOJI] [PUNNY HEADLINE] [EMOJI]
(Subheadline with wordplay)

[What the command does - 1 sentence]
[Why it's dangerous - 1 sentence]

[Real-world incident reference - optional]

💡 Safe alternative: [Actionable advice]
```

### Typo Entertainment Template
```
[EMOJI] Oops! Did you mean '[correct_command]'? [EMOJI]

[Fun ASCII art or animation]

[Brief explanation of the typo]
[Offer to execute correct command]
```

### Success/Safe Action Template
```
✅ [POSITIVE MESSAGE]

[Brief confirmation of what happened]
[Optional: Educational tip]
```

## Seasonal Variations (Future Enhancement)

While maintaining the core Halloween theme, consider subtle variations:
- **October**: Full Halloween mode
- **Other months**: Toned-down version (fewer emojis, simpler colors)
- **Configuration**: Allow users to adjust "spookiness level"

## Accessibility Considerations

### Color Blindness
- Don't rely solely on color to convey meaning
- Use symbols and text labels
- Provide `--no-color` flag

### Screen Readers
- Ensure emoji don't break screen reader flow
- Provide text alternatives for ASCII art
- Use semantic structure in messages

### Cognitive Load
- Keep messages concise (3-5 lines max)
- Use clear hierarchy (headline → explanation → action)
- Avoid overwhelming with too many visual effects

## Examples of Good vs. Bad Design

### Example 1: rm -rf / Warning

✅ **Good:**
```
🔥 YOU'RE FIRED! 🔥
(And so is your entire filesystem!)

This command deletes EVERYTHING on your system.
No undo button. No trash bin. Just... gone.

💡 Safe alternative: Use 'rm -i' for confirmation prompts.
```

❌ **Too Scary:**
```
💀 SYSTEM DESTRUCTION IMMINENT 💀
YOUR CAREER IS OVER
ALL DATA WILL BE PERMANENTLY ERASED
THERE IS NO HOPE
```

❌ **Too Bland:**
```
Error: Dangerous command detected.
Command: rm -rf /
Action: Blocked
```

### Example 2: sl Typo

✅ **Good:**
```
🚂 Choo choo! All aboard the typo train! 🚂

[ASCII art of steam locomotive]

Looks like you meant 'ls' (list files).
Want me to run that instead? (y/n)
```

❌ **Too Serious:**
```
Command not found: sl
Did you mean: ls
```

## Implementation Notes

### Color Testing Checklist
- [ ] Test on macOS Terminal (light theme)
- [ ] Test on macOS Terminal (dark theme)
- [ ] Test on Windows Terminal
- [ ] Test on Linux GNOME Terminal
- [ ] Test on iTerm2
- [ ] Verify color reset works properly
- [ ] Check for color bleeding between messages

### ASCII Art Guidelines
- Store in separate `.txt` files
- Include metadata (width, height, color scheme)
- Provide both colored and plain versions
- Test with `cat` command before integration

### Emoji Compatibility
- Use widely-supported emoji (Unicode 12.0 or earlier)
- Provide text fallback for unsupported terminals
- Test on Windows (emoji support varies)

## Inspiration Sources

### Good Examples
- `sl` command (steam locomotive)
- `cowsay` (friendly ASCII art)
- `lolcat` (rainbow colors, but we use Halloween colors)
- Halloween candy packaging (bright, fun, inviting)

### Avoid
- Horror movie aesthetics
- Dark, gritty designs
- Excessive gore or violence themes
- Anything genuinely frightening

## Future Enhancements

### Customization Options
```json
{
  "theme": {
    "spookiness_level": "medium",  // low, medium, high
    "color_scheme": "halloween",    // halloween, monochrome, custom
    "emoji_enabled": true,
    "ascii_art_enabled": true
  }
}
```

### Seasonal Themes
- Halloween (October): Full theme
- Christmas: Winter variant (optional)
- Default: Toned-down version

---

**Remember:** The goal is to make CLI mistakes **memorable and educational**, not traumatic. We want users to smile when they see our warnings, then learn from them.
