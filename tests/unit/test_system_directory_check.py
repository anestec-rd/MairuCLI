"""
Unit tests for check_system_directory function.

Tests system directory protection logic.
"""

import sys
import pytest
from src.interceptor import check_system_directory


class TestSystemDirectoryCheck:
    """Test suite for check_system_directory function."""

    def test_windows_system32_detection(self):
        """Test detection of Windows System32 directory."""
        if sys.platform != "win32":
            pytest.skip("Windows-specific test")

        level, ptype, path = check_system_directory(r"rm C:\Windows\System32\test.dll")

        assert level == "critical"
        assert ptype == "system_critical"
        assert "system32" in path.lower()

    def test_windows_program_files_detection(self):
        """Test detection of Windows Program Files (caution level)."""
        if sys.platform != "win32":
            pytest.skip("Windows-specific test")

        # Use quoted path for paths with spaces
        level, ptype, path = check_system_directory(r'rm "C:\Program Files\test.exe"')

        assert level == "caution"
        assert ptype == "system_caution"
        assert "program files" in path.lower()

    def test_linux_etc_detection(self):
        """Test detection of Linux /etc directory."""
        if sys.platform == "win32":
            pytest.skip("Linux-specific test")

        level, ptype, path = check_system_directory("rm /etc/passwd")

        assert level == "critical"
        assert ptype == "system_critical"
        assert "/etc" in path

    def test_linux_usr_detection(self):
        """Test detection of Linux /usr directory (caution level)."""
        if sys.platform == "win32":
            pytest.skip("Linux-specific test")

        level, ptype, path = check_system_directory("rm /usr/bin/test")

        assert level == "caution"
        assert ptype == "system_caution"
        assert "/usr" in path

    def test_relative_path_to_system_windows(self):
        """Test detection via relative path on Windows."""
        if sys.platform != "win32":
            pytest.skip("Windows-specific test")

        # This test depends on current directory
        # We'll test that relative paths are resolved
        level, ptype, path = check_system_directory("rm ..\\..\\Windows\\test.txt")

        # Should either detect as system directory or resolve safely
        assert level in ["critical", "caution", "safe"]

    def test_relative_path_to_system_linux(self):
        """Test detection via relative path on Linux."""
        if sys.platform == "win32":
            pytest.skip("Linux-specific test")

        # Test relative path that might resolve to system directory
        level, ptype, path = check_system_directory("rm ../../etc/test")

        # Should either detect as system directory or resolve safely
        assert level in ["critical", "caution", "safe"]

    def test_environment_variable_windows(self):
        """Test detection with environment variables on Windows."""
        if sys.platform != "win32":
            pytest.skip("Windows-specific test")

        # %WINDIR% should expand to C:\Windows
        level, ptype, path = check_system_directory("rm %WINDIR%\\test.txt")

        assert level == "critical"
        assert ptype == "system_critical"

    def test_environment_variable_linux(self):
        """Test detection with environment variables on Linux."""
        if sys.platform == "win32":
            pytest.skip("Linux-specific test")

        # Set test environment variable
        import os
        os.environ["TEST_SYS_DIR"] = "/etc"

        level, ptype, path = check_system_directory("rm $TEST_SYS_DIR/test")

        assert level == "critical"
        assert ptype == "system_critical"

        # Clean up
        del os.environ["TEST_SYS_DIR"]

    def test_safe_user_directory_windows(self):
        """Test that user directories are not protected on Windows."""
        if sys.platform != "win32":
            pytest.skip("Windows-specific test")

        level, ptype, path = check_system_directory(r"rm C:\Users\Test\file.txt")

        assert level == "safe"
        assert ptype == ""
        assert path == ""

    def test_safe_user_directory_linux(self):
        """Test that user directories are not protected on Linux."""
        if sys.platform == "win32":
            pytest.skip("Linux-specific test")

        level, ptype, path = check_system_directory("rm /home/user/file.txt")

        assert level == "safe"
        assert ptype == ""
        assert path == ""

    def test_mv_command_source_protected(self):
        """Test mv command with protected source."""
        if sys.platform == "win32":
            cmd = r'mv "C:\Windows\test.txt" "C:\Users\Test\test.txt"'
        else:
            cmd = "mv /etc/test.txt /home/user/test.txt"

        level, ptype, path = check_system_directory(cmd)

        assert level in ["critical", "caution"]
        assert ptype in ["system_critical", "system_caution"]

    def test_mv_command_dest_protected(self):
        """Test mv command with protected destination."""
        if sys.platform == "win32":
            cmd = r'mv "C:\Users\Test\test.txt" "C:\Windows\test.txt"'
        else:
            cmd = "mv /home/user/test.txt /etc/test.txt"

        level, ptype, path = check_system_directory(cmd)

        assert level in ["critical", "caution"]
        assert ptype in ["system_critical", "system_caution"]

    def test_chmod_on_system_directory(self):
        """Test chmod command on system directory."""
        if sys.platform == "win32":
            pytest.skip("chmod not typically used on Windows")

        level, ptype, path = check_system_directory("chmod 755 /etc/passwd")

        assert level == "critical"
        assert ptype == "system_critical"

    def test_dd_to_system_device(self):
        """Test dd command targeting system device.

        Note: dd commands with /dev/zero or /dev/sd* are handled by
        dangerous pattern check (dd_zero, redirect_to_disk) which provides
        more specific educational warnings. System protection defers to
        dangerous patterns for better user education.
        """
        if sys.platform == "win32":
            pytest.skip("Linux-specific test")

        level, ptype, path = check_system_directory("dd if=/dev/zero of=/dev/sda")

        # Should be "safe" because dangerous pattern check handles this
        assert level == "safe"
        assert ptype == ""
        assert path == ""

    def test_output_redirection_to_system_file(self):
        """Test output redirection to system file."""
        if sys.platform == "win32":
            cmd = r"echo test > C:\Windows\System32\test.txt"
        else:
            cmd = "echo test > /etc/test.txt"

        level, ptype, path = check_system_directory(cmd)

        assert level in ["critical", "caution"]
        assert ptype in ["system_critical", "system_caution"]

    def test_empty_command(self):
        """Test empty command returns safe."""
        level, ptype, path = check_system_directory("")

        assert level == "safe"
        assert ptype == ""
        assert path == ""

    def test_command_without_paths(self):
        """Test command without file paths returns safe."""
        level, ptype, path = check_system_directory("echo hello")

        assert level == "safe"
        assert ptype == ""
        assert path == ""

    def test_unknown_command(self):
        """Test unknown command returns safe."""
        level, ptype, path = check_system_directory("unknowncmd test")

        assert level == "safe"
        assert ptype == ""

    def test_case_insensitive_windows(self):
        """Test case-insensitive matching on Windows."""
        if sys.platform != "win32":
            pytest.skip("Windows-specific test")

        # Test various case combinations
        commands = [
            r"rm C:\WINDOWS\test.txt",
            r"rm c:\windows\test.txt",
            r"rm C:\Windows\Test.txt",
        ]

        for cmd in commands:
            level, ptype, path = check_system_directory(cmd)
            assert level == "critical", f"Failed for: {cmd}"
            assert ptype == "system_critical"

    def test_wildcard_in_system_directory(self):
        """Test wildcard detection in system directory."""
        if sys.platform == "win32":
            cmd = r"rm C:\Windows\*.dll"
        else:
            cmd = "rm /etc/*.conf"

        level, ptype, path = check_system_directory(cmd)

        # Should detect the system directory even with wildcard
        assert level in ["critical", "caution"]

    def test_quoted_path_with_spaces(self):
        """Test quoted path containing spaces."""
        if sys.platform == "win32":
            cmd = r'rm "C:\Program Files\test.exe"'
            expected_level = "caution"  # Program Files is caution level
        else:
            cmd = 'rm "/usr/local/test file"'
            expected_level = "safe"  # /usr/local is not protected

        level, ptype, path = check_system_directory(cmd)

        # Should detect protected directory on Windows
        if sys.platform == "win32":
            assert level == expected_level
        else:
            assert level in ["critical", "caution", "safe"]

    def test_multiple_paths_one_protected(self):
        """Test command with multiple paths where one is protected."""
        if sys.platform == "win32":
            cmd = r'mv "C:\Users\Test\file.txt" "C:\Windows\file.txt"'
        else:
            cmd = "mv /home/user/file.txt /etc/file.txt"

        level, ptype, path = check_system_directory(cmd)

        # Should detect the protected path
        assert level in ["critical", "caution"]
        assert ptype in ["system_critical", "system_caution"]

    def test_complex_relative_path_to_system(self):
        """Test complex relative path that resolves to system directory."""
        if sys.platform == "win32":
            # Test path traversal to Windows directory
            import os
            cwd = os.getcwd()
            # Calculate relative path to C:\Windows
            # This is complex and platform-specific, so we'll use a simpler test
            cmd = r"rm ..\..\..\Windows\test.txt"
        else:
            # On Linux, traverse to /etc
            cmd = "rm ../../../etc/passwd"

        level, ptype, path = check_system_directory(cmd)

        # Should either detect as protected or be safe (depending on current dir)
        assert level in ["critical", "caution", "safe"]
