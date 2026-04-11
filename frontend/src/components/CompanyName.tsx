import React from 'react';

/**
 * CompanyName component.
 * Showcases the company name with distinctive, brand-aligned typography.
 */
export const CompanyName: React.FC = () => {
  return (
    <div className="company-name-container" data-testid="company-name">
      <h1 className="company-name-heading">Madhuri Real Estate</h1>
      <p className="company-name-tagline">Your Trusted Partner in Property</p>
    </div>
  );
};
