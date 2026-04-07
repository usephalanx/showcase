/**
 * Root application shell.
 *
 * Renders the main TodoPage component. Acts as the top-level layout
 * wrapper for the application.
 */
import React from 'react';
import TodoPage from './pages/TodoPage';

const App: React.FC = () => {
  return (
    <div className="app">
      <TodoPage />
    </div>
  );
};

export default App;
