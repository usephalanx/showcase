import React, { useState } from 'react';
import styles from './Counter.module.css';

/**
 * Counter component.
 *
 * Displays the current count value with increment and decrement buttons.
 * The count starts at 0 and can go negative.
 */
function Counter() {
  const [count, setCount] = useState(0);

  /**
   * Increment the count by 1.
   */
  const handleIncrement = () => {
    setCount((prev) => prev + 1);
  };

  /**
   * Decrement the count by 1.
   */
  const handleDecrement = () => {
    setCount((prev) => prev - 1);
  };

  return (
    <div className={styles.counter} data-testid="counter-container">
      <h2 className={styles.title}>Counter</h2>
      <p className={styles.count} data-testid="count-display">
        {count}
      </p>
      <div className={styles.buttons}>
        <button
          className={styles.button}
          onClick={handleDecrement}
          aria-label="Decrement"
        >
          −
        </button>
        <button
          className={styles.button}
          onClick={handleIncrement}
          aria-label="Increment"
        >
          +
        </button>
      </div>
    </div>
  );
}

export default Counter;
