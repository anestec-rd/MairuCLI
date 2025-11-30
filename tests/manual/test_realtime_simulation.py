"""
Manual test for real-time timeline simulation display.

This test demonstrates the new real-time display feature for timeline simulations.
Run this manually to see the dramatic effect of the real-time display.
"""

import os
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.display.breakdown_formatter import BreakdownFormatter
from src.display.educational_loader import EducationalLoader


def test_realtime_display():
    """Test the real-time display of timeline simulation."""
    print("\n" + "=" * 70)
    print("Testing Real-Time Timeline Simulation Display")
    print("=" * 70)
    print()
    print("This test will show the timeline simulation with dramatic pauses.")
    print("Watch how each step appears with a delay for dramatic effect.")
    print()
    input("Press Enter to start the simulation...")

    # Load a simulation
    loader = EducationalLoader()
    formatter = BreakdownFormatter()

    # Test with rm_dangerous simulation
    print("\n" + "=" * 70)
    print("Test 1: rm -rf / simulation")
    print("=" * 70)

    simulation = loader.load_simulation("rm_dangerous")
    if simulation:
        formatter._format_simulation_realtime(simulation)
    else:
        print("ERROR: Could not load rm_dangerous simulation")

    print()
    input("Press Enter to see another simulation...")

    # Test with chmod_000 simulation
    print("\n" + "=" * 70)
    print("Test 2: chmod 000 simulation")
    print("=" * 70)

    simulation = loader.load_simulation("chmod_000")
    if simulation:
        formatter._format_simulation_realtime(simulation)
    else:
        print("ERROR: Could not load chmod_000 simulation")

    print()
    print("=" * 70)
    print("Real-time display test complete!")
    print("=" * 70)
    print()
    print("Features demonstrated:")
    print("  ✓ Real-time printing of each step")
    print("  ✓ Color coding based on severity")
    print("  ✓ Dramatic pauses between steps")
    print("  ✓ Longer pauses for critical events")
    print()


if __name__ == "__main__":
    test_realtime_display()
