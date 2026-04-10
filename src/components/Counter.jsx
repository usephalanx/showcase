import React, { useState } from 'react';

/**
 * Counter component with increment and decrement functionality.
 *
 * Displays the current count and provides buttons to increase or
 * decrease the value by one.
 */
function Counter() {
  const [count, setCount] = useState(0);

  /**
   * Increment the counter by 1.
   */
  const handleIncrement = () => {
    setCount((prev) => prev + 1);
  };

  /**
   * Decrement the counter by 1.
   */
  const handleDecrement = () => {
    setCount((prev) => prev - 1);
  };

  return (
    <div className="counter">
      <p data-testid="count-display">Count: {count}</p>
      <button onClick={handleIncrement}>Increment</button>
      <button onClick={handleDecrement}>Decrement</button>
    </div>
  );
}

export default Counter;
