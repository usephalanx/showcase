import React from 'react';

/**
 * Main application component.
 * Renders a centered "Hello World" heading on a white background.
 */
function App(): React.ReactElement {
  return (
    <div
      style={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        minHeight: '100vh',
        backgroundColor: '#ffffff',
      }}
    >
      <h1>Hello World</h1>
    </div>
  );
}

export default App;
