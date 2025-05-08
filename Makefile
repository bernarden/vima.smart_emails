.PHONY: test lint format check install clean

install:
	pip install -e .[dev]

test:
	pytest --cov=smart_emails --cov-report=term-missing tests/

lint:
	flake8 smart_emails tests
	mypy smart_emails tests

format:
	black smart_emails tests

check: lint test

clean:
	find . -type d -name '__pycache__' -exec rm -rf {} +
	rm -rf .pytest_cache .mypy_cache .coverage htmlcov
