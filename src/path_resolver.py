"""
Path resolution module for MairuCLI system directory protection.

This module provides utilities to resolve relative paths, expand environment
variables, and normalize paths for cross-platform protection checking.
"""

import os
import sys
from typing import Optional


class PathResolver:
    """Resolves and normalizes file paths for protection checking."""

    def __init__(self):
        """Initialize PathResolver with platform detection."""
        self.platform = sys.platform
        self.case_sensitive = self.platform not in ['win32', 'darwin']

    def resolve_path(self, path: str) -> str:
        """
        Resolve relative path to absolute path with full normalization.

        Args:
            path: Raw path from command (may be relative, contain ~, or env vars)

        Returns:
            Absolute normalized path

        Raises:
            ValueError: If path is empty or None
            PermissionError: If path cannot be accessed
            OSError: If path resolution fails
        """
        if not path:
            raise ValueError("Path cannot be empty")

        try:
            # Expand environment variables ($VAR, %VAR%, ${VAR})
            path = os.path.expandvars(path)

            # Expand user home directory (~)
            path = os.path.expanduser(path)

            # Convert to absolute path
            path = os.path.abspath(path)

            # Normalize path separators and remove redundant separators
            path = os.path.normpath(path)

            # Normalize case for case-insensitive systems
            if not self.case_sensitive:
                path = path.lower()

            return path

        except PermissionError as e:
            # Cannot access path - re-raise for fail-safe handling
            raise PermissionError(f"Cannot access path: {path}") from e
        except Exception as e:
            # Any other error - re-raise for fail-safe handling
            raise OSError(f"Path resolution failed for: {path}") from e

    def is_subpath(self, path: str, parent: str) -> bool:
        """
        Check if path is a subpath of parent directory.

        Args:
            path: Path to check
            parent: Parent directory path

        Returns:
            True if path is under parent directory
        """
        try:
            # Resolve both paths
            resolved_path = self.resolve_path(path)
            resolved_parent = self.resolve_path(parent)

            # Ensure parent ends with separator for accurate comparison
            if not resolved_parent.endswith(os.sep):
                resolved_parent += os.sep

            # Check if path starts with parent
            return resolved_path.startswith(resolved_parent)

        except (ValueError, PermissionError, OSError):
            # If resolution fails, assume it's protected (fail-safe)
            return True

    def normalize_for_comparison(self, path: str) -> str:
        """
        Normalize path for comparison with protected directories.

        Args:
            path: Path to normalize

        Returns:
            Normalized path suitable for string comparison
        """
        try:
            normalized = self.resolve_path(path)

            # Ensure consistent trailing separator handling
            # Remove trailing separator unless it's root
            if len(normalized) > 1 and normalized.endswith(os.sep):
                normalized = normalized.rstrip(os.sep)

            return normalized

        except (ValueError, PermissionError, OSError):
            # If normalization fails, return original (will be caught later)
            return path
