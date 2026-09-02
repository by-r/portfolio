# Contributing

Thanks for contributing to the Portfolio. It's a small Django-Ninja + Vite/React
repo; this guide keeps contributions consistent. The agent-facing `AGENTS.md`
has the full command/architecture reference.

## Setup

```bash
# Python deps (uv) + local env
make setup                                  # uv sync — or: cd backend && uv sync
cp backend/.env.example backend/.env        # edit SECRET_KEY / DEBUG for local dev
make migrate && make seed && make superuser

# Frontend deps
make frontend-install                       # npm ci — or: cd frontend && npm install

# Run both (two terminals)
make run                                    # Django  -> http://127.0.0.1:8000  (admin /staff/)
make frontend-dev                           # Vite    -> http://localhost:5173
```

## Where things live

- Backend API + admin: `backend/` — `config/` (Django project) and `portfolio/` (the app: models, ninja API, admin, middleware, tests).
- Blog content: authored in Django admin as Markdown. `Post.is_published` controls visibility — the API only serves published posts (drafts return 404).
- Frontend SPA: `frontend/src/` — `pages/`, `components/Layout.tsx`, `lib/api.ts` (typed API client).

## Workflow

- Branch per change (`git checkout -b feat/…` or `fix/…`); keep commits small and focused, with imperative messages.
- Don't mix refactors with features in one commit.
- Post-related changes: add a test in `backend/portfolio/tests.py` covering the behavior (published-only, 404s, security).

## Before submitting

- `make check` must pass — ruff lint + format-check + pytest (14 tests).
- `make frontend-typecheck` and `make frontend-build` must pass (TS + production build).
- Never commit secrets: `.env` is gitignored; only `.env.example` is tracked. New env vars go into `backend/.env.example` and should be documented in `README.md`.
- Dependency changes: backend → update `backend/pyproject.toml` and commit the regenerated `uv.lock`; frontend → update `frontend/package.json` + `package-lock.json`.
- Respect the security invariants: API stays GET-only and published-only, Markdown is never rendered as raw HTML (react-markdown / escaping preview), rate limiting and the non-default `ADMIN_URL` stay intact.

## Reporting issues

Include: expected vs. actual behavior, steps to reproduce, and versions
(`uv run python --version`, `node --version`).
