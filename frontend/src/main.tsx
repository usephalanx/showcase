/**
 * Application entry point.
 *
 * Mounts the root <App /> component into the DOM element with id "root".
 * Wraps the tree in React.StrictMode for development-time checks.
 */
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './App.css';

const rootElement = document.getElementById('root')!;

ReactDOM.createRoot(rootElement).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);
