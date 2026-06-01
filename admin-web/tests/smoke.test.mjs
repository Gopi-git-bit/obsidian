import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import { test } from "node:test";

const requiredPaths = [
  ["post", "/api/v1/auth/dev-login"],
  ["get", "/api/v1/orders"],
  ["get", "/api/v1/orders/{order_id}"],
  ["get", "/api/v1/orders/{order_id}/events"],
  ["post", "/api/v1/orders/{order_id}/transition"],
  ["get", "/api/v1/orders/{order_id}/flow-summary"],
  ["post", "/api/v1/orders/{order_id}/quote"],
  ["get", "/api/v1/orders/{order_id}/match"],
  ["post", "/api/v1/matches/{match_id}/accept"],
  ["post", "/api/v1/orders/{order_id}/payments/advance"],
  ["post", "/api/v1/trips/{trip_id}/loading-photo"],
  ["post", "/api/v1/trips/{trip_id}/milestones"],
  ["post", "/api/v1/trips/{trip_id}/pod"],
  ["post", "/api/v1/trips/{trip_id}/pod/verify"],
  ["post", "/api/v1/trips/{trip_id}/otp/verify"],
  ["post", "/api/v1/trips/{trip_id}/settlements/release"]
];

test("admin page loads the dashboard module", async () => {
  const html = await readFile(new URL("../index.html", import.meta.url), "utf8");
  assert.match(html, /Zippy Admin/);
  assert.match(html, /src\/app\.js/);
  assert.match(html, /ordersList/);
  assert.match(html, /auditTrail/);
});

test("generated OpenAPI contract includes admin dependencies", async () => {
  const raw = await readFile(new URL("../src/api/openapi.json", import.meta.url), "utf8");
  const openapi = JSON.parse(raw);

  for (const [verb, path] of requiredPaths) {
    assert.ok(openapi.paths[path], `${path} is missing`);
    assert.ok(openapi.paths[path][verb], `${verb.toUpperCase()} ${path} is missing`);
  }
});

test("generated client exposes required admin methods", async () => {
  const client = await readFile(new URL("../src/api/generated-client.js", import.meta.url), "utf8");
  for (const method of [
    "listOrders",
    "devLogin",
    "getOrder",
    "getOrderEvents",
    "transitionOrder",
    "getOrderFlowSummary",
    "createQuote",
    "findMatches",
    "acceptMatch",
    "recordAdvancePayment",
    "uploadLoadingPhoto",
    "recordTripMilestone",
    "uploadPod",
    "verifyPod",
    "verifyOtp",
    "releaseSettlement"
  ]) {
    assert.match(client, new RegExp(`async ${method}\\(`));
  }
});
