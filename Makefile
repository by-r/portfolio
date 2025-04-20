# Makefile for Django project using Black for linting

# Django manage command
DJANGO_MANAGE = manage.py

# Linting command (using black)
.PHONY: lint
lint:
	black .

# Run Django development server
.PHONY: runserver
runserver:
	python $(DJANGO_MANAGE) runserver

# Clean the SQLite database (use with caution)
.PHONY: clean-sqlite
clean-sqlite:
	@echo "WARNING: This will delete the SQLite database!"
	rm -f db.sqlite3
	python $(DJANGO_MANAGE) migrate --fake

# Clear pyc files (optional cleanup)
.PHONY: clear-pyc
clear-pyc:
	find . -name "*.pyc" -exec rm -f {} \;

# Install requirements (if needed)
.PHONY: install-requirements
install-requirements:
	pip install -r requirements.txt

# Run tests (optional if you're using pytest)
.PHONY: test
test:
	python $(DJANGO_MANAGE) test

# Collect static files (optional)
.PHONY: collectstatic
collectstatic:
	python $(DJANGO_MANAGE) collectstatic --noinput

# Default target: help message
.PHONY: help
help:
	@echo "Usage:"
	@echo "  make lint            # Run Black to lint your code"
	@echo "  make runserver       # Run Django development server"
	@echo "  make clean-sqlite    # Clean the SQLite database (deletes db.sqlite3)"
	@echo "  make clear-pyc       # Clear all .pyc files"
	@echo "  make install-requirements  # Install requirements from requirements.txt"
	@echo "  make test            # Run Django tests"
	@echo "  make collectstatic   # Collect static files"
