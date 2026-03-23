import React from 'react';
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { render, screen, waitFor, act } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

import { AuthProvider, AuthContext } from '../context/AuthContext';

// Mock the auth API module
vi.mock('../api/auth', () => ({
  loginUser: vi.fn(),
}));

import { loginUser } from '../api/auth';

/**
 * Test component that exposes AuthContext values for assertions.
 */
function TestConsumer() {
  const auth = React.useContext(AuthContext);

  return (
    <div>
      <span data-testid="authenticated">
        {auth.isAuthenticated ? 'yes' : 'no'}
      </span>
      <span data-testid="token">{auth.token || 'none'}</span>
      <span data-testid="error">{auth.error || 'none'}</span>
      <button
        onClick={() => auth.login('admin', 'admin123')}
        data-testid="login-btn"
      >
        Login
      </button>
      <button onClick={auth.logout} data-testid="logout-btn">
        Logout
      </button>
    </div>
  );
}

describe('AuthContext', () => {
  beforeEach(() => {
    localStorage.clear();
    vi.clearAllMocks();
  });

  afterEach(() => {
    localStorage.clear();
  });

  it('initialises as unauthenticated when no token in localStorage', async () => {
    render(
      <AuthProvider>
        <TestConsumer />
      </AuthProvider>,
    );

    await waitFor(() => {
      expect(screen.getByTestId('authenticated').textContent).toBe('no');
      expect(screen.getByTestId('token').textContent).toBe('none');
    });
  });

  it('initialises as authenticated when token exists in localStorage', async () => {
    localStorage.setItem('access_token', 'existing-token');

    render(
      <AuthProvider>
        <TestConsumer />
      </AuthProvider>,
    );

    await waitFor(() => {
      expect(screen.getByTestId('authenticated').textContent).toBe('yes');
      expect(screen.getByTestId('token').textContent).toBe('existing-token');
    });
  });

  it('sets token on successful login', async () => {
    loginUser.mockResolvedValue({ access_token: 'new-token', token_type: 'bearer' });

    render(
      <AuthProvider>
        <TestConsumer />
      </AuthProvider>,
    );

    const user = userEvent.setup();
    await user.click(screen.getByTestId('login-btn'));

    await waitFor(() => {
      expect(screen.getByTestId('authenticated').textContent).toBe('yes');
      expect(screen.getByTestId('token').textContent).toBe('new-token');
      expect(localStorage.getItem('access_token')).toBe('new-token');
    });
  });

  it('sets error on failed login', async () => {
    loginUser.mockRejectedValue({
      response: { data: { detail: 'Invalid credentials' } },
    });

    render(
      <AuthProvider>
        <TestConsumer />
      </AuthProvider>,
    );

    const user = userEvent.setup();
    await user.click(screen.getByTestId('login-btn'));

    await waitFor(() => {
      expect(screen.getByTestId('authenticated').textContent).toBe('no');
      expect(screen.getByTestId('error').textContent).toBe(
        'Invalid credentials',
      );
    });
  });

  it('clears token on logout', async () => {
    localStorage.setItem('access_token', 'existing-token');

    render(
      <AuthProvider>
        <TestConsumer />
      </AuthProvider>,
    );

    await waitFor(() => {
      expect(screen.getByTestId('authenticated').textContent).toBe('yes');
    });

    const user = userEvent.setup();
    await user.click(screen.getByTestId('logout-btn'));

    await waitFor(() => {
      expect(screen.getByTestId('authenticated').textContent).toBe('no');
      expect(screen.getByTestId('token').textContent).toBe('none');
      expect(localStorage.getItem('access_token')).toBeNull();
    });
  });
});
