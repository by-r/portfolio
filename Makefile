# Portfolio — developer Makefile
#
# Python deps are managed with uv (backend/pyproject.toml + uv.lock); the
# frontend uses npm. Recipes are POSIX-shell commands (git-bash / WSL / macOS /
# Linux). On Windows without make, run the recipes directly — each one is a
# plain shell command.

BACKEND  := backend
FRONTEND := frontend
UV       := uv

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
	cd $(BACKEND) && $(UV) run python manage.py runserver 127.0.0.1:8000

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

# --- Local convenience aliases ---------------------------------------------

.PHONY: local-setup
local-setup: setup frontend-install ## Install native backend and frontend dependencies

.PHONY: local-migrate
local-migrate: migrate ## Apply Django migrations using the native environment

.PHONY: local-backend
local-backend: run ## Run Django locally at http://127.0.0.1:8000

.PHONY: local-frontend
local-frontend: frontend-dev ## Run Vite locally at http://localhost:5173

.PHONY: local-check
local-check: check frontend-typecheck ## Run backend checks and frontend typecheck

# --- Docker ----------------------------------------------------------------

COMPOSE           ?= docker compose
DEV_COMPOSE_FILE  ?= compose.dev.yml
PROD_COMPOSE_FILE ?= compose.yml
NGINX_PORT        ?= 80

.PHONY: docker-dev-up
docker-dev-up: ## Build and start Docker development services (Vite :5173, Django :8000)
	$(COMPOSE) -f $(DEV_COMPOSE_FILE) up --build -d

.PHONY: docker-dev-down
docker-dev-down: ## Stop Docker development services
	$(COMPOSE) -f $(DEV_COMPOSE_FILE) down

.PHONY: docker-dev-logs
docker-dev-logs: ## Follow Docker development logs
	$(COMPOSE) -f $(DEV_COMPOSE_FILE) logs -f

.PHONY: docker-dev-migrate
docker-dev-migrate: ## Apply Django migrations in Docker development services
	$(COMPOSE) -f $(DEV_COMPOSE_FILE) run --rm web python manage.py migrate

.PHONY: docker-prod-up
docker-prod-up: ## Build and start production containers (requires backend/.env)
	NGINX_PORT=$(NGINX_PORT) $(COMPOSE) -f $(PROD_COMPOSE_FILE) up --build -d

.PHONY: docker-prod-down
docker-prod-down: ## Stop production containers; preserves SQLite and static volumes
	$(COMPOSE) -f $(PROD_COMPOSE_FILE) down

.PHONY: docker-prod-logs
docker-prod-logs: ## Follow production container logs
	$(COMPOSE) -f $(PROD_COMPOSE_FILE) logs -f

.PHONY: docker-prod-ps
docker-prod-ps: ## Show production container status
	$(COMPOSE) -f $(PROD_COMPOSE_FILE) ps

.PHONY: docker-prod-deploy
docker-prod-deploy: ## Pull a clean working tree, rebuild, and restart production
	@set -eu; \
	if [ -n "$$(git status --porcelain)" ]; then \
		echo "Refusing deploy: working tree is not clean."; \
		echo "Commit, stash, or discard local changes first."; \
		exit 1; \
	fi; \
	git pull --ff-only; \
	NGINX_PORT=$(NGINX_PORT) $(COMPOSE) -f $(PROD_COMPOSE_FILE) up --build -d
