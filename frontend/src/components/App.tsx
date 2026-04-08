/**
 * Root application component.
 *
 * Renders a simple "Hello World" heading centered on the page with
 * clean, minimal inline styling. Serves as the top-level component
 * mounted by main.tsx.
 */

export interface AppProps {
  /** The main heading text to display. Defaults to "Hello World". */
  title?: string;
}

function App({ title = "Hello World" }: AppProps): JSX.Element {
  return (
    <div
      style={{
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        minHeight: "100vh",
        margin: 0,
        fontFamily:
          "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif",
        backgroundColor: "#f9fafb",
      }}
    >
      <h1
        style={{
          fontSize: "3rem",
          fontWeight: 700,
          color: "#111827",
          letterSpacing: "-0.025em",
        }}
      >
        {title}
      </h1>
    </div>
  );
}

export default App;
