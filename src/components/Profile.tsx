import React from 'react';

/** Props for the Profile component. */
interface ProfileProps {
  /** URL of the profile photo. */
  imageUrl?: string;
  /** Name of the agent. */
  name?: string;
  /** Bio / description of the agent. */
  bio?: string;
}

/**
 * Profile component presents the agent or company profile with a
 * photo and biographical description in a responsive layout.
 */
const Profile: React.FC<ProfileProps> = ({
  imageUrl = '/profile.jpg',
  name = 'Madhuri Patel',
  bio = 'With over 15 years of experience in residential and commercial real estate, Madhuri Patel is dedicated to helping families find their dream homes. Her deep knowledge of the local market and commitment to client satisfaction have made her one of the most trusted names in the industry.',
}) => {
  return (
    <section className="section profile-section" data-testid="profile-section">
      <img
        src={imageUrl}
        alt={`${name} profile photo`}
        className="profile-image"
        onError={(e) => {
          const target = e.currentTarget;
          target.style.display = 'none';
        }}
      />
      <div className="profile-details">
        <h3>{name}</h3>
        <p>{bio}</p>
      </div>
    </section>
  );
};

export default Profile;
