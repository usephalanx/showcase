import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

/**
 * Vite configuration for the React + TypeScript application.
 *
 * Uses the official React plugin for Fast Refresh and JSX transform.
 * The dev server listens on 0.0.0.0:5173 so it is accessible from
 * within Docker containers.
 */
export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0',
    port: 5173,
  },
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: './src/setupTests.ts',
    css: true,
  },
});
