import React from 'react';

/**
 * Profile component presents the agent/company profile
 * with a photo and biographical description.
 */
const Profile: React.FC = () => {
  return (
    <div data-testid="profile-section" className="profile-section">
      <img
        src="/profile.jpg"
        alt="Madhuri - Real Estate Agent"
        className="profile-image"
      />
      <div className="profile-bio">
        <h2>About Madhuri</h2>
        <p>
          With over 15 years of experience in the real estate market, Madhuri
          is dedicated to helping clients find their dream homes. Specializing
          in residential properties, Madhuri brings expertise, integrity, and
          a personalized approach to every transaction.
        </p>
      </div>
    </div>
  );
};

export default Profile;
