import React from 'react';
import './styles/global.css';
import Logo from './components/Logo';
import CompanyName from './components/CompanyName';

/**
 * Main application component for Madhuri Real Estate SPA.
 *
 * Composes the page layout with the Logo and CompanyName components
 * arranged at the top in a branded header section.
 */
const App: React.FC = () => {
  return (
    <div className="app-container" data-testid="app">
      <header className="app-header" role="banner">
        <Logo />
        <CompanyName />
      </header>
      <main className="app-main" role="main">
        {/* Future sections: Profile, RecentSales, ContactInfo */}
      </main>
    </div>
  );
};

export default App;
