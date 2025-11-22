"""
System protection warning display for MairuCLI.

This module displays educational warnings when users attempt to modify
protected system directories.
"""

from typing import Dict
from src.display.ascii_renderer import AsciiRenderer


# Directory information for educational messages
DIRECTORY_INFO = {
    # Windows directories
    r"c:\windows": {
        "description": "Windows system directory contains core OS files",
        "risk": "Modifying files here can make Windows unbootable",
        "consequence": "System may fail to start, requiring reinstallation",
        "alternatives": [
            "Work in your user directory: C:\\Users\\YourName\\",
            "Use Documents, Downloads, or Desktop folders",
            "Ask an experienced user if you need to modify system files"
        ]
    },
    r"c:\windows\system32": {
        "description": "System32 contains essential Windows components",
        "risk": "Deleting files here will break Windows immediately",
        "consequence": "Windows will crash and become unbootable",
        "alternatives": [
            "NEVER modify System32 unless you're an expert",
            "Use your user directory for all personal files",
            "System files are protected for a reason!"
        ]
    },
    r"c:\program files": {
        "description": "Program Files contains installed applications",
        "risk": "Modifying files here can break installed programs",
        "consequence": "Applications may stop working or crash",
        "alternatives": [
            "Uninstall programs properly using Control Panel",
            "Install personal software in your user directory",
            "Contact the software vendor for support"
        ]
    },

    # Linux/Unix directories
    "/etc": {
        "description": "/etc contains system configuration files",
        "risk": "Incorrect changes can break system services",
        "consequence": "System may become unstable or unbootable",
        "alternatives": [
            "Work in your home directory: /home/username/",
            "Use ~/Documents or ~/Downloads for personal files",
            "Learn about configuration before modifying /etc"
        ]
    },
    "/bin": {
        "description": "/bin contains essential system commands",
        "risk": "Deleting files here breaks basic system functionality",
        "consequence": "System will become unusable",
        "alternatives": [
            "Never modify /bin unless you're a system administrator",
            "Install personal scripts in ~/bin or ~/.local/bin",
            "Use package managers to manage system binaries"
        ]
    },
    "/boot": {
        "description": "/boot contains bootloader and kernel files",
        "risk": "Modifying files here prevents system from booting",
        "consequence": "System will not start, requiring recovery",
        "alternatives": [
            "Never touch /boot unless you know what you're doing",
            "Use package managers for kernel updates",
            "Consult documentation before any changes"
        ]
    },
    "/usr": {
        "description": "/usr contains user programs and libraries",
        "risk": "Modifying files here can break installed software",
        "consequence": "Applications may stop working",
        "alternatives": [
            "Use package managers to install/remove software",
            "Install personal software in ~/.local/",
            "Work in your home directory for personal files"
        ]
    },

    # macOS directories
    "/system": {
        "description": "/System contains macOS system files",
        "risk": "Modifying files here can break macOS",
        "consequence": "System may become unstable or unbootable",
        "alternatives": [
            "Work in your home directory: /Users/username/",
            "Use ~/Documents or ~/Downloads for personal files",
            "macOS System Integrity Protection exists for a reason"
        ]
    },
    "/library": {
        "description": "/Library contains system-wide resources",
        "risk": "Modifying files here can affect all users",
        "consequence": "Applications may malfunction system-wide",
        "alternatives": [
            "Use ~/Library for user-specific settings",
            "Install apps through App Store or official installers",
            "Consult documentation before modifying /Library"
        ]
    }
}


class SystemProtectionWarning:
    """Display system directory protection warnings."""

    def __init__(self, renderer: AsciiRenderer):
        """
        Initialize system protection warning display.

        Args:
            renderer: AsciiRenderer instance for colorization
        """
        self.renderer = renderer

    def display(self, level: str, target_path: str, command: str) -> bool:
        """
        Display system protection warning.

        Args:
            level: "critical" or "caution"
            target_path: The protected path being targeted
            command: The blocked command

        Returns:
            True if user confirms (caution level), False otherwise
        """
        if level == "critical":
            self._display_critical_warning(target_path, command)
            return False
        else:
            return self._display_caution_warning(target_path, command)

    def _display_critical_warning(
        self,
        target_path: str,
        command: str
    ) -> None:
        """
        Display critical system directory warning (no confirmation).

        Args:
            target_path: The protected path being targeted
            command: The blocked command
        """
        print()
        print("=" * 60)
        print(f"🎃 {self.renderer.colorize('WHOA THERE, EXPLORER!', 'orange')}")
        print("=" * 60)
        print()

        # Get directory info
        dir_info = self._get_directory_info(target_path)

        print(f"You found a {self.renderer.colorize('protected area', 'red')}: "
              f"{self.renderer.colorize(target_path, 'orange')}")
        print()
        print(f"🧙 {self.renderer.colorize('Why this area is enchanted:', 'purple')}")
        print(f"  - {dir_info['description']}")
        print(f"  - {dir_info['risk']}")
        print(f"  - {dir_info['consequence']}")
        print()
        print(f"🗺️  {self.renderer.colorize('Safe places to explore:', 'green')}")
        for alt in dir_info['alternatives']:
            print(f"  - {alt}")
        print()
        print(self.renderer.colorize(
            "🛡️  Protected by MairuCLI's magic shield!",
            "purple"
        ))
        print("=" * 60)
        print()

    def _display_caution_warning(
        self,
        target_path: str,
        command: str
    ) -> bool:
        """
        Display caution-level warning with confirmation prompt.

        Args:
            target_path: The protected path being targeted
            command: The command to execute

        Returns:
            True if user confirms, False if cancelled
        """
        print()
        print("=" * 60)
        print(f"🦇 {self.renderer.colorize('CAREFUL, ADVENTURER!', 'orange')}")
        print("=" * 60)
        print()

        # Get directory info
        dir_info = self._get_directory_info(target_path)

        print(f"You're venturing into: "
              f"{self.renderer.colorize(target_path, 'orange')}")
        print()
        print(f"🕷️  {self.renderer.colorize('Here be dragons:', 'purple')}")
        print(f"  - {dir_info['description']}")
        print(f"  - {dir_info['risk']}")
        print()
        print(f"🗺️  {self.renderer.colorize('Safer paths:', 'chocolate')}")
        for alt in dir_info['alternatives']:
            print(f"  - {alt}")
        print()

        # Ask for confirmation
        prompt = self.renderer.colorize(
            "🎃 Still want to proceed? (yes/no): ",
            "orange"
        )
        response = input(prompt).strip().lower()

        print("=" * 60)
        print()

        return response in ['yes', 'y']

    def _get_directory_info(self, path: str) -> Dict[str, any]:
        """
        Get information about a protected directory.

        Args:
            path: Path to get information for

        Returns:
            Dictionary with description, risk, consequence, alternatives
        """
        # Normalize path for lookup
        path_lower = path.lower()

        # Try exact match first
        if path_lower in DIRECTORY_INFO:
            return DIRECTORY_INFO[path_lower]

        # Try to find parent directory
        for dir_path, info in DIRECTORY_INFO.items():
            if path_lower.startswith(dir_path):
                return info

        # Default fallback
        return {
            "description": "This is a protected system directory",
            "risk": "Modifying files here can damage your system",
            "consequence": "System may become unstable or unusable",
            "alternatives": [
                "Work in your user/home directory instead",
                "Consult documentation before modifying system files",
                "Ask an experienced user for help"
            ]
        }
