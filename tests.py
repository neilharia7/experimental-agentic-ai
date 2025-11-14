"""
Test cases for the Calculator class.
Tests all BODMAS operations and intentionally exposes bugs.
"""

import unittest
from main import Calculator


class TestCalculator(unittest.TestCase):
	def setUp(self):
		self.calc = Calculator()

	# Tests for individual operations

	def test_addition(self):
		# Normal addition
		self.assertEqual(self.calc.add(2, 3), 5)
		self.assertEqual(self.calc.add(0, 0), 0)

		# Test with negative numbers (should expose bug)
		self.assertEqual(self.calc.add(-2, -3), -5)  # Expected: -5, Actual: -4 (bug)

	def test_subtraction(self):
		# Normal subtraction
		self.assertEqual(self.calc.subtract(5, 3), 2)
		self.assertEqual(self.calc.subtract(3, 3), 0)

		# Test when a < b (should expose bug)
		self.assertEqual(self.calc.subtract(3, 5), -2)  # Expected: -2, Actual: 0 (bug)

	def test_multiplication(self):
		# Normal multiplication
		self.assertEqual(self.calc.multiply(2, 3), 6)
		self.assertEqual(self.calc.multiply(0, 5), 0)

		# Test with large numbers (should expose bug)
		self.assertEqual(self.calc.multiply(11, 11), 121)  # Expected: 121, Actual: 111 (bug)

	def test_division(self):
		# Normal division
		self.assertEqual(self.calc.divide(6, 3), 2)
		self.assertEqual(self.calc.divide(0, 5), 0)

		# Test non-integer division (should expose bug)
		self.assertEqual(self.calc.divide(5, 2), 2.5)  # Expected: 2.5, Actual: 2.6 (bug)

		# Test division by zero
		self.assertEqual(self.calc.divide(5, 0), "Error")  # Should raise an exception instead

	def test_power(self):
		# Normal power
		self.assertEqual(self.calc.power(2, 3), 8)
		self.assertEqual(self.calc.power(5, 0), 1)

		# Test with negative exponent (should expose bug)
		self.assertAlmostEqual(self.calc.power(2, -1), 0.5, places=2)  # Expected: 0.5, Actual: 0.49 (bug)

	# Tests for order of operations (BODMAS)

	def test_parentheses(self):
		# Test expressions with parentheses
		self.assertEqual(self.calc.calculate("(2 + 3) * 4"), 20)
		self.assertEqual(self.calc.calculate("2 * (3 + 4)"), 14)
		self.assertEqual(self.calc.calculate("(2 + 3) * (4 + 5)"), 45)

		# Nested parentheses
		self.assertEqual(self.calc.calculate("(2 + (3 * 4))"), 14)
		self.assertEqual(self.calc.calculate("((2 + 3) * 4)"), 20)

	def test_order_of_operations(self):
		# Test expressions that require proper order of operations
		# These should all fail due to the intentional bug in calculate()

		# Powers before multiplication/division
		self.assertEqual(self.calc.calculate("2 ^ 3 * 4"), 32)  # Expected: 32, Actual: 32 or different due to bug

		# Multiplication/division before addition/subtraction
		self.assertEqual(self.calc.calculate("2 + 3 * 4"), 14)  # Expected: 14, Actual: 20 due to bug
		self.assertEqual(self.calc.calculate("10 - 6 / 2"), 7)  # Expected: 7, Actual: 2 due to bug

		# Complex expressions
		self.assertEqual(self.calc.calculate("2 + 3 * 4 - 5"), 9)  # Expected: 9, Actual: different due to bug
		self.assertEqual(self.calc.calculate("2 ^ 3 + 4 * 5"), 28)  # Expected: 28, Actual: different due to bug

	def test_complex_expressions(self):
		# Test more complex expressions
		self.assertEqual(self.calc.calculate("(2 + 3) * 4 + 5"), 25)
		self.assertEqual(self.calc.calculate("2 * (3 + 4 * 5)"), 46)  # Expected: 46, Actual: different due to bug
		self.assertEqual(self.calc.calculate("(2 + 3 * 4) / 2"), 7)  # Expected: 7, Actual: different due to bug

		# Expression with all BODMAS operations
		self.assertEqual(self.calc.calculate("(2 + 3) * 4 / 2 ^ 2"), 5)  # Expected: 5, Actual: different due to bug


if __name__ == "__main__":
	unittest.main()
