import React from 'react';

export interface TrustBadgeData {
  icon: string;
  label: string;
}

export interface AboutProps {
  sectionId?: string;
  sectionLabel: string;
  bioText: string;
  avatarImageUrl?: string;
  avatarAlt?: string;
  trustBadges: TrustBadgeData[];
}

function TrustBadge({ icon, label }: TrustBadgeData) {
  return (
    <div className="flex flex-col items-center gap-2 px-4 py-3">
      <span className="text-2xl" role="img" aria-label={label}>
        {icon}
      </span>
      <span className="text-sm font-medium text-slate-700 text-center whitespace-nowrap">
        {label}
      </span>
    </div>
  );
}

export default function About({
  sectionId = 'about',
  sectionLabel,
  bioText = 'With over 10 years in luxury residential real estate, Maddie helps buyers and sellers navigate the market with confidence and care.',
  avatarImageUrl = 'https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=400&q=80',
  avatarAlt = 'Professional headshot',
  trustBadges = [
    { icon: "🏆", label: "Licensed Agent" },
    { icon: "🏠", label: "200+ Homes Sold" },
    { icon: "⭐", label: "5★ Rated" },
  ],
}: AboutProps) {
  return (
    <section
      id={sectionId}
      className="bg-[#FFFDF7] py-16 px-4 sm:px-6 lg:px-8"
    >
      <div className="max-w-6xl mx-auto">
        <div className="flex flex-col md:flex-row items-center gap-10 md:gap-16">
          {/* Left column: Avatar */}
          <div className="flex-shrink-0 flex justify-center">
            <div
              className="w-64 h-64 lg:w-80 lg:h-80 rounded-full p-1.5"
              style={{
                background:
                  'linear-gradient(135deg, #C8A951 0%, #E8D5A3 50%, #D4B968 100%)',
              }}
              data-testid="avatar-border"
            >
              <div className="w-full h-full rounded-full overflow-hidden bg-[#FFF8F0] flex items-center justify-center">
                {avatarImageUrl ? (
                  <img
                    src={avatarImageUrl}
                    alt={avatarAlt}
                    className="w-full h-full object-cover"
                  />
                ) : (
                  <div
                    className="w-full h-full flex items-center justify-center"
                    style={{
                      background:
                        'linear-gradient(180deg, #E8D5A3 0%, #FFF8F0 100%)',
                    }}
                    data-testid="avatar-placeholder"
                  >
                    <svg
                      className="w-24 h-24 lg:w-32 lg:h-32 text-[#C8A951] opacity-60"
                      fill="currentColor"
                      viewBox="0 0 24 24"
                      aria-hidden="true"
                    >
                      <path d="M12 12c2.7 0 4.8-2.1 4.8-4.8S14.7 2.4 12 2.4 7.2 4.5 7.2 7.2 9.3 12 12 12zm0 2.4c-3.2 0-9.6 1.6-9.6 4.8v2.4h19.2v-2.4c0-3.2-6.4-4.8-9.6-4.8z" />
                    </svg>
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* Right column: Text content */}
          <div className="flex-1 text-center md:text-left">
            <p className="text-sm font-semibold tracking-widest uppercase text-[#C8A951] mb-2">
              {sectionLabel}
            </p>
            <div
              className="w-12 h-0.5 bg-[#C8A951] mb-6 mx-auto md:mx-0"
              aria-hidden="true"
            />
            <p
              className="text-base lg:text-lg leading-relaxed text-[#334155] mb-8"
              data-testid="bio-text"
            >
              {bioText}
            </p>

            {/* Trust badges row */}
            <div
              className="flex flex-wrap justify-center md:justify-start gap-4 sm:gap-6"
              data-testid="trust-badges"
            >
              {trustBadges.map((badge, index) => (
                <div
                  key={index}
                  className="bg-white rounded-xl shadow-sm border border-[#E8D5A3]/40 hover:shadow-md transition-shadow duration-200"
                >
                  <TrustBadge icon={badge.icon} label={badge.label} />
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
