/**
 * Main application component.
 * Renders the HelloWorld component inside a centered container.
 */
import React from "react";
import styles from "./App.module.css";
import HelloWorld from "./components/HelloWorld";

const App: React.FC = () => {
  return (
    <div className={styles.container} data-testid="app-container">
      <HelloWorld />
    </div>
  );
};

export default App;
