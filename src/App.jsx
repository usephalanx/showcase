/**
 * Root application component.
 *
 * Layouts and centers the Counter component on the page.
 */
import React from 'react';
import Counter from './components/Counter.jsx';
import './App.css';

/**
 * App component that serves as the root layout.
 *
 * @returns {JSX.Element} The rendered application.
 */
function App() {
  return (
    <div className="app-container">
      <Counter />
    </div>
  );
}

export default App;
