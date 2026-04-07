import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

/// <reference types="vitest" />

/**
 * Vite configuration for the Todo frontend application.
 *
 * - Uses the React plugin for JSX transform and fast-refresh.
 * - Configures Vitest with jsdom for component testing.
 */
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    host: true,
  },
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: './src/setupTests.ts',
    css: true,
  },
});
