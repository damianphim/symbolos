import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// Separate from vite.config.js on purpose: that file has async Sentry-plugin
// loading and production build options (terser, manualChunks) that tests
// don't need and that having vitest evaluate could only add risk for.
// Vitest uses this file instead of (not merged with) vite.config.js once it
// exists, so the react() plugin is repeated here for JSX support in tests.
export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom',
    setupFiles: ['./src/test/setup.js'],
  },
})
