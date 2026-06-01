import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import { test } from "node:test";

const requiredPaths = [
  ["post", "/api/v1/auth/dev-login"],
  ["post", "/api/v1/orders"],
  ["get", "/api/v1/orders"],
  ["get", "/api/v1/orders/{order_id}"],
  ["get", "/api/v1/orders/{order_id}/customer-flow-summary"],
  ["post", "/api/v1/orders/{order_id}/quote"],
  ["post", "/api/v1/orders/{order_id}/payments/advance"]
];

test("customer page loads the dashboard module", async () => {
  const html = await readFile(new URL("../index.html", import.meta.url), "utf8");
  assert.match(html, /Zippy Customer/);
  assert.match(html, /src\/app\.js/);
  assert.match(html, /ordersList/);
  assert.match(html, /orderForm/);
});

test("generated OpenAPI contract includes customer dependencies", async () => {
  const raw = await readFile(new URL("../src/api/openapi.json", import.meta.url), "utf8");
  const openapi = JSON.parse(raw);

  for (const [verb, path] of requiredPaths) {
    assert.ok(openapi.paths[path], `${path} is missing`);
    assert.ok(openapi.paths[path][verb], `${verb.toUpperCase()} ${path} is missing`);
  }
});

test("generated client exposes required customer methods", async () => {
  const client = await readFile(new URL("../src/api/generated-client.js", import.meta.url), "utf8");
  for (const method of [
    "devLogin",
    "createOrder",
    "listOrders",
    "getOrder",
    "getCustomerFlowSummary",
    "createQuote",
    "recordAdvancePayment"
  ]) {
    assert.match(client, new RegExp(`async ${method}\\(`));
  }
});
