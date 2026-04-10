import React from "react";
import Counter from "./components/Counter";
import "./index.css";

/**
 * Root application component.
 *
 * Renders the Counter component centered on the page within a
 * minimal layout wrapper.
 */
function App() {
  return (
    <div className="app">
      <h1>Mini React Counter App</h1>
      <Counter />
    </div>
  );
}

export default App;
