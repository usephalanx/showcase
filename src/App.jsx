/**
 * Main App component that renders the Hello World message.
 *
 * Uses CSS Modules for scoped styling to prevent CSS leakage.
 */
import styles from './App.module.css';

function App() {
  return (
    <div className={styles.container}>
      <h1 className={styles.title}>Hello World</h1>
    </div>
  );
}

export default App;
