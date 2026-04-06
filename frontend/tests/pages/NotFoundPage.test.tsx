import React from 'react';
import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import { HelmetProvider } from 'react-helmet-async';

import NotFoundPage from '../../src/pages/NotFoundPage';

/**
 * Helper to render NotFoundPage within required providers.
 */
const renderNotFoundPage = () => {
  return render(
    <HelmetProvider>
      <MemoryRouter>
        <NotFoundPage />
      </MemoryRouter>
    </HelmetProvider>,
  );
};

describe('NotFoundPage', () => {
  it('renders 404 heading', () => {
    renderNotFoundPage();
    expect(screen.getByText('404')).toBeTruthy();
  });

  it('renders descriptive message', () => {
    renderNotFoundPage();
    expect(screen.getByText(/doesn.t exist/i)).toBeTruthy();
  });

  it('renders a link back to home', () => {
    renderNotFoundPage();
    const link = screen.getByRole('link', { name: /Go back to home/i });
    expect(link.getAttribute('href')).toBe('/');
  });
});
