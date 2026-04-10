/**
 * Vite configuration for the React Counter App.
 *
 * Enables the React plugin and configures vitest for component testing
 * with jsdom as the test environment.
 */
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  test: {
    environment: "jsdom",
    globals: true,
    setupFiles: ["./src/setupTests.js"],
  },
});
