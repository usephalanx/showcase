import React from 'react';
import Logo from './components/Logo';
import CompanyName from './components/CompanyName';
import Profile from './components/Profile';
import RecentSales from './components/RecentSales';
import ContactInfo from './components/ContactInfo';

/**
 * Main application component.
 *
 * Composes all page sections in the correct order:
 * 1. Logo
 * 2. CompanyName
 * 3. Profile
 * 4. RecentSales
 * 5. ContactInfo
 */
const App: React.FC = () => {
  return (
    <div data-testid="app-container" className="app-container">
      <Logo />
      <CompanyName />
      <Profile />
      <RecentSales />
      <ContactInfo />
    </div>
  );
};

export default App;
