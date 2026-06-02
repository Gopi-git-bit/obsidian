import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import { test } from "node:test";

const requiredPaths = [
  ["post", "/api/v1/auth/dev-login"],
  ["get", "/api/v1/finance/settlements"],
  ["get", "/api/v1/finance/settlements/{trip_id}"],
  ["post", "/api/v1/trips/{trip_id}/settlements/release"]
];

test("finance console loads", async () => {
  const html = await readFile(new URL("../index.html", import.meta.url), "utf8");
  assert.match(html, /Zippy Finance/);
  assert.match(html, /settlementList/);
  assert.match(html, /releaseSettlement/);
  assert.match(html, /auditTrail/);
  assert.match(html, /outboxEvents/);
});

test("dev finance login controls exist", async () => {
  const html = await readFile(new URL("../index.html", import.meta.url), "utf8");
  assert.match(html, /finance_admin/);
  assert.match(html, /super_admin/);
  assert.match(html, /Login/);
});

test("generated OpenAPI contract includes finance paths", async () => {
  const openapi = JSON.parse(await readFile(new URL("../src/api/openapi.json", import.meta.url), "utf8"));
  for (const [verb, path] of requiredPaths) {
    assert.ok(openapi.paths[path], `${path} missing`);
    assert.ok(openapi.paths[path][verb], `${verb.toUpperCase()} ${path} missing`);
  }
});

test("generated client exposes finance methods", async () => {
  const client = await readFile(new URL("../src/api/generated-client.js", import.meta.url), "utf8");
  for (const method of ["devLogin", "listSettlements", "getSettlement", "releaseSettlement"]) {
    assert.match(client, new RegExp(`async ${method}\\(`));
  }
});

test("finance UI renders blocked and released labels", async () => {
  const app = await readFile(new URL("../src/app.js", import.meta.url), "utf8");
  assert.match(app, /FRAUD_HOLD_ACTIVE/);
  assert.match(app, /SETTLEMENT_HOLD_ACTIVE/);
  assert.match(app, /journal_created/);
  assert.match(app, /gst_invoice_created/);
  assert.match(app, /release_status/);
  assert.match(app, /outbox_events/);
});
