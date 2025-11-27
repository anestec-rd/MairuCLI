"""
Unit tests for PatternCompiler class in src/interceptor.py
"""

import re
import os
import pytest

# Add project root to path
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))

from src.interceptor import PatternCompiler


class TestPatternCompiler:
    """Test suite for PatternCompiler class."""

    def test_compile_valid_regex_patterns(self):
        """Test compiling valid regex patterns."""
        compiler = PatternCompiler()

        patterns = {
            "rm_dangerous": {
                "pattern": r"rm\s+(-rf|-fr)",
                "category": "deletion",
                "severity": "critical"
            },
            "chmod_777": {
                "pattern": r"chmod\s+777",
                "category": "permission",
                "severity": "high"
            }
        }

        compiled = compiler.compile_patterns(patterns)

        # Verify all patterns were compiled
        assert len(compiled) == 2, "Should compile all valid patterns"
        assert "rm_dangerous" in compiled
        assert "chmod_777" in compiled

        # Verify compiled regex exists
        assert 'compiled' in compiled["rm_dangerous"]
        assert 'compiled' in compiled["chmod_777"]

        # Verify compiled patterns are regex objects
        assert isinstance(compiled["rm_dangerous"]['compiled'],
                          re.Pattern)
        assert isinstance(compiled["chmod_777"]['compiled'],
                          re.Pattern)

    def test_compile_patterns_preserves_original_data(self):
        """Test that compilation preserves original pattern data."""
        compiler = PatternCompiler()

        patterns = {
            "test_pattern": {
                "pattern": r"test\s+pattern",
                "category": "test",
                "severity": "medium",
                "extra_field": "extra_value"
            }
        }

        compiled = compiler.compile_patterns(patterns)

        # Verify original data is preserved
        assert compiled["test_pattern"]["category"] == "test"
        assert compiled["test_pattern"]["severity"] == "medium"
        assert compiled["test_pattern"]["extra_field"] == "extra_value"
        assert compiled["test_pattern"]["pattern"] == r"test\s+pattern"

    def test_compile_empty_patterns_dict(self):
        """Test compiling empty patterns dictionary."""
        compiler = PatternCompiler()

        patterns = {}
        compiled = compiler.compile_patterns(patterns)

        # Should return empty dict
        assert compiled == {}, "Should return empty dict for empty input"

    def test_handle_invalid_regex_gracefully(self):
        """Test handling of invalid regex patterns gracefully."""
        compiler = PatternCompiler()

        patterns = {
            "valid_pattern": {
                "pattern": r"valid\s+pattern",
                "category": "test"
            },
            "invalid_pattern": {
                "pattern": r"invalid[regex",  # Missing closing bracket
                "category": "test"
            },
            "another_valid": {
                "pattern": r"another.*valid",
                "category": "test"
            }
        }

        compiled = compiler.compile_patterns(patterns)

        # Should compile valid patterns and skip invalid ones
        assert "valid_pattern" in compiled, "Should compile valid pattern"
        assert "another_valid" in compiled, "Should compile valid pattern"
        assert "invalid_pattern" not in compiled, \
            "Should skip invalid pattern"

    def test_handle_multiple_invalid_regex_patterns(self):
        """Test handling multiple invalid regex patterns."""
        compiler = PatternCompiler()

        patterns = {
            "invalid1": {
                "pattern": r"(?P<invalid",  # Invalid group
                "category": "test"
            },
            "invalid2": {
                "pattern": r"*invalid",  # Invalid quantifier
                "category": "test"
            },
            "invalid3": {
                "pattern": r"(?P<name>test)(?P<name>dup)",  # Duplicate name
                "category": "test"
            }
        }

        compiled = compiler.compile_patterns(patterns)

        # Should skip all invalid patterns
        assert len(compiled) == 0, "Should skip all invalid patterns"

    def test_pattern_matching_with_compiled_patterns(self):
        """Test that compiled patterns can match commands correctly."""
        compiler = PatternCompiler()

        patterns = {
            "rm_dangerous": {
                "pattern": r"rm\s+(-rf|-fr)\s+/",
                "category": "deletion"
            },
            "chmod_777": {
                "pattern": r"chmod\s+777",
                "category": "permission"
            }
        }

        compiled = compiler.compile_patterns(patterns)

        # Test rm_dangerous pattern matching
        rm_pattern = compiled["rm_dangerous"]['compiled']
        assert rm_pattern.search("rm -rf /"), \
            "Should match 'rm -rf /'"
        assert rm_pattern.search("rm -fr /home"), \
            "Should match 'rm -fr /home'"
        assert not rm_pattern.search("rm file.txt"), \
            "Should not match safe rm command"

        # Test chmod_777 pattern matching
        chmod_pattern = compiled["chmod_777"]['compiled']
        assert chmod_pattern.search("chmod 777 file.txt"), \
            "Should match 'chmod 777 file.txt'"
        assert not chmod_pattern.search("chmod 755 file.txt"), \
            "Should not match safe chmod command"

    def test_case_insensitive_matching(self):
        """Test that patterns are compiled with case-insensitive flag."""
        compiler = PatternCompiler()

        patterns = {
            "test_pattern": {
                "pattern": r"rm\s+-rf",
                "category": "test"
            }
        }

        compiled = compiler.compile_patterns(patterns)
        pattern = compiled["test_pattern"]['compiled']

        # Should match regardless of case
        assert pattern.search("rm -rf"), "Should match lowercase"
        assert pattern.search("RM -RF"), "Should match uppercase"
        assert pattern.search("Rm -Rf"), "Should match mixed case"

    def test_complex_regex_patterns(self):
        """Test compiling complex regex patterns."""
        compiler = PatternCompiler()

        patterns = {
            "complex1": {
                "pattern": r"rm\s+(-rf|-fr|-r\s+-f|-f\s+-r)\s+"
                          r"(/|~|\$HOME|\*|\.(?:\s|$)|\$\w+)",
                "category": "deletion"
            },
            "complex2": {
                "pattern": r"chmod\s+(-R\s+)?777",
                "category": "permission"
            },
            "complex3": {
                "pattern": r"dd\s+if=/dev/(zero|random)\s+of=/dev/sd[a-z]",
                "category": "disk"
            }
        }

        compiled = compiler.compile_patterns(patterns)

        # All complex patterns should compile successfully
        assert len(compiled) == 3, "Should compile all complex patterns"
        assert all('compiled' in data for data in compiled.values()), \
            "All patterns should have compiled regex"

    def test_pattern_with_special_characters(self):
        """Test patterns with special regex characters."""
        compiler = PatternCompiler()

        patterns = {
            "special_chars": {
                "pattern": r"\$\(\(.*\)\)",  # Matches $((...))
                "category": "test"
            },
            "brackets": {
                "pattern": r"\[.*\]",  # Matches [...]
                "category": "test"
            }
        }

        compiled = compiler.compile_patterns(patterns)

        # Should compile patterns with special characters
        assert len(compiled) == 2
        assert compiled["special_chars"]['compiled'].search("$((1+1))")
        assert compiled["brackets"]['compiled'].search("[test]")

    def test_pattern_with_lookahead_lookbehind(self):
        """Test patterns with lookahead and lookbehind assertions."""
        compiler = PatternCompiler()

        patterns = {
            "lookahead": {
                "pattern": r"rm(?=\s+-rf)",  # Positive lookahead
                "category": "test"
            },
            "negative_lookahead": {
                "pattern": r"chmod(?!\s+644)",  # Negative lookahead
                "category": "test"
            }
        }

        compiled = compiler.compile_patterns(patterns)

        # Should compile patterns with assertions
        assert len(compiled) == 2
        assert 'compiled' in compiled["lookahead"]
        assert 'compiled' in compiled["negative_lookahead"]

    def test_pattern_without_pattern_field(self):
        """Test handling of pattern dict without 'pattern' field."""
        compiler = PatternCompiler()

        patterns = {
            "missing_pattern": {
                "category": "test",
                "severity": "high"
                # No 'pattern' field
            }
        }

        # Should handle gracefully (might raise KeyError or skip)
        try:
            compiled = compiler.compile_patterns(patterns)
            # If it doesn't raise, it should skip the pattern
            assert "missing_pattern" not in compiled or \
                   'compiled' not in compiled["missing_pattern"]
        except KeyError:
            # This is also acceptable behavior
            pass

    def test_unicode_patterns(self):
        """Test patterns with unicode characters."""
        compiler = PatternCompiler()

        patterns = {
            "unicode_pattern": {
                "pattern": r"rm.*文件",  # Chinese characters
                "category": "test"
            }
        }

        compiled = compiler.compile_patterns(patterns)

        # Should compile unicode patterns
        assert "unicode_pattern" in compiled
        assert compiled["unicode_pattern"]['compiled'].search("rm 文件.txt")

    def test_empty_pattern_string(self):
        """Test handling of empty pattern string."""
        compiler = PatternCompiler()

        patterns = {
            "empty_pattern": {
                "pattern": "",  # Empty string
                "category": "test"
            }
        }

        compiled = compiler.compile_patterns(patterns)

        # Empty pattern should compile (matches everything)
        assert "empty_pattern" in compiled
        assert 'compiled' in compiled["empty_pattern"]

    def test_whitespace_only_pattern(self):
        """Test pattern that only matches whitespace."""
        compiler = PatternCompiler()

        patterns = {
            "whitespace": {
                "pattern": r"^\s+$",
                "category": "test"
            }
        }

        compiled = compiler.compile_patterns(patterns)

        assert "whitespace" in compiled
        assert compiled["whitespace"]['compiled'].search("   ")
        assert not compiled["whitespace"]['compiled'].search("text")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
