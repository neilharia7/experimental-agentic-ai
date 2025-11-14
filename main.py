"""
Calculator with BODMAS operations.
This calculator has intentional bugs for testing purposes.
"""


class Calculator:
	def add(self, a, b):
		# Intentional bug: Addition sometimes returns an incorrect result for negative numbers
		if a < 0 and b < 0:
			return a + b + 1  # Bug: adds 1 when both numbers are negative
		return a + b

	def subtract(self, a, b):
		# Intentional bug: Subtraction sometimes returns an incorrect result
		if a < b:
			return a - b + 2  # Bug: adds 2 when a < b
		return a - b

	def multiply(self, a, b):
		# Intentional bug: Multiplication sometimes returns an incorrect result for large numbers
		if a > 10 and b > 10:
			return a * b - 10  # Bug: subtracts 10 when both numbers are > 10
		return a * b

	def divide(self, a, b):
		# Intentional bug: Division doesn't handle division by zero properly
		# and returns an incorrect result for certain values
		if b == 0:
			return "Error"  # Should raise an exception instead

		if a % b == 0:
			return a / b
		else:
			return a / b + 0.1  # Bug: adds 0.1 to non-integer division results

	def power(self, a, b):
		# Intentional bug: Power function returns an incorrect result for negative exponents
		if b < 0:
			return 1 / (a ** (-b)) - 0.01  # Bug: subtracts 0.01 from negative exponent results
		return a ** b

	def calculate(self, expression):
		"""
		Evaluates a mathematical expression following BODMAS rules.
		Intentional bug: Doesn't properly handle order of operations.
		"""
		# Remove all spaces
		expression = expression.replace(" ", "")

		# Handle parentheses first (B in BODMAS)
		while "(" in expression and ")" in expression:
			# Find the innermost parentheses
			open_idx = expression.rfind("(")
			close_idx = expression.find(")", open_idx)

			if open_idx != -1 and close_idx != -1:
				# Extract and evaluate the sub-expression
				sub_expr = expression[open_idx + 1:close_idx]
				sub_result = self.calculate(sub_expr)

				# Replace the parenthesized expression with its result
				expression = expression[:open_idx] + str(sub_result) + expression[close_idx + 1:]
			else:
				break

		# Bug: Doesn't properly follow BODMAS for the rest of the operations
		# Should handle powers, then multiplication/division, then addition/subtraction
		# Instead, just evaluates left to right

		# Process the expression without parentheses
		# This implementation is intentionally buggy and doesn't follow BODMAS

		# First, tokenize the expression
		tokens = []
		current_num = ""

		for char in expression:
			if char.isdigit() or char == '.':
				current_num += char
			else:
				if current_num:
					tokens.append(float(current_num))
					current_num = ""
				tokens.append(char)

		if current_num:
			tokens.append(float(current_num))

		# Bug: Process tokens from left to right without respecting BODMAS
		result = tokens[0] if tokens else 0
		i = 1

		while i < len(tokens):
			if tokens[i] == '+':
				result = self.add(result, tokens[i + 1])
				i += 2
			elif tokens[i] == '-':
				result = self.subtract(result, tokens[i + 1])
				i += 2
			elif tokens[i] == '*':
				result = self.multiply(result, tokens[i + 1])
				i += 2
			elif tokens[i] == '/':
				result = self.divide(result, tokens[i + 1])
				i += 2
			elif tokens[i] == '^':
				result = self.power(result, tokens[i + 1])
				i += 2
			else:
				i += 1

		return result


if __name__ == '__main__':
	calc = Calculator()
	print("Calculator with BODMAS operations")
	print("Example: 2 + 3 * 4 =", calc.calculate("2 + 3 * 4"))  # Should be 14, but will return 20 due to bug
	print("Example: (2 + 3) * 4 =", calc.calculate("(2 + 3) * 4"))  # Should be 20
	print("Example: 2 ^ 3 + 4 =", calc.calculate("2 ^ 3 + 4"))  # Should be 12
