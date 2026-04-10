import React, { useState } from 'react';

/**
 * Counter component.
 *
 * Displays a numeric count with increment and decrement buttons.
 * The count state is managed locally via useState and can go negative.
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
      <h1 style={{ fontSize: '2rem', margin: 0 }}>Counter</h1>
      <p
        data-testid="count-display"
        style={{
          fontSize: '3rem',
          fontWeight: 'bold',
          margin: 0,
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
            fontSize: '1.25rem',
            padding: '8px 20px',
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
            fontSize: '1.25rem',
            padding: '8px 20px',
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
