import React, { createContext, useState, useCallback, useMemo, useEffect } from 'react';
import { loginUser } from '../api/auth';

/**
 * AuthContext provides authentication state and methods to the component tree.
 *
 * @typedef {Object} AuthContextValue
 * @property {string|null} token - The current JWT access token.
 * @property {boolean} isAuthenticated - Whether the user is authenticated.
 * @property {boolean} isLoading - Whether auth state is being initialised.
 * @property {function} login - Async function to log in with username/password.
 * @property {function} logout - Function to clear auth state and redirect.
 * @property {string|null} error - Last authentication error message.
 */
export const AuthContext = createContext(null);

/**
 * AuthProvider component that wraps children with authentication context.
 *
 * Manages JWT token state in both React state and localStorage.
 * Provides login and logout functions to descendants.
 *
 * @param {{ children: React.ReactNode }} props
 */
export function AuthProvider({ children }) {
  const [token, setToken] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  // On mount, check localStorage for existing token
  useEffect(() => {
    const storedToken = localStorage.getItem('access_token');
    if (storedToken) {
      setToken(storedToken);
    }
    setIsLoading(false);
  }, []);

  /**
   * Authenticate with username and password.
   * Stores the token in state and localStorage on success.
   *
   * @param {string} username
   * @param {string} password
   * @returns {Promise<boolean>} True on success, false on failure.
   */
  const login = useCallback(async (username, password) => {
    setError(null);
    try {
      const data = await loginUser(username, password);
      const accessToken = data.access_token;
      localStorage.setItem('access_token', accessToken);
      setToken(accessToken);
      return true;
    } catch (err) {
      const message =
        err.response?.data?.detail || 'Login failed. Please try again.';
      setError(message);
      return false;
    }
  }, []);

  /**
   * Log out the current user.
   * Clears token from state and localStorage.
   */
  const logout = useCallback(() => {
    localStorage.removeItem('access_token');
    setToken(null);
    setError(null);
  }, []);

  const value = useMemo(
    () => ({
      token,
      isAuthenticated: !!token,
      isLoading,
      error,
      login,
      logout,
    }),
    [token, isLoading, error, login, logout],
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}
