import React from 'react';

/**
 * Profile component.
 * Presents the agent/company profile with photo and bio.
 * Responsive layout for mobile and desktop.
 */
export const Profile: React.FC = () => {
  return (
    <section className="profile-section" data-testid="profile">
      <h2 className="section-heading">About Us</h2>
      <div className="profile-content">
        <div className="profile-image-wrapper">
          <img
            src="/logo.svg"
            alt="Madhuri Real Estate team"
            className="profile-image"
            width={200}
            height={200}
          />
        </div>
        <div className="profile-bio">
          <p>
            With over 15 years of experience in the real estate market, Madhuri Real
            Estate has helped hundreds of families find their dream homes. Our dedicated
            team of professionals provides personalized service, expert market knowledge,
            and unwavering commitment to our clients&#39; satisfaction.
          </p>
          <p>
            We specialize in residential properties, luxury homes, and commercial real
            estate across the metropolitan area. Whether you&#39;re buying your first home
            or expanding your investment portfolio, we&#39;re here to guide you every step
            of the way.
          </p>
        </div>
      </div>
    </section>
  );
};
