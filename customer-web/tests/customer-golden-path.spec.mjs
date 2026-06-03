import { expect, test } from "@playwright/test";
import { spawn, spawnSync } from "node:child_process";
import { existsSync, rmSync } from "node:fs";
import { readFile } from "node:fs/promises";
import http from "node:http";
import { fileURLToPath } from "node:url";
import path from "node:path";

const here = path.dirname(fileURLToPath(import.meta.url));
const customerRoot = path.resolve(here, "..");
const repoRoot = path.resolve(customerRoot, "..");
const backendRoot = path.join(repoRoot, "backend");
const pythonExe = path.join(backendRoot, ".venv", "Scripts", "python.exe");
const dbPath = path.join(customerRoot, ".playwright-customer.db");
const databaseUrl = "sqlite:///../customer-web/.playwright-customer.db";
const apiBase = "http://127.0.0.1:8000";
const customerBase = "http://127.0.0.1:4174";
const customerUrl = `${customerBase}/index.html`;

let server;
let staticServer;

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

async function devLogin(username) {
  const response = await fetch(`${apiBase}/api/v1/auth/dev-login`, {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({
      username,
      password: "customer-web-dev",
      role: "customer"
    })
  });
  if (!response.ok) {
    throw new Error(`Dev login failed: ${response.status} ${await response.text()}`);
  }
  return (await response.json()).access_token;
}

async function createOrder(token, shipperName) {
  const response = await fetch(`${apiBase}/api/v1/orders`, {
    method: "POST",
    headers: { "content-type": "application/json", authorization: `Bearer ${token}` },
    body: JSON.stringify({
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

async function expectStatus(pathname, token, expectedStatus, method = "GET", body) {
  const response = await fetch(`${apiBase}${pathname}`, {
    method,
    headers: { "content-type": "application/json", authorization: `Bearer ${token}` },
    body: body ? JSON.stringify(body) : undefined
  });
  expect(response.status).toBe(expectedStatus);
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
      const requestPath = decodeURIComponent(new URL(request.url || "/", customerBase).pathname);
      const safePath = path.normalize(requestPath).replace(/^(\.\.[/\\])+/, "");
      const filePath = path.join(customerRoot, safePath === "/" ? "index.html" : safePath);
      if (!filePath.startsWith(customerRoot)) {
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
  await new Promise((resolve) => staticServer.listen(4174, "127.0.0.1", resolve));
}

test.beforeAll(async () => {
  if (existsSync(dbPath)) rmSync(dbPath, { force: true });

  runPython(["-m", "alembic", "upgrade", "head"]);

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

test("customer web creates and reads only the logged-in customer's orders", async ({ page }) => {
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

  const customerOneToken = await devLogin("customer-one-browser");
  const customerTwoToken = await devLogin("customer-two-browser");
  const otherOrder = await createOrder(customerTwoToken, "Other Customer Order");

  await page.goto(customerUrl);
  await page.fill("#apiBase", apiBase);
  await page.fill("#username", "customer-one-browser");
  await page.getByRole("button", { name: "Login" }).click();
  await page.waitForLoadState("networkidle");

  await expect(page.locator("#loginStatus")).toContainText("customer-one-browser");
  await expect(page.locator("#ordersList")).not.toContainText("Other Customer Order");

  await page.getByRole("button", { name: "Create Order" }).click();
  await page.waitForLoadState("networkidle");
  await expect(page.locator("#ordersList")).toContainText("Customer Web Shipper");
  await expect(page.locator("#ordersList")).not.toContainText("Other Customer Order");

  await page.getByRole("button", { name: /Customer Web Shipper/ }).click();
  await page.waitForLoadState("networkidle");
  await expect(page.locator("#lifecycleBadge")).toHaveText("CREATED");
  await expect(page.locator("#flowSections")).toContainText("Quote");
  await expect(page.locator("#flowSections")).toContainText("Match / Trip");
  await expect(page.locator("#flowSections")).toContainText("Milestone");
  await expect(page.locator("#flowSections")).toContainText("POD");
  await expect(page.locator("#flowSections")).toContainText("OTP");
  await expect(page.locator("#flowSections")).toContainText("Settlement / Invoice");

  await expectStatus(`/api/v1/orders/${otherOrder.id}`, customerOneToken, 404);
  await expectStatus(`/api/v1/orders/${otherOrder.id}/customer-flow-summary`, customerOneToken, 404);
  await expectStatus(`/api/v1/orders/${otherOrder.id}/quote`, customerOneToken, 403, "POST");
  await expectStatus(
    `/api/v1/orders/${otherOrder.id}/payments/advance`,
    customerOneToken,
    403,
    "POST",
    {
      amount: 9000,
      currency: "INR",
      provider_ref: "customer-forbidden",
      idempotency_key: "customer-forbidden-advance"
    }
  );

  expect(browserIssues).toEqual([]);
});
