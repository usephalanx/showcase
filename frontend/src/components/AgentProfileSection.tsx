import React from 'react';

export interface AgentSocialLinks {
  linkedin?: string;
  twitter?: string;
  facebook?: string;
  instagram?: string;
}

export interface Agent {
  id: string;
  name: string;
  title: string;
  phone: string;
  email: string;
  photo: string;
  bio: string;
  specialties: string[];
  propertiesCount: number;
  rating: number;
  socialLinks?: AgentSocialLinks;
}

export interface AgentProfileSectionProps {
  agents: Agent[];
  heading?: string;
  introParagraph?: string;
}

function StarRating({ rating }: { rating: number }) {
  const fullStars = Math.floor(rating);
  const hasHalf = rating - fullStars >= 0.5;
  const emptyStars = 5 - fullStars - (hasHalf ? 1 : 0);

  return (
    <div className="flex items-center gap-0.5" aria-label={`Rating: ${rating} out of 5`}>
      {Array.from({ length: fullStars }).map((_, i) => (
        <span key={`full-${i}`} className="text-yellow-400 text-lg">★</span>
      ))}
      {hasHalf && <span className="text-yellow-400 text-lg">★</span>}
      {Array.from({ length: emptyStars }).map((_, i) => (
        <span key={`empty-${i}`} className="text-gray-300 text-lg">★</span>
      ))}
      <span className="ml-1 text-sm text-gray-600">({rating.toFixed(1)})</span>
    </div>
  );
}

function AgentCard({ agent }: { agent: Agent }) {
  return (
    <div
      className="bg-white rounded-2xl shadow-md hover:shadow-xl transition-shadow duration-300 overflow-hidden flex flex-col"
      data-testid={`agent-card-${agent.id}`}
    >
      <div className="relative w-full pt-[100%] overflow-hidden bg-gray-100">
        <img
          src={agent.photo}
          alt={agent.name}
          className="absolute inset-0 w-full h-full object-cover"
          loading="lazy"
        />
      </div>
      <div className="p-6 flex flex-col flex-1">
        <h3 className="text-xl font-bold text-gray-900">{agent.name}</h3>
        <p className="text-sm font-medium text-blue-600 mt-1">{agent.title}</p>
        <StarRating rating={agent.rating} />
        <p className="text-gray-600 text-sm mt-3 line-clamp-3 flex-1">{agent.bio}</p>
        {agent.specialties.length > 0 && (
          <div className="mt-4 flex flex-wrap gap-2">
            {agent.specialties.map((specialty) => (
              <span
                key={specialty}
                className="inline-block bg-blue-50 text-blue-700 text-xs font-medium px-2.5 py-1 rounded-full"
              >
                {specialty}
              </span>
            ))}
          </div>
        )}
        <div className="mt-4 pt-4 border-t border-gray-100 space-y-1">
          <p className="text-sm text-gray-500">
            <span className="font-medium text-gray-700">{agent.propertiesCount}</span> properties
          </p>
          <a
            href={`mailto:${agent.email}`}
            className="text-sm text-blue-600 hover:text-blue-800 hover:underline block truncate"
          >
            {agent.email}
          </a>
          <a
            href={`tel:${agent.phone}`}
            className="text-sm text-gray-600 hover:text-gray-800 block"
          >
            {agent.phone}
          </a>
        </div>
        {agent.socialLinks && Object.keys(agent.socialLinks).length > 0 && (
          <div className="mt-3 flex gap-3">
            {agent.socialLinks.linkedin && (
              <a href={agent.socialLinks.linkedin} target="_blank" rel="noopener noreferrer" aria-label={`${agent.name} LinkedIn`} className="text-gray-400 hover:text-blue-700 transition-colors">
                <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 01-2.063-2.065 2.064 2.064 0 112.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>
              </a>
            )}
            {agent.socialLinks.twitter && (
              <a href={agent.socialLinks.twitter} target="_blank" rel="noopener noreferrer" aria-label={`${agent.name} Twitter`} className="text-gray-400 hover:text-blue-500 transition-colors">
                <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24"><path d="M23.953 4.57a10 10 0 01-2.825.775 4.958 4.958 0 002.163-2.723c-.951.555-2.005.959-3.127 1.184a4.92 4.92 0 00-8.384 4.482C7.69 8.095 4.067 6.13 1.64 3.162a4.822 4.822 0 00-.666 2.475c0 1.71.87 3.213 2.188 4.096a4.904 4.904 0 01-2.228-.616v.06a4.923 4.923 0 003.946 4.827 4.996 4.996 0 01-2.212.085 4.936 4.936 0 004.604 3.417 9.867 9.867 0 01-6.102 2.105c-.39 0-.779-.023-1.17-.067a13.995 13.995 0 007.557 2.209c9.053 0 13.998-7.496 13.998-13.985 0-.21 0-.42-.015-.63A9.935 9.935 0 0024 4.59z"/></svg>
              </a>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

const AgentProfileSection: React.FC<AgentProfileSectionProps> = ({
  agents,
  heading = 'Meet Our Agents',
  introParagraph = 'Our team of experienced real estate professionals is dedicated to helping you find the perfect property. With deep local knowledge and a commitment to exceptional service, our agents are here to guide you every step of the way.',
}) => {
  return (
    <section className="py-16 px-4 sm:px-6 lg:px-8 bg-gray-50" data-testid="agent-profile-section">
      <div className="max-w-7xl mx-auto">
        <div className="text-center mb-12">
          <h2 className="text-3xl sm:text-4xl font-bold text-gray-900 mb-4">{heading}</h2>
          <p className="text-lg text-gray-600 max-w-3xl mx-auto">{introParagraph}</p>
        </div>
        {agents.length === 0 ? (
          <p className="text-center text-gray-500" data-testid="no-agents-message">
            No agents available at this time.
          </p>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">
            {agents.map((agent) => (
              <AgentCard key={agent.id} agent={agent} />
            ))}
          </div>
        )}
      </div>
    </section>
  );
};

export default AgentProfileSection;
