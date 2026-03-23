import React, { useState } from 'react';

/**
 * LoginForm component that renders username and password fields.
 * Calls the onSubmit callback with { username, password } on form submission.
 *
 * @param {{ onSubmit: function, error: string|null, isSubmitting: boolean }} props
 */
export default function LoginForm({ onSubmit, error, isSubmitting }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  /**
   * Handle form submission.
   * Prevents default browser behaviour and delegates to parent.
   *
   * @param {React.FormEvent} e
   */
  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit({ username, password });
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-5">
      {error && (
        <div
          className="rounded border border-red-200 bg-red-50 px-4 py-3 text-sm text-danger"
          role="alert"
        >
          {error}
        </div>
      )}

      <div>
        <label
          htmlFor="username"
          className="mb-1 block text-sm font-medium text-secondary"
        >
          Username
        </label>
        <input
          id="username"
          name="username"
          type="text"
          required
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          className="input-field"
          placeholder="Enter your username"
          autoComplete="username"
          disabled={isSubmitting}
        />
      </div>

      <div>
        <label
          htmlFor="password"
          className="mb-1 block text-sm font-medium text-secondary"
        >
          Password
        </label>
        <input
          id="password"
          name="password"
          type="password"
          required
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="input-field"
          placeholder="Enter your password"
          autoComplete="current-password"
          disabled={isSubmitting}
        />
      </div>

      <button
        type="submit"
        className="btn-primary w-full"
        disabled={isSubmitting}
      >
        {isSubmitting ? 'Signing in...' : 'Sign In'}
      </button>
    </form>
  );
}
