import React from 'react';

/**
 * Profile component presents the real estate agent's profile with a photo
 * and a descriptive bio. Uses a responsive layout that stacks vertically
 * on mobile and arranges side-by-side on desktop.
 */
const Profile: React.FC = () => {
  return (
    <section className="section profile-section" data-testid="profile-section">
      <div className="profile-image-container">
        <img
          className="profile-image"
          src="/profile.jpg"
          alt="Madhuri - Real Estate Agent"
          onError={(e) => {
            const target = e.currentTarget;
            target.style.display = 'none';
          }}
        />
      </div>
      <div className="profile-bio">
        <h2>Madhuri Sharma</h2>
        <p className="role">Senior Real Estate Agent</p>
        <p>
          With over 15 years of experience in the real estate industry, Madhuri
          has helped hundreds of families find their dream homes. Her deep
          knowledge of the local market, combined with a genuine passion for
          connecting people with the perfect property, makes her one of the most
          trusted agents in the region. Whether you are buying your first home or
          looking for a premium investment property, Madhuri provides personalized
          guidance every step of the way.
        </p>
      </div>
    </section>
  );
};

export default Profile;
