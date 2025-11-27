"""
Add help_example and help_description fields to pattern JSON files.
"""

import json
from pathlib import Path

# Help text for each pattern
HELP_DATA = {
    "rm_dangerous": {
        "help_example": "rm -rf /",
        "help_description": "Recursive deletion of critical paths"
    },
    "chmod_777": {
        "help_example": "chmod 777 file",
        "help_description": "Give everyone full file access"
    },
    "chmod_000": {
        "help_example": "chmod 000 file",
        "help_description": "Remove all file permissions"
    },
    "dd_zero": {
        "help_example": "dd if=/dev/zero",
        "help_description": "Write zeros to disk"
    },
    "drop_database": {
        "help_example": "DROP DATABASE prod",
        "help_description": "Delete entire database"
    },
    "fork_bomb": {
        "help_example": ":(){ :|:& };:",
        "help_description": "Crash system with infinite processes"
    },
    "redirect_to_disk": {
        "help_example": "echo data > /dev/sda",
        "help_description": "Write directly to disk device"
    },
    "mkfs_disk": {
        "help_example": "mkfs /dev/sda",
        "help_description": "Format entire disk"
    },
    "mv_to_null": {
        "help_example": "mv file /dev/null",
        "help_description": "Delete file permanently"
    },
    "overwrite_file": {
        "help_example": "> /important/file",
        "help_description": "Erase file contents"
    },
    "dd_random": {
        "help_example": "dd if=/dev/random of=/dev/sda",
        "help_description": "Overwrite disk with random data"
    },
    "kernel_panic": {
        "help_example": "echo c > /proc/sysrq-trigger",
        "help_description": "Trigger kernel crash"
    },
    "shred_secure": {
        "help_example": "shred /dev/sda",
        "help_description": "Securely erase disk"
    },
    "system_modify": {
        "help_example": "echo test > /etc/passwd",
        "help_description": "Modify critical system files"
    }
}

CAUTION_HELP_DATA = {
    "sudo_shell": {
        "help_example": "sudo bash",
        "help_description": "Enter root shell"
    },
    "chmod_permissive": {
        "help_example": "chmod 666 file",
        "help_description": "Make file world-writable"
    },
    "firewall_disable": {
        "help_example": "ufw disable",
        "help_description": "Disable firewall"
    },
    "service_stop": {
        "help_example": "systemctl stop sshd",
        "help_description": "Stop critical service"
    }
}


def add_help_to_warnings():
    """Add help fields to warning_catalog.json"""
    catalog_path = Path("data/warnings/warning_catalog.json")

    with open(catalog_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for pattern_name, pattern_data in data['warnings'].items():
        if pattern_name in HELP_DATA:
            pattern_data['help_example'] = HELP_DATA[pattern_name]['help_example']
            pattern_data['help_description'] = HELP_DATA[pattern_name]['help_description']

    with open(catalog_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"✅ Updated {len(HELP_DATA)} patterns in warning_catalog.json")


def add_help_to_cautions():
    """Add help fields to caution_catalog.json"""
    catalog_path = Path("data/warnings/caution_catalog.json")

    with open(catalog_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for pattern_name, pattern_data in data['cautions'].items():
        if pattern_name in CAUTION_HELP_DATA:
            pattern_data['help_example'] = CAUTION_HELP_DATA[pattern_name]['help_example']
            pattern_data['help_description'] = CAUTION_HELP_DATA[pattern_name]['help_description']

    with open(catalog_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"✅ Updated {len(CAUTION_HELP_DATA)} patterns in caution_catalog.json")


if __name__ == "__main__":
    add_help_to_warnings()
    add_help_to_cautions()
    print("✅ All help fields added successfully!")
