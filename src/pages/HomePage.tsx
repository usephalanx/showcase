/**
 * HomePage component.
 *
 * Serves as the landing page of the application. Composes the
 * Greeting component inside a semantic <main> element.
 */
import Greeting from "../components/Greeting";

/**
 * Render the home page.
 *
 * @returns A JSX element containing the page content.
 */
function HomePage(): JSX.Element {
  return (
    <main>
      <Greeting />
    </main>
  );
}

export default HomePage;
