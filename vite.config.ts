/// <reference types="vitest" />
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

/**
 * Vite configuration for the Hello World React application.
 *
 * Registers the React plugin for JSX transform and configures Vitest
 * to use a jsdom environment with global test APIs.
 */
export default defineConfig({
  plugins: [react()],
  test: {
    globals: true,
    environment: "jsdom",
    setupFiles: ["src/test/setup.ts"],
    css: true,
  },
});
