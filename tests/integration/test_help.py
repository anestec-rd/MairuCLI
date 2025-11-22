"""Test the help command."""

import sys
import os

# Add project root to path
sys.path.insert(
    0,
    os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
)

from src.builtins import BuiltinCommands

print("Testing help command:\n")
BuiltinCommands._cmd_help([])
