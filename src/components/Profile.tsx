import React from 'react';

/**
 * Profile component presents the agent/company profile with a photo
 * placeholder and biographical description. Responsive layout adapts
 * from stacked (mobile) to side-by-side (desktop).
 */
const Profile: React.FC = () => {
  return (
    <section className="profile-section" data-testid="profile-section" aria-label="Agent Profile">
      <img
        className="profile-image"
        src="https://via.placeholder.com/150x150?text=Agent"
        alt="Madhuri - Real Estate Agent"
        width={150}
        height={150}
      />
      <div className="profile-content">
        <h2>About Madhuri</h2>
        <p>
          With over 15 years of experience in the real estate market, Madhuri has
          helped hundreds of families find their dream homes. Specializing in
          residential properties, luxury estates, and investment opportunities,
          Madhuri brings deep market knowledge, unwavering dedication, and a
          personal touch to every transaction. Whether you are buying your first
          home or selling a cherished property, Madhuri is committed to making
          the process seamless and rewarding.
        </p>
      </div>
    </section>
  );
};

export default Profile;
