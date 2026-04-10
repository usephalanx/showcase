/**
 * React entry point for the Vite application.
 *
 * Renders the root App component into the #root DOM element.
 */
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
