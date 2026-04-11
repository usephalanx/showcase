import React from 'react';

/**
 * Logo component for Madhuri Real Estate.
 *
 * Renders the company logo as an accessible image element with
 * appropriate alt text and modern styling. The logo is displayed
 * within a centered container and uses the SVG asset from the
 * public directory.
 */
const Logo: React.FC = () => {
  return (
    <div className="logo-container" data-testid="logo">
      <img
        src="/logo.svg"
        alt="Madhuri Real Estate logo"
        className="logo-image"
        width={120}
        height={120}
        role="img"
      />
    </div>
  );
};

export default Logo;
