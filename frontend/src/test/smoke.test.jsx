import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'

describe('Vitest + React Testing Library setup', () => {
  it('renders a component and finds it in the document', () => {
    render(<div data-testid="smoke">hello</div>)
    expect(screen.getByTestId('smoke')).toBeInTheDocument()
    expect(screen.getByText('hello')).toBeInTheDocument()
  })
})
