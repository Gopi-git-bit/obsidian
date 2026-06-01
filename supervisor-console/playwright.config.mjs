import { defineConfig, devices } from "@playwright/test";

export default defineConfig({
  testDir: "./tests",
  testMatch: /.*\.spec\.mjs/,
  timeout: 60000,
  fullyParallel: false,
  workers: 1,
  reporter: "list",
  use: { ...devices["Desktop Chrome"], trace: "retain-on-failure" }
});
