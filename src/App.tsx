/**
 * Root application component.
 *
 * Renders a simple "Hello World" heading centered on the page
 * using inline flexbox styles.
 */
function App(): JSX.Element {
  return (
    <div
      style={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        minHeight: '100vh',
      }}
    >
      <h1>Hello World</h1>
    </div>
  )
}

export default App
