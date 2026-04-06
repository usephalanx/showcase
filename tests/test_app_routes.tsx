/**
 * Tests for App component routing configuration.
 *
 * Run with: npx vitest run tests/test_app_routes.tsx
 */

import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import App from '../src/App';

// Mock the page components to isolate routing logic
vi.mock('../src/pages/HomePage', () => ({
  default: () => <div data-testid="home-page">Home Page</div>,
}));

vi.mock('../src/pages/PropertyDetailPage', () => ({
  default: () => <div data-testid="property-detail-page">Property Detail Page</div>,
}));

vi.mock('../src/pages/ContactPage', () => ({
  default: () => <div data-testid="contact-page">Contact Page</div>,
}));

describe('App Routing', () => {
  it('renders HomePage at /', () => {
    render(
      <MemoryRouter initialEntries={['/']}>
        <App />
      </MemoryRouter>
    );
    expect(screen.getByTestId('home-page')).toBeDefined();
  });

  it('renders PropertyDetailPage at /property/:id', () => {
    render(
      <MemoryRouter initialEntries={['/property/prop-1']}>
        <App />
      </MemoryRouter>
    );
    expect(screen.getByTestId('property-detail-page')).toBeDefined();
  });

  it('renders ContactPage at /contact', () => {
    render(
      <MemoryRouter initialEntries={['/contact']}>
        <App />
      </MemoryRouter>
    );
    expect(screen.getByTestId('contact-page')).toBeDefined();
  });

  it('renders NotFoundPage for unknown routes', () => {
    render(
      <MemoryRouter initialEntries={['/some/unknown/path']}>
        <App />
      </MemoryRouter>
    );
    expect(screen.getByText('Page Not Found')).toBeDefined();
    expect(screen.getByText('Back to Home')).toBeDefined();
    expect(screen.getByText('Contact Us')).toBeDefined();
  });

  it('renders 404 text for /random-page', () => {
    render(
      <MemoryRouter initialEntries={['/random-page']}>
        <App />
      </MemoryRouter>
    );
    expect(screen.getByText('404')).toBeDefined();
  });
});
