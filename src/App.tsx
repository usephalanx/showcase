/**
 * Main application component.
 *
 * Renders a Hello World heading and an interactive counter button.
 */
import { useState } from 'react';
import './App.css';

/**
 * Root App component that displays a greeting and a click counter.
 */
function App(): JSX.Element {
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

export default App;
