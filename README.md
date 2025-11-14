# Experimental Agentic AI

This repository demonstrates an AI-powered automated code fixing workflow using Google's Generative AI.

## Project Overview

The project consists of:

1. A calculator implementation in `main.py` with intentional logic mistakes
2. Test cases in `tests.py` for all BODMAS operations
3. A GitHub workflow that automatically fixes code issues when tests fail
4. An AI script that analyzes test failures and suggests fixes

## Calculator Implementation

The calculator in `main.py` implements basic BODMAS operations:
- Brackets (parentheses)
- Orders (powers/exponents)
- Division
- Multiplication
- Addition
- Subtraction

The implementation contains intentional bugs to demonstrate the AI's ability to fix them:
- Addition has a bug when both numbers are negative
- Subtraction has a bug when the first number is less than the second
- Multiplication has a bug for large numbers
- Division has bugs for non-integer division and division by zero
- Power function has a bug for negative exponents
- The calculate method doesn't properly follow BODMAS rules for order of operations

## Test Cases

The `tests.py` file contains comprehensive test cases for all BODMAS operations:
- Individual tests for each operation (add, subtract, multiply, divide, power)
- Tests for parentheses handling
- Tests for order of operations
- Tests for complex expressions

The tests are designed to expose the intentional bugs in the calculator implementation.

## GitHub Workflow

The GitHub workflow in `.github/workflows/auto_fix.yml` is triggered when a pull request is opened, synchronized, or reopened. It:

1. Sets up Python 3.11
2. Installs dependencies including pytest and google-genai
3. Runs the tests
4. If tests fail, it runs the AI script to analyze and fix the issues
5. Runs the tests again to verify the fixes
6. Commits and pushes any changes
7. Comments on the PR with the test results

## AI Script

The AI script in `.github/scripts/ai_assist.py` uses Google's Generative AI (Gemini Pro model) to:

1. Analyze test failures
2. Create a plan to fix the issues
3. Generate corrected code
4. Apply the fixes
5. Run the tests again to verify the fixes

## How It Works

1. When a pull request is opened or updated, the GitHub workflow is triggered
2. The workflow runs the tests
3. If tests fail, the AI script is executed
4. The AI script analyzes the test failures and source code
5. It generates a plan and corrected code
6. The fixes are applied to the source files
7. The tests are run again to verify the fixes
8. The workflow comments on the PR with the results

## Environment Variables

The workflow requires the following environment variable:
- `GOOGLE_API_KEY`: API key for Google's Generative AI

## Dependencies

- Python 3.11
- pytest
- google-genai

## Usage

1. Clone the repository
2. Create a new branch
3. Make changes to the code
4. Open a pull request
5. The workflow will automatically run and fix any issues

## Example

If you modify the calculator implementation and break some functionality, the workflow will:
1. Detect the failing tests
2. Analyze the issues
3. Fix the code
4. Verify the fixes
5. Comment on your PR with details about what was fixed

This demonstrates how AI can be used to automate code reviews and fixes in a CI/CD pipeline.