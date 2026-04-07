import React from 'react';

export interface HeroProps {
  /** Main headline text */
  headline: string;
  /** Subheading / supporting text */
  subheading: string;
  /** Background image URL */
  backgroundImageUrl: string;
  /** Primary CTA button label */
  primaryCtaLabel: string;
  /** Primary CTA href (e.g. "#listings") */
  primaryCtaHref: string;
  /** Secondary CTA button label */
  secondaryCtaLabel: string;
  /** Secondary CTA href (e.g. "#contact") */
  secondaryCtaHref: string;
  /** Optional alt text for the background (used as aria-label) */
  backgroundAlt?: string;
}

const Hero: React.FC<HeroProps> = ({
  headline,
  subheading,
  backgroundImageUrl,
  primaryCtaLabel,
  primaryCtaHref,
  secondaryCtaLabel,
  secondaryCtaHref,
  backgroundAlt = 'Luxury home exterior',
}) => {
  return (
    <section
      role="banner"
      aria-label={backgroundAlt}
      style={{
        backgroundImage: `url(${backgroundImageUrl})`,
      }}
      className="relative w-full min-h-[80vh] md:min-h-[90vh] bg-cover bg-center bg-no-repeat flex items-center justify-center"
    >
      {/* Dark overlay gradient */}
      <div
        className="absolute inset-0"
        style={{
          background:
            'linear-gradient(180deg, rgba(30, 41, 59, 0.70) 0%, rgba(30, 41, 59, 0.55) 50%, rgba(30, 41, 59, 0.75) 100%)',
        }}
        aria-hidden="true"
      />

      {/* Content */}
      <div className="relative z-10 flex flex-col items-center text-center px-6 py-16 md:py-24 max-w-4xl mx-auto">
        <h1
          className="text-4xl sm:text-5xl md:text-6xl lg:text-7xl font-bold leading-tight tracking-tight mb-6"
          style={{ fontFamily: "'Playfair Display', Georgia, serif", color: '#FFFDF7' }}
        >
          {headline}
        </h1>

        <p
          className="text-base sm:text-lg md:text-xl leading-relaxed mb-10 max-w-2xl"
          style={{ fontFamily: "'Inter', system-ui, sans-serif", color: '#E8D5A3' }}
        >
          {subheading}
        </p>

        <div className="flex flex-col sm:flex-row gap-4 sm:gap-6 w-full sm:w-auto">
          {/* Primary CTA */}
          <a
            href={primaryCtaHref}
            className="inline-flex items-center justify-center px-8 py-4 text-base font-semibold rounded-md transition-all duration-300 ease-in-out focus:outline-none focus:ring-2 focus:ring-offset-2"
            style={{
              fontFamily: "'Inter', system-ui, sans-serif",
              backgroundColor: '#C8A951',
              color: '#1E293B',
            }}
            onMouseEnter={(e) => {
              (e.currentTarget as HTMLAnchorElement).style.backgroundColor = '#D4B968';
              (e.currentTarget as HTMLAnchorElement).style.transform = 'translateY(-1px)';
            }}
            onMouseLeave={(e) => {
              (e.currentTarget as HTMLAnchorElement).style.backgroundColor = '#C8A951';
              (e.currentTarget as HTMLAnchorElement).style.transform = 'translateY(0)';
            }}
          >
            {primaryCtaLabel}
          </a>

          {/* Secondary CTA */}
          <a
            href={secondaryCtaHref}
            className="inline-flex items-center justify-center px-8 py-4 text-base font-semibold rounded-md border-2 transition-all duration-300 ease-in-out focus:outline-none focus:ring-2 focus:ring-offset-2"
            style={{
              fontFamily: "'Inter', system-ui, sans-serif",
              borderColor: '#FFFDF7',
              color: '#FFFDF7',
              backgroundColor: 'transparent',
            }}
            onMouseEnter={(e) => {
              (e.currentTarget as HTMLAnchorElement).style.backgroundColor = 'rgba(255, 253, 247, 0.12)';
              (e.currentTarget as HTMLAnchorElement).style.transform = 'translateY(-1px)';
            }}
            onMouseLeave={(e) => {
              (e.currentTarget as HTMLAnchorElement).style.backgroundColor = 'transparent';
              (e.currentTarget as HTMLAnchorElement).style.transform = 'translateY(0)';
            }}
          >
            {secondaryCtaLabel}
          </a>
        </div>
      </div>
    </section>
  );
};

export default Hero;
