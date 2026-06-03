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

`.\dev.ps1 test`

- runs the backend test suite with `pytest`

`.\dev.ps1 run`

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

## Deployment And Observability

Required environment:

- `DATABASE_URL`: database connection string. The app fails startup if this is missing.

Optional environment:

- `APP_VERSION`: returned by health/readiness responses. Defaults to `1.0.0`.
- `LOG_LEVEL`: Python logging level. Defaults to `INFO`.
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
