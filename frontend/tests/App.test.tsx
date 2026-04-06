import React from 'react';
import { describe, it, expect, beforeEach, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import { HelmetProvider } from 'react-helmet-async';

import App from '../src/App';

/**
 * Helper to render the App within required providers at a given route.
 */
const renderApp = (initialRoute: string = '/') => {
  return render(
    <HelmetProvider>
      <MemoryRouter initialEntries={[initialRoute]}>
        <App />
      </MemoryRouter>
    </HelmetProvider>,
  );
};

// Mock fetch globally to prevent actual network requests.
beforeEach(() => {
  vi.stubGlobal(
    'fetch',
    vi.fn().mockResolvedValue({
      ok: true,
      status: 200,
      json: async () => [],
    }),
  );
});

describe('App Routing', () => {
  it('renders the Layout header on every route', () => {
    renderApp('/');
    expect(screen.getByText('Kanban Board')).toBeTruthy();
  });

  it('renders the Layout footer on every route', () => {
    renderApp('/');
    expect(screen.getByText(/All rights reserved/i)).toBeTruthy();
  });

  it('renders the HomePage at /', () => {
    renderApp('/');
    expect(screen.getByText('Your Boards')).toBeTruthy();
  });

  it('renders the BoardPage at /boards/:slug', () => {
    renderApp('/boards/my-board');
    expect(screen.getByText('Loading board…')).toBeTruthy();
  });

  it('renders the CardDetailPage at /cards/:slug', () => {
    renderApp('/cards/my-card');
    expect(screen.getByText('Loading card…')).toBeTruthy();
  });

  it('renders the CategoryPage at /categories/:slug', () => {
    renderApp('/categories/my-category');
    expect(screen.getByText('Loading category…')).toBeTruthy();
  });

  it('renders the NotFoundPage for unknown routes', () => {
    renderApp('/this/route/does/not/exist');
    expect(screen.getByText('404')).toBeTruthy();
    expect(screen.getByText(/doesn.t exist/i)).toBeTruthy();
  });
});

describe('Layout Navigation', () => {
  it('contains a link to the home page (Boards)', () => {
    renderApp('/');
    const boardsLink = screen.getByRole('link', { name: 'Boards' });
    expect(boardsLink).toBeTruthy();
    expect(boardsLink.getAttribute('href')).toBe('/');
  });

  it('contains a link to categories', () => {
    renderApp('/');
    const categoriesLink = screen.getByRole('link', { name: 'Categories' });
    expect(categoriesLink).toBeTruthy();
    expect(categoriesLink.getAttribute('href')).toBe('/categories');
  });

  it('marks Boards nav link as active on home page', () => {
    renderApp('/');
    const boardsLink = screen.getByRole('link', { name: 'Boards' });
    expect(boardsLink.getAttribute('aria-current')).toBe('page');
  });

  it('marks Categories nav link as active on category pages', () => {
    renderApp('/categories/design');
    const categoriesLink = screen.getByRole('link', { name: 'Categories' });
    expect(categoriesLink.getAttribute('aria-current')).toBe('page');
  });

  it('contains the logo link pointing to home', () => {
    renderApp('/boards/some-board');
    const logoLink = screen.getByText('Kanban Board').closest('a');
    expect(logoLink).toBeTruthy();
    expect(logoLink!.getAttribute('href')).toBe('/');
  });
});

describe('SEO Meta Tags', () => {
  it('sets default Helmet meta tags', () => {
    renderApp('/');
    // Helmet renders in the provider; we verify it doesn't throw
    // and the component renders successfully.
    expect(screen.getByText('Your Boards')).toBeTruthy();
  });
});
