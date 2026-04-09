import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

/**
 * Vite configuration for the Hello World React application.
 *
 * Enables the React plugin for Fast Refresh and JSX transform support.
 */
export default defineConfig({
  plugins: [react()],
});
