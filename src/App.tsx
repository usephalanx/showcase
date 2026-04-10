/**
 * Main App component.
 *
 * Renders a modern-styled "Hello World" heading as the application root.
 */
import React from 'react';
import styles from './App.module.css';

/**
 * Top-level application component.
 *
 * @returns A React element displaying "Hello World" with modern styling.
 */
export default function App(): React.ReactElement {
  return (
    <div className={styles.container}>
      <h1 className={styles.heading}>Hello World</h1>
      <p className={styles.subtitle}>Welcome to your React + Vite application</p>
    </div>
  );
}
