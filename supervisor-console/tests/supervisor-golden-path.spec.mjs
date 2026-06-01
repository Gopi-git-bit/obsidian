import { expect, test } from "@playwright/test";
import { spawn, spawnSync } from "node:child_process";
import { existsSync, rmSync } from "node:fs";
import { readFile } from "node:fs/promises";
import http from "node:http";
import { fileURLToPath } from "node:url";
import path from "node:path";

const here = path.dirname(fileURLToPath(import.meta.url));
const appRoot = path.resolve(here, "..");
const repoRoot = path.resolve(appRoot, "..");
const backendRoot = path.join(repoRoot, "backend");
const pythonExe = path.join(backendRoot, ".venv", "Scripts", "python.exe");
const dbPath = path.join(appRoot, ".playwright-supervisor.db");
const databaseUrl = "sqlite:///../supervisor-console/.playwright-supervisor.db";
const apiBase = "http://127.0.0.1:8000";
const webBase = "http://127.0.0.1:4177";
const webUrl = `${webBase}/index.html`;

let server;
let staticServer;

function runPython(args) {
  const result = spawnSync(pythonExe, args, { cwd: backendRoot, env: { ...process.env, DATABASE_URL: databaseUrl }, encoding: "utf8" });
  if (result.status !== 0) throw new Error(`Python failed\n${result.stdout}\n${result.stderr}`);
}

async function waitForBackend() {
  const deadline = Date.now() + 30000;
  while (Date.now() < deadline) {
    try {
      const response = await fetch(`${apiBase}/api/v1/health/live`);
      if (response.ok) return;
    } catch {}
    await new Promise((resolve) => setTimeout(resolve, 400));
  }
  throw new Error("Backend did not become ready");
}

async function login(username, role) {
  const response = await fetch(`${apiBase}/api/v1/auth/dev-login`, {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({ username, password: "supervisor-console-dev", role })
  });
  expect(response.status).toBe(200);
  return (await response.json()).access_token;
}

async function apiFetch(pathname, token, options = {}) {
  const response = await fetch(`${apiBase}${pathname}`, {
    method: options.method || "GET",
    headers: { "content-type": "application/json", authorization: `Bearer ${token}` },
    body: options.body ? JSON.stringify(options.body) : undefined
  });
  const text = await response.text();
  return { response, data: text ? JSON.parse(text) : null };
}

async function setupOrderTripEvidence(adminToken, driverToken, supervisorToken) {
  const order = await apiFetch("/api/v1/orders", adminToken, {
    method: "POST",
    body: { shipper_name: "Supervisor E2E", shipper_phone: "9876543210", origin_city: "Tiruppur", origin_state: "Tamil Nadu", destination_city: "Chennai", destination_state: "Tamil Nadu", cargo_type: "general", weight_kg: 1200, num_packages: 12, vehicle_category_preference: "Tractor", estimated_distance_km: 460, offered_price: 18000 }
  });
  expect(order.response.status).toBe(201);
  await apiFetch(`/api/v1/orders/${order.data.id}/transition`, adminToken, { method: "POST", body: { to_state: "CONFIRMED", event: "order_submitted", payload: { payment_mode: "advance", topay_consent_status: "not_required", material_type: "general_goods", body_type_required: "open" }, actor_role: "OMS", idempotency_key: crypto.randomUUID(), trace_id: `sup-e2e-${crypto.randomUUID()}` } });
  const matches = await apiFetch(`/api/v1/orders/${order.data.id}/match?limit=1&min_score=0`, adminToken);
  expect(matches.response.status).toBe(200);
  await apiFetch(`/api/v1/matches/${matches.data.matches[0].match_id}/accept`, adminToken, { method: "POST", body: {} });
  const trip = await apiFetch(`/api/v1/orders/${order.data.id}/trip`, adminToken);
  expect(trip.response.status).toBe(200);
  const driverSub = JSON.parse(Buffer.from(driverToken.split(".")[1], "base64url").toString("utf8")).sub;
  await apiFetch(`/api/v1/trips/${trip.data.trip_id}/assign-driver`, adminToken, { method: "POST", body: { driver_id: driverSub } });
  for (const [toState, event, payload] of [
    ["EN_ROUTE_TO_PICKUP", "driver_started_pickup", {}],
    ["AT_PICKUP_WAITING", "driver_arrived_pickup", {}],
    ["LOADING", "shipment_doc_scanned", { driver_id: driverSub, vehicle_id: trip.data.vehicle_id, doc_type: "loading_photo", doc_url: "s3://docs/loading.jpg", scan_exif: {} }],
    ["DEPARTED_FOR_DELIVERY", "loading_completed", {}],
    ["AT_DELIVERY_WAITING", "driver_arrived_delivery", {}]
  ]) {
    await apiFetch(`/api/v1/orders/${order.data.id}/transition`, adminToken, { method: "POST", body: { to_state: toState, event, payload, actor_role: "DRIVER", idempotency_key: crypto.randomUUID(), trace_id: `sup-e2e-${crypto.randomUUID()}` } });
  }
  const pod = await apiFetch(`/api/v1/trips/${trip.data.trip_id}/pod`, driverToken, { method: "POST", body: { pod_url: "s3://docs/supervisor-pod.jpg", consignee_otp: "123456", pod_exif: {}, uploaded_by: "driver", idempotency_key: `pod-${crypto.randomUUID()}` } });
  expect(pod.response.status).toBe(201);
  const hold = await apiFetch(`/api/v1/supervisor/orders/${order.data.id}/fraud-hold`, supervisorToken, { method: "POST", body: { reason: "POD anomaly", payload: { pod_url: "s3://docs/supervisor-pod.jpg", otp: "123456" } } });
  expect(hold.response.status).toBe(200);
  return { orderId: order.data.id, tripId: trip.data.trip_id, caseId: hold.data.case.case_id };
}

async function startStaticServer() {
  staticServer = http.createServer(async (request, response) => {
    try {
      const requestPath = decodeURIComponent(new URL(request.url || "/", webBase).pathname);
      const safePath = path.normalize(requestPath).replace(/^(\.\.[/\\])+/, "");
      const filePath = path.join(appRoot, safePath === "/" ? "index.html" : safePath);
      if (!filePath.startsWith(appRoot)) return response.writeHead(403).end("Forbidden");
      const body = await readFile(filePath);
      response.writeHead(200, { "content-type": filePath.endsWith(".html") ? "text/html" : filePath.endsWith(".css") ? "text/css" : "text/javascript" });
      response.end(body);
    } catch {
      response.writeHead(404); response.end("Not found");
    }
  });
  await new Promise((resolve) => staticServer.listen(4177, "127.0.0.1", resolve));
}

test.beforeAll(async () => {
  if (existsSync(dbPath)) rmSync(dbPath, { force: true });
  runPython(["-m", "alembic", "upgrade", "head"]);
  runPython(["-c", "from app.database import SessionLocal; from app.models.vehicle_model import VehicleModel; db=SessionLocal(); db.add(VehicleModel(manufacturer='Supervisor Motors', model_name='Tractor E2E', category='Tractor', body_type='open', gvw_kg=3500, payload_kg=2000, mileage_kmpl=12, price_ex_showroom=1200000, is_active=True)); db.commit(); db.close()"]);
  server = spawn(pythonExe, ["-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8000"], { cwd: backendRoot, env: { ...process.env, DATABASE_URL: databaseUrl }, stdio: "pipe" });
  await waitForBackend();
  await startStaticServer();
});

test.afterAll(async () => {
  if (staticServer) await new Promise((resolve) => staticServer.close(resolve));
  if (server) {
    await new Promise((resolve) => {
      server.once("exit", resolve);
      if (process.platform === "win32") spawnSync("taskkill", ["/pid", String(server.pid), "/T", "/F"], { stdio: "ignore" });
      else server.kill();
      setTimeout(resolve, 3000);
    });
  }
  if (existsSync(dbPath)) rmSync(dbPath, { force: true });
});

test("supervisor reviews exception, makes decisions, and wrong roles are blocked", async ({ page }) => {
  const issues = [];
  page.on("console", (m) => { if (m.type() === "error") issues.push(`console: ${m.text()}`); });
  page.on("pageerror", (e) => issues.push(`pageerror: ${e.message}`));
  page.on("requestfailed", (r) => issues.push(`network: ${r.url()}`));
  page.on("dialog", async (d) => { issues.push(`dialog: ${d.message()}`); await d.accept(); });

  const adminToken = await login("sup-e2e-admin", "super_admin");
  const driverToken = await login("sup-e2e-driver", "driver");
  const supervisorToken = await login("sup-e2e-supervisor", "supervisor");
  const customerToken = await login("sup-e2e-customer", "customer");
  const setup = await setupOrderTripEvidence(adminToken, driverToken, supervisorToken);

  await page.goto(webUrl);
  await page.fill("#username", "sup-e2e-supervisor");
  await page.getByRole("button", { name: "Login" }).click();
  await page.waitForLoadState("networkidle");
  await expect(page.locator("#caseList")).toContainText(setup.caseId);
  await page.getByRole("button", { name: new RegExp(setup.caseId) }).click();
  await expect(page.locator("#records")).toContainText("supervisor-pod");
  await page.getByRole("button", { name: "Reject", exact: true }).click();
  await page.waitForLoadState("networkidle");
  await expect(page.locator("#caseBadge")).toHaveText("rejected");
  await page.getByRole("button", { name: "Hold", exact: true }).click();
  await page.waitForLoadState("networkidle");
  await expect(page.locator("#caseBadge")).toHaveText("held");
  await page.getByRole("button", { name: "Approve", exact: true }).click();
  await page.waitForLoadState("networkidle");
  await expect(page.locator("#caseBadge")).toHaveText("approved");
  await expect(page.locator("#auditTrail")).toContainText("approved");

  const wrong = await apiFetch(`/api/v1/supervisor/cases/${setup.caseId}/approve`, customerToken, { method: "POST", body: { reason: "wrong role" } });
  expect(wrong.response.status).toBe(403);
  const driverVerify = await apiFetch(`/api/v1/trips/${setup.tripId}/pod/verify`, driverToken, { method: "POST", body: { verified_by: "driver", idempotency_key: crypto.randomUUID() } });
  expect(driverVerify.response.status).toBe(403);

  expect(issues).toEqual([]);
});
