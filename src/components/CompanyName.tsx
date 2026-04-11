import React from 'react';

/**
 * CompanyName component for Madhuri Real Estate.
 *
 * Displays the company name "Madhuri Real Estate" using an accessible
 * h1 heading tag with distinctive, brand-aligned typography and color.
 * Includes a subtitle tagline for additional context.
 */
const CompanyName: React.FC = () => {
  return (
    <div data-testid="company-name">
      <h1 className="company-name">Madhuri Real Estate</h1>
      <p className="company-name-subtitle">Your Dream Home Awaits</p>
    </div>
  );
};

export default CompanyName;
