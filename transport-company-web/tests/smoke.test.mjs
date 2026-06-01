import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import { test } from "node:test";

const requiredPaths = [
  ["post", "/api/v1/auth/dev-login"],
  ["post", "/api/v1/vehicles"],
  ["get", "/api/v1/vehicles"],
  ["patch", "/api/v1/vehicles/{vehicle_id}"],
  ["get", "/api/v1/matches"],
  ["post", "/api/v1/matches/{match_id}/accept"],
  ["post", "/api/v1/matches/{match_id}/reject"],
  ["get", "/api/v1/transport-company/trips"],
  ["get", "/api/v1/transport-company/trips/{trip_id}"],
  ["post", "/api/v1/orders/{order_id}/quote"],
  ["post", "/api/v1/trips/{trip_id}/settlements/release"]
];

test("transport company page loads", async () => {
  const html = await readFile(new URL("../index.html", import.meta.url), "utf8");
  assert.match(html, /Zippy Transport Company/);
  assert.match(html, /vehicleList/);
  assert.match(html, /matchList/);
});

test("generated OpenAPI contract includes transport paths", async () => {
  const openapi = JSON.parse(await readFile(new URL("../src/api/openapi.json", import.meta.url), "utf8"));
  for (const [verb, path] of requiredPaths) {
    assert.ok(openapi.paths[path], `${path} is missing`);
    assert.ok(openapi.paths[path][verb], `${verb.toUpperCase()} ${path} missing`);
  }
});

test("generated client exposes transport methods", async () => {
  const client = await readFile(new URL("../src/api/generated-client.js", import.meta.url), "utf8");
  for (const method of ["devLogin","createVehicle","listVehicles","updateVehicle","listMatches","acceptMatch","rejectMatch","listTrips","getTrip","createQuote","releaseSettlement"]) {
    assert.match(client, new RegExp(`async ${method}\\(`));
  }
});
