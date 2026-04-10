/**
 * Counter component with increment and decrement functionality.
 *
 * Displays the current count value centered, with two buttons to
 * increment and decrement the count.
 */
import React, { useState } from "react";
import "./Counter.css";

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
      <h1 className="counter__title">Counter</h1>
      <p className="counter__display" data-testid="count-display">
        {count}
      </p>
      <div className="counter__buttons">
        <button
          className="counter__button counter__button--decrement"
          onClick={handleDecrement}
          aria-label="Decrement"
        >
          Decrement
        </button>
        <button
          className="counter__button counter__button--increment"
          onClick={handleIncrement}
          aria-label="Increment"
        >
          Increment
        </button>
      </div>
    </div>
  );
}

export default Counter;
