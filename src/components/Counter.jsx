import React, { useState } from 'react';

/**
 * Counter component with increment and decrement functionality.
 *
 * Renders the current count value and two buttons to modify it.
 * The count has no upper or lower bounds.
 */
function Counter() {
  const [count, setCount] = useState(0);

  const handleIncrement = () => {
    setCount((prev) => prev + 1);
  };

  const handleDecrement = () => {
    setCount((prev) => prev - 1);
  };

  return (
    <div className="counter">
      <h2>Counter</h2>
      <p className="count" data-testid="count">
        {count}
      </p>
      <div className="counter-buttons">
        <button onClick={handleDecrement}>Decrement</button>
        <button onClick={handleIncrement}>Increment</button>
      </div>
    </div>
  );
}

export default Counter;
