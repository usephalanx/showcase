/**
 * Root application component.
 *
 * Acts as the top-level wrapper that composes the page-level components.
 * Currently renders the HelloPage as the sole content.
 */
import React from 'react';
import HelloPage from './pages/HelloPage';

/**
 * App component — root of the component tree.
 *
 * @returns The rendered application wrapped in a styled container div.
 */
function App(): React.JSX.Element {
  return (
    <div className="app">
      <HelloPage />
    </div>
  );
}

export default App;
