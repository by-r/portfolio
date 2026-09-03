# Portfolio — developer Makefile
#
# Python deps are managed with uv (backend/pyproject.toml + uv.lock); the
# frontend uses npm. Recipes are POSIX-shell commands (git-bash / WSL / macOS /
# Linux). On Windows without make, run the recipes directly — each one is a
# plain shell command.

BACKEND  := backend
FRONTEND := frontend
UV       := uv
DJANGO_BIND ?= 127.0.0.1:8000

.DEFAULT_GOAL := help

.PHONY: help
help: ## Show this help
	@printf "Usage: make <target>\n\n"
	@grep -hE '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk -F':.*?## ' '{printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

# --- Python (uv) -----------------------------------------------------------

.PHONY: setup
setup: ## Install all Python deps into .venv (uv sync; run once, then cp .env.example .env)
	cd $(BACKEND) && $(UV) sync

.PHONY: migrate
migrate: ## Apply Django migrations
	cd $(BACKEND) && $(UV) run python manage.py migrate

.PHONY: seed
seed: ## Load sample blog posts (idempotent)
	cd $(BACKEND) && $(UV) run python manage.py seed_posts

.PHONY: superuser
superuser: ## Create a Django admin superuser
	cd $(BACKEND) && $(UV) run python manage.py createsuperuser

.PHONY: run
run: ## Run the Django dev server on http://127.0.0.1:8000
	cd $(BACKEND) && $(UV) run python manage.py runserver $(DJANGO_BIND)

.PHONY: test
test: ## Run the backend test suite (pytest)
	cd $(BACKEND) && $(UV) run pytest

.PHONY: lint
lint: ## Lint backend with ruff
	cd $(BACKEND) && $(UV) run ruff check .

.PHONY: format
format: ## Format backend with ruff
	cd $(BACKEND) && $(UV) run ruff format .

.PHONY: check
check: ## CI-style gate: lint + format-check + tests
	cd $(BACKEND) && $(UV) run ruff check . && $(UV) run ruff format --check . && $(UV) run pytest

.PHONY: deploy-check
deploy-check: ## Run Django's deployment checklist
	cd $(BACKEND) && $(UV) run python manage.py check --deploy

.PHONY: collectstatic
collectstatic: ## Collect static files for production
	cd $(BACKEND) && $(UV) run python manage.py collectstatic --noinput

# --- Frontend (npm) --------------------------------------------------------

.PHONY: frontend-install
frontend-install: ## Install frontend deps from package-lock.json (npm ci)
	cd $(FRONTEND) && npm ci

.PHONY: frontend-dev
frontend-dev: ## Run the Vite dev server on http://localhost:5173
	cd $(FRONTEND) && npm run dev

.PHONY: frontend-build
frontend-build: ## Typecheck + production build
	cd $(FRONTEND) && npm run build

.PHONY: frontend-typecheck
frontend-typecheck: ## Typecheck the frontend only
	cd $(FRONTEND) && npm run typecheck

# --- Cleanup ---------------------------------------------------------------

.PHONY: clean
clean: ## Remove frontend build output (dist/)
	rm -rf $(FRONTEND)/dist

# --- Docker ----------------------------------------------------------------

COMPOSE ?= docker compose
DEV_COMPOSE ?= $(COMPOSE) -f compose.dev.yml
PROD_COMPOSE ?= $(COMPOSE) -f compose.yml

.PHONY: docker-dev docker-dev-down docker-dev-logs docker-dev-migrate
docker-dev: ## Start Docker development (frontend :5173, API :8000)
	$(DEV_COMPOSE) up --build -d

docker-dev-down: ## Stop Docker development containers
	$(DEV_COMPOSE) down

docker-dev-logs: ## Follow Docker development logs
	$(DEV_COMPOSE) logs -f

docker-dev-migrate: ## Run Django migrations in Docker development
	$(DEV_COMPOSE) run --rm web uv run --no-sync python manage.py migrate

.PHONY: docker-prod docker-prod-down docker-prod-logs docker-prod-ps docker-prod-deploy
docker-prod: ## Build and start production containers (requires backend/.env)
	$(PROD_COMPOSE) up --build -d

docker-prod-down: ## Stop production containers; keep volumes
	$(PROD_COMPOSE) down

docker-prod-logs: ## Follow production container logs
	$(PROD_COMPOSE) logs -f

docker-prod-ps: ## Show production container status
	$(PROD_COMPOSE) ps

docker-prod-deploy: ## Pull a clean checkout, rebuild, and restart production
	@set -eu; \
	if [ -n "$$(git status --porcelain)" ]; then \
		echo "Refusing deploy: working tree is not clean."; \
		exit 1; \
	fi; \
	git pull --ff-only; \
	$(PROD_COMPOSE) up --build -d
