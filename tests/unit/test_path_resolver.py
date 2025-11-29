"""
Unit tests for PathResolver module.

Tests path resolution, normalization, and edge case handling.
"""

import os
import sys
import pytest
from src.path_resolver import PathResolver


class TestPathResolver:
    """Test suite for PathResolver class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.resolver = PathResolver()

    def test_resolve_absolute_path(self):
        """Test that absolute paths are returned unchanged (normalized)."""
        if sys.platform == "win32":
            path = r"C:\Windows\System32"
            result = self.resolver.resolve_path(path)
            assert result.lower() == path.lower()
        else:
            path = "/etc/passwd"
            result = self.resolver.resolve_path(path)
            assert result == path

    def test_resolve_relative_path(self):
        """Test relative path resolution to absolute path."""
        # Get current directory
        cwd = os.getcwd()

        # Test relative path
        result = self.resolver.resolve_path(".")
        # macOS and Windows are case-insensitive but case-preserving
        if sys.platform in ("win32", "darwin"):
            assert result.lower() == cwd.lower()
        else:
            assert result == cwd

        # Test parent directory
        parent = os.path.dirname(cwd)
        result = self.resolver.resolve_path("..")
        if sys.platform in ("win32", "darwin"):
            assert result.lower() == parent.lower()
        else:
            assert result == parent

    def test_expand_user_home(self):
        """Test expansion of ~ to user home directory."""
        home = os.path.expanduser("~")
        result = self.resolver.resolve_path("~")

        # macOS and Windows are case-insensitive but case-preserving
        if sys.platform in ("win32", "darwin"):
            assert result.lower() == home.lower()
        else:
            assert result == home

    def test_expand_environment_variables_windows(self):
        """Test environment variable expansion on Windows."""
        if sys.platform != "win32":
            pytest.skip("Windows-specific test")

        # Set test environment variable
        os.environ["TEST_VAR"] = r"C:\Test"

        # Test %VAR% format
        result = self.resolver.resolve_path("%TEST_VAR%\\file.txt")
        assert "test" in result.lower()
        assert "file.txt" in result.lower()

        # Clean up
        del os.environ["TEST_VAR"]

    def test_expand_environment_variables_unix(self):
        """Test environment variable expansion on Unix."""
        if sys.platform == "win32":
            pytest.skip("Unix-specific test")

        # Set test environment variable
        os.environ["TEST_VAR"] = "/tmp/test"

        # Test $VAR format
        result = self.resolver.resolve_path("$TEST_VAR/file.txt")
        assert "/tmp/test" in result
        assert "file.txt" in result

        # Clean up
        del os.environ["TEST_VAR"]

    def test_path_normalization(self):
        """Test path normalization (separators, redundant parts)."""
        if sys.platform == "win32":
            # Test forward slashes on Windows
            result = self.resolver.resolve_path("C:/Windows/System32")
            assert "\\" in result
            assert "/" not in result

            # Test redundant separators
            result = self.resolver.resolve_path(r"C:\Windows\\System32")
            assert r"\\System32" not in result
        else:
            # Test redundant separators on Unix
            result = self.resolver.resolve_path("/etc//passwd")
            assert "//passwd" not in result

    def test_case_normalization_windows(self):
        """Test case normalization on case-insensitive systems."""
        if sys.platform != "win32":
            pytest.skip("Windows-specific test")

        result1 = self.resolver.resolve_path(r"C:\Windows")
        result2 = self.resolver.resolve_path(r"C:\WINDOWS")
        result3 = self.resolver.resolve_path(r"c:\windows")

        # All should be normalized to same case
        assert result1 == result2 == result3

    def test_empty_path_raises_error(self):
        """Test that empty path raises ValueError."""
        with pytest.raises(ValueError, match="Path cannot be empty"):
            self.resolver.resolve_path("")

    def test_none_path_raises_error(self):
        """Test that None path raises ValueError."""
        with pytest.raises(ValueError, match="Path cannot be empty"):
            self.resolver.resolve_path(None)

    def test_invalid_path_characters(self):
        """Test handling of invalid path characters."""
        # This test is platform-specific
        if sys.platform == "win32":
            # Windows doesn't allow certain characters
            invalid_chars = ['<', '>', ':', '"', '|', '?', '*']
            for char in invalid_chars:
                path = f"C:\\Test{char}File.txt"
                # Should either resolve or raise OSError
                try:
                    result = self.resolver.resolve_path(path)
                    # If it resolves, it should be absolute
                    assert os.path.isabs(result)
                except OSError:
                    # Expected for truly invalid paths
                    pass

    def test_is_subpath_true(self):
        """Test is_subpath returns True for actual subpaths."""
        if sys.platform == "win32":
            parent = r"C:\Windows"
            child = r"C:\Windows\System32"
        else:
            parent = "/etc"
            child = "/etc/passwd"

        assert self.resolver.is_subpath(child, parent) is True

    def test_is_subpath_false(self):
        """Test is_subpath returns False for non-subpaths."""
        if sys.platform == "win32":
            parent = r"C:\Windows"
            child = r"C:\Program Files"
        else:
            parent = "/etc"
            child = "/var"

        assert self.resolver.is_subpath(child, parent) is False

    def test_is_subpath_with_relative_paths(self):
        """Test is_subpath with relative paths."""
        # Create relative paths that resolve to different locations
        cwd = os.getcwd()
        parent_dir = os.path.dirname(cwd)

        # Current directory is subpath of parent
        assert self.resolver.is_subpath(".", "..") is True

        # Parent is not subpath of current
        assert self.resolver.is_subpath("..", ".") is False

    def test_normalize_for_comparison(self):
        """Test path normalization for comparison."""
        if sys.platform == "win32":
            path1 = r"C:\Windows\System32"
            path2 = r"C:/Windows/System32"
            path3 = r"C:\WINDOWS\SYSTEM32"

            norm1 = self.resolver.normalize_for_comparison(path1)
            norm2 = self.resolver.normalize_for_comparison(path2)
            norm3 = self.resolver.normalize_for_comparison(path3)

            # All should normalize to same value
            assert norm1 == norm2 == norm3
        else:
            path1 = "/etc/passwd"
            path2 = "/etc//passwd"

            norm1 = self.resolver.normalize_for_comparison(path1)
            norm2 = self.resolver.normalize_for_comparison(path2)

            assert norm1 == norm2

    def test_trailing_separator_handling(self):
        """Test consistent handling of trailing separators."""
        if sys.platform == "win32":
            path_with = r"C:\Windows\\"
            path_without = r"C:\Windows"
        else:
            path_with = "/etc/"
            path_without = "/etc"

        norm_with = self.resolver.normalize_for_comparison(path_with)
        norm_without = self.resolver.normalize_for_comparison(path_without)

        # Should normalize to same value (without trailing separator)
        assert norm_with == norm_without

    def test_platform_detection(self):
        """Test that platform is correctly detected."""
        assert self.resolver.platform == sys.platform
        assert isinstance(self.resolver.case_sensitive, bool)

        if sys.platform in ['win32', 'darwin']:
            assert self.resolver.case_sensitive is False
        else:
            assert self.resolver.case_sensitive is True

    def test_complex_relative_path(self):
        """Test complex relative path with multiple .. components."""
        # Get current directory
        cwd = os.getcwd()

        # Go up two levels then back down
        complex_path = os.path.join("..", "..", os.path.basename(os.path.dirname(cwd)), os.path.basename(cwd))

        result = self.resolver.resolve_path(complex_path)

        # Should resolve to current directory
        # macOS and Windows are case-insensitive but case-preserving
        if sys.platform in ("win32", "darwin"):
            assert result.lower() == cwd.lower()
        else:
            assert result == cwd
