import React from 'react';
import Counter from './components/Counter.jsx';
import './App.css';

/**
 * Root application component.
 * Renders the Counter component centered on the page.
 */
function App() {
  return (
    <div className="app-container" data-testid="app-container">
      <Counter />
    </div>
  );
}

export default App;
