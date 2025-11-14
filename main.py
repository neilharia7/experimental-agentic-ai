"""
Calculator with BODMAS operations.
"""

class Calculator:
	def add(self, a, b):
		return a + b

	def subtract(self, a, b):
		return a - b

	def multiply(self, a, b):
		return a * b

	def divide(self, a, b):
		if b == 0:
			raise ZeroDivisionError("Division by zero")
		return a / b

	def power(self, a, b):
		return a ** b

	def calculate(self, expression):
		"""
		Evaluates a mathematical expression following BODMAS rules.
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

		# Tokenize the expression
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

		# Helper function to perform an operation
		def perform_operation(op_index, tokens):
			operator = tokens[op_index]
			operand1 = tokens[op_index - 1]
			operand2 = tokens[op_index + 1]

			if operator == '^':
				result = self.power(operand1, operand2)
			elif operator == '*':
				result = self.multiply(operand1, operand2)
			elif operator == '/':
				result = self.divide(operand1, operand2)
			elif operator == '+':
				result = self.add(operand1, operand2)
			elif operator == '-':
				result = self.subtract(operand1, operand2)
			else:
				raise ValueError("Invalid operator")

			# Replace the operands and operator with the result
			del tokens[op_index - 1:op_index + 2]
			tokens.insert(op_index - 1, result)
			return tokens

		# Perform operations based on BODMAS order

		# Powers
		i = 1
		while i < len(tokens) - 1:
			if tokens[i] == '^':
				tokens = perform_operation(i, tokens)
				i = 1 # Reset the index after each operation to start from the beginning
			else:
				i += 1

		# Multiplication and Division
		i = 1
		while i < len(tokens) - 1:
			if tokens[i] == '*' or tokens[i] == '/':
				tokens = perform_operation(i, tokens)
				i = 1
			else:
				i += 1

		# Addition and Subtraction
		i = 1
		while i < len(tokens) - 1:
			if tokens[i] == '+' or tokens[i] == '-':
				tokens = perform_operation(i, tokens)
				i = 1
			else:
				i += 1

		return tokens[0] if tokens else 0


if __name__ == '__main__':
	calc = Calculator()
	print("Calculator with BODMAS operations")
	print("Example: 2 + 3 * 4 =", calc.calculate("2 + 3 * 4"))
	print("Example: (2 + 3) * 4 =", calc.calculate("(2 + 3) * 4"))
	print("Example: 2 ^ 3 + 4 =", calc.calculate("2 ^ 3 + 4"))