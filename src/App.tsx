/**
 * Main App component that renders a centered "Hello World" heading.
 */
export default function App() {
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
