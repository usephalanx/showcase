import React from "react";
import ReactDOM from "react-dom/client";
import "./index.css";

/**
 * Application entry point.
 *
 * Mounts the React root into the #root DOM element.
 * The full App component with routing will be added in a later phase.
 */
const rootElement = document.getElementById("root");

if (!rootElement) {
  throw new Error("Root element not found. Ensure index.html contains <div id='root'></div>.");
}

ReactDOM.createRoot(rootElement).render(
  <React.StrictMode>
    <div className="min-h-screen flex items-center justify-center bg-slate-50">
      <h1 className="text-3xl font-bold text-slate-900">
        Real Estate Website — Coming Soon
      </h1>
    </div>
  </React.StrictMode>,
);
