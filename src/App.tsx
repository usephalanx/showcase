/**
 * Root application shell.
 *
 * Renders the main TodoPage component. Acts as the top-level layout
 * wrapper for the application.
 */
import React from 'react';
import TodoPage from './pages/TodoPage';

/**
 * App is the root component that wraps the entire application.
 *
 * It provides a consistent outer container (`div.app`) and delegates
 * all todo-related rendering and state management to TodoPage.
 */
const App: React.FC = () => {
  return (
    <div className="app">
      <TodoPage />
    </div>
  );
};

export default App;
