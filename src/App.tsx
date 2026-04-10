/**
 * Root App component.
 *
 * Serves as the top-level React component rendered by main.tsx.
 * Displays 'Yellow World' as a large heading centered on the page
 * with a bright yellow (#FFD700) background, dark contrasting text,
 * and a welcoming subheading.
 */
import React from "react";
import "./App.css";

function App(): React.JSX.Element {
  /**
   * Root application component that renders the Yellow World greeting
   * with centered layout, yellow background, and welcoming subheading.
   */
  return (
    <div className="app">
      <h1 className="heading">Yellow World</h1>
      <p className="subheading">Welcome to the brightest page on the web!</p>
    </div>
  );
}

export default App;
