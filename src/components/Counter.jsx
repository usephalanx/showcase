/**
 * Counter component.
 *
 * Displays a count value with increment and decrement buttons.
 * Uses React useState hook to manage count state.
 */
import React, { useState } from 'react';

/**
 * Counter functional component.
 *
 * Renders the current count centered within its container,
 * along with increment and decrement buttons.
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
    <div
      className="counter"
      style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        gap: '16px',
        padding: '32px',
        borderRadius: '12px',
        backgroundColor: '#ffffff',
        boxShadow: '0 2px 8px rgba(0, 0, 0, 0.1)',
      }}
    >
      <h1>Counter</h1>
      <p
        data-testid="count-display"
        style={{
          fontSize: '3rem',
          fontWeight: 'bold',
          textAlign: 'center',
        }}
      >
        {count}
      </p>
      <div style={{ display: 'flex', gap: '12px' }}>
        <button
          onClick={handleDecrement}
          aria-label="Decrement"
          style={{
            padding: '8px 24px',
            fontSize: '1.25rem',
            cursor: 'pointer',
            borderRadius: '6px',
            border: '1px solid #ccc',
            backgroundColor: '#f0f0f0',
          }}
        >
          −
        </button>
        <button
          onClick={handleIncrement}
          aria-label="Increment"
          style={{
            padding: '8px 24px',
            fontSize: '1.25rem',
            cursor: 'pointer',
            borderRadius: '6px',
            border: '1px solid #ccc',
            backgroundColor: '#f0f0f0',
          }}
        >
          +
        </button>
      </div>
    </div>
  );
}

export default Counter;
