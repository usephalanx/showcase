import React from 'react';

/**
 * Logo component displays the company logo prominently at the top of the page.
 * Renders an SVG logo with appropriate alt text for accessibility.
 */
const Logo: React.FC = () => {
  return (
    <section className="section logo-section" data-testid="logo-section">
      <img
        src="/logo.svg"
        alt="Madhuri Real Estate Logo"
        width="200"
        height="80"
      />
    </section>
  );
};

export default Logo;
