"""
Test cases for the Calculator class.
Tests all BODMAS operations.
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

		# Test with negative numbers
		self.assertEqual(self.calc.add(-2, -3), -5)

	def test_subtraction(self):
		# Normal subtraction
		self.assertEqual(self.calc.subtract(5, 3), 2)
		self.assertEqual(self.calc.subtract(3, 3), 0)

		# Test when a < b
		self.assertEqual(self.calc.subtract(3, 5), -2)

	def test_multiplication(self):
		# Normal multiplication
		self.assertEqual(self.calc.multiply(2, 3), 6)
		self.assertEqual(self.calc.multiply(0, 5), 0)

		# Test with large numbers
		self.assertEqual(self.calc.multiply(11, 11), 121)

	def test_division(self):
		# Normal division
		self.assertEqual(self.calc.divide(6, 3), 2)
		self.assertEqual(self.calc.divide(0, 5), 0)

		# Test non-integer division
		self.assertEqual(self.calc.divide(5, 2), 2.5)

		# Test division by zero
		with self.assertRaises(ZeroDivisionError):
			self.calc.divide(5, 0)

	def test_power(self):
		# Normal power
		self.assertEqual(self.calc.power(2, 3), 8)
		self.assertEqual(self.calc.power(5, 0), 1)

		# Test with negative exponent
		self.assertEqual(self.calc.power(2, -1), 0.5)

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
		# Powers before multiplication/division
		self.assertEqual(self.calc.calculate("2 ^ 3 * 4"), 32)

		# Multiplication/division before addition/subtraction
		self.assertEqual(self.calc.calculate("2 + 3 * 4"), 14)
		self.assertEqual(self.calc.calculate("10 - 6 / 2"), 7)

		# Complex expressions
		self.assertEqual(self.calc.calculate("2 + 3 * 4 - 5"), 9)
		self.assertEqual(self.calc.calculate("2 ^ 3 + 4 * 5"), 28)

	def test_complex_expressions(self):
		# Test more complex expressions
		self.assertEqual(self.calc.calculate("(2 + 3) * 4 + 5"), 25)
		self.assertEqual(self.calc.calculate("2 * (3 + 4 * 5)"), 46)
		self.assertEqual(self.calc.calculate("(2 + 3 * 4) / 2"), 7)

		# Expression with all BODMAS operations
		self.assertEqual(self.calc.calculate("(2 + 3) * 4 / 2 ^ 2"), 5)


if __name__ == "__main__":
	unittest.main()