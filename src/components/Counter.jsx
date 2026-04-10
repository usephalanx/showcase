import React, { useState } from 'react';

/**
 * Counter component with increment and decrement functionality.
 *
 * Displays the current count and provides buttons to increase or
 * decrease the value by one.
 */
function Counter() {
  const [count, setCount] = useState(0);

  /** Increase the count by one. */
  const handleIncrement = () => {
    setCount((prev) => prev + 1);
  };

  /** Decrease the count by one. */
  const handleDecrement = () => {
    setCount((prev) => prev - 1);
  };

  return (
    <div className="counter" style={styles.container}>
      <h1 style={styles.title}>Counter</h1>
      <p data-testid="count" style={styles.count}>
        {count}
      </p>
      <div style={styles.buttons}>
        <button
          onClick={handleDecrement}
          aria-label="Decrement"
          style={styles.button}
        >
          &minus;
        </button>
        <button
          onClick={handleIncrement}
          aria-label="Increment"
          style={styles.button}
        >
          +
        </button>
      </div>
    </div>
  );
}

const styles = {
  container: {
    textAlign: 'center',
    padding: '2rem 3rem',
    borderRadius: '12px',
    backgroundColor: '#ffffff',
    boxShadow: '0 4px 12px rgba(0, 0, 0, 0.1)',
  },
  title: {
    marginBottom: '0.5rem',
    fontSize: '1.75rem',
  },
  count: {
    fontSize: '3rem',
    fontWeight: 'bold',
    margin: '1rem 0',
  },
  buttons: {
    display: 'flex',
    gap: '1rem',
    justifyContent: 'center',
  },
  button: {
    fontSize: '1.5rem',
    padding: '0.5rem 1.5rem',
    border: '1px solid #ccc',
    borderRadius: '8px',
    backgroundColor: '#fafafa',
    cursor: 'pointer',
  },
};

export default Counter;
