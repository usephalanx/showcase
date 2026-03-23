import React, { useState } from 'react';
import { useNavigate, Navigate } from 'react-router-dom';
import useAuth from '../hooks/useAuth';
import LoginForm from '../components/LoginForm';

/**
 * LoginPage component.
 * Displays a centered login form with username and password fields.
 * Redirects to /projects on successful authentication.
 * If already authenticated, redirects immediately.
 */
export default function LoginPage() {
  const { login, error, isAuthenticated } = useAuth();
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [formError, setFormError] = useState(null);
  const navigate = useNavigate();

  // If already logged in, redirect to projects
  if (isAuthenticated) {
    return <Navigate to="/projects" replace />;
  }

  /**
   * Handle login form submission.
   * Calls the auth context login and navigates on success.
   *
   * @param {{ username: string, password: string }} credentials
   */
  const handleSubmit = async ({ username, password }) => {
    if (!username.trim() || !password.trim()) {
      setFormError('Please enter both username and password.');
      return;
    }

    setIsSubmitting(true);
    setFormError(null);

    const success = await login(username, password);

    if (success) {
      navigate('/projects', { replace: true });
    }

    setIsSubmitting(false);
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-background px-4">
      <div className="w-full max-w-md">
        <div className="card">
          <div className="mb-6 text-center">
            <h1 className="text-2xl font-bold text-primary">TaskBoard</h1>
            <p className="mt-1 text-sm text-gray-500">
              Sign in to manage your projects
            </p>
          </div>
          <LoginForm
            onSubmit={handleSubmit}
            error={formError || error}
            isSubmitting={isSubmitting}
          />
        </div>
      </div>
    </div>
  );
}
