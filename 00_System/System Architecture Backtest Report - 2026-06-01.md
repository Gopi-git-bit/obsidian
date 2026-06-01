---
type: report
domain: architecture
scope: system_backtest
status: active
last_updated: 2026-06-01
related_hubs:
  - "[[Testing and Verification Strategy for Current Project]]"
  - "[[Backend Structure for Current Project]]"
  - "[[API and Event Contract for Current Project]]"
  - "[[Frontend Architecture for Current Project]]"
  - "[[02_Agentic_AI_Application]]"
tags:
  - testing
  - backtest
  - backend
  - frontend
  - database
  - ai-agents
---

# System Architecture Backtest Report - 2026-06-01

## Executive Result

The backend runtime behavior is healthy when bootstrapped from the current SQLAlchemy models, but the migration/database path is not release-safe.

Key result:

- `create_all` clean database: backend tests pass, `38 passed`.
- Alembic-migrated clean database: backend order tests fail because migration `001_initial_schema.py` creates legacy `orders.status NOT NULL`, while the current model writes `current_state`.
- Existing `backend/test.db`: stale/mixed schema. It has old `orders` columns, some newer state-machine tables, and no Alembic revision value.

This is a release blocker for customer, driver, transport company, admin, backend, AI-agent API, and database integration because all order lifecycle surfaces depend on successful order creation.

## Test Coverage Matrix

| Surface | Current Artifact | Test Performed | Result | Architecture Finding |
|---|---|---|---|---|
| Customer mobile app | Specification notes only | Repo scan for frontend app/package | Not runnable | No implemented RN/Expo app found in workspace |
| Driver mobile app | Specification notes only | Repo scan for frontend app/package | Not runnable | No implemented RN/Expo app found in workspace |
| Transport company app | Specification notes only | Repo scan for frontend app/package | Not runnable | No implemented RN/Expo app found in workspace |
| Web admin | Specification notes only | Repo scan for frontend app/package | Not runnable | No implemented Next/Vite/admin app found in workspace |
| Backend API | FastAPI app under `backend/app` | Pytest against clean `create_all` DB | Pass | Runtime model/API behavior passes current tests |
| Backend migrations | Alembic migrations under `backend/alembic` | Alembic upgrade + pytest | Fail | Migration schema and model schema are out of sync |
| Database | SQLite local DB + Alembic | Existing DB inspection + migration validation | Fail | `backend/test.db` is stale/mixed and not revision-stamped |
| AI agents | Agent clients + docs | Static contract scan | Partial | Client wrappers exist, but public `/agents`, `/rag`, `/supervisor` API surfaces are not fully implemented |
| AI agent API | Transition API and agent clients | Pytest transition/idempotency tests via clean `create_all` DB | Pass | State transition, idempotency, DLQ, and reservation tests pass only when DB schema matches model |
| Pricing backtest | `backend/scripts/pricing_backtest.py` | Script execution | Pass | 10 rows, 8 pass, 2 review |
| Accounting policy backtest | `backend/scripts/accounting_policy_backtest.py` | Script execution | Pass | 8 rows, 8 pass, 0 fail, 1 blocked, 2 review |
| Partnership terms backtest | `backend/scripts/partnership_terms_backtest.py` | Script execution | Pass | 16 rows, 8 approve, 2 review, 6 block, 0 fail |

## Commands Executed

```powershell
.\.venv\Scripts\python.exe -m pytest -q
$env:DATABASE_URL='sqlite:///./architecture_verification.db'; .\.venv\Scripts\python.exe -m alembic upgrade head
$env:DATABASE_URL='sqlite:///./architecture_verification.db'; .\.venv\Scripts\python.exe -m pytest -q
$env:DATABASE_URL='sqlite:///./create_all_verification.db'; .\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe scripts\pricing_backtest.py
.\.venv\Scripts\python.exe scripts\accounting_policy_backtest.py
.\.venv\Scripts\python.exe scripts\partnership_terms_backtest.py
```

## Detailed Results

### Backend With Existing `test.db`

Result:

```text
22 failed, 16 passed
```

Root cause:

```text
sqlite3.OperationalError: no such column: orders.customer_id
sqlite3.OperationalError: table orders has no column named customer_id
```

Interpretation:

The checked local DB is not aligned with the current model. It lacks state-machine columns such as `customer_id`, `vehicle_id`, `current_state`, and related metadata.

### Backend With Fresh Alembic DB

Result:

```text
21 failed, 17 passed
```

Root cause:

```text
sqlite3.IntegrityError: NOT NULL constraint failed: orders.status
```

Interpretation:

Alembic creates a legacy physical `orders.status` column in `001_initial_schema.py`. The current SQLAlchemy model exposes `status` as a compatibility property derived from `current_state`; it does not write a physical `status` column. Therefore, any order insert fails on an Alembic-created DB.

### Backend With Fresh `create_all` DB

Result:

```text
38 passed
```

Interpretation:

The current runtime model, API routes, order state-machine service, idempotency behavior, DLQ behavior, and reservation behavior are internally coherent when the DB schema is generated directly from models.

## Release Blockers

1. Migration path is not authoritative.
   - Production and staging cannot rely on `create_all`.
   - Alembic must be fixed so a fresh migrated DB matches the current model.

2. Local `backend/test.db` is stale.
   - It is neither a clean initial schema nor a correctly migrated schema.
   - It should be regenerated or isolated per test run.

3. Frontend apps are not present as runnable packages.
   - Customer, driver, transport company, and web admin cannot be functionally tested in this workspace yet.
   - Current frontend validation is limited to PRD/spec review.

4. AI-agent APIs are incomplete as concrete public routes.
   - Agent clients exist for transition calls.
   - `/agents`, `/rag`, and `/supervisor` route families from the architecture contract are not fully implemented in the FastAPI surface.

## Required Fixes Before Full End-to-End Testing

1. Align Alembic with the canonical model.
   - Remove or neutralize legacy `orders.status` as a required physical column.
   - Ensure `orders.current_state` is the only lifecycle truth.
   - Add migration-level checks for state audit, DLQ, reservation, idempotency, and metadata columns.

2. Make tests use isolated databases.
   - Use a fresh temporary SQLite file per run or in-memory DB with shared connection handling.
   - Do not depend on a long-lived `backend/test.db`.

3. Add migration parity tests.
   - One test must create a clean DB through Alembic and run the order creation/state-machine test path.
   - This catches model/migration drift immediately.

4. Implement frontend packages or mark them explicitly as not yet built.
   - Customer app
   - Driver app
   - Transport company app
   - Web admin

5. Implement concrete AI-agent API endpoints.
   - `/agents/{agent_code}/context/{entity_type}/{entity_id}`
   - `/agents/{agent_code}/recommendations`
   - `/agents/{agent_code}/actions`
   - `/supervisor/policy/check`
   - `/rag/query`
   - `/rag/ocr/validate`

6. Add contract tests across agent interconnections.
   - OPS to RAG validation.
   - OPS to FIN payment intent.
   - OPS to IMS/RMA reservation.
   - TMS to OPS geofence transition.
   - FIN to SUP settlement approval.
   - RAG/OCR to SUP fraud hold.
   - Any worker to DLQ and replay.

## Architect Recommendation

Treat this system as ready for backend behavioral iteration, but not ready for full autonomous application integration until database migration parity is fixed.

The next highest-value engineering step is to repair Alembic and add a migration-backed test job. After that, scaffold the four frontend apps and wire smoke tests for:

- customer creates order
- driver accepts assignment
- transport company provides capacity
- admin views DLQ/audit
- supervisor approves or holds settlement
- finance releases settlement only after POD/OTP evidence
