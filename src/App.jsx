import styles from './App.module.css';

/**
 * Main App component that renders a styled 'Hello World' message.
 *
 * @returns {JSX.Element} The rendered App component.
 */
function App() {
  return (
    <div className={styles.container}>
      <h1 className={styles.heading}>Hello World</h1>
    </div>
  );
}

export default App;
