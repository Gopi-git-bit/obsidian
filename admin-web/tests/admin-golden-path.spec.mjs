import { expect, test } from "@playwright/test";
import { spawn, spawnSync } from "node:child_process";
import { existsSync, rmSync } from "node:fs";
import { readFile } from "node:fs/promises";
import http from "node:http";
import { fileURLToPath } from "node:url";
import path from "node:path";

const here = path.dirname(fileURLToPath(import.meta.url));
const adminRoot = path.resolve(here, "..");
const repoRoot = path.resolve(adminRoot, "..");
const backendRoot = path.join(repoRoot, "backend");
const pythonExe = path.join(backendRoot, ".venv", "Scripts", "python.exe");
const dbPath = path.join(adminRoot, ".playwright-admin.db");
const databaseUrl = "sqlite:///../admin-web/.playwright-admin.db";
const apiBase = "http://127.0.0.1:8000";
const adminBase = "http://127.0.0.1:4173";
const adminUrl = `${adminBase}/index.html`;

let server;
let staticServer;
let apiToken;

function runPython(args) {
  const result = spawnSync(pythonExe, args, {
    cwd: backendRoot,
    env: { ...process.env, DATABASE_URL: databaseUrl, APP_ENV: "development", CORS_ORIGINS: "*" },
    encoding: "utf8"
  });
  if (result.status !== 0) {
    throw new Error(`Python command failed\nSTDOUT:\n${result.stdout}\nSTDERR:\n${result.stderr}`);
  }
  return result.stdout;
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

async function createOrder() {
  const response = await fetch(`${apiBase}/api/v1/orders`, {
    method: "POST",
    headers: { "content-type": "application/json", authorization: `Bearer ${apiToken}` },
    body: JSON.stringify({
      shipper_name: "Browser Flow Customer",
      shipper_phone: "9876543210",
      shipper_email: "browser-flow@example.com",
      origin_city: "Tiruppur",
      origin_state: "Tamil Nadu",
      destination_city: "Chennai",
      destination_state: "Tamil Nadu",
      cargo_type: "general",
      weight_kg: 1200,
      num_packages: 12,
      vehicle_category_preference: "LCV",
      is_interstate: false,
      estimated_distance_km: 460,
      offered_price: 18000
    })
  });
  if (!response.ok) {
    throw new Error(`Order creation failed: ${response.status} ${await response.text()}`);
  }
  return response.json();
}

async function devLogin(role = "super_admin") {
  const response = await fetch(`${apiBase}/api/v1/auth/dev-login`, {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({
      username: `playwright-${role}`,
      password: "playwright-dev",
      role
    })
  });
  if (!response.ok) {
    throw new Error(`Dev login failed: ${response.status} ${await response.text()}`);
  }
  return (await response.json()).access_token;
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
      const requestPath = decodeURIComponent(new URL(request.url || "/", adminBase).pathname);
      const safePath = path.normalize(requestPath).replace(/^(\.\.[/\\])+/, "");
      const filePath = path.join(adminRoot, safePath === "/" ? "index.html" : safePath);
      if (!filePath.startsWith(adminRoot)) {
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
  await new Promise((resolve) => staticServer.listen(4173, "127.0.0.1", resolve));
}

async function clickAction(page, name) {
  const button = page.getByRole("button", { name });
  await expect(button).toBeVisible();
  await expect(button).toBeEnabled();
  await button.click();
  await page.waitForLoadState("networkidle");
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
      "vehicle=VehicleModel(manufacturer='Browser Test Motors', model_name='LCV Browser', category='LCV', body_type='open', gvw_kg=3500, payload_kg=2000, mileage_kmpl=12, price_ex_showroom=1200000, is_active=True)",
      "db.add(vehicle)",
      "db.commit()",
      "db.close()"
    ].join(";")
  ]);

  server = spawn(
    pythonExe,
    ["-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8000"],
    {
      cwd: backendRoot,
      env: { ...process.env, DATABASE_URL: databaseUrl, APP_ENV: "development", CORS_ORIGINS: "*" },
      stdio: "pipe"
    }
  );
  await waitForBackend();
  apiToken = await devLogin("super_admin");
  await createOrder();
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

test("admin web drives the real order-to-settlement golden path", async ({ page }) => {
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
    if (dialog.type() === "alert") {
      browserIssues.push(`alert: ${dialog.message()}`);
    }
    await dialog.accept(dialog.defaultValue() || "admin");
  });

  await page.goto(adminUrl);
  await page.waitForLoadState("networkidle");

  await expect(page.locator("#ordersList")).toContainText("Browser Flow Customer");
  await page.getByRole("button", { name: /Browser Flow Customer/ }).click();
  await page.waitForLoadState("networkidle");

  await expect(page.locator("#lifecycleBadge")).toHaveText("CREATED");
  await expect(page.locator("#flowSteps")).toContainText("quote");
  await expect(page.locator("#missingSteps")).toContainText("Missing or failed steps");
  await expect(page.locator("#recordSections")).toContainText("Quote");
  await expect(page.locator("#auditTrail")).toContainText("No audit events recorded");

  await clickAction(page, "Generate Quote");
  await clickAction(page, "Confirm Order");
  await expect(page.locator("#lifecycleBadge")).toHaveText("CONFIRMED");
  await clickAction(page, "Find Matches");
  await expect(page.locator("#lifecycleBadge")).toHaveText("RINGING");
  await clickAction(page, "Accept Match");
  await expect(page.locator("#lifecycleBadge")).toHaveText("ASSIGNED");
  await clickAction(page, "Record Advance");
  await clickAction(page, "Start Pickup");
  await expect(page.locator("#lifecycleBadge")).toHaveText("EN_ROUTE_TO_PICKUP");
  await clickAction(page, "Arrived Pickup");
  await expect(page.locator("#lifecycleBadge")).toHaveText("AT_PICKUP_WAITING");
  await clickAction(page, "Start Loading");
  await expect(page.locator("#lifecycleBadge")).toHaveText("LOADING");
  await clickAction(page, "Upload Loading Photo");
  await clickAction(page, "Depart Delivery");
  await expect(page.locator("#lifecycleBadge")).toHaveText("DEPARTED_FOR_DELIVERY");
  await clickAction(page, "Add Milestone");
  await clickAction(page, "Arrive Delivery");
  await expect(page.locator("#lifecycleBadge")).toHaveText("AT_DELIVERY_WAITING");
  await clickAction(page, "Upload POD");
  await expect(page.locator("#lifecycleBadge")).toHaveText("DELIVERED_PENDING_SETTLEMENT");
  await clickAction(page, "Verify POD");
  await clickAction(page, "Verify OTP");
  await clickAction(page, "Release Settlement");
  await expect(page.locator("#lifecycleBadge")).toHaveText("COMPLETED");

  await expect(page.locator("#missingSteps")).toHaveText("No missing flow steps detected.");
  for (const label of [
    "Quote",
    "Match",
    "Trip",
    "Payment",
    "Loading Photo",
    "Milestone",
    "POD",
    "OTP",
    "Settlement",
    "Journal Entry",
    "GST Invoice"
  ]) {
    await expect(page.locator("#recordSections")).toContainText(label);
  }
  for (const field of [
    "quote_id",
    "match_score",
    "trip_id",
    "payment_id",
    "loading_photo",
    "in_transit",
    "document_url",
    "otp_verified",
    "settlement_id",
    "journal_entry_id",
    "invoice_number"
  ]) {
    await expect(page.locator("#recordSections")).toContainText(field);
  }
  await expect(page.locator("#auditTrail")).toContainText("order_submitted");
  await expect(page.locator("#auditTrail")).toContainText("payment_captured");

  expect(browserIssues).toEqual([]);
});
