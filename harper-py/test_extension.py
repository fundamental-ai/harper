import harper_py

# Test basic functionality
linter = harper_py.HarperLinter()

# Test the functions
test_text = "There is a error"
print(f"Error count: {linter.count_errors(test_text)}")
print(f"Has errors: {linter.has_errors(test_text)}")

errors = linter.lint(test_text)
print(f"Detailed errors: {len(errors)} found")
for error in errors:
    print(f"  - {error.start}-{error.end}: {error.message}")