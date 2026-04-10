/**
 * Vite configuration file.
 *
 * Sets up the React plugin and Vitest test environment.
 */
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: './src/test-setup.js',
  },
  server: {
    host: '0.0.0.0',
    port: 5173,
  },
});
