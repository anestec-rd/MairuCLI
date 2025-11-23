"""Tests for search and file management builtin commands."""

import unittest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch
from src.builtins import BuiltinCommands


class TestSearchCommands(unittest.TestCase):
    """Test cases for search-related builtin commands."""

    def setUp(self):
        """Set up test fixtures."""
        # Create temporary directory for testing
        self.test_dir = tempfile.mkdtemp()
        self.original_cwd = Path.cwd()

    def tearDown(self):
        """Clean up test fixtures."""
        # Remove temporary directory
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_touch_creates_file(self):
        """Test touch command creates a new file."""
        test_file = Path(self.test_dir) / "test.txt"

        with patch('pathlib.Path.cwd', return_value=Path(self.test_dir)):
            result = BuiltinCommands._cmd_touch([str(test_file)])

        self.assertTrue(result)
        self.assertTrue(test_file.exists())

    def test_touch_without_args(self):
        """Test touch command without arguments shows usage."""
        result = BuiltinCommands._cmd_touch([])
        self.assertTrue(result)

    def test_mkdir_creates_directory(self):
        """Test mkdir command creates a new directory."""
        test_dir = Path(self.test_dir) / "newdir"

        result = BuiltinCommands._cmd_mkdir([str(test_dir)])

        self.assertTrue(result)
        self.assertTrue(test_dir.exists())
        self.assertTrue(test_dir.is_dir())

    def test_mkdir_existing_directory(self):
        """Test mkdir command with existing directory."""
        test_dir = Path(self.test_dir) / "existing"
        test_dir.mkdir()

        result = BuiltinCommands._cmd_mkdir([str(test_dir)])

        self.assertTrue(result)

    def test_mkdir_without_args(self):
        """Test mkdir command without arguments shows usage."""
        result = BuiltinCommands._cmd_mkdir([])
        self.assertTrue(result)

    def test_find_with_pattern(self):
        """Test find command with file pattern."""
        # Create test files
        (Path(self.test_dir) / "test1.txt").touch()
        (Path(self.test_dir) / "test2.txt").touch()
        (Path(self.test_dir) / "other.py").touch()

        with patch('pathlib.Path.cwd', return_value=Path(self.test_dir)):
            result = BuiltinCommands._cmd_find(["*.txt"])

        self.assertTrue(result)

    def test_find_without_args(self):
        """Test find command without arguments shows usage."""
        result = BuiltinCommands._cmd_find([])
        self.assertTrue(result)

    def test_grep_finds_pattern(self):
        """Test grep command finds pattern in file."""
        test_file = Path(self.test_dir) / "test.txt"
        test_file.write_text("Hello World\nTest Line\nAnother Line")

        result = BuiltinCommands._cmd_grep(["Test", str(test_file)])

        self.assertTrue(result)

    def test_grep_without_args(self):
        """Test grep command without arguments shows usage."""
        result = BuiltinCommands._cmd_grep([])
        self.assertTrue(result)

    def test_grep_with_only_pattern(self):
        """Test grep command with only pattern shows usage."""
        result = BuiltinCommands._cmd_grep(["pattern"])
        self.assertTrue(result)

    def test_which_builtin_command(self):
        """Test which command with builtin."""
        result = BuiltinCommands._cmd_which(["cd"])
        self.assertTrue(result)

    def test_which_system_command(self):
        """Test which command with system command."""
        result = BuiltinCommands._cmd_which(["python"])
        self.assertTrue(result)

    def test_which_without_args(self):
        """Test which command without arguments shows usage."""
        result = BuiltinCommands._cmd_which([])
        self.assertTrue(result)

    def test_whoami_command(self):
        """Test whoami command returns username."""
        result = BuiltinCommands._cmd_whoami([])
        self.assertTrue(result)

    def test_date_command(self):
        """Test date command returns date."""
        result = BuiltinCommands._cmd_date([])
        self.assertTrue(result)

    def test_hostname_command(self):
        """Test hostname command returns hostname."""
        result = BuiltinCommands._cmd_hostname([])
        self.assertTrue(result)

    def test_tree_command(self):
        """Test tree command displays directory structure."""
        # Create test directory structure
        test_subdir = Path(self.test_dir) / "subdir"
        test_subdir.mkdir()
        (test_subdir / "file.txt").touch()

        result = BuiltinCommands._cmd_tree([self.test_dir])

        self.assertTrue(result)

    def test_tree_without_args(self):
        """Test tree command without arguments uses current directory."""
        with patch('pathlib.Path.cwd', return_value=Path(self.test_dir)):
            result = BuiltinCommands._cmd_tree([])

        self.assertTrue(result)

    def test_tree_nonexistent_directory(self):
        """Test tree command with nonexistent directory."""
        result = BuiltinCommands._cmd_tree(["/nonexistent/path"])
        self.assertTrue(result)

    def test_all_new_commands_registered(self):
        """Test that all new commands are registered as builtins."""
        new_commands = ['touch', 'mkdir', 'find', 'grep', 'which',
                       'whoami', 'date', 'hostname', 'tree']

        for cmd in new_commands:
            self.assertTrue(
                BuiltinCommands.is_builtin(cmd),
                f"{cmd} should be registered as builtin"
            )


if __name__ == '__main__':
    unittest.main()
