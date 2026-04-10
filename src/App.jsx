/**
 * Root application component.
 * Renders the Counter component as the main content of the page.
 */
import React from 'react';
import Counter from './components/Counter';

/**
 * App component that serves as the root of the component tree.
 * @returns {JSX.Element} The rendered application.
 */
function App() {
  return (
    <div className="app">
      <Counter />
    </div>
  );
}

export default App;
