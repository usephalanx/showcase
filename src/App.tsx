/**
 * Main application component.
 *
 * Renders a "Hello World" heading and a counter button that increments
 * on each click.
 */
import { useState } from 'react';
import './App.css';

/** Root component of the application. */
export default function App(): JSX.Element {
  const [count, setCount] = useState<number>(0);

  return (
    <div className="app">
      <h1>Hello World</h1>
      <button onClick={() => setCount((c) => c + 1)}>
        Count: {count}
      </button>
    </div>
  );
}
