import React from "react";

/**
 * Root application shell.
 *
 * Renders the top-level layout and will eventually host
 * TaskList, TaskForm, and TaskFilter components.
 */
const App: React.FC = () => {
  return (
    <div className="app">
      <header className="app-header">
        <h1>Todo App</h1>
      </header>
      <main className="app-main">
        <p>Welcome! Your task list will appear here.</p>
      </main>
    </div>
  );
};

export default App;
