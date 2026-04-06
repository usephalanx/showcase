/**
 * Application entry point.
 *
 * Mounts the root <App /> component into the DOM element with id "root"
 * using React 18's createRoot API, wrapped in StrictMode for additional
 * development-time checks.
 */

import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);
