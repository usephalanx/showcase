import { render, screen } from '@testing-library/react'
import { describe, it, expect } from 'vitest'
import App from '../src/App'

/**
 * Tests for the root App component.
 */
describe('App', () => {
  it('renders without crashing', () => {
    render(<App />)
    const heading = screen.getByRole('heading', { level: 1 })
    expect(heading).toBeInTheDocument()
  })

  it('displays "Hello World" text', () => {
    render(<App />)
    expect(screen.getByText('Hello World')).toBeInTheDocument()
  })

  it('has the app class on the wrapper div', () => {
    const { container } = render(<App />)
    const appDiv = container.querySelector('.app')
    expect(appDiv).toBeInTheDocument()
  })
})
