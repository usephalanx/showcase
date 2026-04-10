import styles from './App.module.css';

/**
 * App component — renders a centered "Hello World" message
 * with modern styling applied via CSS Modules.
 */
function App() {
  return (
    <div className={styles.container}>
      <h1 className={styles.title}>Hello World</h1>
    </div>
  );
}

export default App;
