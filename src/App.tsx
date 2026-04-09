/**
 * Root application component.
 *
 * Renders a simple "Hello World" heading centered on the page using
 * flexbox.  This is the top-level component mounted by main.tsx.
 */
import React from 'react'

const containerStyle: React.CSSProperties = {
  display: 'flex',
  justifyContent: 'center',
  alignItems: 'center',
  minHeight: '100vh',
}

function App(): JSX.Element {
  return (
    <div style={containerStyle}>
      <h1>Hello World</h1>
    </div>
  )
}

export default App
