"""
Project path utilities for MairuCLI.

Provides reliable absolute paths to project directories regardless of
current working directory or execution context.
"""

from pathlib import Path
from typing import Optional


def get_project_root() -> Path:
    """
    Get absolute path to project root directory.

    The project root is identified by the presence of src/ directory
    and is determined at import time to ensure consistency.

    Returns:
        Absolute Path to project root directory

    Raises:
        RuntimeError: If project root cannot be determined
    """
    # Start from this file's location
    current_file = Path(__file__).resolve()

    # This file is in src/, so parent is project root
    project_root = current_file.parent.parent

    # Verify this is actually the project root
    if not (project_root / "src").is_dir():
        raise RuntimeError(
            f"Cannot determine project root. "
            f"Expected src/ directory at {project_root}"
        )

    return project_root


def get_data_dir() -> Path:
    """
    Get absolute path to data directory.

    Returns:
        Absolute Path to data/ directory
    """
    return get_project_root() / "data"


def get_ascii_art_dir() -> Path:
    """
    Get absolute path to ASCII art directory.

    Returns:
        Absolute Path to data/ascii_art/ directory
    """
    return get_data_dir() / "ascii_art"


def get_warnings_dir() -> Path:
    """
    Get absolute path to warnings data directory.

    Returns:
        Absolute Path to data/warnings/ directory
    """
    return get_data_dir() / "warnings"


def get_educational_dir() -> Path:
    """
    Get absolute path to educational content directory.

    Returns:
        Absolute Path to data/educational/ directory
    """
    return get_data_dir() / "educational"


def get_builtins_dir() -> Path:
    """
    Get absolute path to builtins data directory.

    Returns:
        Absolute Path to data/builtins/ directory
    """
    return get_data_dir() / "builtins"


# Cache the project root at module import time
_PROJECT_ROOT: Optional[Path] = None


def _get_cached_project_root() -> Path:
    """Get cached project root, computing it once on first access."""
    global _PROJECT_ROOT
    if _PROJECT_ROOT is None:
        _PROJECT_ROOT = get_project_root()
    return _PROJECT_ROOT
