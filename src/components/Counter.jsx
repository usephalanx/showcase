/**
 * Counter component with increment and decrement functionality.
 *
 * Manages a count state value and provides buttons to increase or
 * decrease the count. Displays the current count value.
 */
import { useState } from 'react';
import styles from './Counter.module.css';

/**
 * Counter functional component.
 *
 * @param {object} props
 * @param {number} [props.initialCount=0] - The starting count value.
 * @returns {JSX.Element} The rendered Counter component.
 */
export default function Counter({ initialCount = 0 }) {
  const [count, setCount] = useState(initialCount);

  /**
   * Increment the count by one.
   */
  const handleIncrement = () => {
    setCount((prev) => prev + 1);
  };

  /**
   * Decrement the count by one.
   */
  const handleDecrement = () => {
    setCount((prev) => prev - 1);
  };

  return (
    <div className={styles.counter}>
      <h2 className={styles.title}>Counter</h2>
      <p className={styles.display} data-testid="count-display">
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
