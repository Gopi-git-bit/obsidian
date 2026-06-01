import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import { test } from "node:test";

const requiredPaths = [
  ["post", "/api/v1/auth/dev-login"],
  ["get", "/api/v1/driver/trips"],
  ["get", "/api/v1/driver/trips/{trip_id}"],
  ["post", "/api/v1/driver/trips/{trip_id}/acknowledge"],
  ["post", "/api/v1/trips/{trip_id}/milestones"],
  ["post", "/api/v1/trips/{trip_id}/loading-photo"],
  ["post", "/api/v1/trips/{trip_id}/pod"],
  ["post", "/api/v1/trips/{trip_id}/assign-driver"],
  ["post", "/api/v1/trips/{trip_id}/settlements/release"],
  ["post", "/api/v1/orders/{order_id}/transition"]
];

test("driver page loads the trip dashboard module", async () => {
  const html = await readFile(new URL("../index.html", import.meta.url), "utf8");
  assert.match(html, /Zippy Driver/);
  assert.match(html, /src\/app\.js/);
  assert.match(html, /tripsList/);
  assert.match(html, /recordSections/);
});

test("generated OpenAPI contract includes driver dependencies", async () => {
  const raw = await readFile(new URL("../src/api/openapi.json", import.meta.url), "utf8");
  const openapi = JSON.parse(raw);

  for (const [verb, path] of requiredPaths) {
    assert.ok(openapi.paths[path], `${path} is missing`);
    assert.ok(openapi.paths[path][verb], `${verb.toUpperCase()} ${path} is missing`);
  }
});

test("generated client exposes required driver methods", async () => {
  const client = await readFile(new URL("../src/api/generated-client.js", import.meta.url), "utf8");
  for (const method of [
    "devLogin",
    "listDriverTrips",
    "getDriverTrip",
    "acknowledgeTrip",
    "recordTripMilestone",
    "uploadLoadingPhoto",
    "uploadPod",
    "assignTripDriver",
    "releaseSettlement",
    "transitionOrder"
  ]) {
    assert.match(client, new RegExp(`async ${method}\\(`));
  }
});
