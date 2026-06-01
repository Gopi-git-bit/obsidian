import { expect, test } from "@playwright/test";
import { spawn, spawnSync } from "node:child_process";
import { existsSync, rmSync } from "node:fs";
import { readFile } from "node:fs/promises";
import http from "node:http";
import { fileURLToPath } from "node:url";
import path from "node:path";

const here = path.dirname(fileURLToPath(import.meta.url));
const driverRoot = path.resolve(here, "..");
const repoRoot = path.resolve(driverRoot, "..");
const backendRoot = path.join(repoRoot, "backend");
const pythonExe = path.join(backendRoot, ".venv", "Scripts", "python.exe");
const dbPath = path.join(driverRoot, ".playwright-driver.db");
const databaseUrl = "sqlite:///../driver-web/.playwright-driver.db";
const apiBase = "http://127.0.0.1:8000";
const driverBase = "http://127.0.0.1:4175";
const driverUrl = `${driverBase}/index.html`;

let server;
let staticServer;

function runPython(args) {
  const result = spawnSync(pythonExe, args, {
    cwd: backendRoot,
    env: { ...process.env, DATABASE_URL: databaseUrl },
    encoding: "utf8"
  });
  if (result.status !== 0) {
    throw new Error(`Python command failed\nSTDOUT:\n${result.stdout}\nSTDERR:\n${result.stderr}`);
  }
  return result.stdout;
}

function tokenSubject(token) {
  return JSON.parse(Buffer.from(token.split(".")[1], "base64url").toString("utf8")).sub;
}

async function waitForBackend() {
  const deadline = Date.now() + 30000;
  let lastError;
  while (Date.now() < deadline) {
    try {
      const response = await fetch(`${apiBase}/api/v1/health/live`);
      if (response.ok) return;
    } catch (error) {
      lastError = error;
    }
    await new Promise((resolve) => setTimeout(resolve, 400));
  }
  throw new Error(`Backend did not become ready: ${lastError?.message || "timeout"}`);
}

async function devLogin(username, role) {
  const response = await fetch(`${apiBase}/api/v1/auth/dev-login`, {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({ username, password: "driver-web-dev", role })
  });
  if (!response.ok) {
    throw new Error(`Dev login failed: ${response.status} ${await response.text()}`);
  }
  return (await response.json()).access_token;
}

async function apiFetch(pathname, token, options = {}) {
  const response = await fetch(`${apiBase}${pathname}`, {
    method: options.method || "GET",
    headers: { "content-type": "application/json", authorization: `Bearer ${token}` },
    body: options.body ? JSON.stringify(options.body) : undefined
  });
  const text = await response.text();
  const data = text ? JSON.parse(text) : null;
  if (options.expectStatus && response.status !== options.expectStatus) {
    throw new Error(`Expected ${options.expectStatus}, got ${response.status} for ${pathname}: ${text}`);
  }
  return { response, data };
}

async function createAssignedTrip(adminToken, driverId, shipperName, vehicleCategory) {
  await apiFetch("/api/v1/orders", adminToken, {
    method: "POST",
    expectStatus: 201,
    body: {
      shipper_name: shipperName,
      shipper_phone: "9876543210",
      shipper_email: `${shipperName.toLowerCase().replaceAll(" ", "-")}@example.com`,
      origin_city: "Tiruppur",
      origin_state: "Tamil Nadu",
      destination_city: "Chennai",
      destination_state: "Tamil Nadu",
      cargo_type: "general",
      weight_kg: 1200,
      num_packages: 12,
      vehicle_category_preference: vehicleCategory,
      is_interstate: false,
      estimated_distance_km: 460,
      offered_price: 18000
    }
  });
  const orders = await apiFetch("/api/v1/orders?limit=1", adminToken, { expectStatus: 200 });
  const order = orders.data.orders[0];
  await apiFetch(`/api/v1/orders/${order.id}/quote`, adminToken, { method: "POST", expectStatus: 201, body: {} });
  await apiFetch(`/api/v1/orders/${order.id}/transition`, adminToken, {
    method: "POST",
    expectStatus: 200,
    body: {
      to_state: "CONFIRMED",
      event: "order_submitted",
      payload: {
        payment_mode: "advance",
        topay_consent_status: "not_required",
        material_type: "general_goods",
        body_type_required: "open"
      },
      actor_role: "OMS",
      idempotency_key: crypto.randomUUID(),
      trace_id: `driver-e2e-${crypto.randomUUID()}`
    }
  });
  const matches = await apiFetch(`/api/v1/orders/${order.id}/match?limit=1&min_score=0`, adminToken, { expectStatus: 200 });
  const matchId = matches.data.matches[0].match_id;
  await apiFetch(`/api/v1/matches/${matchId}/accept`, adminToken, { method: "POST", expectStatus: 200, body: {} });
  const trip = await apiFetch(`/api/v1/orders/${order.id}/trip`, adminToken, { expectStatus: 200 });
  const tripId = trip.data.trip_id;
  await apiFetch(`/api/v1/trips/${tripId}/assign-driver`, adminToken, {
    method: "POST",
    expectStatus: 200,
    body: { driver_id: driverId }
  });
  for (const [toState, event, payload] of [
    ["EN_ROUTE_TO_PICKUP", "driver_started_pickup", {}],
    ["AT_PICKUP_WAITING", "driver_arrived_pickup", {}],
    ["LOADING", "shipment_doc_scanned", {
      driver_id: driverId,
      vehicle_id: trip.data.vehicle_id,
      doc_type: "loading_photo",
      doc_url: "s3://docs/setup-loading.jpg",
      scan_exif: {}
    }],
    ["DEPARTED_FOR_DELIVERY", "loading_completed", {}],
    ["AT_DELIVERY_WAITING", "driver_arrived_delivery", {}]
  ]) {
    await apiFetch(`/api/v1/orders/${order.id}/transition`, adminToken, {
      method: "POST",
      expectStatus: 200,
      body: {
        to_state: toState,
        event,
        payload,
        actor_role: "DRIVER",
        idempotency_key: crypto.randomUUID(),
        trace_id: `driver-e2e-${crypto.randomUUID()}`
      }
    });
  }
  return { order, tripId };
}

function contentType(filePath) {
  if (filePath.endsWith(".html")) return "text/html";
  if (filePath.endsWith(".css")) return "text/css";
  if (filePath.endsWith(".js")) return "text/javascript";
  if (filePath.endsWith(".json")) return "application/json";
  return "application/octet-stream";
}

async function startStaticServer() {
  staticServer = http.createServer(async (request, response) => {
    try {
      const requestPath = decodeURIComponent(new URL(request.url || "/", driverBase).pathname);
      const safePath = path.normalize(requestPath).replace(/^(\.\.[/\\])+/, "");
      const filePath = path.join(driverRoot, safePath === "/" ? "index.html" : safePath);
      if (!filePath.startsWith(driverRoot)) {
        response.writeHead(403);
        response.end("Forbidden");
        return;
      }
      const body = await readFile(filePath);
      response.writeHead(200, { "content-type": contentType(filePath) });
      response.end(body);
    } catch {
      response.writeHead(404);
      response.end("Not found");
    }
  });
  await new Promise((resolve) => staticServer.listen(4175, "127.0.0.1", resolve));
}

test.beforeAll(async () => {
  if (existsSync(dbPath)) rmSync(dbPath, { force: true });
  runPython(["-m", "alembic", "upgrade", "head"]);
  runPython([
    "-c",
    [
      "from app.database import SessionLocal",
      "from app.models.vehicle_model import VehicleModel",
      "db=SessionLocal()",
      "vehicle_one=VehicleModel(manufacturer='Driver Test Motors', model_name='Tractor Driver One', category='Tractor', body_type='open', gvw_kg=3500, payload_kg=2000, mileage_kmpl=12, price_ex_showroom=1200000, is_active=True)",
      "vehicle_two=VehicleModel(manufacturer='Driver Test Motors', model_name='Tipper Driver Two', category='Tipper', body_type='tipper', gvw_kg=3500, payload_kg=2000, mileage_kmpl=12, price_ex_showroom=1200000, is_active=True)",
      "db.add_all([vehicle_one, vehicle_two])",
      "db.commit()",
      "db.close()"
    ].join(";")
  ]);

  server = spawn(
    pythonExe,
    ["-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8000"],
    {
      cwd: backendRoot,
      env: { ...process.env, DATABASE_URL: databaseUrl },
      stdio: "pipe"
    }
  );
  await waitForBackend();
  await startStaticServer();
});

test.afterAll(async () => {
  if (staticServer) {
    await new Promise((resolve) => staticServer.close(resolve));
  }
  if (server) {
    await new Promise((resolve) => {
      server.once("exit", resolve);
      if (process.platform === "win32") {
        spawnSync("taskkill", ["/pid", String(server.pid), "/T", "/F"], { stdio: "ignore" });
      } else {
        server.kill();
      }
      setTimeout(resolve, 3000);
    });
  }
  for (let attempt = 0; attempt < 5; attempt += 1) {
    try {
      if (existsSync(dbPath)) rmSync(dbPath, { force: true });
      break;
    } catch {
      await new Promise((resolve) => setTimeout(resolve, 500));
    }
  }
});

test("driver web handles assigned trip actions and blocks cross-driver access", async ({ page }) => {
  const browserIssues = [];
  page.on("console", (message) => {
    if (message.type() === "error") browserIssues.push(`console: ${message.text()}`);
  });
  page.on("pageerror", (error) => browserIssues.push(`pageerror: ${error.message}`));
  page.on("requestfailed", (request) => {
    browserIssues.push(`network: ${request.method()} ${request.url()} ${request.failure()?.errorText}`);
  });
  page.on("response", (response) => {
    if (response.url().startsWith(apiBase) && response.status() >= 400) {
      browserIssues.push(`http ${response.status()}: ${response.url()}`);
    }
  });
  page.on("dialog", async (dialog) => {
    browserIssues.push(`dialog: ${dialog.message()}`);
    await dialog.accept();
  });

  const adminToken = await devLogin("driver-e2e-admin", "super_admin");
  const driverOneToken = await devLogin("driver-one-browser", "driver");
  const driverTwoToken = await devLogin("driver-two-browser", "driver");
  const driverTrip = await createAssignedTrip(adminToken, tokenSubject(driverOneToken), "Driver One Order", "Tractor");
  const otherTrip = await createAssignedTrip(adminToken, tokenSubject(driverTwoToken), "Driver Two Order", "Tipper");

  await page.goto(driverUrl);
  await page.fill("#username", "driver-one-browser");
  await page.getByRole("button", { name: "Login" }).click();
  await page.waitForLoadState("networkidle");

  await expect(page.locator("#loginStatus")).toContainText("driver-one-browser");
  await expect(page.locator("#tripsList")).toContainText(driverTrip.tripId);
  await expect(page.locator("#tripsList")).not.toContainText(otherTrip.tripId);

  await page.getByRole("button", { name: new RegExp(driverTrip.tripId) }).click();
  await page.waitForLoadState("networkidle");
  await expect(page.locator("#recordSections")).toContainText("Order Route / Status");
  await expect(page.locator("#recordSections")).toContainText("Assigned Vehicle / Match");

  await page.getByRole("button", { name: "Add Milestone" }).click();
  await page.waitForLoadState("networkidle");
  await expect(page.locator("#recordSections")).toContainText("in_transit");

  await page.getByRole("button", { name: "Upload Loading Proof" }).click();
  await page.waitForLoadState("networkidle");
  await expect(page.locator("#recordSections")).toContainText("driver-loading");

  await page.getByRole("button", { name: "Upload POD" }).click();
  await page.waitForLoadState("networkidle");
  await expect(page.locator("#recordSections")).toContainText("POD Status");
  await expect(page.locator("#recordSections")).toContainText("uploaded");

  const otherRead = await apiFetch(`/api/v1/driver/trips/${otherTrip.tripId}`, driverOneToken);
  expect(otherRead.response.status).toBe(404);
  const otherUpdate = await apiFetch(`/api/v1/trips/${otherTrip.tripId}/milestones`, driverOneToken, {
    method: "POST",
    body: {
      milestone_type: "forbidden",
      status: "recorded",
      payload: {},
      idempotency_key: `forbidden-${crypto.randomUUID()}`
    }
  });
  expect(otherUpdate.response.status).toBe(404);
  const adminAction = await apiFetch(`/api/v1/trips/${driverTrip.tripId}/assign-driver`, driverOneToken, {
    method: "POST",
    body: { driver_id: tokenSubject(driverOneToken) }
  });
  expect(adminAction.response.status).toBe(403);
  const financeAction = await apiFetch(`/api/v1/trips/${driverTrip.tripId}/settlements/release`, driverOneToken, {
    method: "POST",
    body: {
      amount: 18000,
      commission_amount: 1800,
      gst_amount: 324,
      driver_payable_amount: 16200,
      currency: "INR",
      idempotency_key: `driver-forbidden-${crypto.randomUUID()}`
    }
  });
  expect(financeAction.response.status).toBe(403);

  expect(browserIssues).toEqual([]);
});
