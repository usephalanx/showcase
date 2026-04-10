/**
 * Counter component with increment and decrement functionality.
 * Displays a numeric count and two buttons to modify the value.
 */
import React, { useState } from 'react';

/**
 * A counter component that manages its own count state.
 * The count starts at 0 and can be incremented or decremented
 * without any upper or lower bounds.
 *
 * @returns {JSX.Element} The rendered counter UI.
 */
function Counter() {
  const [count, setCount] = useState(0);

  /**
   * Increase the count by 1.
   */
  const handleIncrement = () => {
    setCount((prev) => prev + 1);
  };

  /**
   * Decrease the count by 1.
   */
  const handleDecrement = () => {
    setCount((prev) => prev - 1);
  };

  return (
    <div className="counter-container">
      <h1>Counter</h1>
      <div className="count" data-testid="count">
        {count}
      </div>
      <div>
        <button onClick={handleDecrement}>Decrement</button>
        <button onClick={handleIncrement}>Increment</button>
      </div>
    </div>
  );
}

export default Counter;
