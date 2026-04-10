import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

/**
 * Vite configuration for React application.
 *
 * Uses the official React plugin for Fast Refresh and JSX support.
 * Test configuration uses jsdom for DOM environment simulation.
 */
export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: './src/setupTests.js',
  },
});
