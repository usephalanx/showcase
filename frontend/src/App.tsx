import React from "react";

/**
 * Root application shell.
 *
 * Renders the top-level layout wrapper including a branded header
 * and a main content area that will eventually host the
 * TaskList, TaskForm, and TaskFilter components.
 */
const App: React.FC = () => {
  return (
    <div className="app">
      <header className="app-header">
        <h1>Todo App</h1>
        <p className="app-subtitle">Organize your tasks, get things done.</p>
      </header>

      <main className="app-main">
        <section className="card">
          <p>Welcome! Your task list will appear here.</p>
        </section>
      </main>

      <footer className="app-footer">
        <p>&copy; {new Date().getFullYear()} Todo App</p>
      </footer>
    </div>
  );
};

export default App;
