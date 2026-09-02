# AGENTS.md

Portfolio: a minimal portfolio site + blog. Django 5.2 + django-ninja backend in
`backend/`, Vite + React + TypeScript + Tailwind CSS v4 + Kumo UI SPA in
`frontend/`. Blog posts are authored as Markdown in Django admin, stored in the
DB, and served read-only via the API.

## Commands

Run from the repo root. Python deps are managed with uv (`backend/pyproject.toml`
+ committed `backend/uv.lock`; interpreter pinned via `backend/.python-version`).

- `make setup` — `uv sync`: create/refresh `backend/.venv` and install deps
- `make migrate` / `make seed` / `make superuser` — Django migrate / seed sample posts / create admin user
- `make docker-dev` — migrate, seed demo data, and start Docker development services
- `make docker-prod` — build and start production services (requires `backend/.env`)
- `make run` — Django dev server → http://127.0.0.1:8000 (admin at `/{ADMIN_URL}` = `/staff/`)
- `make test` — `uv run pytest` (suite in `backend/portfolio/tests.py`, 14 tests)
- `make lint` / `make format` — `uv run ruff check .` / `uv run ruff format .`
- `make check` — lint + format-check + tests (CI-style gate)
- `make deploy-check` — `uv run python manage.py check --deploy`
- `make frontend-install` — `npm ci`; `make frontend-dev` — Vite dev server → http://localhost:5173 (proxies `/api` → `127.0.0.1:8000`); `make frontend-build` — `tsc && vite build`; `make frontend-typecheck` — `tsc --noEmit`
- Direct equivalents: `cd backend && uv run python manage.py runserver`; `cd frontend && npm run dev`

Env: copy `backend/.env.example` → `backend/.env` (gitignored; a local dev `.env`
with `DEBUG=True` already exists). Django fails fast when `DEBUG=False` and
`SECRET_KEY` is still the placeholder. Tests set their own `SECRET_KEY` via
`backend/pytest_plugin.py` (loaded through `pytest.ini`).

## Architecture

- `backend/config/` — Django project: `settings.py` (env-driven; security: CORS allowlist, CSP 4.x, HTTPS/secure-cookie toggles, rate limits, `ADMIN_URL`), `urls.py` (mounts `ADMIN_URL` + `/api/`), `api.py` (NinjaAPI instance + `GET /api/health`).
- `backend/portfolio/` — the app:
  - `models.py` — `Post` (title, slug auto from title, content=Markdown, `is_published`, timestamps)
  - `api.py` — read-only GET endpoints `/api/posts`, `/api/posts/{slug}` (published only; drafts/unknown → 404)
  - `admin.py` + `widgets.py` — admin with a live XSS-safe Markdown preview widget (`static/portfolio/admin/…`)
  - `middleware.py` — per-IP rate limiting (API + admin login)
  - `management/commands/seed_posts.py` — idempotent sample posts
  - `management/commands/seed_demo.py` — DEBUG-only Docker development user/posts
  - `tests.py` — pytest suite (API behavior + security: headers, CORS, admin path, rate limits)
- `frontend/src/` — `main.tsx` entry → `App.tsx` (BrowserRouter + Kumo `LinkProvider` adapter), `pages/` (Home, Blog, BlogPost), `components/Layout.tsx`, `lib/api.ts` (typed fetch client, `VITE_API_URL` fallback `/api`), `index.css` (Kumo styles imported before Tailwind).

## Conventions

- Python 3.10+; lint/format via ruff (line-length 100; RUF012 ignored for Django class-attr idiom) — see `backend/pyproject.toml`.
- Deps only through `backend/pyproject.toml` + `uv.lock` (uv sync); commit `uv.lock`; frontend deps via npm (`package-lock.json` committed).
- Settings are env-driven; never hardcode secrets. `DEBUG=False` + placeholder `SECRET_KEY` must fail fast.
- The API is GET-only and returns only `is_published=True` posts — keep it that way (no write endpoints, no draft leaks).
- Blog content is Markdown: the frontend renders with `react-markdown` (raw HTML escaped by default); the admin preview widget HTML-escapes input first. Never use `rehype-raw` or `dangerouslySetInnerHTML` for post content.
- Frontend: TypeScript strict; Tailwind v4 + Kumo UI import order in `index.css` must stay `@source` → `@import "@cloudflare/kumo/styles/tailwind"` → `@import "tailwindcss"`.
- Tests: pytest + pytest-django (`DJANGO_SETTINGS_MODULE=config.settings`, `pythonpath=.`, `-p pytest_plugin` in `backend/pytest.ini`). New behavior → new test in `backend/portfolio/tests.py`.

## Notes

(quick notes for future sessions — e.g. deployment specifics, gotchas)
