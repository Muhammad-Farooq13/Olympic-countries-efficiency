# Contributing to Olympic Countries Efficiency Analysis

Thank you for your interest in contributing! Please follow these guidelines:

## Code of Conduct
- Be respectful and inclusive
- Welcome diverse perspectives
- Focus on constructive feedback

## How to Contribute

### Reporting Bugs
1. Check if the issue already exists
2. Provide a clear description with steps to reproduce
3. Include environment details (Python version, OS, etc.)

### Suggesting Enhancements
1. Use the issue tracker with clear description
2. Explain the use case and benefits
3. Provide examples if possible

### Pull Requests
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/YourFeature`
3. Make changes and commit: `git commit -m 'Add YourFeature'`
4. Push to the branch: `git push origin feature/YourFeature`
5. Submit a Pull Request with description

## Development Setup

```bash
# Clone repository
git clone https://github.com/Muhammad-Farooq-13/olympic-countries-efficiency.git
cd olympic-countries-efficiency

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install development tools
pip install -e .[dev]
```

## Code Quality

- Follow PEP 8 style guide
- Write meaningful commit messages
- Include docstrings for functions
- Add unit tests for new features
- Run tests before submitting: `pytest tests/ -v`

## Testing

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest --cov=src tests/

# Run specific test file
pytest tests/test_data.py -v
```

## Documentation

- Update README.md for major changes
- Include docstrings in all modules
- Provide usage examples
- Comment complex logic

## Questions?

Feel free to open an issue for questions or discussions!

Thank you for contributing! 🙌
