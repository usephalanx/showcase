import React from 'react';
import { describe, it, expect, beforeEach, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import { HelmetProvider } from 'react-helmet-async';

import HomePage from '../../src/pages/HomePage';

/**
 * Helper to render HomePage within required providers.
 */
const renderHomePage = () => {
  return render(
    <HelmetProvider>
      <MemoryRouter>
        <HomePage />
      </MemoryRouter>
    </HelmetProvider>,
  );
};

describe('HomePage', () => {
  it('shows loading state initially', () => {
    vi.stubGlobal(
      'fetch',
      vi.fn().mockReturnValue(new Promise(() => {})), // never resolves
    );
    renderHomePage();
    expect(screen.getByText('Loading boards…')).toBeTruthy();
  });

  it('renders a list of boards after fetching', async () => {
    const mockBoards = [
      {
        id: 1,
        title: 'Project Alpha',
        slug: 'project-alpha',
        description: 'Alpha board',
        meta_title: null,
        meta_description: null,
        created_at: '2024-01-01T00:00:00Z',
        updated_at: '2024-01-01T00:00:00Z',
      },
      {
        id: 2,
        title: 'Project Beta',
        slug: 'project-beta',
        description: null,
        meta_title: null,
        meta_description: null,
        created_at: '2024-01-02T00:00:00Z',
        updated_at: '2024-01-02T00:00:00Z',
      },
    ];

    vi.stubGlobal(
      'fetch',
      vi.fn().mockResolvedValue({
        ok: true,
        status: 200,
        json: async () => mockBoards,
      }),
    );

    renderHomePage();

    await waitFor(() => {
      expect(screen.getByText('Project Alpha')).toBeTruthy();
    });

    expect(screen.getByText('Project Beta')).toBeTruthy();
    expect(screen.getByText('Alpha board')).toBeTruthy();
  });

  it('renders board links with slug-based URLs', async () => {
    const mockBoards = [
      {
        id: 1,
        title: 'My Board',
        slug: 'my-board',
        description: null,
        meta_title: null,
        meta_description: null,
        created_at: '2024-01-01T00:00:00Z',
        updated_at: '2024-01-01T00:00:00Z',
      },
    ];

    vi.stubGlobal(
      'fetch',
      vi.fn().mockResolvedValue({
        ok: true,
        status: 200,
        json: async () => mockBoards,
      }),
    );

    renderHomePage();

    await waitFor(() => {
      expect(screen.getByText('My Board')).toBeTruthy();
    });

    const link = screen.getByRole('link', { name: /Open board: My Board/i });
    expect(link.getAttribute('href')).toBe('/boards/my-board');
  });

  it('shows empty state when no boards exist', async () => {
    vi.stubGlobal(
      'fetch',
      vi.fn().mockResolvedValue({
        ok: true,
        status: 200,
        json: async () => [],
      }),
    );

    renderHomePage();

    await waitFor(() => {
      expect(screen.getByText(/No boards yet/i)).toBeTruthy();
    });
  });

  it('shows error state when fetch fails', async () => {
    vi.stubGlobal(
      'fetch',
      vi.fn().mockResolvedValue({
        ok: false,
        status: 500,
        json: async () => ({}),
      }),
    );

    renderHomePage();

    await waitFor(() => {
      expect(screen.getByRole('alert')).toBeTruthy();
    });

    expect(screen.getByText(/Failed to load boards/i)).toBeTruthy();
  });
});
