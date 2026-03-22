import React, { useState } from 'react';
import { login, register } from '../api.js';

/**
 * Authentication component with login/register toggle.
 *
 * Renders a dark-themed form that allows users to either log in with
 * existing credentials or register a new account. On successful
 * authentication the JWT is stored in localStorage and the onAuth
 * callback is invoked to update the parent App state.
 *
 * @param {Object} props
 * @param {Function} props.onAuth - Callback invoked after successful authentication.
 */
function Auth({ onAuth }) {
  const [isLogin, setIsLogin] = useState(true);
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  /**
   * Validate form inputs before submission.
   *
   * @returns {string|null} An error message string, or null if valid.
   */
  const validate = () => {
    if (!username.trim()) {
      return 'Username is required.';
    }
    if (username.trim().length < 3) {
      return 'Username must be at least 3 characters.';
    }
    if (!isLogin && !email.trim()) {
      return 'Email is required.';
    }
    if (!isLogin && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.trim())) {
      return 'Please enter a valid email address.';
    }
    if (!password) {
      return 'Password is required.';
    }
    if (password.length < 6) {
      return 'Password must be at least 6 characters.';
    }
    return null;
  };

  /**
   * Handle form submission for login or registration.
   *
   * @param {React.FormEvent} e - The form submit event.
   */
  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    const validationError = validate();
    if (validationError) {
      setError(validationError);
      return;
    }

    setLoading(true);

    try {
      let data;
      if (isLogin) {
        data = await login(username.trim(), password);
      } else {
        data = await register(username.trim(), email.trim(), password);
      }

      if (data && data.token) {
        localStorage.setItem('token', data.token);
        onAuth();
      } else if (data && data.access_token) {
        localStorage.setItem('token', data.access_token);
        onAuth();
      } else {
        setError('Unexpected response from server.');
      }
    } catch (err) {
      if (err.response && err.response.data) {
        const detail = err.response.data.detail || err.response.data.message || err.response.data.error;
        setError(detail || 'Authentication failed. Please try again.');
      } else {
        setError('Network error. Please check your connection.');
      }
    } finally {
      setLoading(false);
    }
  };

  /**
   * Toggle between login and register modes, clearing errors.
   */
  const toggleMode = () => {
    setIsLogin((prev) => !prev);
    setError('');
    setEmail('');
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-900 px-4">
      <div className="w-full max-w-md bg-gray-800 rounded-lg shadow-xl p-8">
        <h2 className="text-2xl font-bold text-white text-center mb-6">
          {isLogin ? 'Sign In' : 'Create Account'}
        </h2>

        {error && (
          <div
            className="mb-4 p-3 bg-red-900/50 border border-red-700 rounded text-red-300 text-sm"
            role="alert"
            data-testid="auth-error"
          >
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} noValidate>
          <div className="mb-4">
            <label
              htmlFor="username"
              className="block text-sm font-medium text-gray-300 mb-1"
            >
              Username
            </label>
            <input
              id="username"
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="Enter your username"
              autoComplete="username"
              data-testid="input-username"
            />
          </div>

          {!isLogin && (
            <div className="mb-4">
              <label
                htmlFor="email"
                className="block text-sm font-medium text-gray-300 mb-1"
              >
                Email
              </label>
              <input
                id="email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="Enter your email"
                autoComplete="email"
                data-testid="input-email"
              />
            </div>
          )}

          <div className="mb-6">
            <label
              htmlFor="password"
              className="block text-sm font-medium text-gray-300 mb-1"
            >
              Password
            </label>
            <input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="Enter your password"
              autoComplete={isLogin ? 'current-password' : 'new-password'}
              data-testid="input-password"
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full py-2 px-4 bg-blue-600 hover:bg-blue-700 disabled:bg-blue-800 disabled:cursor-not-allowed text-white font-medium rounded transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 focus:ring-offset-gray-800"
            data-testid="btn-submit"
          >
            {loading ? 'Please wait...' : isLogin ? 'Sign In' : 'Create Account'}
          </button>
        </form>

        <div className="mt-6 text-center">
          <button
            type="button"
            onClick={toggleMode}
            className="text-sm text-blue-400 hover:text-blue-300 transition-colors"
            data-testid="btn-toggle"
          >
            {isLogin
              ? "Don't have an account? Register"
              : 'Already have an account? Sign In'}
          </button>
        </div>
      </div>
    </div>
  );
}

export default Auth;
