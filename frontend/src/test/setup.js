import { afterEach } from 'vitest'
import { cleanup } from '@testing-library/react'
import '@testing-library/jest-dom/vitest'

// RTL's automatic per-test cleanup relies on detecting a global `afterEach`
// (i.e. `test.globals: true`). We deliberately run without globals (see
// vitest.config.js), so without this, every render() in every test stacks
// into the same jsdom document and never unmounts.
afterEach(() => {
  cleanup()
})

// jsdom does not implement window.matchMedia. Without this stub, any component
// reaching useViewport() — i.e. anything that adapts its layout for mobile —
// throws `window.matchMedia is not a function` the moment a test renders it.
// Defaults to the desktop branch (matches: false) so existing characterization
// tests keep asserting against the layout they were written for. A test that
// wants the mobile branch can override window.matchMedia itself.
if (typeof window !== 'undefined' && typeof window.matchMedia !== 'function') {
  Object.defineProperty(window, 'matchMedia', {
    configurable: true,
    writable: true,
    value: (query) => ({
      matches: false,
      media: query,
      onchange: null,
      addEventListener: () => {},
      removeEventListener: () => {},
      // Deprecated MediaQueryList API — some libraries still call these.
      addListener: () => {},
      removeListener: () => {},
      dispatchEvent: () => false,
    }),
  })
}

// Node >=22's built-in `localStorage` global (unconfigured, no --localstorage-file)
// shadows jsdom's fully-functional window.localStorage with a non-functional
// stub (getItem/setItem/clear all missing). CI pins Node 22 without this
// issue, but newer local Node versions hit it. Swap in a real in-memory
// Storage impl whenever the ambient one isn't usable.
if (typeof localStorage === 'undefined' || typeof localStorage.setItem !== 'function') {
  class MemoryStorage {
    #store = new Map()
    get length() { return this.#store.size }
    key(i) { return Array.from(this.#store.keys())[i] ?? null }
    getItem(k) { return this.#store.has(k) ? this.#store.get(k) : null }
    setItem(k, v) { this.#store.set(String(k), String(v)) }
    removeItem(k) { this.#store.delete(k) }
    clear() { this.#store.clear() }
  }
  const memoryStorage = new MemoryStorage()
  Object.defineProperty(globalThis, 'localStorage', { value: memoryStorage, configurable: true, writable: true })
  if (typeof window !== 'undefined') {
    Object.defineProperty(window, 'localStorage', { value: memoryStorage, configurable: true, writable: true })
  }
}
