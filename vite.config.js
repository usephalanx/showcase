/**
 * Vite configuration for the React project.
 *
 * Enables the React plugin and configures Vitest for testing
 * with jsdom as the DOM environment.
 */
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom',
    globals: true,
  },
});
