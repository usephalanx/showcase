import React from 'react';

/**
 * Logo component.
 * Displays the company logo prominently at the top of the page.
 */
export const Logo: React.FC = () => {
  return (
    <div className="logo-container" data-testid="logo">
      <img
        src="/logo.svg"
        alt="Madhuri Real Estate Logo"
        className="logo-image"
        width={120}
        height={120}
      />
    </div>
  );
};
