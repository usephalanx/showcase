import React from 'react';
import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';

import Layout from '../../src/components/Layout';

/**
 * Helper to render Layout within required providers.
 */
const renderLayout = (initialRoute: string = '/', children?: React.ReactNode) => {
  return render(
    <MemoryRouter initialEntries={[initialRoute]}>
      <Layout>{children ?? <div data-testid="child-content">Page Content</div>}</Layout>
    </MemoryRouter>,
  );
};

describe('Layout', () => {
  it('renders header with logo', () => {
    renderLayout();
    const logo = screen.getByText('Kanban Board');
    expect(logo).toBeTruthy();
    expect(logo.closest('a')!.getAttribute('href')).toBe('/');
  });

  it('renders navigation links', () => {
    renderLayout();
    expect(screen.getByRole('link', { name: 'Boards' })).toBeTruthy();
    expect(screen.getByRole('link', { name: 'Categories' })).toBeTruthy();
  });

  it('renders children in main area', () => {
    renderLayout();
    expect(screen.getByTestId('child-content')).toBeTruthy();
    expect(screen.getByText('Page Content')).toBeTruthy();
  });

  it('renders footer with copyright', () => {
    renderLayout();
    const currentYear = new Date().getFullYear().toString();
    expect(screen.getByText(new RegExp(currentYear))).toBeTruthy();
    expect(screen.getByText(/All rights reserved/i)).toBeTruthy();
  });

  it('has an accessible navigation landmark', () => {
    renderLayout();
    const nav = screen.getByRole('navigation', { name: 'Main navigation' });
    expect(nav).toBeTruthy();
  });

  it('marks the active nav link for home route', () => {
    renderLayout('/');
    const boardsLink = screen.getByRole('link', { name: 'Boards' });
    expect(boardsLink.getAttribute('aria-current')).toBe('page');

    const categoriesLink = screen.getByRole('link', { name: 'Categories' });
    expect(categoriesLink.getAttribute('aria-current')).toBeNull();
  });

  it('marks the active nav link for categories route', () => {
    renderLayout('/categories/design');
    const categoriesLink = screen.getByRole('link', { name: 'Categories' });
    expect(categoriesLink.getAttribute('aria-current')).toBe('page');

    const boardsLink = screen.getByRole('link', { name: 'Boards' });
    expect(boardsLink.getAttribute('aria-current')).toBeNull();
  });
});
