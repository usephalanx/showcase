import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom',
    globals: true,
    css: {
      modules: {
        classNameStrategy: 'non-scoped',
      },
    },
    setupFiles: ['./src/setupTests.js'],
  },
});
