import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

/**
 * Vite configuration for the React Todo application.
 *
 * Uses @vitejs/plugin-react for Fast Refresh and JSX transform support.
 */
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    host: true,
  },
  build: {
    outDir: "dist",
  },
});
