import React from 'react';

/** Props for the Logo component. */
interface LogoProps {
  /** Optional custom source for the logo image. */
  src?: string;
  /** Optional alt text for the logo. */
  alt?: string;
}

/**
 * Logo component displays the company logo prominently at the top of the page.
 * Falls back to a text-based logo if no image is provided.
 */
const Logo: React.FC<LogoProps> = ({
  src = '/logo.svg',
  alt = 'Madhuri Real Estate Logo',
}) => {
  return (
    <div className="section logo-section" data-testid="logo-section">
      <img src={src} alt={alt} className="logo-image" />
    </div>
  );
};

export default Logo;
