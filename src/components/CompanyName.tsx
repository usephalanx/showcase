import React from 'react';

/**
 * CompanyName component showcases the company name with distinctive
 * typography and an optional tagline beneath it.
 */
const CompanyName: React.FC = () => {
  return (
    <section className="section company-name-section" data-testid="company-name-section">
      <h1>Madhuri Real Estate</h1>
      <p className="tagline">Your Trusted Partner in Finding the Perfect Home</p>
    </section>
  );
};

export default CompanyName;
