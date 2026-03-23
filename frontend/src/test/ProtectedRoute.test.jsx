import React from 'react';
import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import { MemoryRouter, Routes, Route } from 'react-router-dom';

import ProtectedRoute from '../components/ProtectedRoute';
import { AuthContext } from '../context/AuthContext';

/**
 * Helper to render a ProtectedRoute with configurable auth state.
 *
 * @param {Object} authOverrides - Partial overrides for AuthContext value.
 * @param {string} initialPath - Initial route path.
 */
function renderProtected(authOverrides = {}, initialPath = '/protected') {
  const defaultAuth = {
    token: null,
    isAuthenticated: false,
    isLoading: false,
    error: null,
    login: vi.fn(),
    logout: vi.fn(),
    ...authOverrides,
  };

  return render(
    <AuthContext.Provider value={defaultAuth}>
      <MemoryRouter initialEntries={[initialPath]}>
        <Routes>
          <Route path="/login" element={<div>Login Page</div>} />
          <Route
            path="/protected"
            element={
              <ProtectedRoute>
                <div>Protected Content</div>
              </ProtectedRoute>
            }
          />
        </Routes>
      </MemoryRouter>
    </AuthContext.Provider>,
  );
}

describe('ProtectedRoute', () => {
  it('renders children when authenticated', () => {
    renderProtected({ isAuthenticated: true, token: 'test-token' });

    expect(screen.getByText('Protected Content')).toBeInTheDocument();
  });

  it('redirects to /login when not authenticated', () => {
    renderProtected({ isAuthenticated: false });

    expect(screen.getByText('Login Page')).toBeInTheDocument();
    expect(screen.queryByText('Protected Content')).not.toBeInTheDocument();
  });

  it('shows loading state while auth is initialising', () => {
    renderProtected({ isLoading: true });

    expect(screen.getByText('Loading...')).toBeInTheDocument();
    expect(screen.queryByText('Protected Content')).not.toBeInTheDocument();
  });
});
