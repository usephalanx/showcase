import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

/**
 * Vite configuration.
 *
 * - Enables the React plugin for JSX transform.
 * - Configures Vitest with jsdom environment for component testing.
 */
export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom',
    globals: false,
    css: {
      modules: {
        classNameStrategy: 'non-scoped',
      },
    },
  },
});
