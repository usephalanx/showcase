import React from 'react';
import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { MemoryRouter } from 'react-router-dom';

import Layout from '../components/Layout';
import { AuthContext } from '../context/AuthContext';

/**
 * Helper to render Layout with required providers.
 *
 * @param {Object} authOverrides - Partial overrides for AuthContext value.
 */
function renderLayout(authOverrides = {}) {
  const defaultAuth = {
    token: 'test-token',
    isAuthenticated: true,
    isLoading: false,
    error: null,
    login: vi.fn(),
    logout: vi.fn(),
    ...authOverrides,
  };

  return {
    ...render(
      <AuthContext.Provider value={defaultAuth}>
        <MemoryRouter>
          <Layout />
        </MemoryRouter>
      </AuthContext.Provider>,
    ),
    auth: defaultAuth,
  };
}

describe('Layout', () => {
  it('renders the TaskBoard brand link', () => {
    renderLayout();

    expect(screen.getByText('TaskBoard')).toBeInTheDocument();
  });

  it('renders the Projects navigation link', () => {
    renderLayout();

    expect(screen.getByText('Projects')).toBeInTheDocument();
  });

  it('renders the Logout button', () => {
    renderLayout();

    expect(
      screen.getByRole('button', { name: /logout/i }),
    ).toBeInTheDocument();
  });

  it('calls logout when logout button is clicked', async () => {
    const { auth } = renderLayout();
    const user = userEvent.setup();

    await user.click(screen.getByRole('button', { name: /logout/i }));

    expect(auth.logout).toHaveBeenCalledTimes(1);
  });
});
