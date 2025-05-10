# Makefile for Django project using Black for linting

# Django manage command
DJANGO_MANAGE = manage.py
DEV_SETTINGS := base.settings.local
PROD_SETTINGS := base.settings.production
VENV_DIR := venv
RUN = uv run

# Linting command (using black)
.PHONY: install-pre-commit
install-pre-commit:
	uv run pre-commit uninstall; uv run pre-commit install

.PHONY: lint
lint:
	uv run pre-commit run --all-files

.PHONY: update
update: install-pre-commit lint

# Run dev server
.PHONY: local
local:
	@echo "Starting dev server..."
	$(RUN) $(DJANGO_MANAGE) runserver --settings=$(DEV_SETTINGS)

# Make migrations
.PHONY: migrate
migrate:
	@echo "Making migrations..."
	$(RUN) $(DJANGO_MANAGE) makemigrations --settings=$(DEV_SETTINGS) --traceback
	@echo "Running migrate..."
	$(RUN) $(DJANGO_MANAGE) migrate --settings=$(DEV_SETTINGS) --traceback

# Reset DB using reset_db command
.PHONY: resetdb
resetdb:
	@echo "Removing the database..."
	rm -rf db.sqlite3
	rm -rf */migrations/*

.PHONY: clean
clean: migrate resetdb

# Run tests (optional if you're using pytest)
.PHONY: test
test:
	$(RUN) $(DJANGO_MANAGE) test portfolio.tests

# Default target: help message
.PHONY: help
help:
	@echo "Usage:"
	@echo "  make lint            # Run Black to lint your code"
	@echo "  make local       # Run Django development server"
	@echo "  make migrate       # Make migrations"
	@echo "  make clean       # Reset the database"
	@echo "  make test            # (WIP)Run Django tests"
