import React from 'react';

/** Props for the CompanyName component. */
interface CompanyNameProps {
  /** Optional company name override. */
  name?: string;
  /** Optional tagline displayed below the name. */
  tagline?: string;
}

/**
 * CompanyName component showcases the company name with distinctive
 * typography and an optional tagline beneath.
 */
const CompanyName: React.FC<CompanyNameProps> = ({
  name = 'Madhuri Real Estate',
  tagline = 'Your Trusted Partner in Real Estate',
}) => {
  return (
    <div className="section company-name-section" data-testid="company-name-section">
      <h1>{name}</h1>
      {tagline && <p className="tagline">{tagline}</p>}
    </div>
  );
};

export default CompanyName;
