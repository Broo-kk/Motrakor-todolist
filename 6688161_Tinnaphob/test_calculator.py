"""Tests for the Calculator module."""

import pytest
from calculator import Calculator, calculate_velocity


class TestCalculatorBasicOperations:
    """Test basic arithmetic operations."""

    @pytest.fixture
    def calculator(self):
        """Provide a fresh calculator instance for each test."""
        return Calculator()

    def test_add_positive_numbers(self, calculator):
        """Test adding two positive numbers."""
        result = calculator.add(5, 3)
        assert result == 8

    def test_add_negative_numbers(self, calculator):
        """Test adding two negative numbers."""
        result = calculator.add(-5, -3)
        assert result == -8

    def test_add_mixed_numbers(self, calculator):
        """Test adding positive and negative numbers."""
        result = calculator.add(10, -5)
        assert result == 5

    def test_subtract_positive_numbers(self, calculator):
        """Test subtracting positive numbers."""
        result = calculator.subtract(10, 3)
        assert result == 7

    def test_subtract_negative_numbers(self, calculator):
        """Test subtracting negative numbers."""
        result = calculator.subtract(-5, -3)
        assert result == -2

    def test_subtract_resulting_in_negative(self, calculator):
        """Test subtraction resulting in negative number."""
        result = calculator.subtract(3, 10)
        assert result == -7

    def test_multiply_positive_numbers(self, calculator):
        """Test multiplying positive numbers."""
        result = calculator.multiply(4, 5)
        assert result == 20

    def test_multiply_negative_numbers(self, calculator):
        """Test multiplying negative numbers."""
        result = calculator.multiply(-4, -5)
        assert result == 20

    def test_multiply_mixed_sign_numbers(self, calculator):
        """Test multiplying numbers with different signs."""
        result = calculator.multiply(-4, 5)
        assert result == -20

    def test_multiply_by_zero(self, calculator):
        """Test multiplying by zero."""
        result = calculator.multiply(10, 0)
        assert result == 0

    def test_divide_positive_numbers(self, calculator):
        """Test dividing positive numbers."""
        result = calculator.divide(10, 2)
        assert result == 5

    def test_divide_negative_numbers(self, calculator):
        """Test dividing negative numbers."""
        result = calculator.divide(-10, -2)
        assert result == 5

    def test_divide_mixed_sign_numbers(self, calculator):
        """Test dividing numbers with different signs."""
        result = calculator.divide(-10, 2)
        assert result == -5

    def test_divide_by_zero_raises_error(self, calculator):
        """Test that division by zero raises ValueError."""
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            calculator.divide(10, 0)

    def test_divide_fractional_result(self, calculator):
        """Test division resulting in fractional value."""
        result = calculator.divide(7, 2)
        assert result == 3.5


class TestCalculatorLastResult:
    """Test last result tracking functionality."""

    @pytest.fixture
    def calculator(self):
        """Provide a fresh calculator instance for each test."""
        return Calculator()

    def test_last_result_initial_value(self, calculator):
        """Test that initial last result is 0."""
        assert calculator.get_last_result() == 0

    def test_last_result_after_add(self, calculator):
        """Test that last result is updated after addition."""
        calculator.add(5, 3)
        assert calculator.get_last_result() == 8

    def test_last_result_after_subtract(self, calculator):
        """Test that last result is updated after subtraction."""
        calculator.subtract(10, 3)
        assert calculator.get_last_result() == 7

    def test_last_result_after_multiply(self, calculator):
        """Test that last result is updated after multiplication."""
        calculator.multiply(4, 5)
        assert calculator.get_last_result() == 20

    def test_last_result_after_divide(self, calculator):
        """Test that last result is updated after division."""
        calculator.divide(10, 2)
        assert calculator.get_last_result() == 5

    def test_last_result_overwrites_previous(self, calculator):
        """Test that operations overwrite the previous last result."""
        calculator.add(5, 3)
        assert calculator.get_last_result() == 8
        calculator.multiply(2, 3)
        assert calculator.get_last_result() == 6


class TestCalculatorFloatingPoint:
    """Test floating point arithmetic."""

    @pytest.fixture
    def calculator(self):
        """Provide a fresh calculator instance for each test."""
        return Calculator()

    def test_add_floats(self, calculator):
        """Test adding floating point numbers."""
        result = calculator.add(1.5, 2.5)
        assert result == 4.0

    def test_subtract_floats(self, calculator):
        """Test subtracting floating point numbers."""
        result = calculator.subtract(5.5, 2.3)
        assert abs(result - 3.2) < 0.0001

    def test_multiply_floats(self, calculator):
        """Test multiplying floating point numbers."""
        result = calculator.multiply(2.5, 4.0)
        assert result == 10.0

    def test_divide_floats(self, calculator):
        """Test dividing floating point numbers."""
        result = calculator.divide(7.5, 2.5)
        assert result == 3.0


class TestVelocityCalculation:
    """Test velocity calculation functionality."""

    def test_calculate_velocity_basic(self):
        """Test basic velocity calculation."""
        result = calculate_velocity(100, 10)
        assert result == 10.0

    def test_calculate_velocity_fractional(self):
        """Test velocity calculation with fractional result."""
        result = calculate_velocity(50, 4)
        assert result == 12.5

    def test_calculate_velocity_zero_distance(self):
        """Test velocity calculation with zero distance."""
        result = calculate_velocity(0, 10)
        assert result == 0.0

    def test_calculate_velocity_negative_distance(self):
        """Test velocity calculation with negative distance (moving backwards)."""
        result = calculate_velocity(-100, 10)
        assert result == -10.0

    def test_calculate_velocity_zero_time_raises_error(self):
        """Test that zero time raises ValueError."""
        with pytest.raises(ValueError, match="Time must be greater than zero"):
            calculate_velocity(100, 0)

    def test_calculate_velocity_negative_time_raises_error(self):
        """Test that negative time raises ValueError."""
        with pytest.raises(ValueError, match="Time must be greater than zero"):
            calculate_velocity(100, -5)

    def test_calculate_velocity_float_inputs(self):
        """Test velocity calculation with float inputs."""
        result = calculate_velocity(75.5, 5.2)
        assert abs(result - 14.519) < 0.001

    def test_calculate_velocity_large_numbers(self):
        """Test velocity calculation with large numbers."""
        result = calculate_velocity(1000000, 5000)
        assert result == 200.0
