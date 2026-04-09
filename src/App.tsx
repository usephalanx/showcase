/**
 * Root application component.
 *
 * Renders a centered "Hello World" heading with minimal styling.
 */
export default function App(): JSX.Element {
  return (
    <div
      style={{
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        minHeight: "100vh",
        margin: 0,
        fontFamily: "sans-serif",
        backgroundColor: "#f5f5f5",
      }}
    >
      <h1
        data-testid="hello-heading"
        style={{ fontSize: "3rem", color: "#333" }}
      >
        Hello World
      </h1>
    </div>
  );
}
