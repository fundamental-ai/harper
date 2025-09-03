# Harper Python Bindings

Python bindings for the Harper grammar checker with direct Rust integration for fast grammar checking.

## Installation

```bash
pip install git+https://github.com/fundamental-ai/harper.git#subdirectory=harper-py
```

## Usage

```python
import harper_py

# Create a linter instance
linter = harper_py.HarperLinter()

# Count errors
error_count = linter.count_errors("There is a error")  # Returns: 1

# Get detailed errors
errors = linter.lint("There is a error")
for error in errors:
    print(f"{error.start}-{error.end}: {error.message}")

# Quick boolean check
has_errors = linter.has_errors("Perfect text.")  # Returns: False
```

## License

Licensed under the Apache License, Version 2.0.

Based on [Harper](https://github.com/elijah-potter/harper) by Elijah Potter.