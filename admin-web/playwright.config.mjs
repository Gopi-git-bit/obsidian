import { defineConfig } from "@playwright/test";

export default defineConfig({
  testDir: "./tests",
  testMatch: /.*\.spec\.mjs/,
  timeout: 60000,
  use: {
    browserName: "chromium",
    headless: true,
    viewport: { width: 1440, height: 960 }
  }
});
