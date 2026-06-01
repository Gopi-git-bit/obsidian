import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import { test } from "node:test";

const requiredPaths = [
  ["post", "/api/v1/auth/dev-login"],
  ["get", "/api/v1/supervisor/cases"],
  ["get", "/api/v1/supervisor/cases/{case_id}"],
  ["post", "/api/v1/supervisor/cases/{case_id}/hold"],
  ["post", "/api/v1/supervisor/cases/{case_id}/approve"],
  ["post", "/api/v1/supervisor/cases/{case_id}/reject"],
  ["post", "/api/v1/supervisor/orders/{order_id}/fraud-hold"],
  ["post", "/api/v1/supervisor/settlements/{settlement_id}/hold"],
  ["post", "/api/v1/supervisor/settlements/{settlement_id}/release-hold"]
];

test("supervisor console page loads", async () => {
  const html = await readFile(new URL("../index.html", import.meta.url), "utf8");
  assert.match(html, /Zippy Supervisor/);
  assert.match(html, /caseList/);
  assert.match(html, /auditTrail/);
});

test("generated OpenAPI contract includes supervisor paths", async () => {
  const openapi = JSON.parse(await readFile(new URL("../src/api/openapi.json", import.meta.url), "utf8"));
  for (const [verb, path] of requiredPaths) {
    assert.ok(openapi.paths[path], `${path} missing`);
    assert.ok(openapi.paths[path][verb], `${verb.toUpperCase()} ${path} missing`);
  }
});

test("generated client exposes supervisor methods", async () => {
  const client = await readFile(new URL("../src/api/generated-client.js", import.meta.url), "utf8");
  for (const method of ["devLogin", "listCases", "getCase", "holdCase", "approveCase", "rejectCase", "placeFraudHold", "placeSettlementHold", "releaseSettlementHold"]) {
    assert.match(client, new RegExp(`async ${method}\\(`));
  }
});
