import React from 'react';

/**
 * CompanyName component displays the company name with distinctive
 * brand typography and an optional tagline.
 */
const CompanyName: React.FC = () => {
  return (
    <section className="company-name-section" data-testid="company-name-section" aria-label="Company Name">
      <h1>Madhuri Real Estate</h1>
      <p className="tagline">Your Trusted Partner in Finding the Perfect Home</p>
    </section>
  );
};

export default CompanyName;
