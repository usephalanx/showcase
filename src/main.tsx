import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';

/**
 * Application entry point.
 *
 * Mounts the root <App /> component into the DOM element with id "root".
 */
const rootElement = document.getElementById('root');

if (!rootElement) {
  throw new Error('Root element not found. Ensure index.html contains a <div id="root"></div>.');
}

ReactDOM.createRoot(rootElement).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);
