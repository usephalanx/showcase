import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'

/**
 * Application entry point.
 *
 * Creates a React root attached to the #root DOM element and renders
 * the top-level <App /> component inside React.StrictMode.
 */
const root = ReactDOM.createRoot(document.getElementById('root')!)
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
