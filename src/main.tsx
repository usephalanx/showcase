import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';

/**
 * Application bootstrap.
 *
 * Mounts the root <App /> component into the #root DOM element
 * using React 18's createRoot API with StrictMode enabled.
 */
const rootElement = document.getElementById('root');

if (!rootElement) {
  throw new Error('Root element with id "root" not found in the DOM.');
}

ReactDOM.createRoot(rootElement).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);
