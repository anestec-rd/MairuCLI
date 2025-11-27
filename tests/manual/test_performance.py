"""
Performance testing for system directory protection.

This script measures the performance of system directory checks
to verify they meet the < 50ms target.
"""

import time
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.interceptor import check_system_directory


def measure_performance(command: str, iterations: int = 100) -> dict:
    """
    Measure performance of system directory check.

    Args:
        command: Command to test
        iterations: Number of iterations to run

    Returns:
        Dictionary with timing statistics
    """
    times = []

    for _ in range(iterations):
        start = time.perf_counter()
        check_system_directory(command)
        end = time.perf_counter()
        times.append((end - start) * 1000)  # Convert to milliseconds

    return {
        'min': min(times),
        'max': max(times),
        'avg': sum(times) / len(times),
        'median': sorted(times)[len(times) // 2]
    }


def main():
    """Run performance tests."""
    print("=" * 70)
    print("System Directory Protection - Performance Testing")
    print("=" * 70)
    print()
    print("Target: < 50ms per check")
    print("Running 100 iterations per test...")
    print()

    # Test cases covering different scenarios
    test_cases = [
        # Windows system directories
        ("rm -rf C:\\Windows\\System32", "Windows System32 (critical)"),
        ("chmod 777 C:\\Program Files", "Windows Program Files (caution)"),
        ("rm C:\\Users\\test\\file.txt", "Windows user directory (safe)"),

        # Linux system directories
        ("rm -rf /etc", "Linux /etc (critical)"),
        ("chmod 777 /usr/bin", "Linux /usr/bin (caution)"),
        ("rm /home/user/file.txt", "Linux home directory (safe)"),

        # Relative paths
        ("rm -rf ../../Windows/System32", "Relative path to System32"),
        ("rm -rf ../../../etc", "Relative path to /etc"),

        # Environment variables
        ("rm -rf $WINDIR", "Environment variable $WINDIR"),
        ("rm -rf %SYSTEMROOT%", "Environment variable %SYSTEMROOT%"),

        # Command chaining
        ("cd /tmp && rm -rf /etc", "Command chaining with critical path"),
        ("echo test > /dev/sda; ls", "Multiple commands with redirection"),

        # Complex commands
        ("rm -rf /etc/passwd /etc/shadow /etc/group", "Multiple paths"),
        ("mv /etc/passwd /tmp/backup", "Move with system source"),
    ]

    results = []
    all_pass = True

    for command, description in test_cases:
        print(f"Testing: {description}")
        print(f"Command: {command}")

        stats = measure_performance(command)

        print(f"  Min:    {stats['min']:.2f} ms")
        print(f"  Max:    {stats['max']:.2f} ms")
        print(f"  Avg:    {stats['avg']:.2f} ms")
        print(f"  Median: {stats['median']:.2f} ms")

        # Check if meets target
        if stats['avg'] < 50:
            print(f"  ✅ PASS (avg < 50ms)")
        else:
            print(f"  ❌ FAIL (avg >= 50ms)")
            all_pass = False

        print()

        results.append({
            'description': description,
            'command': command,
            'stats': stats,
            'pass': stats['avg'] < 50
        })

    # Summary
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print()

    passed = sum(1 for r in results if r['pass'])
    total = len(results)

    print(f"Tests passed: {passed}/{total}")
    print()

    # Overall statistics
    all_avgs = [r['stats']['avg'] for r in results]
    overall_avg = sum(all_avgs) / len(all_avgs)
    overall_max = max(r['stats']['max'] for r in results)

    print(f"Overall average: {overall_avg:.2f} ms")
    print(f"Overall maximum: {overall_max:.2f} ms")
    print()

    if all_pass:
        print("✅ ALL TESTS PASSED - Performance target met!")
    else:
        print("❌ SOME TESTS FAILED - Performance target not met")
        print()
        print("Failed tests:")
        for r in results:
            if not r['pass']:
                print(f"  - {r['description']}: {r['stats']['avg']:.2f} ms")

    print()
    print("=" * 70)

    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(main())
