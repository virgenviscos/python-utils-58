# python-utils-58

`python-utils-58` is a collection of lightweight utility functions designed to simplify and streamline common Python programming tasks. With a focus on code reusability and efficiency, this library provides essential tools that enhance productivity and aid in rapid development.

## Features

- **File Operations**: Easily read, write, and manipulate files with a straightforward interface that supports both text and binary formats.
- **Data Validation**: Simple and powerful functions for validating data types and structures, ensuring cleaner code and fewer bugs.
- **Formatting Helpers**: Quickly format strings, dates, and numbers, allowing for consistent output across different application modules.
- **Environment Configurations**: Load environment variables from `.env` files seamlessly, improving the management of application settings.

## Installation

To install `python-utils-58`, simply run the following command:

```bash
pip install python-utils-58
```

## Basic Usage

Here’s a quick example demonstrating how to use a couple of features from the library:

```python
from python_utils import FileUtils, Validator

# Read from a file
content = FileUtils.read_file('example.txt')
print(content)

# Validate an email address
email = 'user@example.com'
if Validator.validate_email(email):
    print(f"{email} is valid.")
else:
    print(f"{email} is not valid.")
```

Feel free to customize and expand upon these utilities to fit your project's unique needs. The functionality is designed to be flexible and easy to integrate into your codebase.

## License

![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.