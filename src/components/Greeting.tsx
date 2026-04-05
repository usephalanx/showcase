/**
 * Reusable Greeting component.
 *
 * Displays a configurable "Hello {name}" heading.
 */

/** Props accepted by the {@link Greeting} component. */
export interface GreetingProps {
  /** The name to greet. Defaults to "World". */
  name?: string;
}

/**
 * Render a greeting heading.
 *
 * @param props - Component props.
 * @returns A JSX heading element.
 */
function Greeting({ name = "World" }: GreetingProps): JSX.Element {
  return <h1 data-testid="greeting">Hello {name}</h1>;
}

export default Greeting;
