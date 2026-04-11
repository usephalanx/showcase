import React from 'react';

/**
 * Main application component.
 *
 * Renders a centered "Hello World" heading on a white background.
 * Uses inline styles for layout so that tests can verify centering
 * and background color via the style property.
 */
function App(): React.JSX.Element {
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
