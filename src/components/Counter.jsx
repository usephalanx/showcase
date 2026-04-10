/**
 * Counter component with increment and decrement functionality.
 */
import React, { useState } from 'react';

/**
 * Counter – displays a numeric count with increment and decrement buttons.
 *
 * @returns {JSX.Element} The rendered counter UI.
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
    <div className="counter">
      <p data-testid="count-display">Count: {count}</p>
      <button onClick={handleIncrement} aria-label="Increment">
        Increment
      </button>
      <button onClick={handleDecrement} aria-label="Decrement">
        Decrement
      </button>
    </div>
  );
}

export default Counter;
