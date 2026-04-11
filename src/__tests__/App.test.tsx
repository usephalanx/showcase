import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import App from '../App';

/**
 * Test suite for the main App component.
 * Verifies all sections render in the correct order.
 */
describe('App', () => {
  beforeEach(() => {
    render(<App />);
  });

  it('renders the app container', () => {
    expect(screen.getByTestId('app-container')).toBeInTheDocument();
  });

  it('renders the Logo section', () => {
    expect(screen.getByTestId('logo-section')).toBeInTheDocument();
  });

  it('renders the logo image with accessible alt text', () => {
    expect(screen.getByAltText('Madhuri Real Estate Logo')).toBeInTheDocument();
  });

  it('renders the CompanyName section', () => {
    expect(screen.getByTestId('company-name-section')).toBeInTheDocument();
  });

  it('renders the company name heading', () => {
    expect(screen.getByRole('heading', { name: /madhuri real estate/i })).toBeInTheDocument();
  });

  it('renders the Profile section', () => {
    expect(screen.getByTestId('profile-section')).toBeInTheDocument();
  });

  it('renders the RecentSales section', () => {
    expect(screen.getByTestId('recent-sales-section')).toBeInTheDocument();
  });

  it('renders the ContactInfo section', () => {
    expect(screen.getByTestId('contact-section')).toBeInTheDocument();
  });

  it('renders all sections in the correct order', () => {
    const container = screen.getByTestId('app-container');
    const children = Array.from(container.children);

    expect(children).toHaveLength(5);
    expect(children[0]).toHaveAttribute('data-testid', 'logo-section');
    expect(children[1]).toHaveAttribute('data-testid', 'company-name-section');
    expect(children[2]).toHaveAttribute('data-testid', 'profile-section');
    expect(children[3]).toHaveAttribute('data-testid', 'recent-sales-section');
    expect(children[4]).toHaveAttribute('data-testid', 'contact-section');
  });
});
