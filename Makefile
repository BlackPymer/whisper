.PHONY: install dev-install run test lint format check clean

# Install production dependencies
install:
	uv sync

# Install with development dependencies
dev-install:
	uv sync --group dev

# Run the server
run:
	export PATH="$(PWD)/bin:$$PATH" && python3 run_server.py

# Run tests
test:
	python3 -m pytest tests/ -v

# Run linting
lint:
	uv run ruff check .
	uv run pyright .

# Format code
format:
	uv run ruff format .

# Run all checks (format, lint, test)
check: format lint test

# Clean cache files
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 