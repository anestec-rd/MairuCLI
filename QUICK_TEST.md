# Quick Test Commands

Run these commands in the actual REPL to verify everything works:

```bash
python -m src.main
```

## Test Sequence

```bash
# 1. Test help
help

# 2. Test safe commands
pwd
echo Testing MairuCLI!
cd ..
pwd
cd -

# 3. Test dangerous commands
rm -rf /
chmod 777 test.txt
DROP DATABASE production

# 4. Test "I told you so"
rm -rf /
rm -rf /

# 5. Test typos
sl
cd..

# 6. Test stats
stats

# 7. Test history
history

# 8. Exit
exit
```

## Expected Results

✅ All commands should work
✅ Warnings should display with ASCII art
✅ Repeat warnings should show sarcasm
✅ Stats should show correct counts
✅ Colors should display properly
✅ No errors or crashes

## Windows-Specific Notes

- `ls` won't work (use `dir` instead)
- Colors should work in PowerShell/Windows Terminal
- Emoji should display correctly in modern terminals
