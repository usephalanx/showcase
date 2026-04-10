import React from 'react';
import styles from './App.module.css';

/**
 * Main application component.
 *
 * Renders a centered "Hello World" heading with scoped CSS module styling.
 *
 * @returns {JSX.Element} The root UI element.
 */
function App() {
  return (
    <div className={styles.container}>
      <h1 className={styles.heading}>Hello World</h1>
    </div>
  );
}

export default App;
