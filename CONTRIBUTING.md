# Contributing to Cascade Backup Utils

First off, thank you for considering contributing to Cascade Backup Utils! It's people like you that make this tool better for everyone.

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the existing issues as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible:

* Use a clear and descriptive title
* Describe the exact steps which reproduce the problem
* Provide specific examples to demonstrate the steps
* Describe the behavior you observed after following the steps
* Explain which behavior you expected to see instead and why
* Include screenshots if possible

### Suggesting Enhancements

If you have a suggestion for the project, we'd love to hear it. Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

* A clear and descriptive title
* A detailed description of the proposed feature
* Any possible drawbacks or challenges
* If possible, a rough proposal of how to implement it

### Pull Requests

1. Fork the repo and create your branch from `main`
2. If you've added code that should be tested, add tests
3. If you've changed APIs, update the documentation
4. Ensure the test suite passes
5. Make sure your code lints
6. Issue that pull request!

## Development Process

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # For development dependencies
   ```

### Code Style

* Follow PEP 8 guidelines
* Use meaningful variable names
* Add comments for complex logic
* Keep functions focused and small
* Write docstrings for all public functions

### Testing

* Write unit tests for new features
* Ensure all tests pass before submitting PR
* Run tests using:
  ```bash
  pytest
  ```

### Documentation

* Update README.md with any new features
* Document new functions and classes
* Include examples for new features
* Keep documentation clear and concise

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
