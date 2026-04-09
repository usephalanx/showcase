/**
 * Main App component rendering a centered "Hello World" heading.
 *
 * Uses inline styles for centering: display flex, justifyContent center,
 * alignItems center, height 100vh, margin 0, fontFamily sans-serif,
 * fontSize 2rem.
 */
function App(): JSX.Element {
  return (
    <div
      style={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        height: '100vh',
        margin: 0,
        fontFamily: 'sans-serif',
        fontSize: '2rem',
      }}
    >
      Hello World
    </div>
  )
}

export default App
