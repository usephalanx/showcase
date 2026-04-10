import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import "./main.css";

/**
 * Application entry point.
 *
 * Imports global styles and renders the root App component into the
 * #root element defined in index.html.
 */
ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
