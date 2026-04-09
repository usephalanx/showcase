/// <reference types="vitest" />
/**
 * Vite configuration.
 *
 * Configures the React plugin and Vitest test runner settings.
 */
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: './src/setupTests.ts',
  },
});
