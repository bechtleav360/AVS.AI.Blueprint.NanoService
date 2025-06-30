# Contributing Guidelines

Thank you for your interest in contributing to the AVS AI Blueprint NanoService! This document outlines the guidelines and best practices for contributing to the project.

## Table of Contents

- [Code Style](#code-style)
- [Development Setup](#development-setup)
- [Version Control](#version-control)
- [Testing](#testing)
- [Code Review](#code-review)
- [Documentation](#documentation)
- [VS Code Setup](#vs-code-setup)
- [Commit Messages](#commit-messages)
- [Pull Requests](#pull-requests)

## Code Style

### Python

We follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) for Python code style with the following specific rules:

- **Line Length**: 120 characters 
- **Indentation**: 4 spaces (no tabs)
- **Quotes**: Double quotes (`"`) for strings, single quotes (`'`) for characters
- **Imports**: Sorted and grouped in the following order:
  1. Standard library imports
  2. Third-party imports
  3. Local application imports
- **Type Hints**: All new functions, methods, and class attributes must use type hints. Add typing for variable definitions as well

### Formatting

We use the following tools for code formatting:

- **Black**: Primary code formatter
- **isort**: Sorts imports automatically
- **autoflake**: Removes unused imports and variables

### Linting

We use the following linters:

- **Flake8**: General Python style guide enforcement
- **mypy**: Static type checking
- **bandit**: Security linter
- **pydocstyle**: Docstring style checker

## Development Setup

### Prerequisites

- Python 3.12+
- [uv](https://github.com/astral-sh/uv) (recommended) or pip (Python package manager)
- pre-commit (for git hooks)
- Docker and Docker Compose (for containerized development)

### Development with Docker

For a consistent development environment, you can use Docker:

1. **Build the development container**:
   ```bash
   docker build -t your-service-name .
   ```

2. **Run the service in development mode**:
   ```bash
   docker run -it --rm \
     -p 8000:8000 \
     -v ${PWD}:/app \
     -e PYTHONPATH=/app \
     your-service-name
   ```

3. **Access the service**:
   - API Documentation: http://localhost:8000/docs
   - Alternative Documentation: http://localhost:8000/redoc

4. **For development with auto-reload**:
   ```bash
   docker run -it --rm \
     -p 8000:8000 \
     -v ${PWD}:/app \
     -e PYTHONPATH=/app \
     -e ENVIRONMENT=development \
     avs-ai-nanoservice-dev \
     uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
   ```

### Local Development Setup

#### Prerequisites

Ensure you have the prerequisites installed, then follow these setup instructions:

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd AVS.AI.Blueprint.NanoService
   ```

2. Set up the virtual environment and install dependencies:
   
   Using uv (recommended):
   ```bash
   # Create and activate virtual environment
   python -m venv .venv
   .\.venv\Scripts\activate  # On Windows
   # or
   # source .venv/bin/activate  # On Unix/macOS
   
   # Install UV
   pip install uv

   # Install dependencies
   uv pip install -r requirements.txt
   ```
   
   Or using pip:
   ```bash
   # Create and activate virtual environment
   python -m venv .venv
   .\.venv\Scripts\activate  # On Windows
   # or
   # source .venv/bin/activate  # On Unix/macOS
   
   # Install dependencies
   pip install -r requirements.txt
   ```

3. Install pre-commit hooks:
   ```bash
   pre-commit install
   ```

4. Install development dependencies (if any):
   ```bash
   # If you have a requirements-dev.txt
   uv pip install -r requirements-dev.txt  # or use pip
   ```

5. Configure environment variables:
   ```bash
   copy .env.example .env  # On Windows
   # or
   # cp .env.example .env  # On Unix/macOS
   # Edit .env with your configuration
   ```

## VS Code Setup

### Recommended Extensions

- **Python**: Official Python extension
- **Pylance**: Python language server
- **Black Formatter**: For code formatting
- **isort**: For import sorting
- **Flake8**: For linting
- **Mypy**: For type checking
- **Docker**: If using Docker
- **GitLens**: For Git integration

### Settings

Add the following to your VS Code settings (`.vscode/settings.json`):

```json
{
  "python.linting.enabled": true,
  "python.linting.flake8Enabled": true,
  "python.linting.mypyEnabled": true,
  "python.formatting.provider": "black",
  "python.formatting.blackArgs": ["--line-length=120"],
  "python.linting.flake8Args": [
    "--max-line-length=120",
    "--ignore=E203,W503"
  ],
  "python.linting.pylintEnabled": false,
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.organizeImports": true,
    "source.fixAll": true
  },
  "files.autoSave": "onFocusChange",
  "python.analysis.typeCheckingMode": "basic"
}
```

## Version Control

### Branch Naming

Use the following branch naming convention:

```
<type>/<description>-<issue-number>
```

Types:
- `feature/`: New feature
- `fix/`: Bug fix
- `docs/`: Documentation changes
- `refactor/`: Code refactoring
- `test/`: Adding or updating tests
- `chore/`: Maintenance tasks

### Commit Messages

Follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

Example:
```
feat(api): add user authentication endpoint

- Add POST /auth/login endpoint
- Add JWT token generation
- Update documentation

Closes #123
```

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=src --cov-report=term-missing

# Run a specific test file
pytest tests/path/to/test_file.py

# Run a specific test
pytest tests/path/to/test_file.py::test_function_name
```

### Writing Tests

- Follow the Arrange-Act-Assert pattern
- Use descriptive test names
- Test edge cases and error conditions
- Mock external dependencies
- Keep tests independent and isolated

## Code Review

### Process

1. Create a draft pull request for early feedback
2. Request reviews from relevant team members
3. Address all review comments
4. Ensure all tests pass
5. Update documentation if needed
6. Squash and merge when approved

### Review Guidelines

- Check for code quality and consistency
- Verify tests cover new functionality
- Ensure proper error handling
- Check for security vulnerabilities
- Verify documentation is up to date
- For high-impact or sensitive PRs, local checks should be done as well. E.g. Manually test basic functionalities and some edge cases, use a debugger to check, if type hints are correct.

## Documentation

### Code Documentation

- Use Google-style docstrings for all public modules, classes, and functions
- Document all parameters, return values, and exceptions
- Include examples for complex functions

### API Documentation

API documentation is automatically generated using FastAPI's built-in OpenAPI support.

To view the API docs:

1. Start the development server:
   ```bash
   uvicorn src.app:app --reload
   ```

2. Visit `http://localhost:8000/docs` for interactive API documentation.

## Pull Requests

### Creating a Pull Request

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to your fork
5. Open a pull request

### PR Template

```markdown
## Description

[Description of the changes made]

## Related Issues

- Fixes #issue-number
- Related to #issue-number

## Type of Change

- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] This change requires a documentation update

## Checklist

- [ ] My code follows the style guidelines of this project
- [ ] I have performed a self-review of my own code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have made corresponding changes to the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] New and existing unit tests pass locally with my changes
- [ ] Any dependent changes have been merged and published in downstream modules
```

## License

By contributing, you agree that your contributions will be licensed under the project's [LICENSE](LICENSE) file.
