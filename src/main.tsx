/**
 * Application entry point.
 *
 * Mounts the root React component into the DOM element with id "root".
 */
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';

ReactDOM.createRoot(document.getElementById('root')!).render(
  <App />
);
