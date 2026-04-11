import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

/**
 * Vite configuration for the Madhuri Real Estate SPA.
 */
export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
  },
});
