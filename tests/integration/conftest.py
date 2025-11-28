"""
Pytest configuration for integration tests.

This file sets up the test environment for all integration tests.
"""

import os
import pytest


@pytest.fixture(scope="session", autouse=True)
def set_test_mode():
    """
    Set MAIRU_TEST_MODE environment variable for all integration tests.

    This prevents input() calls from blocking pytest during test execution.
    """
    os.environ['MAIRU_TEST_MODE'] = '1'
    yield
    # Cleanup after all tests
    if 'MAIRU_TEST_MODE' in os.environ:
        del os.environ['MAIRU_TEST_MODE']
