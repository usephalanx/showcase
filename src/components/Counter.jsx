import React, { useState } from 'react';

/**
 * Counter component with increment and decrement functionality.
 *
 * Displays the current count value and provides buttons to
 * increase or decrease the count by one.
 */
function Counter() {
  const [count, setCount] = useState(0);

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
    <div className="counter-wrapper" data-testid="counter-wrapper">
      <h1>Counter</h1>
      <div
        className="count-display"
        data-testid="count-display"
        aria-live="polite"
      >
        {count}
      </div>
      <div className="counter-buttons">
        <button
          onClick={handleDecrement}
          aria-label="Decrement"
          data-testid="decrement-button"
        >
          −
        </button>
        <button
          onClick={handleIncrement}
          aria-label="Increment"
          data-testid="increment-button"
        >
          +
        </button>
      </div>
    </div>
  );
}

export default Counter;
