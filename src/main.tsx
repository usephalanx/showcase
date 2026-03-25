import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'

/**
 * Application entry point.
 *
 * Mounts the root React component into the DOM element with id "root".
 */
ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
