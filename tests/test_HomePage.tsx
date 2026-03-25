import { render, screen } from '@testing-library/react'
import { describe, it, expect } from 'vitest'
import HomePage from '../src/pages/HomePage'

/**
 * Tests for the HomePage component.
 */
describe('HomePage', () => {
  it('renders an h1 with "Hello World"', () => {
    render(<HomePage />)
    const heading = screen.getByRole('heading', { level: 1 })
    expect(heading).toHaveTextContent('Hello World')
  })

  it('renders inside a main element', () => {
    render(<HomePage />)
    const main = screen.getByRole('main')
    expect(main).toBeInTheDocument()
  })

  it('has the home-page class', () => {
    const { container } = render(<HomePage />)
    const mainEl = container.querySelector('.home-page')
    expect(mainEl).toBeInTheDocument()
  })
})
