/**
 * HomePage component.
 *
 * Serves as the landing page of the application. Composes the
 * Greeting component inside a semantic <main> element with
 * full-viewport flexbox centering and a clean white background.
 */
import Greeting from "../components/Greeting";

const containerStyle: React.CSSProperties = {
  display: "flex",
  alignItems: "center",
  justifyContent: "center",
  minHeight: "100vh",
  backgroundColor: "#ffffff",
  margin: 0,
  padding: 0,
};

/**
 * Render the home page.
 *
 * @returns A JSX element containing the page content.
 */
function HomePage(): JSX.Element {
  return (
    <main style={containerStyle}>
      <Greeting />
    </main>
  );
}

export default HomePage;
