# AGENTS.md

# Zippy Logistics Coding Agent Instructions

## 1. Project Identity

This repository is the MVP implementation for **Zippy Logistics**, a logistics platform for customer shipment booking, driver/vehicle operations, transport company participation, supervisor exception control, finance settlement, policy validation, and operational auditability.

The current project status is:

* Controlled internal pilot ready.
* Not public production ready.
* Backend runtime is verified.
* Docker runtime is verified.
* PostgreSQL migrations are verified.
* Policy preflight is wired into high-risk actions.
* Settlement release is strict, auditable, and idempotent.
* Supervisor holds and finance console are working.
* Dev-login is blocked outside development mode.
* External production integrations are still absent or simulated.

This project must be treated as a **pre-production MVP with safety controls**, not as a playground for broad rewrites.

---

## 2. Current Verified Baseline

Before changing code, assume the current working baseline is:

* Backend tests: `90 passed`
* Admin smoke: `3 passed`
* Customer smoke: `3 passed`
* Driver smoke: `3 passed`
* Transport company smoke: `3 passed`
* Supervisor smoke: `3 passed`
* Finance smoke: `5 passed`
* Admin E2E: `1 passed`
* Customer E2E: `1 passed`
* Driver E2E: `1 passed`
* Transport company E2E: `1 passed`
* Supervisor E2E: `1 passed`
* Finance E2E: `1 passed`
* Docker backend: healthy
* Docker Postgres: healthy
* `/health`: healthy
* `/ready`: ready
* Docker backend runs in `APP_ENV=pilot`
* `/api/v1/auth/dev-login` returns `404` outside development

If your change reduces this baseline, stop and report the regression.

---

## 3. Core Engineering Principle

The system follows this rule:

**Agents propose. Backend enforces. Audit records. Outbox announces.**

Do not allow AI agents, frontend code, or test shortcuts to bypass deterministic backend enforcement.

High-risk backend actions must remain guarded by:

1. RBAC
2. Policy preflight
3. Hard backend validation
4. Idempotency
5. Audit trail
6. Event outbox where applicable

---

## 4. Do Not Break These Critical Flows

The following flows are MVP-critical.

### 4.1 Order Lifecycle

Do not break:

* Order creation
* Order transition endpoint
* State-machine validation
* Policy preflight on order transition
* Invalid transition rejection
* Trace/idempotency metadata handling
* Admin/customer/driver harness flows

Relevant files may include:

* `backend/app/api/orders.py`
* `backend/app/api/flow.py`
* `backend/app/schemas/order.py`
* `backend/tests/test_orders.py`
* `backend/tests/test_order_to_settlement_flow.py`

### 4.2 Settlement Release

Settlement release must only succeed when:

* Order exists
* Trip exists
* POD is verified
* OTP is verified
* No active fraud hold exists
* No active settlement hold exists
* Actor role is `finance_admin` or `super_admin`
* Policy preflight approves
* Existing hard backend validation passes

Do not weaken this.

Relevant files may include:

* `backend/app/api/flow.py`
* `backend/app/api/finance.py`
* `backend/tests/test_settlement_release.py`
* `finance-console/src/app.js`

### 4.3 Supervisor Holds

Do not break:

* Exception case listing/detail
* Fraud hold creation
* Settlement hold creation
* Settlement hold release
* Supervisor decision audit
* Wrong-role blocking
* Driver POD/OTP verification blocking

Relevant files may include:

* `backend/app/api/supervisor.py`
* `backend/app/models/supervisor_model.py`
* `backend/tests/test_supervisor.py`
* `supervisor-console/src/app.js`

### 4.4 Policy Kernel

Do not break:

* `POST /api/v1/policy/check`
* `policy_registry`
* `policy_decisions`
* `route_zone_policy`
* `compliance_document_rules`
* `confidence_thresholds`
* Hold/reject decision creation
* Policy outbox events
* Duplicate idempotency handling

Relevant files may include:

* `backend/app/api/policy.py`
* `backend/app/models/policy_model.py`
* `backend/app/services/policy_service.py`
* `backend/tests/test_policy_kernel.py`

### 4.5 Event Outbox

Do not break:

* Event creation
* Idempotent event handling
* Event read/mark endpoints
* Policy hold/reject outbox events
* Settlement released/block events

Relevant files may include:

* `backend/app/api/outbox.py`
* outbox model/service files
* outbox tests

### 4.6 Auth and Environment Safety

Do not re-enable dev-login outside development.

Rules:

* `APP_ENV=development`: dev-login may work.
* `APP_ENV=pilot`: dev-login must be unavailable.
* `APP_ENV=production`: dev-login must be unavailable.

Relevant files may include:

* `backend/app/config.py`
* `backend/app/api/auth.py`
* `backend/tests/test_api.py`
* `docker-compose.runtime.yml`
* `backend/.env.example`

---

## 5. Repository Structure

Expected major areas:

```text
backend/
  app/
    api/
    models/
    schemas/
    services/
    main.py
    config.py
    observability.py
  alembic/
    versions/
  tests/
  Dockerfile
  docker-entrypoint.sh
  .env.example
  .dockerignore

admin-web/
customer-web/
driver-web/
transport-company-web/
supervisor-console/
finance-console/

docker-compose.runtime.yml
.env.example
AGENTS.md
```

Do not move folders unless explicitly requested.

Do not rename APIs unless tests and frontend clients are updated.

---

## 6. Backend Rules

### 6.1 Framework

Follow the existing backend framework and style.

Do not migrate frameworks.

Do not convert the backend to another stack.

Do not add a second backend architecture.

### 6.2 Migrations

Use Alembic for schema changes.

Every persistent schema change must include:

* Alembic migration
* SQLAlchemy/model update if applicable
* migration parity test where relevant
* PostgreSQL compatibility check
* SQLite/local test compatibility if existing tests depend on it

PostgreSQL enum rules:

* Do not blindly recreate existing enum types.
* Use idempotent enum creation patterns.
* Use `create_type=False` where the enum already exists.
* Never drop live enum/data casually.

Alembic revision ID rule:

* Keep revision IDs within safe length, or ensure `alembic_version.version_num` supports long IDs.
* Current project widened this column for long revision names.

### 6.3 Idempotency

For state-changing actions:

* Require or preserve `idempotency_key`.
* Duplicate requests must not double-create settlements, journal records, GST records, outbox events, or policy decisions.
* Same key with different payload should be handled safely according to existing project pattern.

### 6.4 Traceability

High-risk requests should include:

* `trace_id`
* `idempotency_key`
* `decision_reason`
* `confidence_score`
* `evidence_refs` where applicable

### 6.5 Errors

Return consistent JSON errors.

Include request ID/correlation ID where existing middleware supports it.

Do not expose stack traces in pilot/production mode.

---

## 7. Frontend Harness Rules

The frontend folders are MVP web harnesses/consoles, not final production mobile apps.

Existing surfaces:

* `admin-web`
* `customer-web`
* `driver-web`
* `transport-company-web`
* `supervisor-console`
* `finance-console`

Do not redesign UI unless requested.

Do not add large UI frameworks unless requested.

Do not break smoke or E2E tests.

If backend request metadata changes, update the relevant harness minimally.

E2E spawned backend must run with:

* `APP_ENV=development`
* `CORS_ORIGINS=*` or test-compatible equivalent

This prevents pilot runtime settings from breaking local E2E tests.

---

## 8. Environment Rules

Supported environments:

```text
development
pilot
production
```

### 8.1 Development

Allowed:

* Dev-login
* Local test data
* Local E2E backend
* Open docs if project currently exposes them

### 8.2 Pilot

Required:

* Dev-login blocked
* Controlled users only
* Strong JWT secret
* Restricted CORS
* Docker runtime or managed runtime
* Manual external operations
* No automatic real money movement

### 8.3 Production

Required before public launch:

* Real auth/provisioning
* Real secrets management
* TLS/reverse proxy
* Backup/restore policy
* Payment gateway
* Communication provider
* Object storage
* OCR/document validation
* Live compliance integrations where legally approved
* Monitoring/metrics

Do not pretend the project is production-ready until these exist.

---

## 9. Docker Runtime Rules

Docker runtime profile currently includes:

* Backend container
* PostgreSQL container
* Alembic-on-startup
* `/ready` healthcheck
* `.env.example` templates

Do not hardcode secrets in Dockerfile or compose.

Do not serve app if Alembic migration fails.

Container startup must follow:

```text
alembic upgrade head -> uvicorn app.main:app
```

If migration fails, container should exit.

### Port Warning

Docker backend and Playwright harnesses may both use port `8000`.

Avoid collision:

* Stop Docker runtime before E2E, or
* Configure Docker backend to another port, or
* Configure E2E backend to another port.

---

## 10. Testing Commands

Use Windows-safe commands.

### 10.1 Backend

From `backend/` or project root depending on repo convention:

```powershell
..\.venv\Scripts\python.exe -m pytest -q
```

or if already in root and venv path differs:

```powershell
.\.venv\Scripts\python.exe -m pytest backend/tests -q
```

Use the command that matches the current repo layout.

### 10.2 Frontend Smoke

Run in each frontend folder:

```powershell
npm.cmd test
```

Folders:

```text
admin-web
customer-web
driver-web
transport-company-web
supervisor-console
finance-console
```

### 10.3 Frontend E2E

Run in each frontend folder:

```powershell
npm.cmd run test:e2e
```

Use `npm.cmd`, not `npm`, on Windows PowerShell.

### 10.4 Docker Runtime

From project root:

```powershell
docker compose --env-file backend/.env.example -f docker-compose.runtime.yml config
docker compose --env-file backend/.env.example -f docker-compose.runtime.yml up -d --build
docker compose --env-file backend/.env.example -f docker-compose.runtime.yml ps
```

Health checks:

```powershell
Invoke-RestMethod http://localhost:8000/health
Invoke-RestMethod http://localhost:8000/ready
```

Use configured `BACKEND_PORT` if not `8000`.

Stop runtime:

```powershell
docker compose --env-file backend/.env.example -f docker-compose.runtime.yml down
```

Use `down -v` only when intentionally deleting local Postgres volume.

---

## 11. Git Rules

Before changing code:

```powershell
git status --short
git log --oneline --decorate -10
```

Do not mix unrelated tasks in one commit.

Commit messages should be specific:

```text
mvp: harden pilot runtime environment
mvp: add verified docker runtime profile
mvp: wire policy preflight into settlement and order transitions
chore: ignore playwright test artifacts
```

Do not commit:

* real secrets
* `.env` with credentials
* Playwright `test-results/`
* `playwright-report/`
* local DB files
* generated temporary artifacts

---

## 12. What Not To Build Without Explicit Approval

Do not implement these unless specifically requested:

* Real Razorpay/payment gateway
* Real WhatsApp/SMS/email provider
* Real GST/NIC/e-way filing
* Real ULIP/VAHAN integration
* Real OCR vendor integration
* Full RAG/contextual policy injection
* Full autonomous agent execution layer
* Kubernetes
* Complex Datadog/OpenTelemetry collector
* Full production mobile apps
* Large UI redesign
* Multi-tenant billing
* Public launch setup

These are post-pilot or controlled integration tasks.

---

## 13. Current External Integration Status

Treat these as missing or simulated unless code proves otherwise:

| Integration | Status |
| --- | --- |
| Payment gateway | Not real production integration |
| WhatsApp/SMS/email | Not real production integration |
| Document storage | Not real production integration |
| OCR | Not real production integration |
| GST/NIC/e-way | Not real production integration |
| ULIP/VAHAN | Not real production integration |
| Secrets manager | Not implemented |
| TLS/reverse proxy | Not implemented |
| Metrics exporter | Not implemented |
| Hosted backup/restore | Not implemented |

Do not claim these are complete.

---

## 14. Pilot Readiness Rules

The MVP is suitable for controlled internal pilot only if:

* Backend tests pass.
* Six frontend smoke suites pass.
* Six frontend E2E suites pass.
* Docker runtime is healthy.
* `/health` works.
* `/ready` works.
* Dev-login is blocked in pilot.
* No real money automation is enabled.
* Users are controlled.
* External operations are manual or simulated.
* Backups are planned for pilot data.

---

## 15. Public Production Blockers

Do not call this production-ready until these are completed:

* Real auth/provisioning
* Strong deployed secrets
* TLS/reverse proxy
* DB backup and restore drill
* Real payment gateway with webhook verification
* Real communications provider
* Real document storage and OCR
* GST/NIC/e-way compliance workflow
* ULIP/VAHAN verification if required
* Rate limiting
* Monitoring and alerting
* Frontend production deployment
* Support/incident runbook

---

## 16. Required Response Format for Coding Agents

After every task, return:

```text
1. What was already working
2. What was added
3. Files changed
4. Backend endpoints added/changed
5. Database/migration changes
6. Frontend changes
7. Tests added/updated
8. Commands run
9. Test results
10. Docker/runtime verification result, if relevant
11. Remaining gaps
12. Recommended next task
```

Be factual.

Do not claim completion unless tests pass.

If a command was not run, say so.

If Docker was not available, say so.

If only compose config was verified but runtime was not started, say so.

---

## 17. Required Evidence

Every meaningful claim should include evidence:

* file path
* test command
* test result
* endpoint name
* migration name
* commit hash where relevant

Avoid vague phrases like:

* "probably works"
* "should be fine"
* "production ready"
* "fully complete"

Use precise labels:

* Implemented
* Partial
* Simulated
* Documented only
* Not found
* Not verified

---

## 18. Safe Development Workflow

For any new task:

1. Read current status.
2. Inspect relevant files.
3. Make the smallest change that satisfies the task.
4. Add or update tests.
5. Run targeted tests.
6. Run full backend tests.
7. Run affected frontend smoke/E2E.
8. Run all smoke/E2E if cross-cutting.
9. Verify Docker only if runtime/deployment changed.
10. Report exact results.
11. Commit only when requested or when task explicitly includes commit.

---

## 19. MVP Operating Spine

Do not break this golden path:

```text
Customer creates order
-> order is validated
-> price/payment terms are accepted
-> vehicle/driver assigned
-> driver accepts
-> loading evidence uploaded
-> trip starts
-> delivery reached
-> POD uploaded
-> OTP verified by authorized role
-> supervisor clears exceptions if needed
-> finance releases settlement
-> journal/GST visibility records created
-> audit/outbox records created
-> order closes
```

This is the core of the MVP.

Everything else is secondary.

---

## 20. Final Instruction

Your job as a coding agent is not to make the system bigger.

Your job is to make the current MVP safer, more testable, more deployable, and more truthful.

When in doubt:

* preserve existing tests
* preserve settlement safety
* preserve policy preflight
* preserve RBAC
* preserve auditability
* preserve Docker readiness
* avoid new integrations
* avoid broad rewrites
* ask for clarification if the task could affect money, compliance, legal exposure, or security
