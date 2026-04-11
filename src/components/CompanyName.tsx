import React from 'react';

/**
 * CompanyName component showcases the company name
 * 'Madhuri Real Estate' with distinctive typography.
 */
const CompanyName: React.FC = () => {
  return (
    <div data-testid="company-name-section" className="company-name-section">
      <h1 className="company-name-heading">Madhuri Real Estate</h1>
    </div>
  );
};

export default CompanyName;
