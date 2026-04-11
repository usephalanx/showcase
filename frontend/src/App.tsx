import React from 'react';
import { Logo } from './components/Logo';
import { CompanyName } from './components/CompanyName';
import { Profile } from './components/Profile';
import { RecentSales } from './components/RecentSales';
import { ContactInfo } from './components/ContactInfo';

/**
 * Main application component.
 * Composes all page sections in order: Logo, CompanyName, Profile, RecentSales, ContactInfo.
 */
const App: React.FC = () => {
  return (
    <div className="app-container">
      <header className="app-header">
        <Logo />
        <CompanyName />
      </header>

      <main className="app-main">
        <Profile />
        <RecentSales />
        <ContactInfo />
      </main>

      <footer className="app-footer">
        <p>&copy; {new Date().getFullYear()} Madhuri Real Estate. All rights reserved.</p>
      </footer>
    </div>
  );
};

export default App;
