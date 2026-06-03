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
const dbPath = path.join(appRoot, ".playwright-transport.db");
const databaseUrl = "sqlite:///../transport-company-web/.playwright-transport.db";
const apiBase = "http://127.0.0.1:8000";
const webBase = "http://127.0.0.1:4176";
const webUrl = `${webBase}/index.html`;

let server;
let staticServer;

function runPython(args) {
  const result = spawnSync(pythonExe, args, { cwd: backendRoot, env: { ...process.env, DATABASE_URL: databaseUrl, APP_ENV: "development", CORS_ORIGINS: "*" }, encoding: "utf8" });
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
    body: JSON.stringify({ username, password: "transport-company-web-dev", role })
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

async function createCompanyMatch(adminToken, companyToken, category, shipperName) {
  const vehicle = await apiFetch("/api/v1/vehicles", companyToken, {
    method: "POST",
    body: { manufacturer: "Company Fleet", model_name: `${category} Unit`, category, body_type: category === "Tipper" ? "tipper" : "open", gvw_kg: 3500, payload_kg: 2000, mileage_kmpl: 12, price_ex_showroom: 1200000 }
  });
  expect(vehicle.response.status).toBe(201);
  const order = await apiFetch("/api/v1/orders", adminToken, {
    method: "POST",
    body: { shipper_name: shipperName, shipper_phone: "9876543210", origin_city: "Tiruppur", origin_state: "Tamil Nadu", destination_city: "Chennai", destination_state: "Tamil Nadu", cargo_type: "general", weight_kg: 1200, num_packages: 12, vehicle_category_preference: category, estimated_distance_km: 460, offered_price: 18000 }
  });
  expect(order.response.status).toBe(201);
  await apiFetch(`/api/v1/orders/${order.data.id}/transition`, adminToken, {
    method: "POST",
    body: { to_state: "CONFIRMED", event: "order_submitted", payload: { payment_mode: "advance", topay_consent_status: "not_required", material_type: "general_goods", body_type_required: "open" }, actor_role: "OMS", idempotency_key: crypto.randomUUID(), trace_id: `transport-${crypto.randomUUID()}` }
  });
  const matches = await apiFetch(`/api/v1/orders/${order.data.id}/match?limit=1&min_score=0`, companyToken);
  expect(matches.response.status).toBe(200);
  return { vehicleId: vehicle.data.id, matchId: matches.data.matches[0].match_id };
}

async function startStaticServer() {
  staticServer = http.createServer(async (request, response) => {
    try {
      const requestPath = decodeURIComponent(new URL(request.url || "/", webBase).pathname);
      const filePath = path.join(appRoot, path.normalize(requestPath).replace(/^(\.\.[/\\])+/, "") === "/" ? "index.html" : path.normalize(requestPath).replace(/^(\.\.[/\\])+/, ""));
      if (!filePath.startsWith(appRoot)) return response.writeHead(403).end("Forbidden");
      const body = await readFile(filePath);
      response.writeHead(200, { "content-type": filePath.endsWith(".html") ? "text/html" : filePath.endsWith(".css") ? "text/css" : "text/javascript" });
      response.end(body);
    } catch {
      response.writeHead(404); response.end("Not found");
    }
  });
  await new Promise((resolve) => staticServer.listen(4176, "127.0.0.1", resolve));
}

test.beforeAll(async () => {
  if (existsSync(dbPath)) rmSync(dbPath, { force: true });
  runPython(["-m", "alembic", "upgrade", "head"]);
  server = spawn(pythonExe, ["-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8000"], { cwd: backendRoot, env: { ...process.env, DATABASE_URL: databaseUrl, APP_ENV: "development", CORS_ORIGINS: "*" }, stdio: "pipe" });
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

test("transport company sees only owned fleet, matches, and trips", async ({ page }) => {
  const issues = [];
  page.on("console", (m) => { if (m.type() === "error") issues.push(`console: ${m.text()}`); });
  page.on("pageerror", (e) => issues.push(`pageerror: ${e.message}`));
  page.on("requestfailed", (r) => issues.push(`network: ${r.url()}`));
  page.on("dialog", async (d) => { issues.push(`dialog: ${d.message()}`); await d.accept(); });

  const adminToken = await login("transport-e2e-admin", "super_admin");
  const companyOneToken = await login("transport-company-one", "transport_company");
  const companyTwoToken = await login("transport-company-two", "transport_company");
  const owned = await createCompanyMatch(adminToken, companyOneToken, "Tipper", "Owned Company Order");
  const other = await createCompanyMatch(adminToken, companyTwoToken, "Tractor", "Other Company Order");

  await page.goto(webUrl);
  await page.fill("#username", "transport-company-one");
  await page.getByRole("button", { name: "Login" }).click();
  await page.waitForLoadState("networkidle");
  await expect(page.locator("#loginStatus")).toContainText("transport-company-one");
  await expect(page.locator("#vehicleList")).toContainText(owned.vehicleId);
  await expect(page.locator("#vehicleList")).not.toContainText(other.vehicleId);
  await expect(page.locator("#matchList")).toContainText(owned.matchId);
  await expect(page.locator("#matchList")).not.toContainText(other.matchId);

  await page.getByRole("button", { name: new RegExp(owned.matchId) }).click();
  await page.getByRole("button", { name: "Accept Match" }).click();
  await page.waitForLoadState("networkidle");
  await expect(page.locator("#matchList")).toContainText("accepted");
  await expect(page.locator("#matchList")).toContainText("Trip");

  const blockedVehicle = await apiFetch(`/api/v1/vehicles/${other.vehicleId}`, companyOneToken);
  expect(blockedVehicle.response.status).toBe(404);
  const blockedAccept = await apiFetch(`/api/v1/matches/${other.matchId}/accept`, companyOneToken, { method: "POST", body: {} });
  expect(blockedAccept.response.status).toBe(404);
  const blockedAdmin = await apiFetch(`/api/v1/orders/${crypto.randomUUID()}/quote`, companyOneToken, { method: "POST", body: {} });
  expect(blockedAdmin.response.status).toBe(403);
  const blockedFinance = await apiFetch(`/api/v1/trips/${crypto.randomUUID()}/settlements/release`, companyOneToken, { method: "POST", body: { amount: 1, commission_amount: 0, gst_amount: 0, driver_payable_amount: 1, idempotency_key: crypto.randomUUID() } });
  expect(blockedFinance.response.status).toBe(403);

  expect(issues).toEqual([]);
});
