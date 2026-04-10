import React, { useState } from "react";

/**
 * Counter component with increment and decrement functionality.
 *
 * Renders the current count value alongside two buttons that allow
 * the user to increase or decrease the count by one.
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
      <p className="count-display" data-testid="count-display">
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
