import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

/**
 * Vite configuration for the Hello World React application.
 *
 * Uses the official React plugin and serves on port 3000 during
 * local development.
 */
export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
  },
})
