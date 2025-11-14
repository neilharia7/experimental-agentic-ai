#!/usr/bin/env python3
"""
AI-powered code fixer for GitHub Actions workflow.
This script analyzes test failures and uses Google's Generative AI to suggest and apply fixes.
"""

import os
import sys
import subprocess
import re
from pathlib import Path
from typing import List, Dict, Tuple

try:
	from google import genai

	HAS_GENAI = True
except ImportError:
	HAS_GENAI = False
	print("Warning: google.genai package not found. Please install it with 'pip install google-genai'")
	sys.exit(1)


class AICodeFixer:
	def __init__(self):
		self.google_api_key = os.getenv('GOOGLE_API_KEY')
		if not self.google_api_key:
			print("Error: GOOGLE_API_KEY environment variable not set")
			sys.exit(1)

		self.project_root = Path('.')

		# Configure the Google Generative AI client
		client = genai.Client(api_key=self.google_api_key)

		# Use Gemini Pro model
		self.model = client.models

	def get_test_output(self) -> str:
		"""Read the test output file."""
		try:
			command = "python -m pytest tests.py -v --tb=short > test_output.txt 2>&1"
			command = command.split()
			_ = subprocess.run(
				command,
				capture_output=True,
				text=True,
				check=False,
			)

			with open('test_output.txt', 'r') as f:
				return f.read()
		except FileNotFoundError:
			return "No test output found"

	def get_source_files(self) -> Dict[str, str]:
		"""Get all Python source files in the project."""
		source_files = {}

		# Get main Python files
		for file_path in self.project_root.glob('*.py'):
			if file_path.name not in ['setup.py', 'conftest.py']:
				try:
					with open(file_path, 'r', encoding='utf-8') as f:
						source_files[str(file_path)] = f.read()
				except Exception as e:
					print(f"Warning: Could not read {file_path}: {e}")

		# Get files from common directories
		for directory in ['src', 'app', 'lib', 'calculator']:
			dir_path = self.project_root / directory
			if dir_path.exists():
				for file_path in dir_path.rglob('*.py'):
					try:
						with open(file_path, 'r', encoding='utf-8') as f:
							source_files[str(file_path)] = f.read()
					except Exception as e:
						print(f"Warning: Could not read {file_path}: {e}")

		return source_files

	def analyze_test_failures(self, test_output: str) -> List[Dict]:
		"""
		Analyze test failures from the test output.
		Returns a list of dictionaries with information about each failure.
		"""
		failures = []

		# Extract failure information using regex
		# Pattern matches: tests.py::TestCalculator::test_addition FAILED
		failure_pattern = r"tests\.py::([\w]+)::(test_\w+) FAILED"

		# Pattern matches the assertion errors
		# Example: E   AssertionError: -4 != -5
		error_pattern = r"E\s+AssertionError:\s*(.+?)(?=\n[_=]|\n\w+\.py:|\Z)"

		failure_matches = list(re.finditer(failure_pattern, test_output))

		for match in failure_matches:
			test_class = match.group(1)
			test_name = match.group(2)

			# Find the corresponding error message in the FAILURES section
			# Look for the specific test failure section
			test_section_pattern = rf"_{{{20,}}} {test_class}\.{test_name} _{{{20,}}}(.*?)(?=_{{{20,}}}|={{{20,}}})"
			section_match = re.search(test_section_pattern, test_output, re.DOTALL)

			error_message = "Unknown error"
			if section_match:
				section_content = section_match.group(1)
				error_match = re.search(error_pattern, section_content, re.DOTALL)
				if error_match:
					error_message = error_match.group(1).strip()

			failures.append({
				"test_name": test_name,
				"test_class": test_class,
				"error_message": error_message
			})

		return failures

	def create_fix_prompt(self, test_output: str, source_files: Dict[str, str], failures: List[Dict]) -> str:
		"""Create a prompt for the AI to fix the code."""
		prompt = """
You are an expert Python developer tasked with fixing bugs in a calculator implementation.
The calculator should follow BODMAS (Brackets, Orders, Division, Multiplication, Addition, Subtraction) rules.

Here are the test failures:

"""
		for failure in failures:
			prompt += f"- Test: {failure['test_name']} in {failure['test_class']}\n"
			prompt += f"  Error: {failure['error_message']}\n\n"

		prompt += "Here is the source code of the relevant files:\n\n"

		for file_path, content in source_files.items():
			prompt += f"--- {file_path} ---\n{content}\n\n"

		prompt += """
Please analyze the test failures and the source code to identify the bugs.
Then, provide a plan to fix the issues and the corrected code for each file that needs to be modified.

Your response should be in the following format:

## Analysis
[Your analysis of the issues]

## Plan
[Your plan to fix the issues]

## Fixed Code
```python
# For each file that needs to be modified, provide the full corrected code
# Filename: [filename]
[corrected code]
```

Make sure your fixes address all the test failures and follow proper BODMAS rules.
"""
		return prompt

	def apply_fixes(self, ai_response: str) -> Dict[str, str]:
		"""
		Extract and apply the fixes from the AI response.
		Returns a dictionary mapping file paths to their updated content.
		"""
		fixed_files = {}

		# Extract code blocks from the AI response
		code_blocks = re.finditer(r"```python\n# Filename: ([\w\.\/]+)\n(.*?)```", ai_response, re.DOTALL)

		for match in code_blocks:
			filename = match.group(1).strip()
			code = match.group(2).strip()

			# Save the fixed code
			fixed_files[filename] = code

			# Write the fixed code to the file
			try:
				with open(filename, 'w', encoding='utf-8') as f:
					f.write(code)
				print(f"Updated file: {filename}")
			except Exception as e:
				print(f"Error writing to {filename}: {e}")

		return fixed_files

	def run_tests(self) -> Tuple[bool, str]:
		"""
		Run the tests and return whether they passed and the output.
		"""
		try:
			result = subprocess.run(
				["python", "-m", "pytest", "tests.py", "-v"],
				capture_output=True,
				text=True,
				check=False
			)
			return result.returncode == 0, result.stdout + result.stderr
		except Exception as e:
			return False, f"Error running tests: {e}"

	def run(self):
		"""Main execution flow."""
		print("Starting AI Code Fixer...")

		# Get test output and source files
		test_output = self.get_test_output()
		source_files = self.get_source_files()

		# Analyze test failures
		failures = self.analyze_test_failures(test_output)
		if not failures:
			print("No test failures found or could not parse test output.")
			return

		print(f"Found {len(failures)} test failures.")

		# Create prompt for AI
		prompt = self.create_fix_prompt(test_output, source_files, failures)
		print(f"\n{prompt}")
		# Get AI response
		print("Requesting AI analysis and fixes...")
		try:
			response = self.model.generate_content(model="gemini-2.0-flash-001", contents=prompt)
			ai_response = response.text

			print("\nAI Analysis and Plan:")
			# Extract and print the analysis and plan sections
			analysis_match = re.search(r"## Analysis\n(.*?)##", ai_response, re.DOTALL)
			if analysis_match:
				print(analysis_match.group(1).strip())

			plan_match = re.search(r"## Plan\n(.*?)##", ai_response, re.DOTALL)
			if plan_match:
				print(plan_match.group(1).strip())

			# Apply the fixes
			print("\nApplying fixes...")
			fixed_files = self.apply_fixes(ai_response)

			if not fixed_files:
				print("No fixes were applied. AI response may not contain properly formatted code blocks.")
				return

			print(f"Applied fixes to {len(fixed_files)} files.")

			# Run tests again to verify fixes
			print("\nRunning tests to verify fixes...")
			tests_pass, test_output = self.run_tests()

			if tests_pass:
				print("✅ All tests are now passing!")
			else:
				print("❌ Some tests are still failing after fixes.")
				print("\nTest output:")
				print(test_output)

		except Exception as e:
			print(f"Error getting AI response: {e}")


if __name__ == "__main__":
	fixer = AICodeFixer()
	fixer.run()
