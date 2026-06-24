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
