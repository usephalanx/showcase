/**
 * Root application component.
 *
 * Renders the Counter component as the main content of the app.
 */
import React from "react";
import Counter from "./components/Counter";
import "./index.css";

function App() {
  return (
    <div className="app">
      <Counter />
    </div>
  );
}

export default App;
