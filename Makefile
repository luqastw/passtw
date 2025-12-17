.PHONY: install test sec run clean build

PYTHON_VERSION := 3.11

install:
	@echo "[ + ] Installing dependencies..."
	poetry install

test:
	@echo "[ ✔ ] Running tests..."
	poetry run pytest -v

sec:
	@echo "[ ★ ] Running security checks..."
	poetry run bandit -r src/
	poetry run pip-audit

run:
	@echo "[ ➤ ] Starting in DEV mode..."
	PASSTW_ENV=dev poetry run passtw $(ARGS)

clean:
	@echo "[ ✘ ] Cleaning up artifacts..."
	rm -rf dist build .pytest_cache
	find . -type d -name "__pycache__" -exec rm -rf {} +

build: clean test sec
	@echo "[ ⬆ ] Building package..."
	poetry build