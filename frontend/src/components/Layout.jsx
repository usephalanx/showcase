import React from 'react';
import { Outlet, Link, useNavigate } from 'react-router-dom';
import useAuth from '../hooks/useAuth';

/**
 * Layout component providing a navigation bar and main content area.
 * Renders child routes via the <Outlet /> component.
 * Shows a logout button in the nav bar when authenticated.
 */
export default function Layout() {
  const { logout } = useAuth();
  const navigate = useNavigate();

  /**
   * Handle logout button click.
   * Clears auth state and redirects to login page.
   */
  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <div className="min-h-screen bg-background">
      <nav className="border-b border-gray-200 bg-white shadow-sm">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-3 sm:px-6 lg:px-8">
          <div className="flex items-center gap-6">
            <Link
              to="/projects"
              className="text-xl font-bold text-primary transition-colors hover:text-blue-700"
            >
              TaskBoard
            </Link>
            <Link
              to="/projects"
              className="text-sm font-medium text-secondary transition-colors hover:text-primary"
            >
              Projects
            </Link>
          </div>
          <button
            onClick={handleLogout}
            className="btn-danger text-sm"
            type="button"
          >
            Logout
          </button>
        </div>
      </nav>
      <main className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
        <Outlet />
      </main>
    </div>
  );
}
