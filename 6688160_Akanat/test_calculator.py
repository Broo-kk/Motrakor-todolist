"""
Unit tests for the calculator module.
"""

import pytest
from calculator import add, subtract, multiply, divide


class TestAddition:
    """Test cases for the add function."""
    
    def test_add_positive_numbers(self):
        assert add(5, 3) == 8
    
    def test_add_negative_numbers(self):
        assert add(-5, -3) == -8
    
    def test_add_mixed_numbers(self):
        assert add(5, -3) == 2
    
    def test_add_zeros(self):
        assert add(0, 0) == 0
    
    def test_add_decimals(self):
        assert add(1.5, 2.5) == 4.0


class TestSubtraction:
    """Test cases for the subtract function."""
    
    def test_subtract_positive_numbers(self):
        assert subtract(10, 3) == 7
    
    def test_subtract_negative_numbers(self):
        assert subtract(-5, -3) == -2
    
    def test_subtract_mixed_numbers(self):
        assert subtract(5, -3) == 8
    
    def test_subtract_zeros(self):
        assert subtract(0, 0) == 0
    
    def test_subtract_decimals(self):
        assert subtract(5.5, 2.5) == 3.0


class TestMultiplication:
    """Test cases for the multiply function."""
    
    def test_multiply_positive_numbers(self):
        assert multiply(4, 5) == 20
    
    def test_multiply_negative_numbers(self):
        assert multiply(-4, -5) == 20
    
    def test_multiply_mixed_signs(self):
        assert multiply(-4, 5) == -20
    
    def test_multiply_by_zero(self):
        assert multiply(5, 0) == 0
    
    def test_multiply_decimals(self):
        assert multiply(2.5, 4) == 10.0


class TestDivision:
    """Test cases for the divide function."""
    
    def test_divide_positive_numbers(self):
        assert divide(10, 2) == 5.0
    
    def test_divide_negative_numbers(self):
        assert divide(-10, -2) == 5.0
    
    def test_divide_mixed_signs(self):
        assert divide(-10, 2) == -5.0
    
    def test_divide_decimals(self):
        assert divide(7.5, 2.5) == 3.0
    
    def test_divide_by_zero(self):
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            divide(10, 0)
    
    def test_divide_zero_by_number(self):
        assert divide(0, 5) == 0.0
