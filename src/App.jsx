/**
 * Main application component.
 * Renders the Counter component as the primary UI.
 */
import React from 'react';
import Counter from './components/Counter';

/**
 * App component – top-level wrapper that renders the Counter.
 *
 * @returns {JSX.Element} The rendered application.
 */
function App() {
  return (
    <div className="app">
      <h1>Mini React Counter</h1>
      <Counter />
    </div>
  );
}

export default App;
