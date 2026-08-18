# Portfolio

A simple, minimalistic portfolio site with a blog.

- **Backend**: Django 5.2 + [django-ninja](https://django-ninja.dev) — read-only REST API, Django admin for authoring
- **Frontend**: Vite + React + TypeScript + Tailwind CSS v4 + [Kumo UI](https://kumo-ui.com) (`@cloudflare/kumo`)
- **Blog**: posts authored as Markdown in Django admin, stored in the DB, served via the ninja API, rendered safely with `react-markdown`

## Layout

```
backend/   Django project (API + admin) — Python 3.10+, SQLite by default
frontend/  Vite React SPA — Node 18+
```

## Prerequisites

- Python 3.10+
- Node 18+ (tested with 18.18)
- (optional) PostgreSQL for production

## Backend setup

```bash
cd backend
python -m venv .venv
# Windows: .venv\Scripts\activate   ·  macOS/Linux: source .venv/bin/activate
pip install -r requirements-dev.txt
cp .env.example .env               # then edit .env (SECRET_KEY etc.)

python manage.py migrate
python manage.py seed_posts        # optional: 2 sample posts
python manage.py createsuperuser  # for Django admin access
python manage.py runserver        # http://127.0.0.1:8000
```

- API: `http://127.0.0.1:8000/api/` — `GET /api/health`, `GET /api/posts`, `GET /api/posts/{slug}`
- Interactive docs (dev only): `http://127.0.0.1:8000/api/docs` (disabled when `DEBUG=False`)
- Admin: `http://127.0.0.1:8000/staff/` (default non-default path — change via `ADMIN_URL`)

## Frontend setup

```bash
cd frontend
npm install
npm run dev                       # http://localhost:5173
```

The dev server proxies `/api` to `http://127.0.0.1:8000` (see `vite.config.ts`), so no CORS config is needed locally. For a production build: `npm run build` (typechecks + bundles to `dist/`).

## Environment variables

See `backend/.env.example` (and `frontend/.env.example`):

| Variable | Purpose | Default |
| --- | --- | --- |
| `SECRET_KEY` | Django secret — generate a strong one for production | dev placeholder |
| `DEBUG` | Debug mode — keep `False` in production | `False` |
| `ALLOWED_HOSTS` | Comma-separated host allowlist | `localhost,127.0.0.1` |
| `DATABASE_URL` | `postgres://user:pass@host:port/name`; empty = SQLite | empty |
| `ADMIN_URL` | Non-default admin path | `staff/` |
| `HTTPS` | Enables secure cookies, SSL redirect, HSTS (prod) | `False` |
| `SECURE_HSTS_SECONDS` | HSTS max-age (e.g. `31536000` in prod) | `0` |
| `CORS_ALLOWED_ORIGINS` | Frontend origins allowed cross-origin | `http://localhost:5173` |
| `RATE_LIMIT_PER_MINUTE` | API requests/minute/IP (uses Django cache) | `120` |
| `RATE_LIMIT_TRUST_PROXY` | Trust `X-Forwarded-For` (only behind a trusted proxy) | `False` |
| `VITE_API_URL` | API origin for the built frontend; empty → `/api` (dev proxy) | empty |

## Security

- **Secrets**: everything env-driven; only `.env.example` is committed, `.env` is gitignored. Django refuses to start (`ImproperlyConfigured`) when `DEBUG=False` and `SECRET_KEY` is missing or still the dev placeholder.
- **Headers**: CSP (`default-src 'self'`, no inline scripts; inline styles only for the admin), `X-Frame-Options: DENY`, `X-Content-Type-Options: nosniff`, `Referrer-Policy: same-origin`, plus HSTS/secure cookies when `HTTPS=True`.
- **CORS**: locked to `CORS_ALLOWED_ORIGINS`; API is GET-only, credentials disabled.
- **Rate limiting**: per-IP fixed-window limiter on `/api/*` and on the admin login endpoint (10 attempts/min), using atomic `cache.add`/`incr`. Uses the Django cache — use a shared cache like Redis in production for accuracy across workers.
- **Admin**: non-default path (`ADMIN_URL`), Django's built-in auth (CSRF, password validators, login throttling).
- **XSS**: blog content is Markdown rendered client-side; `react-markdown` escapes raw HTML by default, and the admin preview widget HTML-escapes all input before rendering.
- **Docs exposure**: OpenAPI/Swagger UI only when `DEBUG=True`.
- **Fixes a Windows install gotcha**: `@tailwindcss/oxide-win32-x64-msvc` is pinned in `package.json` (npm's optional-deps bug).

### Known residual risks

- `react-router-dom@6` (latest 6.x) has two *moderate* advisories (GHSA-wrjc-x8rr-h8h6 open redirect; GHSA-337j-9hxr-rhxg SSR hydration). The open-redirect only affects links with backslash `href`s (our links are internal routes; external links are plain `<a rel="noopener noreferrer">`), and the SSR issue does not apply to this client-only SPA. The fix ships in v7, which requires Node ≥ 20 — upgrade when you move to Node 20+.
- `@shikijs/*` (pulled in by Kumo) warns about Node ≥ 20; it only runs if you use Kumo's `CodeHighlighted` component, which this site does not.

## Testing

```bash
cd backend
python -m pytest -q               # 12 tests: API, drafts/404s, headers, CORS, admin path, API + admin-login rate limits
python manage.py check --deploy   # Django's deployment checklist (warns about HTTPS/HSTS in dev)
```

## Deployment notes

1. Set real env vars (`SECRET_KEY`, `DEBUG=False`, `ALLOWED_HOSTS`, `HTTPS=True`, `SECURE_HSTS_SECONDS`, `CORS_ALLOWED_ORIGINS`, optional `DATABASE_URL`) — startup fails fast if `SECRET_KEY` is missing.
2. Serve Django behind TLS (reverse proxy); set `RATE_LIMIT_TRUST_PROXY=True` only for a trusted proxy that sets `X-Forwarded-For`.
3. `python manage.py collectstatic --noinput` and run with a production WSGI server (e.g. gunicorn).
4. Build the frontend (`npm run build`) and serve `dist/` statically, or point `VITE_API_URL` at the API origin.
5. Use a shared cache (Redis/memcached) so rate limiting is accurate across workers.
