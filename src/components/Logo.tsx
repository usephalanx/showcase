import React from 'react';

/**
 * Logo component displays the Madhuri Real Estate logo prominently
 * at the top of the page.
 */
const Logo: React.FC = () => {
  return (
    <div data-testid="logo-section" className="logo-section">
      <img
        src="/logo.svg"
        alt="Madhuri Real Estate Logo"
        className="logo-image"
      />
    </div>
  );
};

export default Logo;
