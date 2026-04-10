import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

/**
 * Vite configuration for the React SPA.
 *
 * - Enables the React plugin for JSX/fast-refresh support.
 * - Configures Vitest with jsdom for component testing.
 */
export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: './src/setupTests.js',
  },
});
