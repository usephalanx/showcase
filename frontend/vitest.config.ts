/// <reference types="vitest" />

/**
 * Vitest configuration for the frontend test suite.
 */
import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    globals: true,
    environment: "node",
    include: ["tests/**/*.test.ts"],
  },
});
