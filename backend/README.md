# Zippy Logitech Backend

FastAPI backend for the logistics workspace. This backend now supports a simple local test setup using SQLite for development and pytest runs.

## Quick Start

From PowerShell:

```powershell
cd "C:\Users\user\Downloads\MiniMax Agent_ Minimize Effort, Maximize Intelligence_files\backend"
.\dev.ps1 setup
.\dev.ps1 test
.\dev.ps1 run
```

## What The Helper Script Does

`.\dev.ps1 setup`

- creates `.venv` if it does not exist
- upgrades `pip`
- installs `requirements.txt`
- creates a local `.env` with `DATABASE_URL=sqlite:///./test.db` if missing
- runs `alembic upgrade head`

`.\dev.ps1 test`

- runs the backend test suite with `pytest`

`.\dev.ps1 run`

- runs `alembic upgrade head`
- starts the FastAPI app with `uvicorn` and reload enabled

## Manual Commands

If you prefer to run commands yourself:

```powershell
cd "C:\Users\user\Downloads\MiniMax Agent_ Minimize Effort, Maximize Intelligence_files\backend"
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

## Local Test Database

- Local development and tests use `backend/.env`
- The default local database is SQLite at `backend/test.db`
- `backend/test.db` is ignored by git

If you later want to point the app at PostgreSQL, replace the `DATABASE_URL` value in `backend/.env`.

## Container Runtime

The backend image is defined in `backend/Dockerfile`. It installs the FastAPI backend, runs Alembic migrations on startup, starts Uvicorn, and exposes a Docker healthcheck against `/ready`.

Build only the backend image from the repository root:

```powershell
docker build -f backend/Dockerfile -t zippy-backend:local backend
```

Run the minimal runtime profile with Postgres and the backend:

```powershell
docker compose --env-file backend/.env.example -f docker-compose.runtime.yml up --build
```

Validate compose configuration without starting containers:

```powershell
docker compose --env-file backend/.env.example -f docker-compose.runtime.yml config
```

The container startup path is intentionally:

```text
alembic upgrade head -> uvicorn app.main:app
```

If migrations fail, the backend container exits instead of serving with a drifted schema.

## Deployment And Observability

Required environment:

- `DATABASE_URL`: database connection string. The app fails startup if this is missing.
- `JWT_SECRET`: signing secret for JWT tokens. Use a strong non-default value for pilot/production.

Optional environment:

- `APP_ENV`: `development`, `pilot`, or `production`. Defaults to `development`.
- `APP_VERSION`: returned by health/readiness responses. Defaults to `1.0.0`.
- `LOG_LEVEL`: Python logging level. Defaults to `INFO`.
- `CORS_ORIGINS`: comma-separated browser origins. Defaults to `*` in local development.
- `SENTRY_DSN`: enables Sentry only when set and `sentry_sdk` is installed.
- `SENTRY_TRACES_SAMPLE_RATE`: optional Sentry trace sample rate. Defaults to `0`.

Operational endpoints:

- `GET /health`: service status, app version, database connectivity, timestamp.
- `GET /ready`: database connectivity plus required migration-backed table availability.
- Existing prefixed probes remain available under `/api/v1/health`, `/api/v1/health/live`, and `/api/v1/ready`.

Request tracing:

- Send `X-Request-ID` to preserve an upstream request id.
- If omitted, the backend generates one and returns it in `X-Request-ID`.
- Request logs include method, path, status code, latency, request id, and trace id.

## Pilot Security Profile

`POST /api/v1/auth/dev-login` is available only when `APP_ENV=development`.

For pilot or production runtime:

```powershell
$env:APP_ENV="pilot"
$env:JWT_SECRET="<strong-random-secret>"
```

Use `POST /api/v1/auth/login` with seeded or manually provisioned accounts for pilot operators. Do not expose dev-login outside local development.

For browser deployments, set `CORS_ORIGINS` to the exact frontend origins, for example:

```text
CORS_ORIGINS=https://admin-pilot.example.com,https://finance-pilot.example.com
```

Avoid `CORS_ORIGINS=*` outside local development.

## Port Isolation For E2E

The Playwright E2E harnesses start their own FastAPI backend on port `8000`. Stop the Docker runtime stack before running E2E tests, or run Docker with another published port:

```powershell
docker compose --env-file backend/.env.example -f ..\docker-compose.runtime.yml down
npm.cmd run test:e2e
```

Alternative:

```powershell
$env:BACKEND_PORT="8010"
docker compose --env-file backend/.env.example -f ..\docker-compose.runtime.yml up -d
```

## Pilot Postgres Backup And Restore

Create a logical backup:

```powershell
docker compose --env-file backend/.env.example -f ..\docker-compose.runtime.yml exec -T postgres pg_dump -U zippy -d zippy -Fc > zippy-pilot.dump
```

Restore into an empty pilot database:

```powershell
docker compose --env-file backend/.env.example -f ..\docker-compose.runtime.yml exec -T postgres pg_restore -U zippy -d zippy --clean --if-exists < zippy-pilot.dump
```

Before restore, take a fresh backup and stop the backend container to avoid writes during restore. Store pilot backups outside the repo and protect them as sensitive data.

## API Documentation

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Project Structure

```text
backend/
├── app/
│   ├── api/          # API routes
│   ├── database/     # Engine and session management
│   ├── models/       # SQLAlchemy models
│   ├── schemas/      # Pydantic schemas
│   └── services/     # Business logic
├── tests/            # Backend test suite
├── .env              # Local developer database config
├── dev.ps1           # Setup/test/run helper
├── pytest.ini        # Pytest defaults
└── requirements.txt  # Python dependencies
```

## Current Status

- Local environment bootstraps from PowerShell
- Backend tests pass cleanly
- Local test database config is already wired for this workspace
