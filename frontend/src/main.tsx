import React from 'react';
import ReactDOM from 'react-dom/client';

/**
 * Application root component.
 *
 * Renders the top-level UI for the Todo application.
 */
function App(): React.ReactElement {
  return (
    <div>
      <h1>Todo App</h1>
      <p>Welcome to the Todo application.</p>
    </div>
  );
}

const rootElement = document.getElementById('root');

if (!rootElement) {
  throw new Error('Failed to find the root element. Ensure index.html contains a <div id="root"></div>.');
}

ReactDOM.createRoot(rootElement).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);
