#!/usr/bin/env python3
"""
Basic tests for harper-py Python wrapper.
Tests all core functionality to ensure the bindings work correctly.
"""

import pytest
import harper_py


class TestHarperLinter:
    """Test the HarperLinter class functionality."""
    
    def setup_method(self):
        """Set up a fresh linter instance for each test."""
        self.linter = harper_py.HarperLinter()
    
    def test_linter_creation(self):
        """Test that HarperLinter can be created successfully."""
        linter = harper_py.HarperLinter()
        assert linter is not None
        assert "HarperLinter" in str(linter)
    
    def test_linter_with_dialect(self):
        """Test HarperLinter creation with different dialects."""
        american_linter = harper_py.HarperLinter(dialect="American")
        british_linter = harper_py.HarperLinter(dialect="British")
        
        assert american_linter is not None
        assert british_linter is not None
    
    def test_count_errors_clean_text(self):
        """Test count_errors with grammatically correct text."""
        clean_text = "This is a perfectly written sentence."
        error_count = self.linter.count_errors(clean_text)
        assert isinstance(error_count, int)
        assert error_count >= 0
    
    def test_count_errors_with_errors(self):
        """Test count_errors with text containing obvious errors."""
        error_text = "This are a sentence with obvious grammer errors."
        error_count = self.linter.count_errors(error_text)
        assert isinstance(error_count, int)
        assert error_count > 0
    
    def test_has_errors_clean_text(self):
        """Test has_errors with clean text."""
        clean_text = "This is a well-written sentence."
        has_errors = self.linter.has_errors(clean_text)
        assert isinstance(has_errors, bool)
    
    def test_has_errors_with_errors(self):
        """Test has_errors with problematic text."""
        error_text = "This are definitelys wrong."
        has_errors = self.linter.has_errors(error_text)
        assert isinstance(has_errors, bool)
        assert has_errors is True
    
    def test_lint_clean_text(self):
        """Test lint method with clean text."""
        clean_text = "This is a properly constructed sentence."
        lint_results = self.linter.lint(clean_text)
        assert isinstance(lint_results, list)
        # Should return a list (might be empty for clean text)
    
    def test_lint_with_errors(self):
        """Test lint method with text containing errors."""
        error_text = "This are an sentence with so many problems."
        lint_results = self.linter.lint(error_text)
        assert isinstance(lint_results, list)
        assert len(lint_results) > 0
        
        # Check that each lint result has the expected structure
        for error in lint_results:
            assert hasattr(error, 'start')
            assert hasattr(error, 'end')
            assert hasattr(error, 'message')
            assert isinstance(error.start, int)
            assert isinstance(error.end, int)
            assert isinstance(error.message, str)
            assert error.start < error.end
    
    def test_lint_error_representation(self):
        """Test LintError string representations."""
        error_text = "This are wrong."
        lint_results = self.linter.lint(error_text)
        
        if lint_results:  # If we found errors
            error = lint_results[0]
            
            # Test __str__ and __repr__
            str_repr = str(error)
            repr_repr = repr(error)
            
            assert isinstance(str_repr, str)
            assert isinstance(repr_repr, str)
            assert "LintError" in repr_repr
            assert str(error.start) in str_repr
            assert str(error.end) in str_repr
    
    def test_empty_text(self):
        """Test all methods with empty text."""
        empty_text = ""
        
        assert self.linter.count_errors(empty_text) >= 0
        assert isinstance(self.linter.has_errors(empty_text), bool)
        assert isinstance(self.linter.lint(empty_text), list)
    
    def test_consistency_between_methods(self):
        """Test that count_errors, has_errors, and lint are consistent."""
        test_text = "This are a test sentence with errors."
        
        error_count = self.linter.count_errors(test_text)
        has_errors = self.linter.has_errors(test_text)
        lint_results = self.linter.lint(test_text)
        
        # Consistency checks
        if error_count > 0:
            assert has_errors is True
            assert len(lint_results) > 0
        
        if has_errors:
            assert error_count > 0
            assert len(lint_results) > 0
        
        if len(lint_results) > 0:
            assert error_count > 0
            assert has_errors is True
    
    def test_multiple_calls_same_instance(self):
        """Test that multiple calls on the same instance work (cached linter)."""
        test_text = "This is a test sentence."
        
        # Multiple calls should work without issues
        result1 = self.linter.count_errors(test_text)
        result2 = self.linter.count_errors(test_text)
        result3 = self.linter.has_errors(test_text)
        
        assert result1 == result2  # Should be consistent
        assert isinstance(result3, bool)


class TestModuleLevel:
    """Test module-level functionality."""
    
    def test_module_attributes(self):
        """Test that the module has expected attributes."""
        assert hasattr(harper_py, 'HarperLinter')
        assert hasattr(harper_py, 'LintError')
        assert hasattr(harper_py, '__version__')
        assert hasattr(harper_py, '__doc__')
    
    def test_version_string(self):
        """Test that version is a string."""
        assert isinstance(harper_py.__version__, str)
        assert len(harper_py.__version__) > 0


if __name__ == "__main__":
    # Run tests if called directly
    pytest.main([__file__, "-v"])