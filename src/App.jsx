import React from 'react';
import Counter from './components/Counter';
import './index.css';

/**
 * Root application component.
 *
 * Renders the Counter component inside a minimal layout.
 */
function App() {
  return (
    <div className="app">
      <h1>Mini React Counter App</h1>
      <Counter />
    </div>
  );
}

export default App;
