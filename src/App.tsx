import React from 'react';
import Logo from './components/Logo';
import CompanyName from './components/CompanyName';
import Profile from './components/Profile';
import RecentSales from './components/RecentSales';
import ContactInfo from './components/ContactInfo';
import './styles/global.css';

/**
 * App is the main application component that composes all page sections
 * in the correct order for the Madhuri Real Estate single-page website.
 */
const App: React.FC = () => {
  return (
    <div className="app-container" data-testid="app-container">
      <Logo />
      <CompanyName />
      <Profile />
      <RecentSales />
      <ContactInfo />
    </div>
  );
};

export default App;
