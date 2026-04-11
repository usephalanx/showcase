import React from 'react';

/**
 * Logo component displays the Madhuri Real Estate brand logo
 * prominently at the top of the page with accessible alt text.
 */
const Logo: React.FC = () => {
  return (
    <section className="logo-section" data-testid="logo-section" aria-label="Company Logo">
      <img
        src="/logo.svg"
        alt="Madhuri Real Estate Logo"
        width={150}
        height={150}
      />
    </section>
  );
};

export default Logo;
