import type { CSSProperties } from "react";

/** Styles for the outer full-viewport container. */
const containerStyle: CSSProperties = {
  display: "flex",
  justifyContent: "center",
  alignItems: "center",
  minHeight: "100vh",
  margin: 0,
  fontFamily: "sans-serif",
  backgroundColor: "#f5f5f5",
};

/** Styles for the heading text. */
const headingStyle: CSSProperties = {
  fontSize: "3rem",
  color: "#333",
};

/**
 * Root application component.
 *
 * Renders a centered "Hello World" heading within a full-viewport container.
 */
export default function App(): JSX.Element {
  return (
    <div style={containerStyle}>
      <h1 style={headingStyle} data-testid="hello-heading">
        Hello World
      </h1>
    </div>
  );
}
