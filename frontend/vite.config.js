import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// Sentry source-map upload. Only active when SENTRY_AUTH_TOKEN + SENTRY_ORG
// + SENTRY_PROJECT are set (i.e. in the Vercel build env). Locally / in CI /
// in preview without those, the plugin is omitted and the build behaves
// exactly as before.
const sentryEnabled =
  !!process.env.SENTRY_AUTH_TOKEN &&
  !!process.env.SENTRY_ORG &&
  !!process.env.SENTRY_PROJECT

export default defineConfig(async () => {
  const plugins = [react()]

  if (sentryEnabled) {
    const { sentryVitePlugin } = await import('@sentry/vite-plugin')
    plugins.push(
      sentryVitePlugin({
        org: process.env.SENTRY_ORG,
        project: process.env.SENTRY_PROJECT,
        authToken: process.env.SENTRY_AUTH_TOKEN,
        release: { name: process.env.VERCEL_GIT_COMMIT_SHA || undefined },
        sourcemaps: {
          // Upload the maps, then DELETE them from the build output so they
          // never ship to end users (they'd leak source otherwise).
          filesToDeleteAfterUpload: ['./dist/**/*.map'],
        },
        errorHandler: (err) => {
          console.warn('[sentry-vite-plugin] non-fatal:', err?.message || err)
        },
      })
    )
  }

  return {
    plugins,
    build: {
      // Emit source maps ONLY when Sentry is set to consume + delete them.
      // Otherwise stay at false (the prior behavior) so we never accidentally
      // ship maps to users.
      sourcemap: sentryEnabled ? true : false,
      minify: 'terser',
      terserOptions: {
        compress: {
          // Keep console.error/warn so the ErrorBoundary's local logging
          // still works; strip the noisy debug/log/info calls.
          pure_funcs: ['console.log', 'console.debug', 'console.info'],
          drop_debugger: true,
        },
      },
      rollupOptions: {
        output: {
          manualChunks: {
            'react-vendor': ['react', 'react-dom'],
            'markdown': ['react-markdown', 'remark-gfm'],
          },
        },
      },
    },
  }
})
