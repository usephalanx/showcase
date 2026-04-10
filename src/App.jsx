import React from 'react';
import Counter from './components/Counter';

/**
 * App component — main entry point that renders the Counter.
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
