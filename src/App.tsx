import React from 'react';

/**
 * Root application component.
 * Serves as the top-level layout wrapper for all page sections.
 */
const App: React.FC = () => {
  return (
    <div className="min-h-screen bg-cream">
      <main>
        <div className="section-container section-padding">
          <h1>Maddie | Luxury Real Estate</h1>
          <p className="mt-4 text-lg text-slate-600">
            Welcome to a new standard of luxury living.
          </p>
        </div>
      </main>
    </div>
  );
};

export default App;
