# Absolute Path Requirements

## Purpose

Ensure all file loading uses absolute paths to prevent issues when current working directory changes.

---

## Core Rule

**NEVER use relative paths for loading project data files.**

---

## ❌ WRONG: Relative Path Construction

```python
# DON'T DO THIS
from pathlib import Path

# Bad: Depends on __file__ location and breaks if cwd changes
project_root = Path(__file__).parent.parent.parent
data_path = project_root / "data" / "file.json"

# Bad: Depends on current working directory
data_path = Path("data/file.json")
data_path = Path("../data/file.json")
```

---

## ✅ CORRECT: Use project_paths Utility

```python
# DO THIS
from src.project_paths import (
    get_project_root,
    get_data_dir,
    get_ascii_art_dir,
    get_warnings_dir,
    get_educational_dir,
    get_builtins_dir
)

# Good: Always returns absolute path
data_path = get_data_dir() / "file.json"
art_path = get_ascii_art_dir() / "banner.txt"
```

---

## Available Path Functions

### `get_project_root() -> Path`
Returns absolute path to project root directory.

### `get_data_dir() -> Path`
Returns absolute path to `data/` directory.

### `get_ascii_art_dir() -> Path`
Returns absolute path to `data/ascii_art/` directory.

### `get_warnings_dir() -> Path`
Returns absolute path to `data/warnings/` directory.

### `get_educational_dir() -> Path`
Returns absolute path to `data/educational/` directory.

### `get_builtins_dir() -> Path`
Returns absolute path to `data/builtins/` directory.

---

## When Adding New Features

### Loading Data Files

**Always use `project_paths` utility:**

```python
from src.project_paths import get_data_dir

def load_my_data():
    # Correct: Absolute path
    data_file = get_data_dir() / "my_feature" / "config.json"
    with open(data_file, 'r') as f:
        return json.load(f)
```

### Creating New Loaders

**Follow existing patterns:**

```python
from pathlib import Path
from typing import Optional
from src.project_paths import get_data_dir

class MyLoader:
    def __init__(self, base_path: Optional[Path] = None):
        if base_path is None:
            # Use absolute path from project_paths
            self.base_path = get_data_dir() / "my_feature"
        else:
            self.base_path = Path(base_path)
```

### Adding New Data Directories

**If you need a new data subdirectory:**

1. Add function to `src/project_paths.py`:
```python
def get_my_feature_dir() -> Path:
    """
    Get absolute path to my feature directory.

    Returns:
        Absolute Path to data/my_feature/ directory
    """
    return get_data_dir() / "my_feature"
```

2. Use it in your code:
```python
from src.project_paths import get_my_feature_dir

data_path = get_my_feature_dir() / "config.json"
```

---

## Why This Matters

### Problem with Relative Paths

```python
# User runs from project root
os.getcwd()  # → /path/to/MairuCLI
Path("data/file.json")  # → /path/to/MairuCLI/data/file.json ✓

# User runs cd command to change directory
os.chdir("mydir")
os.getcwd()  # → /path/to/MairuCLI/mydir
Path("data/file.json")  # → /path/to/MairuCLI/mydir/data/file.json ✗
```

### Solution with Absolute Paths

```python
# Always works regardless of current directory
from src.project_paths import get_data_dir

# User runs from project root
os.getcwd()  # → /path/to/MairuCLI
get_data_dir()  # → /path/to/MairuCLI/data ✓

# User runs cd command
os.chdir("mydir")
os.getcwd()  # → /path/to/MairuCLI/mydir
get_data_dir()  # → /path/to/MairuCLI/data ✓ (still correct!)
```

---

## Testing Your Code

### Manual Test

```python
import os
from src.project_paths import get_data_dir

# Change to different directory
os.chdir('mydir')

# Your code should still work
data_path = get_data_dir() / "your_file.json"
print(f"Path exists: {data_path.exists()}")  # Should be True
```

### Automated Test

Add test to verify paths work from any directory:

```python
def test_my_loader_works_from_any_directory():
    import os
    original_dir = os.getcwd()

    try:
        # Change to different directory
        os.chdir('mydir')

        # Your loader should still work
        loader = MyLoader()
        data = loader.load_data()

        assert data is not None
    finally:
        os.chdir(original_dir)
```

---

## Code Review Checklist

When reviewing code, check for:

- [ ] No `Path(__file__).parent.parent` constructions
- [ ] No `Path("data/...")` relative paths
- [ ] Uses `from src.project_paths import ...`
- [ ] All file loading uses absolute paths
- [ ] New data directories have utility functions

---

## Common Mistakes

### ❌ Mistake 1: Using __file__ for Data Paths

```python
# Wrong
data_dir = Path(__file__).parent.parent / "data"
```

**Fix:**
```python
# Right
from src.project_paths import get_data_dir
data_dir = get_data_dir()
```

### ❌ Mistake 2: Hardcoded Relative Paths

```python
# Wrong
with open("data/config.json") as f:
    config = json.load(f)
```

**Fix:**
```python
# Right
from src.project_paths import get_data_dir
config_path = get_data_dir() / "config.json"
with open(config_path) as f:
    config = json.load(f)
```

### ❌ Mistake 3: Assuming Current Directory

```python
# Wrong
if Path("data").exists():
    # Load data
```

**Fix:**
```python
# Right
from src.project_paths import get_data_dir
if get_data_dir().exists():
    # Load data
```

---

## Summary

**Golden Rule:** Always use `src.project_paths` utility for loading project data files.

**Benefits:**
- ✅ Works from any current directory
- ✅ Works after `cd` commands
- ✅ Works in tests
- ✅ Works when packaged/installed
- ✅ Centralized path management

**Remember:** If you're loading a file from the `data/` directory, use `project_paths`.

---

**This steering file prevents path-related bugs in future development.**
