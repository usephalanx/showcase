import React, { useState, useEffect } from 'react';
import Auth from './components/Auth.jsx';

/**
 * Root application component.
 *
 * Manages authentication state and conditionally renders the Auth
 * component or the main application content based on whether a JWT
 * token exists in localStorage.
 */
function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      setIsAuthenticated(true);
    }
  }, []);

  /**
   * Callback invoked after successful login or registration.
   * Updates application authentication state.
   */
  const handleAuth = () => {
    setIsAuthenticated(true);
  };

  /**
   * Logs the user out by clearing the token and resetting state.
   */
  const handleLogout = () => {
    localStorage.removeItem('token');
    setIsAuthenticated(false);
  };

  if (!isAuthenticated) {
    return <Auth onAuth={handleAuth} />;
  }

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      <header className="flex items-center justify-between px-6 py-4 bg-gray-800 border-b border-gray-700">
        <h1 className="text-xl font-bold">Kanban Board</h1>
        <button
          onClick={handleLogout}
          className="px-4 py-2 text-sm font-medium text-gray-300 bg-gray-700 rounded hover:bg-gray-600 transition-colors"
        >
          Logout
        </button>
      </header>
      <main className="p-6">
        <p className="text-gray-400">Welcome! Board view coming soon.</p>
      </main>
    </div>
  );
}

export default App;
