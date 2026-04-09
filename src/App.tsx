import type { CSSProperties } from "react";

/** Styles for the outer full-viewport container. */
const containerStyle: CSSProperties = {
  display: "flex",
  justifyContent: "center",
  alignItems: "center",
  height: "100vh",
  margin: 0,
};

/**
 * Root application component.
 *
 * Renders a centered "Hello World" heading within a full-viewport container
 * using inline flexbox styles.
 */
export default function App(): JSX.Element {
  return (
    <div style={containerStyle}>
      <h1 data-testid="hello-heading">Hello World</h1>
    </div>
  );
}
