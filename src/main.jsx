/**
 * Vite/React entry point.
 *
 * Mounts the App component into the DOM element with id "root".
 */
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
