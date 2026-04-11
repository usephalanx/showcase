import React from 'react';
import HelloWorld from './components/HelloWorld';
import styles from './App.module.css';

/**
 * Root application component.
 *
 * Provides a full-viewport centered container that renders
 * the HelloWorld greeting component.
 */
const App: React.FC = () => {
  return (
    <div className={styles.container} data-testid="app-container">
      <HelloWorld />
    </div>
  );
};

export default App;
