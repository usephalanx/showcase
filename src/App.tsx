/**
 * Main App component — renders a centered "Hello World" heading.
 */

/**
 * Root application component.
 *
 * Displays a vertically and horizontally centered "Hello World" heading
 * using inline styles for simplicity.
 */
function App(): JSX.Element {
  return (
    <div
      className="app-container"
      style={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        minHeight: '100vh',
        margin: 0,
        fontFamily: "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
      }}
    >
      <h1 style={{ fontSize: '3rem', color: '#333' }}>Hello World</h1>
    </div>
  )
}

export default App
