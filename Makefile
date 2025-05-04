# Makefile for Django project using Black for linting

# Django manage command
DJANGO_MANAGE = manage.py
DEV_SETTINGS := base.settings.local
PROD_SETTINGS := base.settings.production
VENV_DIR := venv

# Linting command (using black)
.PHONY: lint
lint:
	black .

# Run dev server
.PHONY: local
local:
	@echo "Starting dev server..."
	python $(DJANGO_MANAGE) runserver --settings=$(DEV_SETTINGS)

# Make migrations
.PHONY: migrate
migrate:
	@echo "Making migrations..."
	python $(DJANGO_MANAGE) makemigrations --settings=$(DEV_SETTINGS) --traceback
	@echo "Running migrate..."
	python $(DJANGO_MANAGE) migrate --settings=$(DEV_SETTINGS) --traceback

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
	python $(DJANGO_MANAGE) test

# Default target: help message
.PHONY: help
help:
	@echo "Usage:"
	@echo "  make lint            # Run Black to lint your code"
	@echo "  make local       # Run Django development server"
	@echo "  make migrate       # Make migrations"
	@echo "  make clean       # Reset the database"
	@echo "  make test            # (WIP)Run Django tests"
