import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

/**
 * Vite configuration.
 *
 * Enables the React plugin for JSX transform and fast-refresh,
 * and configures the dev server port.
 */
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
  },
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: './tests/setup.ts',
  },
} as any)
