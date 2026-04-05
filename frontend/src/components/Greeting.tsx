/**
 * Reusable Greeting component.
 *
 * Displays a configurable "Hello {name}" heading with centered,
 * minimal styling.
 */

/** Props accepted by the {@link Greeting} component. */
export interface GreetingProps {
  /** The name to greet. Defaults to "World". */
  name?: string;
}

/** Inline styles for the greeting heading. */
const headingStyle: React.CSSProperties = {
  fontSize: "2.5rem",
  fontWeight: 600,
  textAlign: "center",
  color: "#334155",
  fontFamily: "system-ui, -apple-system, sans-serif",
  letterSpacing: "-0.025em",
  margin: 0,
  padding: "1rem",
};

/**
 * Render a greeting heading.
 *
 * @param props - Component props.
 * @returns A JSX heading element.
 */
function Greeting({ name = "World" }: GreetingProps): JSX.Element {
  return (
    <h1 data-testid="greeting" style={headingStyle}>
      Hello {name}
    </h1>
  );
}

export default Greeting;
