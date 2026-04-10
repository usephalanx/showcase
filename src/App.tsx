import React from "react";
import styles from "./App.module.css";

/**
 * Main application component.
 *
 * Renders a heading with the text "yellow world" using yellow-themed
 * styling provided by CSS modules.
 */
const App: React.FC = () => {
  return (
    <div className={styles.container} data-testid="app-container">
      <h1 className={styles.heading}>yellow world</h1>
    </div>
  );
};

export default App;
