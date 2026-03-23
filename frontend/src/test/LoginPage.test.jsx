import React from 'react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { BrowserRouter } from 'react-router-dom';

import LoginPage from '../pages/LoginPage';
import { AuthContext } from '../context/AuthContext';

/**
 * Helper to render LoginPage wrapped in required providers.
 *
 * @param {Object} authOverrides - Partial overrides for AuthContext value.
 */
function renderLoginPage(authOverrides = {}) {
  const defaultAuth = {
    token: null,
    isAuthenticated: false,
    isLoading: false,
    error: null,
    login: vi.fn().mockResolvedValue(false),
    logout: vi.fn(),
    ...authOverrides,
  };

  return render(
    <AuthContext.Provider value={defaultAuth}>
      <BrowserRouter>
        <LoginPage />
      </BrowserRouter>
    </AuthContext.Provider>,
  );
}

describe('LoginPage', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('renders the login form with username and password fields', () => {
    renderLoginPage();

    expect(screen.getByLabelText(/username/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/password/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /sign in/i })).toBeInTheDocument();
  });

  it('renders the TaskBoard heading', () => {
    renderLoginPage();

    expect(screen.getByText('TaskBoard')).toBeInTheDocument();
  });

  it('calls login with username and password on form submit', async () => {
    const mockLogin = vi.fn().mockResolvedValue(true);
    renderLoginPage({ login: mockLogin });

    const user = userEvent.setup();
    await user.type(screen.getByLabelText(/username/i), 'admin');
    await user.type(screen.getByLabelText(/password/i), 'admin123');
    await user.click(screen.getByRole('button', { name: /sign in/i }));

    await waitFor(() => {
      expect(mockLogin).toHaveBeenCalledWith('admin', 'admin123');
    });
  });

  it('shows validation error when fields are empty', async () => {
    renderLoginPage();

    const user = userEvent.setup();
    // Type and clear to trigger empty submission
    await user.click(screen.getByRole('button', { name: /sign in/i }));

    // Browser native validation should prevent submission of empty required fields
    // So we test with spaces
    await user.type(screen.getByLabelText(/username/i), '   ');
    await user.type(screen.getByLabelText(/password/i), '   ');
    await user.click(screen.getByRole('button', { name: /sign in/i }));

    await waitFor(() => {
      expect(
        screen.getByText(/please enter both username and password/i),
      ).toBeInTheDocument();
    });
  });

  it('displays error from auth context', () => {
    renderLoginPage({ error: 'Invalid username or password' });

    expect(
      screen.getByText('Invalid username or password'),
    ).toBeInTheDocument();
  });

  it('disables the submit button while submitting', async () => {
    // Create a login that never resolves to simulate loading state
    const mockLogin = vi.fn(
      () => new Promise(() => {}),
    );
    renderLoginPage({ login: mockLogin });

    const user = userEvent.setup();
    await user.type(screen.getByLabelText(/username/i), 'admin');
    await user.type(screen.getByLabelText(/password/i), 'admin123');
    await user.click(screen.getByRole('button', { name: /sign in/i }));

    await waitFor(() => {
      expect(
        screen.getByRole('button', { name: /signing in/i }),
      ).toBeDisabled();
    });
  });
});
