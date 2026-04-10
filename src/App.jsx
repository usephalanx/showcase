import React from 'react';
import Counter from './components/Counter.jsx';
import './App.css';

/**
 * Root application component.
 *
 * Renders the Counter component centered on the page using a
 * flexbox-based container layout.
 */
function App() {
  return (
    <div className="app-container">
      <Counter />
    </div>
  );
}

export default App;
