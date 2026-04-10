import React from 'react';
import styles from './App.module.css';

/**
 * Main application component.
 *
 * Renders a "yellow world" heading inside a yellow-themed container.
 * Styling is applied via CSS modules defined in App.module.css.
 */
const App: React.FC = () => {
  return (
    <div className={styles.container} data-testid="app-container">
      <h1 className={styles.heading} data-testid="app-heading">
        yellow world
      </h1>
    </div>
  );
};

export default App;
