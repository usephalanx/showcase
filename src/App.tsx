import React from 'react';
import HelloWorld from './components/HelloWorld';
import styles from './App.module.css';

/**
 * Root application component.
 *
 * Renders the HelloWorld component inside a centered flex container.
 */
function App(): React.JSX.Element {
  return (
    <div className={styles.container} data-testid="app-container">
      <HelloWorld />
    </div>
  );
}

export default App;
